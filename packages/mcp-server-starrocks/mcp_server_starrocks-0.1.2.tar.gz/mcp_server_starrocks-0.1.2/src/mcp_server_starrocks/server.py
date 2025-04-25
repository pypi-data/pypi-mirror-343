# Copyright 2021-present StarRocks, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import math
import sys
import os
import io
import time
import traceback
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from pydantic import AnyUrl
from mysql.connector import Error as MySQLError
import mysql.connector
import pandas as pd
import plotly.express as px
import base64

SERVER_VERSION = "0.1.2"

server = Server("mcp-server-starrocks", SERVER_VERSION)

global_connection = None
default_database = os.getenv('STARROCKS_DB')
# a hint for soft limit, not enforced
overview_length_limit = int(os.getenv('STARROCKS_OVERVIEW_LIMIT', str(20000)))
# Global cache for table overviews: {(db_name, table_name): overview_string}
global_table_overview_cache = {}


def get_connection():
    global global_connection, default_database
    if global_connection is None:
        connection_params = {
            'host': os.getenv('STARROCKS_HOST', 'localhost'),
            'port': os.getenv('STARROCKS_PORT', '9030'),
            'user': os.getenv('STARROCKS_USER', 'root'),
            'password': os.getenv('STARROCKS_PASSWORD', '')
        }

        # Use default_database if set during initial connection attempt
        if default_database:
            connection_params['database'] = default_database

        try:
            global_connection = mysql.connector.connect(**connection_params)
            # If connection succeeds without db and default_database is set, try USE DB
            if 'database' not in connection_params and default_database:
                try:
                    cursor = global_connection.cursor()
                    cursor.execute(f"USE {default_database}")
                    cursor.close()
                except MySQLError as db_err:
                    # Warn but don't fail connection if USE DB fails
                    print(f"Warning: Could not switch to default database '{default_database}': {db_err}")
        except MySQLError as conn_err:
            # Reset global connection on failure
            global_connection = None
            # Re-raise the exception to be caught by callers
            raise conn_err

    # Ensure connection is alive, reconnect if not
    if global_connection is not None:
        try:
            if not global_connection.is_connected():
                global_connection.reconnect()
                # Re-apply default database if needed after reconnect
                if default_database:
                    try:
                        cursor = global_connection.cursor()
                        cursor.execute(f"USE {default_database}")
                        cursor.close()
                    except MySQLError as db_err:
                        print(
                            f"Warning: Could not switch to default database '{default_database}' after reconnect: {db_err}")

        except MySQLError as check_err:
            print(f"Connection check/reconnect failed: {check_err}")
            reset_connection()  # Force reset if reconnect fails
            raise check_err  # Raise error to indicate connection failure

    return global_connection


def reset_connection():
    global global_connection
    if global_connection is not None:
        try:
            global_connection.close()
        except Exception as e:
            print(f"Error closing connection: {e}")  # Log error but proceed
        finally:
            global_connection = None


def _format_rows_to_string(columns, rows, limit=None):
    """Helper to format rows similar to handle_read_query but without row count."""
    output = io.StringIO()

    def to_csv_line(row):
        return ",".join(
            str(item).replace("\"", "\"\"") if isinstance(item, str) else str(item) for item in row)

    output.write(to_csv_line(columns) + "\n")
    for row in rows:
        l = to_csv_line(row) + "\n";
        if limit is not None and output.tell() + len(l) > limit:
            break
        output.write(l)
    return output.getvalue()


def _get_table_details(conn, db_name, table_name, limit=None):
    """
    Helper function to get description, sample rows, and count for a table.
    Returns a formatted string. Handles DB errors internally and returns error messages.
    """
    global global_table_overview_cache  # Access cache for potential updates
    output_lines = []
    # Use backticks for safety
    full_table_name = f"`{table_name}`"
    if db_name:
        full_table_name = f"`{db_name}`.`{table_name}`"
    else:  # Should ideally not happen if logic is correct, but handle defensively
        output_lines.append(
            f"Warning: Database name missing for table '{table_name}'. Using potentially incorrect context.")
    count = 0
    output_lines.append(f"--- Overview for {full_table_name} ---")
    cursor = None  # Initialize cursor to None
    try:
        cursor = conn.cursor()
        # 1. Get Row Count
        try:
            query = f"SELECT COUNT(*) FROM {full_table_name}"
            # print(f"Executing: {query}") # Debug
            cursor.execute(query)
            count_result = cursor.fetchone()
            if count_result:
                count = count_result[0]
                output_lines.append(f"\nTotal rows: {count}")
            else:
                output_lines.append(f"\nCould not determine total row count.")
        except MySQLError as e:
            output_lines.append(f"Error getting row count for {full_table_name}: {e}")

        # 2. Get Columns (DESCRIBE)
        if count > 0:
            try:
                query = f"DESCRIBE {full_table_name}"
                # print(f"Executing: {query}") # Debug
                cursor.execute(query)
                cols = [desc[0] for desc in cursor.description] if cursor.description else []
                rows = cursor.fetchall()
                output_lines.append(f"\nColumns:")
                if rows:
                    output_lines.append(_format_rows_to_string(cols, rows, limit=limit))
                else:
                    output_lines.append("(Could not retrieve column information or table has no columns).")
            except MySQLError as e:
                output_lines.append(f"Error getting columns for {full_table_name}: {e}")
                # If DESCRIBE fails, likely the table doesn't exist or no access,
                # return early as other queries will also fail.
                return "\n".join(output_lines)

            # 3. Get Sample Rows (LIMIT 5)
            try:
                query = f"SELECT * FROM {full_table_name} LIMIT 3"
                # print(f"Executing: {query}") # Debug
                cursor.execute(query)
                cols = [desc[0] for desc in cursor.description] if cursor.description else []
                rows = cursor.fetchall()
                output_lines.append(f"\nSample rows (limit 3):")
                if rows:
                    output_lines.append(_format_rows_to_string(cols, rows, limit=limit))
                else:
                    output_lines.append(f"(No rows found in {full_table_name}).")
            except MySQLError as e:
                output_lines.append(f"Error getting sample rows for {full_table_name}: {e}")

    except MySQLError as outer_e:
        # Catch errors potentially related to cursor creation or initial connection state
        output_lines.append(f"Database error during overview for {full_table_name}: {outer_e}")
        reset_connection()  # Reset connection on error
    except Exception as gen_e:
        output_lines.append(f"Unexpected error during overview for {full_table_name}: {gen_e}")
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception as close_err:
                print(f"Warning: Error closing cursor for {full_table_name}: {close_err}")  # Log non-critical error

    overview_string = "\n".join(output_lines)
    # Update cache even if there were partial errors, so we cache the error message too
    cache_key = (db_name, table_name)
    global_table_overview_cache[cache_key] = overview_string
    return overview_string


def handle_single_column_query(conn, query):
    # return csv like result set, with column names as first row
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows:
            # Assuming the desired column is the first one
            return "\n".join([str(row[0]) for row in rows])
        else:
            return "None"
    except MySQLError as e:  # Catch specific DB errors
        reset_connection()  # Reset connection on DB error
        return f"Error executing query '{query}': {str(e)}"
    except Exception as e:  # Catch other potential errors
        return f"Unexpected error executing query '{query}': {str(e)}"
    finally:
        if cursor:
            cursor.close()


def handle_read_query(conn, query):
    # return csv like result set, with column names as first row
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        if cursor.description:  # Check if there's a result set description
            columns = [desc[0] for desc in cursor.description]  # Get column names
            rows = cursor.fetchall()

            output = io.StringIO()

            # Convert rows to CSV-like format
            def to_csv_line(row):
                return ",".join(
                    str(item).replace("\"", "\"\"") if isinstance(item, str) else str(item) for item in row)

            output.write(to_csv_line(columns) + "\n")  # Write column names
            for row in rows:
                output.write(to_csv_line(row) + "\n")  # Write data rows

            output.write(f"\n{len(rows)} rows in set\n")
            return output.getvalue()
        else:
            # Handle commands that don't return rows but might have messages (e.g., USE DB)
            # Or potentially commands that succeeded but produced no results (e.g., SELECT on empty table)
            # For simplicity, return a message indicating no result set.
            # More sophisticated handling could check cursor.warning_count etc.
            return "Query executed successfully, but no result set was returned."

    except MySQLError as e:  # Catch specific DB errors
        reset_connection()  # Reset connection on DB error
        return f"Error executing query '{query}': {str(e)}"
    except Exception as e:  # Catch other potential errors
        return f"Unexpected error executing query '{query}': {str(e)}"
    finally:
        if cursor:
            cursor.close()


def handle_write_query(conn, query):
    cursor = conn.cursor()
    start_time = time.time()
    try:
        cursor.execute(query)
        conn.commit()  # Commit changes for DML/DDL
        affected_rows = cursor.rowcount
        elapsed_time = time.time() - start_time
        # Provide a more informative message for DDL/DML
        if affected_rows >= 0:  # rowcount is >= 0 for DML, -1 for DDL or not applicable
            return f"Query OK, {affected_rows} rows affected ({elapsed_time:.2f} sec)"
        else:
            return f"Query OK ({elapsed_time:.2f} sec)"  # For DDL or commands where rowcount is not applicable
    except MySQLError as e:  # Catch specific DB errors
        reset_connection()  # Reset connection on DB error
        try:
            conn.rollback()  # Rollback on error
        except Exception as rb_err:
            print(f"Error during rollback: {rb_err}")  # Log rollback error
        return f"Error executing query '{query}': {str(e)}"
    except Exception as e:  # Catch other potential errors
        return f"Unexpected error executing query '{query}': {str(e)}"
    finally:
        if cursor:
            cursor.close()


@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri="starrocks:///databases",
            name="All Databases",
            description="List all databases in StarRocks",
            mimeType="text/plain"
        )
    ]


SR_PROC_DESC = '''
Internal information exposed by StarRocks similar to linux /proc, following are some common paths:

'/frontends'	Shows the information of FE nodes.
'/backends'	Shows the information of BE nodes if this SR is non cloud native deployment.
'/compute_nodes'	Shows the information of CN nodes if this SR is cloud native deployment.
'/dbs'	Shows the information of databases.
'/dbs/<DB_ID>'	Shows the information of a database by database ID.
'/dbs/<DB_ID>/<TABLE_ID>'	Shows the information of tables by database ID.
'/dbs/<DB_ID>/<TABLE_ID>/partitions'	Shows the information of partitions by database ID and table ID.
'/transactions'	Shows the information of transactions by database.
'/transactions/<DB_ID>' Show the information of transactions by database ID.
'/transactions/<DB_ID>/running' Show the information of running transactions by database ID.
'/transactions/<DB_ID>/finished' Show the information of finished transactions by database ID.
'/jobs'	Shows the information of jobs.
'/statistic'	Shows the statistics of each database.
'/tasks'	Shows the total number of all generic tasks and the failed tasks.
'/cluster_balance'	Shows the load balance information.
'/routine_loads'	Shows the information of Routine Load.
'/colocation_group'	Shows the information of Colocate Join groups.
'/catalog'	Shows the information of catalogs.
'''


@server.list_resource_templates()
async def handle_list_resource_templates() -> list[types.ResourceTemplate]:
    return [
        types.ResourceTemplate(
            uriTemplate="starrocks:///{db}/{table}/schema",
            name="Table Schema",
            description="Get the schema of a table using SHOW CREATE TABLE",
            mimeType="text/plain"
        ),
        types.ResourceTemplate(
            uriTemplate="starrocks:///{db}/tables",
            name="Database Tables",
            description="List all tables in a specific database",
            mimeType="text/plain"
        ),
        types.ResourceTemplate(
            uriTemplate="proc:///{+path}",
            name="System internal information",
            description=SR_PROC_DESC,
            mimeType="text/plain"
        )
    ]


@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    try:
        conn = get_connection()
        if uri.scheme == 'proc':
            return handle_read_query(conn, f"show proc '{uri.path}'")
        if uri.scheme != "starrocks":
            raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

        path_parts = uri.path.strip('/').split('/')
        if len(path_parts) == 3 and path_parts[2] == "schema":
            db, table = path_parts[:2]
            return handle_single_column_query(conn, f"SHOW CREATE TABLE {db}.{table}")
        elif len(path_parts) == 1 and path_parts[0] == "databases":
            return handle_single_column_query(conn, "SHOW DATABASES")
        elif len(path_parts) == 2 and path_parts[1] == "tables":
            return handle_single_column_query(conn, f"SHOW TABLES FROM {path_parts[0]}")
        else:
            raise ValueError(f"Unsupported URI path: {uri.path}")
    except MySQLError as e:  # Catch DB errors
        reset_connection()
        # Return error message suitable for MCP client
        return f"Database Error: {str(e)}"
    except Exception as e:
        reset_connection()
        raise ValueError(f"Error retrieving resource: {str(e)}")


@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return []


@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
    raise ValueError(f"Unsupported get_prompt")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    table_overview_desc = "Get an overview of a specific table: columns, sample rows (up to 5), and total row count. Uses cache unless refresh=true."
    table_overview_prop_desc = "<db>.<table> required."
    if default_database:
        table_overview_prop_desc = f"[db.]<table> required. Uses default database '{default_database}' if `db` part is omitted."

    db_overview_desc = "Get an overview (columns, sample rows, row count) for ALL tables in a database. Uses cache unless refresh=True."
    db_overview_prop_desc = "Database name required."
    if default_database:
        db_overview_prop_desc = f"Database name. Optional: uses the default database '{default_database}' if not provided."
    return [
        types.Tool(
            name="read_query",
            description="Execute a SELECT query or commands that return a ResultSet",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "SQL query to execute"},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="write_query",
            description="Execute an DDL/DML or other StarRocks command that do not have a ResultSet",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "SQL to execute"},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="query_and_plotly_chart",
            description="using sql `query` to extract data from database, then using python `plotly_expr` to generate a chart for UI to display",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL query to execute",
                    },
                    "plotly_expr": {
                        "type": "string",
                        "description": "a one function call expression, with 2 vars binded: `px` as `import plotly.express as px`, and `df` as dataframe generated by query `plotly_expr` example: `px.scatter(df, x=\"sepal_width\", y=\"sepal_length\", color=\"species\", marginal_y=\"violin\", marginal_x=\"box\", trendline=\"ols\", template=\"simple_white\")`",
                    },
                },
            }
        ),
        types.Tool(
            name="table_overview",
            description=table_overview_desc,
            inputSchema={
                "type": "object",
                "properties": {
                    "table": {
                        "type": "string",
                        "description": table_overview_prop_desc,
                    },
                    "refresh": {
                        "type": "boolean",
                        "description": "Optional: Set to true to force refresh the overview, ignoring the cache. Defaults to false.",
                        "default": False,
                    }
                },
                "required": ["table"],
            },
        ),
        types.Tool(
            name="db_overview",
            description=db_overview_desc,
            inputSchema={
                "type": "object",
                "properties": {
                    "db": {
                        "type": "string",
                        "description": db_overview_prop_desc,
                    },
                    "refresh": {
                        "type": "boolean",
                        "description": "Optional: Set to true to force refresh the overview, ignoring the cache. Defaults to false.",
                        "default": False,
                    }
                },
                "required": [] if default_database else ["db"]
            },
        ),
    ]


def query_and_plotly_chart(conn, query: str, plotly_expr: str):
    """
    Executes an SQL query, creates a Pandas DataFrame, generates a Plotly chart
    using the provided expression, encodes the chart as a base64 PNG image,
    and returns it along with optional text.

    Args:
        conn: A database connection object (DB-API 2.0 compliant).
        query: The SQL query string to execute.
        plotly_expr: A Python string expression using 'px' (plotly.express)
                     and 'df' (the DataFrame from the query) to generate a figure.
                     Example: "px.scatter(df, x='col1', y='col2')"

    Returns:
        A list containing types.TextContent and types.ImageContent,
        or just types.TextContent in case of an error or no data.

    Raises:
        Exception: Propagates exceptions from database interaction,
                   pandas, plotly expression evaluation, or image generation,
                   after attempting to close the cursor.
    """
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        # Check if cursor.description is None (happens for non-SELECT queries)
        if cursor.description is None:
            return [types.TextContent(type="text", text=f'Query "{query}" did not return data suitable for plotting.')]
        column_names = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=column_names)
        if df.empty:
            return [types.TextContent(type="text", text='Query returned no data to plot.')]

        # evaluate the plotly expression using px and df, get result figure as `fig`
        # SECURITY WARNING: eval() can execute arbitrary code. Only use this if
        # 'plotly_expr' comes from a trusted source or is heavily sanitized.
        # In a production scenario with untrusted input, consider safer alternatives
        # like AST parsing or a restricted execution environment.
        local_vars = {'df': df}
        fig = eval(plotly_expr, {"px": px}, local_vars)  # Pass px in globals, df in locals

        if not hasattr(fig, 'to_image'):
            raise ValueError(
                f"The evaluated expression did not return a Plotly figure object. Result type: {type(fig)}")

        img_bytes = fig.to_image(format='jpg', width=960, height=720)
        # save to tmp file for debugging
        # with open("chart.jpg", "wb") as f:
        #     f.write(img_bytes)
        # base64 encode the image bytes
        img_base64_bytes = base64.b64encode(img_bytes)
        # Decode bytes to utf-8 string for easier handling (e.g., JSON serialization)
        img_base64_string = img_base64_bytes.decode('utf-8')
        return [
            types.TextContent(type="text", text=f'dataframe data:\n{df}\nChart generated but for UI only'),
            types.ImageContent(type="image", mimeType="image/jpg", data=img_base64_string)
        ]
    except (MySQLError, pd.errors.EmptyDataError) as db_pd_err:
        # Handle DB or Pandas specific errors gracefully
        return [types.TextContent(type="text", text=f'Error during data fetching or processing: {db_pd_err}')]
    except Exception as eval_err:
        # Handle errors during eval or image generation
        return [types.TextContent(type="text", text=f'Error during chart generation: {eval_err}')]
    finally:
        # Ensure the cursor is always closed
        if cursor:
            cursor.close()


@server.call_tool()
async def handle_call_tool(
        name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    try:
        conn = get_connection()
        if name == "read_query":
            return [types.TextContent(type="text", text=handle_read_query(conn, arguments["query"]))]

        elif name == "write_query":
            return [types.TextContent(type="text", text=handle_write_query(conn, arguments["query"]))]

        elif name == "query_and_plotly_chart":
            return query_and_plotly_chart(conn, arguments["query"], arguments['plotly_expr'])

        elif name == "table_overview":
            table_arg = arguments.get("table")
            refresh = arguments.get("refresh", False)
            if not table_arg:
                return [types.TextContent(type="text", text="Error: Missing 'table' argument.")]

            # Parse table argument: [db.]<table>
            parts = table_arg.split('.', 1)
            db_name = None
            table_name = None
            if len(parts) == 2:
                db_name, table_name = parts[0], parts[1]
            elif len(parts) == 1:
                table_name = parts[0]
                db_name = default_database  # Use default if only table name is given

            if not table_name:  # Should not happen if table_arg exists, but check
                return [types.TextContent(type="text", text=f"Error: Invalid table name format '{table_arg}'.")]
            if not db_name:
                return [types.TextContent(type="text",
                                          text=f"Error: Database name not specified for table '{table_name}' and no default database is set.")]

            cache_key = (db_name, table_name)

            # Check cache
            if not refresh and cache_key in global_table_overview_cache:
                # print(f"Cache hit for table overview: {cache_key}") # Debug
                return [types.TextContent(type="text", text=global_table_overview_cache[cache_key])]

            # Fetch details (will also update cache)
            # print(f"Cache miss or refresh for table overview: {cache_key}") # Debug
            overview_text = _get_table_details(conn, db_name, table_name, limit=overview_length_limit)
            return [types.TextContent(type="text", text=overview_text)]

        elif name == "db_overview":
            db_name_arg = arguments.get("db")
            refresh = arguments.get("refresh", False)

            db_name = db_name_arg if db_name_arg else default_database
            if not db_name:
                return [types.TextContent(type="text",
                                          text="Error: Database name not provided and no default database is set.")]

            # List tables in the database
            cursor = None
            try:
                cursor = conn.cursor()
                query = f"SHOW TABLES FROM `{db_name}`"  # Use backticks
                # print(f"Executing: {query}") # Debug
                cursor.execute(query)
                tables = [row[0] for row in cursor.fetchall()]
            except MySQLError as e:
                print(f"Error listing tables in '{db_name}': {e}")
                reset_connection()
                return [types.TextContent(type="text", text=f"Database Error listing tables in '{db_name}': {e}")]
            except Exception as e:
                print(f"Unexpected error listing tables in '{db_name}': {e}")
                return [types.TextContent(type="text", text=f"Unexpected error listing tables in '{db_name}': {e}")]
            finally:
                if cursor:
                    try:
                        cursor.close()
                    except Exception as ce:
                        print(f"Warning: error closing cursor: {ce}")

            if not tables:
                return [types.TextContent(type="text", text=f"No tables found in database '{db_name}'.")]

            all_overviews = [f"--- Overview for Database: `{db_name}` ({len(tables)} tables) ---"]
            # print(f"Generating overview for {len(tables)} tables in '{db_name}' (refresh={refresh})") # Debug

            total_length = 0
            limit_per_table = overview_length_limit * (math.log10(len(tables)) + 1) // len(tables)  # Limit per table
            for table_name in tables:
                cache_key = (db_name, table_name)
                overview_text = None

                # Check cache first
                if not refresh and cache_key in global_table_overview_cache:
                    # print(f"Cache hit for db overview (table): {cache_key}") # Debug
                    overview_text = global_table_overview_cache[cache_key]
                else:
                    # print(f"Cache miss or refresh for db overview (table): {cache_key}") # Debug
                    # Fetch details for this table (will update cache via _get_table_details)
                    overview_text = _get_table_details(conn, db_name, table_name, limit=limit_per_table)

                all_overviews.append(overview_text)
                all_overviews.append("\n")  # Add separator
                total_length += len(overview_text)+1

            return [types.TextContent(type="text", text="\n".join(all_overviews))]

        # If tool name not found
        return [types.TextContent(type="text", text=f"Error: Unknown tool name '{name}'")]
    except MySQLError as e:  # Catch DB errors at tool call level
        reset_connection()
        return [types.TextContent(type="text", text=f"Database Error executing tool '{name}': {type(e).__name__}: {e}")]
    except Exception as e:
        # Catch any other unexpected errors during tool execution
        reset_connection()  # Also reset connection on unexpected errors
        stack_trace = traceback.format_exc()
        return [
            types.TextContent(type="text",
                              text=f"Unexpected Error executing tool '{name}': {type(e).__name__}: {e}\nStack Trace:\n{stack_trace}")]


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-server-starrocks",
                server_version=SERVER_VERSION,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


async def run_tool_test():
    result_table = await handle_call_tool("table_overview", {"table":"quickstart.crashdata"})
    print("Result:")
    for item in result_table:
        if isinstance(item, types.TextContent):
            print(item.text)
        else:
            print(f"Received non-text content: {type(item)}")
    print("-" * 20)


if __name__ == "__main__":
    import asyncio

    # Example usage (requires environment variables set)
    print(f"Default database (STARROCKS_DB): {default_database or 'Not Set'}")
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Run the test function
        try:
            asyncio.run(run_tool_test())
        except Exception as test_err:
            print(f"\nError running test function: {test_err}")
        finally:
            reset_connection()  # Ensure cleanup even if run_tool_test fails badly
    else:
        asyncio.run(main())
        print("MCP Server script loaded. Run via MCP host.")

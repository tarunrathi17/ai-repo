import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
import time

def data_inference_agent(state: dict) -> dict:
    user_query = state.get("user_query", "")
    print(f"\n🔎 Data Inference Agent received query: {user_query}")

    query = user_query.lower().strip()

    # Handle help requests
    help_keywords = ["help", "what can you do", "how can you help"]
    if any(kw in query for kw in help_keywords):
        return {
            **state,
            "message": "Here’s what I can help you with:",
            "inference": (
                "I can help you:\n"
                "- Filter sales by value (e.g., 'sales more than 30000')\n"
                "- Show top/bottom N states by sales (e.g., 'top 5 states')\n"
                "- Find highest or lowest performing states in a region\n"
                "- Calculate average sales for a region\n"
                "- Export results to CSV and charts"
            )
        }

    # Connect to DB
    conn = sqlite3.connect("database.db")

    # ------------------------------
    # 1. Top/Bottom N states
    # ------------------------------
    top_match = re.search(r"top\s+(\d+)", query)
    bottom_match = re.search(r"bottom\s+(\d+)", query)

    if top_match or bottom_match:
        n = int(top_match.group(1)) if top_match else int(bottom_match.group(1))
        order = "DESC" if top_match else "ASC"

        sql_query = f"""
        SELECT region, state, sales
        FROM sales_data
        ORDER BY sales {order}
        LIMIT {n}
        """
        df = pd.read_sql_query(sql_query, conn)

    # ------------------------------
    # 2. Highest/Lowest in region
    # ------------------------------
    elif "highest in" in query or "lowest in" in query:
        region_match = re.search(r"(highest|lowest)\s+in\s+(\w+)", query)
        if region_match:
            direction = region_match.group(1)
            region = region_match.group(2).capitalize()
            order = "DESC" if direction == "highest" else "ASC"

            sql_query = f"""
            SELECT region, state, sales
            FROM sales_data
            WHERE region = '{region}'
            ORDER BY sales {order}
            LIMIT 1
            """
            df = pd.read_sql_query(sql_query, conn)
        else:
            return {**state, "message": "Could not parse region for highest/lowest query."}

    # ------------------------------
    # 3. Average sales in region
    # ------------------------------
    elif "average in" in query:
        region_match = re.search(r"average\s+in\s+(\w+)", query)
        if region_match:
            region = region_match.group(1).capitalize()
            sql_query = f"""
            SELECT region, state, sales
            FROM sales_data
            WHERE region = '{region}'
            """
            df = pd.read_sql_query(sql_query, conn)
        else:
            return {**state, "message": "Could not parse region for average query."}

    # ------------------------------
    # 4. Standard filter: more than / less than
    # ------------------------------
    else:
        min_val = max_val = None
        more_than_match = re.search(r"more than\s+(\d+)", query)
        less_than_match = re.search(r"less than\s+(\d+)", query)

        if more_than_match:
            min_val = int(more_than_match.group(1))
        if less_than_match:
            max_val = int(less_than_match.group(1))

        if min_val is None and max_val is None:
            return {
                **state,
                "error": "Unsupported query. Try 'top 3 states', 'sales more than 50000', etc."
            }

        sql_query = "SELECT region, state, sales FROM sales_data WHERE"
        conditions = []
        if min_val is not None:
            conditions.append(f" sales > {min_val} ")
        if max_val is not None:
            conditions.append(f" sales < {max_val} ")
        sql_query += " AND ".join(conditions)
        df = pd.read_sql_query(sql_query, conn)

    conn.close()

    # If empty
    if df.empty:
        return {
            **state,
            "sql_query": sql_query,
            "message": "No data found for this query.",
            "inference": "No matching data for the given filters."
        }

    # Save outputs
    os.makedirs("output", exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    csv_path = f"output/query_result_{timestamp}.csv"
    plot_path = f"output/query_plot_{timestamp}.png"
    df.to_csv(csv_path, index=False)

    # Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x="state", y="sales", hue="region", data=df)
    plt.title("Sales by State and Region")
    plt.xlabel("State")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    # Inference
    total_sales = df["sales"].sum()
    avg_sales = df["sales"].mean()
    top_row = df.loc[df["sales"].idxmax()]
    inference = (
        f"The data includes {len(df)} states with total sales of {total_sales:,}. "
        f"Average sales is {avg_sales:,.0f}. "
        f"Top performing state is {top_row['state']} ({top_row['region']}) with {top_row['sales']:,}."
    )

    return {
        **state,
        "sql_query": sql_query,
        "csv_path": csv_path,
        "plot_path": plot_path,
        "inference": inference,
        "message": "Query executed successfully with smart inference."
    }

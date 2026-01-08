#!/usr/bin/env python3
"""
Export Gold Layer Tables from DBT DuckDB to CSV Format

Script to extract analytics-ready tables from the gold layer
and save them as CSV files for Power BI import.
"""

import duckdb
import pandas as pd
from pathlib import Path

# Configuration - Project Paths
PROJECT_ROOT = Path(__file__).parent  # Root directory of the project
DBT_PROJECT_PATH = PROJECT_ROOT / "dbt_project"  # DBT project directory
GOLD_LAYER_PATH = PROJECT_ROOT / "data" / "gold"  # Gold layer output directory
DBT_DATABASE_PATH = DBT_PROJECT_PATH / "target" / "duckdb.db"  # DBT compiled database

# Ensure output directory exists
GOLD_LAYER_PATH.mkdir(parents=True, exist_ok=True)

# Gold Layer Tables to Export
GOLD_LAYER_TABLES = [
    "dim_time",
    "dim_company",
    "dim_location",
    "dim_skills",
    "fact_job_offers",
    "fact_job_skills",
    "agg_job_offers_by_category_time",
    "agg_skills_demand",
    "agg_location_analysis"
]

def export_tables():
    """Export all gold layer tables to CSV format"""
    print(f"\nExporting Gold Layer Tables to CSV\n")
    print(f"{'=' * 70}")
    
    try:
        # Connect to DuckDB
        if DBT_DATABASE_PATH.exists():
            print(f"Database found: {DBT_DATABASE_PATH}")
            dbt_connection = duckdb.connect(str(DBT_DATABASE_PATH), read_only=True)
        else:
            print(f"Warning: Database not found at {DBT_DATABASE_PATH}")
            print(f"Creating in-memory connection")
            dbt_connection = duckdb.connect(":memory:")
            return False
        
        # Export each table
        exported_table_count = 0
        for table_name in GOLD_LAYER_TABLES:
            try:
                # Try different schema patterns
                schema_names = ["main_gold", "gold", "main"]
                table_found = False
                
                for schema_name in schema_names:
                    try:
                        # Build query
                        sql_query = f"SELECT * FROM {schema_name}.{table_name}"
                        
                        # Execute query
                        query_result = dbt_connection.execute(sql_query).fetchdf()
                        
                        # Define output CSV file
                        csv_output_file = GOLD_LAYER_PATH / f"{table_name}.csv"
                        
                        # Export to CSV
                        query_result.to_csv(csv_output_file, index=False)
                        
                        # Print success
                        row_count = len(query_result)
                        print(f"Exported {table_name:40} ({row_count:>8} rows)")
                        exported_table_count += 1
                        table_found = True
                        break
                    except:
                        continue
                
                if not table_found:
                    print(f"Warning: Table {table_name} not found in any schema")
                        
            except Exception as error:
                print(f"Error exporting {table_name}: {error}")
        
        # Summary
        print(f"\n{'=' * 70}")
        print(f"Export Complete: {exported_table_count}/{len(GOLD_LAYER_TABLES)} tables")
        print(f"Output directory: {GOLD_LAYER_PATH}\n")
        
        dbt_connection.close()
        return True
        
    except Exception as error:
        print(f"Error during export: {error}")
        return False

if __name__ == "__main__":
    export_success = export_tables()
    exit(0 if export_success else 1)

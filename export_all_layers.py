#!/usr/bin/env python3
"""
Export ALL Data Layers (Bronze, Silver, Gold) from DBT DuckDB to CSV Format

Script to extract all transformation layers from the DBT project
and save them as CSV files for analysis and validation.
"""

import duckdb
import pandas as pd
from pathlib import Path

# Configuration - Project Paths
PROJECT_ROOT = Path(__file__).parent  # Root directory of the project
DBT_PROJECT_PATH = PROJECT_ROOT / "dbt_project"  # DBT project directory
DATA_LAYERS_PATH = PROJECT_ROOT / "data"  # Data layers root directory
DBT_DATABASE_PATH = DBT_PROJECT_PATH / "target" / "duckdb.db"  # DBT compiled database

# Data Layers Structure
DATA_LAYERS_STRUCTURE = {
    "bronze": [
        "stg_jobs_raw"
    ],
    "silver": [
        "int_jobs_cleaned",
        "int_job_title_normalization",
        "int_skills_extraction"
    ],
    "gold": [
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
}

# Database Schema Mapping
DBT_SCHEMA_MAPPING = {
    "bronze": "main_bronze",
    "silver": "main_silver",
    "gold": "main_gold"
}

def export_all_layers():
    """Export all data layers to CSV format"""
    print(f"\nExporting All Data Layers (Bronze/Silver/Gold) to CSV\n")
    print(f"{'=' * 80}")
    
    try:
        # Validate database exists
        if not DBT_DATABASE_PATH.exists():
            print(f"Error: Database not found at {DBT_DATABASE_PATH}")
            return False
        
        print(f"Database found: {DBT_DATABASE_PATH}\n")
        
        # Connect to DuckDB
        dbt_connection = duckdb.connect(str(DBT_DATABASE_PATH), read_only=True)
        
        total_tables_exported = 0
        
        # Export each layer
        for layer_name, layer_tables in DATA_LAYERS_STRUCTURE.items():
            # Create output directory for layer
            layer_output_path = DATA_LAYERS_PATH / layer_name
            layer_output_path.mkdir(parents=True, exist_ok=True)
            
            # Get database schema
            database_schema = DBT_SCHEMA_MAPPING.get(layer_name, f"main_{layer_name}")
            
            print(f"\n{layer_name.upper()} Layer")
            print(f"{'-' * 80}")
            
            # Export each table in layer
            for table_name in layer_tables:
                try:
                    # Build SQL query
                    sql_query = f"SELECT * FROM {database_schema}.{table_name}"
                    
                    # Execute query
                    table_data = dbt_connection.execute(sql_query).fetchdf()
                    
                    # Define output CSV file
                    csv_output_file = layer_output_path / f"{table_name}.csv"
                    
                    # Export to CSV
                    table_data.to_csv(csv_output_file, index=False)
                    
                    # Get statistics
                    row_count = len(table_data)
                    file_size_mb = csv_output_file.stat().st_size / (1024 * 1024)
                    
                    # Print success message
                    print(f"  {table_name:45} {row_count:>8} rows  {file_size_mb:>7.2f} MB")
                    total_tables_exported += 1
                    
                except Exception as export_error:
                    error_message = str(export_error)[:50]
                    print(f"  {table_name:45} Error: {error_message}")
        
        # Summary
        total_tables_available = sum(len(tables) for tables in DATA_LAYERS_STRUCTURE.values())
        print(f"\n{'=' * 80}")
        print(f"Export Summary: {total_tables_exported}/{total_tables_available} tables exported")
        
        print(f"\nOutput Directories:")
        for layer_name in DATA_LAYERS_STRUCTURE.keys():
            layer_path = DATA_LAYERS_PATH / layer_name
            print(f"  {layer_name.capitalize():10} - {layer_path}")
        print()
        
        # Close connection
        dbt_connection.close()
        return True
        
    except Exception as error:
        print(f"Error during export: {error}")
        return False

if __name__ == "__main__":
    export_success = export_all_layers()
    exit(0 if export_success else 1)

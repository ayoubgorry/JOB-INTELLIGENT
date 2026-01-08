#!/usr/bin/env python3
"""
JOB INTELLIGENT - Data Pipeline Orchestration Script
Purpose: Orchestrate DBT runs and export data to CSV/Parquet
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# Configuration - Project Paths
PROJECT_ROOT = Path(__file__).parent  # Root directory of the project
DBT_PROJECT_PATH = PROJECT_ROOT / "dbt_project"  # DBT project directory
DATA_PATH = PROJECT_ROOT / "data"  # Data layers root directory
BRONZE_LAYER_PATH = DATA_PATH / "bronze"  # Raw data layer (staging)
SILVER_LAYER_PATH = DATA_PATH / "silver"  # Transformed data layer
GOLD_LAYER_PATH = DATA_PATH / "gold"  # Analytics-ready data layer
SOURCE_DATA_FILE = PROJECT_ROOT / "final_data.csv"  # Source data file

# Colors for console output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_section(title):
    """Print a section header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Colors.ENDC}\n")

def print_success(message):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def print_info(message):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")

def run_command(command, cwd=None):
    """Run a shell command"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def check_dependencies():
    """Check if required packages are installed"""
    print_section("Checking Dependencies")
    
    dependencies = {
        'dbt': 'dbt-core',
        'duckdb': 'duckdb',
        'pandas': 'pandas'
    }
    
    missing = []
    for name, package in dependencies.items():
        try:
            __import__(name)
            print_success(f"{package} is installed")
        except ImportError:
            print_warning(f"{package} is NOT installed")
            missing.append(package)
    
    if missing:
        print_error(f"\nMissing dependencies: {', '.join(missing)}")
        print_info(f"Install with: pip install {' '.join(missing)}")
        return False
    
    return True

def initialize_dbt():
    """Initialize DBT project"""
    print_section("Initializing DBT")
    
    # Check dbt_project.yml exists
    if not (DBT_PROJECT_PATH / "dbt_project.yml").exists():
        print_error("dbt_project.yml not found!")
        return False
    
    print_info(f"DBT Project Path: {DBT_PROJECT_PATH}")
    
    # Run dbt debug
    success, output = run_command("dbt debug", cwd=DBT_PROJECT_PATH)
    if success:
        print_success("DBT debug passed")
        return True
    else:
        print_error(f"DBT debug failed: {output}")
        return False

def copy_source_data():
    """Copy source data from root to bronze layer"""
    print_section("Copying Source Data to Bronze Layer")
    
    source_file = SOURCE_DATA_FILE
    bronze_output_path = BRONZE_LAYER_PATH / "final_data.csv"
    
    if not source_file.exists():
        print_error(f"Source file not found: {source_file}")
        return False
    
    try:
        # Ensure bronze directory exists
        BRONZE_LAYER_PATH.mkdir(parents=True, exist_ok=True)
        
        # Copy file to bronze layer
        shutil.copy2(source_file, bronze_output_path)
        print_success(f"Copied {source_file.name} to {BRONZE_LAYER_PATH}")
        
        # Get file size
        size_mb = source_file.stat().st_size / (1024 * 1024)
        print_info(f"File size: {size_mb:.2f} MB")
        
        return True
    except Exception as e:
        print_error(f"Failed to copy file: {e}")
        return False

def run_dbt_transformation():
    """Run DBT transformation"""
    print_section("Running DBT Transformation")
    
    print_info("Executing: dbt run")
    success, output = run_command("dbt run", cwd=DBT_PROJECT_PATH)
    
    if success:
        print_success("DBT run completed successfully")
        print(output)
        return True
    else:
        print_error(f"DBT run failed: {output}")
        return False

def run_dbt_tests():
    """Run DBT tests (optional)"""
    print_section("Running DBT Tests")
    
    print_info("Executing: dbt test")
    success, output = run_command("dbt test", cwd=DBT_PROJECT_PATH)
    
    if success:
        print_success("All tests passed")
        return True
    else:
        print_warning(f"Some tests failed: {output}")
        return True  # Don't fail pipeline

def export_to_csv():
    """Export Gold layer tables to CSV format"""
    print_section("Exporting Gold Layer to CSV")
    
    try:
        import duckdb
        import pandas as pd
    except ImportError:
        print_error("duckdb and pandas required for export")
        return False
    
    try:
        # Ensure gold directory exists
        GOLD_LAYER_PATH.mkdir(parents=True, exist_ok=True)
        
        # Connect to DuckDB database
        dbt_database_path = DBT_PROJECT_PATH / "target" / "duckdb.db"
        
        if not dbt_database_path.exists():
            print_warning(f"Database not found: {dbt_database_path}")
            print_info("Using in-memory database instead")
            dbt_connection = duckdb.connect(":memory:")
        else:
            dbt_connection = duckdb.connect(str(dbt_database_path))
        
        # List of Gold tables to export
        gold_layer_tables = [
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
        
        # Export each table
        exported_count = 0
        for table_name in gold_layer_tables:
            try:
                # Query the table from gold schema
                query_result = dbt_connection.execute(f"SELECT * FROM gold.{table_name}").fetchdf()
                
                # Define output path
                csv_output_file = GOLD_LAYER_PATH / f"{table_name}.csv"
                
                # Export to CSV
                query_result.to_csv(csv_output_file, index=False)
                
                print_success(f"Exported {table_name} ({len(query_result)} rows)")
                exported_count += 1
                
            except Exception as e:
                print_warning(f"Failed to export {table_name}: {e}")
        
        # Close database connection
        dbt_connection.close()
        
        print_info(f"Total tables exported: {exported_count}/{len(gold_layer_tables)}")
        return True
        
    except Exception as e:
        print_error(f"Export failed: {e}")
        return False

def generate_summary():
    """Generate summary of transformation execution"""
    print_section("Summary Report")
    
    try:
        # Count files in each layer
        bronze_layer_files = list(BRONZE_LAYER_PATH.glob("*.csv"))
        silver_layer_files = list(SILVER_LAYER_PATH.glob("*.csv"))
        gold_layer_files = list(GOLD_LAYER_PATH.glob("*.csv"))
        
        print(f"\n{Colors.BOLD}Data Layers Summary:{Colors.ENDC}")
        print(f"  Bronze Layer: {len(bronze_layer_files)} files")
        print(f"  Silver Layer: {len(silver_layer_files)} files")
        print(f"  Gold Layer: {len(gold_layer_files)} files")
        
        # Check DBT documentation
        dbt_documentation_path = DBT_PROJECT_PATH / "target"
        if dbt_documentation_path.exists():
            print(f"\n{Colors.BOLD}DBT Documentation:{Colors.ENDC}")
            print(f"  Location: {dbt_documentation_path}")
            print(f"  View with: dbt docs serve")
        
        print(f"\n{Colors.BOLD}Next Steps:{Colors.ENDC}")
        print(f"  1. Review CSV files in: {GOLD_LAYER_PATH}")
        print(f"  2. Open Power BI Desktop")
        print(f"  3. Import CSV files from: {GOLD_LAYER_PATH}")
        print(f"  4. Create relationships and dashboards")
        
        # Timestamp
        execution_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{Colors.OKGREEN}Successfully completed at {execution_timestamp}{Colors.ENDC}\n")
        
    except Exception as e:
        print_error(f"Failed to generate summary: {e}")

def main():
    """Main orchestration function"""
    
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("  JOB INTELLIGENT - Data Pipeline")
    print(f"{Colors.ENDC}\n")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print_error("Please install missing dependencies and try again")
        sys.exit(1)
    
    # Step 2: Initialize DBT
    if not initialize_dbt():
        print_error("Failed to initialize DBT")
        sys.exit(1)
    
    # Step 3: Copy source data
    if not copy_source_data():
        print_warning("Failed to copy source data, continuing...")
    
    # Step 4: Run DBT
    if not run_dbt_transformation():
        print_error("DBT transformation failed")
        sys.exit(1)
    
    # Step 5: Run tests (optional)
    run_dbt_tests()
    
    # Step 6: Export to CSV
    if not export_to_csv():
        print_warning("Failed to export CSV files")
    
    # Step 7: Summary
    generate_summary()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\n\nPipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nFatal error: {e}")
        sys.exit(1)

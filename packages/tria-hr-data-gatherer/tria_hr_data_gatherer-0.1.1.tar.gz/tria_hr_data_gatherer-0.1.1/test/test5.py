#!/usr/bin/env python
"""
Improved test script for TriaHRDataGatherer with demo mode
"""

import logging
import time
import argparse
import sys
import os
from datetime import datetime
import pandas as pd

from tria_hr_data_gatherer import TriaHRDataGatherer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("deduplication_test.log", encoding='utf-8'),  # Specify UTF-8 encoding
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_test(interactive: bool = False, demo_mode: bool = False):
    """
    Test the enhanced deduplication functionality

    Args:
        interactive: Whether to run in interactive mode
        demo_mode: Whether to use demo mode (faster, fewer employees)
    """
    mode_desc = []
    if interactive:
        mode_desc.append("interactive")
    if demo_mode:
        mode_desc.append("demo")
    mode_str = " and ".join(mode_desc) if mode_desc else "standard"

    start_time = time.time()
    logger.info(f"Starting deduplication test in {mode_str} mode")

    try:
        # Create data gatherer with debug mode enabled
        gatherer = TriaHRDataGatherer(
            base_url="https://decasport.triahr.com",
            client_id="13_61ev6jlbu6ko8sgk4cg0cg0scss4oc8sg8wkwsokoowo48gooo",
            client_secret="4jqizm9xg1kwk8c88gkow0w0owkcss4sk8kg4c0kkwwwwo0gos",
            debug=True
        )

        # Define test parameters
        company_id = 1
        test_month = 3
        test_year = 2025

        logger.info(f"Fetching data for company_id={company_id}, month={test_month}/{test_year}")

        # Get company data with potential interactive deduplication
        result = gatherer.get_data_by_company(
            month=test_month,
            year=test_year,
            company_id=company_id,
            interactive=interactive,
            demo_mode=demo_mode
        )

        company_data = result['employees']
        duplicates = result['duplicates']

        logger.info(f"Successfully fetched data for {len(company_data)} employees")
        logger.info(f"Found {len(duplicates)} potential duplicate employees")

        # Create output directory
        output_dir = "deduplication_test_output"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save duplicate report if duplicates were found
        if duplicates:
            # Save as CSV
            duplicate_filename = f"{output_dir}/duplicate_report_{timestamp}.csv"
            gatherer.save_duplicate_report(duplicates, duplicate_filename)

            # Display summary in log
            logger.info("\nDuplicate Employees Summary:")
            for i, dup in enumerate(duplicates[:5]):  # Show up to 5 duplicates in log
                logger.info(f"  {i + 1}. {dup['hrid']} - {dup['name']} {dup['surname']} - {dup['action']}")

            if len(duplicates) > 5:
                logger.info(f"  ... and {len(duplicates) - 5} more (see {duplicate_filename})")

            # Analyze duplicates by unit (safely using ASCII arrow instead of Unicode)
            duplication_by_unit = {}
            for dup in duplicates:
                first_unit = dup.get('first_unit') or 'Unknown'
                dup_unit = dup.get('duplicate_unit') or 'Unknown'

                key = f"{first_unit} to {dup_unit}"  # Using simple ASCII 'to' instead of Unicode arrow
                duplication_by_unit[key] = duplication_by_unit.get(key, 0) + 1

            logger.info("\nDuplication patterns by unit:")
            for pattern, count in sorted(duplication_by_unit.items(), key=lambda x: x[1], reverse=True):
                logger.info(f"  {pattern}: {count} duplicates")

        # Convert to DataFrames for employee data
        debug_df, workforce_df, time_df, cb_df = gatherer.to_dataframes(company_data)

        # Save employee data
        workforce_df.to_csv(f"{output_dir}/workforce_data_{timestamp}.csv", index=False)

        # Run a test with date range to demonstrate functionality across multiple months
        if not interactive:  # Skip in interactive mode to avoid too many prompts
            # In demo mode, only do a 2-month range to keep it quick
            month_from = 2 if demo_mode else 1
            year_from = 2025

            logger.info(f"\nTesting date range functionality ({month_from}-{test_month}/{year_from})")

            date_range_result = gatherer.get_data_time_segment_by_company(
                month_from=month_from,
                year_from=year_from,
                month_to=test_month,
                year_to=test_year,
                company_id=company_id,
                interactive=False,
                demo_mode=demo_mode
            )

            # Count total duplicates across all months
            total_duplicates = sum(len(dups) for dups in date_range_result['duplicates'].values())
            logger.info(f"Date range test completed with {total_duplicates} total duplicates across all months")

            # Save the multi-month duplicate report
            if total_duplicates > 0:
                all_duplicates = []
                for (year, month), month_duplicates in date_range_result['duplicates'].items():
                    for dup in month_duplicates:
                        dup['year'] = year
                        dup['month'] = month
                        all_duplicates.append(dup)

                # Save as CSV
                multi_month_filename = f"{output_dir}/multi_month_duplicates_{timestamp}.csv"
                pd.DataFrame(all_duplicates).to_csv(multi_month_filename, index=False)
                logger.info(f"Multi-month duplicate report saved to {multi_month_filename}")

        elapsed_time = time.time() - start_time
        logger.info(f"Test completed in {elapsed_time:.2f} seconds")
        return True

    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)
        return False


def main():
    """Main function to run the test with commandline options"""
    parser = argparse.ArgumentParser(description='Test TriaHRDataGatherer deduplication functionality')
    parser.add_argument('--interactive', action='store_true',
                        help='Run in interactive mode with prompts for duplicate resolution')
    parser.add_argument('--demo', action='store_true',
                        help='Run in demo mode with limited data for faster testing')

    args = parser.parse_args()

    return 0 if run_test(interactive=args.interactive, demo_mode=args.demo) else 1


if __name__ == "__main__":
    sys.exit(main())
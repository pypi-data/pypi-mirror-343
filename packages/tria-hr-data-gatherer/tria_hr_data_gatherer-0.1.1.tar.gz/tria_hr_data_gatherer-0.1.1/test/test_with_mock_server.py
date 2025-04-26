#!/usr/bin/env python
"""
Test script for the TriaHRDataGatherer using the mock server
"""

import os
import sys
import logging
from datetime import datetime

from tria_hr_data_gatherer import TriaHRDataGatherer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mock_server_test.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_test(interactive: bool = False):
    """Run test against the mock server"""
    logger.info("Starting test with mock server")

    try:
        # Create data gatherer with mock server config
        gatherer = TriaHRDataGatherer.from_config(
            config_path='../mock_server/config.ini',  # Using the mock server config
            environment='stage',  # This should point to localhost:5000
            debug=True  # Enable debug logging
        )

        # Test the connection
        logger.info("Testing connection to mock server...")
        gatherer.test_connection()
        logger.info("Connection successful!")

        # Test company-level data retrieval
        logger.info("Retrieving data for company 1 for March 2025")
        result = gatherer.get_data_by_company(
            month=3,
            year=2025,
            company_id=1,
            interactive=interactive
        )

        company_data = result['employees']
        duplicates = result['duplicates']

        logger.info(f"Successfully fetched data for {len(company_data)} employees")
        logger.info(f"Found {len(duplicates)} potential duplicate employees")

        # Create output directory
        output_dir = "mock_test_output"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save duplicate report if duplicates were found
        if duplicates:
            duplicate_filename = f"{output_dir}/mock_duplicate_report_{timestamp}.csv"
            gatherer.save_duplicate_report(duplicates, duplicate_filename)

            logger.info("\nDuplicate Employees Summary:")
            for i, dup in enumerate(duplicates):
                logger.info(f"  {i + 1}. {dup['hrid']} - {dup['name']} {dup['surname']} - {dup['action']}")

        # Convert to DataFrames
        debug_df, workforce_df, time_df, cb_df = gatherer.to_dataframes(company_data)

        # Save employee data
        workforce_df.to_csv(f"{output_dir}/mock_workforce_data_{timestamp}.csv", index=False)
        time_df.to_csv(f"{output_dir}/mock_time_data_{timestamp}.csv", index=False)
        cb_df.to_csv(f"{output_dir}/mock_cb_data_{timestamp}.csv", index=False)

        # Test individual unit data retrieval
        logger.info("\nTesting unit-specific data retrieval")
        for unit_id in [1, 2]:
            unit_data = gatherer.get_data_by_unit(unit_id=unit_id, month=3, year=2025)
            logger.info(f"Unit {unit_id}: Found {len(unit_data)} employees")

        # Test email-based lookup
        logger.info("\nTesting email-based employee lookup")
        email_test = gatherer.get_data_by_email(email="john.smith@example.com", month=3, year=2025)
        logger.info(f"Retrieved data for {email_test['debug_data']['name']} {email_test['debug_data']['surname']}")

        # Test date range functionality
        logger.info("\nTesting date range functionality")
        date_range = gatherer.get_data_time_segment_by_company(
            month_from=1,
            year_from=2025,
            month_to=3,
            year_to=2025,
            company_id=1
        )

        logger.info("Date range results:")
        for (year, month), employees in date_range['months'].items():
            dups = date_range['duplicates'].get((year, month), [])
            logger.info(f"  {month}/{year}: {len(employees)} employees, {len(dups)} duplicates")

        logger.info("\nTest completed successfully!")
        return True

    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)
        return False


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description='Test TriaHRDataGatherer with mock server')
    parser.add_argument('--interactive', action='store_true',
                        help='Run in interactive mode with prompts for duplicate resolution')

    args = parser.parse_args()

    return 0 if run_test(interactive=args.interactive) else 1


if __name__ == "__main__":
    sys.exit(main())
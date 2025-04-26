#!/usr/bin/env python
"""
Test script for the get_data_by_company method of TriaHRDataGatherer
"""

import logging
import time
import pandas as pd
from datetime import datetime

from tria_hr_data_gatherer import TriaHRDataGatherer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("company_test.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_test():
    """Run the single month company data test"""
    start_time = time.time()
    logger.info("Starting single month company data test")

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

        # Get company data for March 2025
        company_data = gatherer.get_data_by_company(
            month=test_month,
            year=test_year,
            company_id=company_id
        )

        logger.info(f"Successfully fetched data for {len(company_data)} employees")

        # Convert to DataFrames
        logger.info("Converting to DataFrames")
        debug_df, workforce_df, time_df, cb_df = gatherer.to_dataframes(company_data)

        # Summary statistics
        logger.info("DataFrame shapes:")
        logger.info(f"  debug_df: {debug_df.shape}")
        logger.info(f"  workforce_df: {workforce_df.shape}")
        logger.info(f"  time_df: {time_df.shape}")
        logger.info(f"  cb_df: {cb_df.shape}")

        # Save to CSV files
        output_dir = "company_data_output"
        import os
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_df.to_csv(f"{output_dir}/debug_data_{test_month}_{test_year}_{timestamp}.csv", index=False)
        workforce_df.to_csv(f"{output_dir}/workforce_data_{test_month}_{test_year}_{timestamp}.csv", index=False)
        time_df.to_csv(f"{output_dir}/time_data_{test_month}_{test_year}_{timestamp}.csv", index=False)
        cb_df.to_csv(f"{output_dir}/cb_data_{test_month}_{test_year}_{timestamp}.csv", index=False)

        logger.info(f"Data saved to {output_dir} directory")

        # Print some sample data
        logger.info("\nSample workforce data (first 5 rows):")
        sample_columns = ['Local_HRID', 'worker_gender', 'teammate_job_starting_date',
                          'job_category', 'teammate_working_time', 'teammate_seniority_date']
        sample_df = workforce_df[sample_columns].head(5)
        for _, row in sample_df.iterrows():
            logger.info(f"  Employee {row['Local_HRID']}: {dict(row)}")

        elapsed_time = time.time() - start_time
        logger.info(f"Test completed in {elapsed_time:.2f} seconds")
        return True

    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)
        return False


if __name__ == "__main__":
    run_test()
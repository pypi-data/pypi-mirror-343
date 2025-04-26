#!/usr/bin/env python
"""
Test script for the get_data_time_segment_by_company method of TriaHRDataGatherer
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
        logging.FileHandler("date_range_test.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_test():
    """Run the date range company data test"""
    start_time = time.time()
    logger.info("Starting date range company data test")

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
        month_from = 2
        year_from = 2025
        month_to = 3
        year_to = 2025

        logger.info(f"Fetching data for company_id={company_id}, "
                    f"period {month_from}/{year_from} to {month_to}/{year_to}")

        # Get company data for February-March 2025
        date_range_data = gatherer.get_data_time_segment_by_company(
            month_from=month_from,
            year_from=year_from,
            month_to=month_to,
            year_to=year_to,
            company_id=company_id
        )

        logger.info(f"Successfully fetched data for {len(date_range_data)} months")

        # Create directory for output
        output_dir = "date_range_output"
        import os
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Process each month's data
        all_workforce_data = []

        for (year, month), month_data in date_range_data.items():
            logger.info(f"Processing data for {month}/{year}: {len(month_data)} employees")

            # Convert to DataFrames
            debug_df, workforce_df, time_df, cb_df = gatherer.to_dataframes(month_data)

            # Add month/year identification columns
            workforce_df['year'] = year
            workforce_df['month'] = month

            # Save individual month data
            workforce_df.to_csv(
                f"{output_dir}/workforce_data_{month}_{year}_{timestamp}.csv",
                index=False
            )

            # Collect for combined analysis
            all_workforce_data.append(workforce_df)

        # Combine all months' data
        if all_workforce_data:
            combined_df = pd.concat(all_workforce_data, ignore_index=True)

            # Save combined data
            combined_df.to_csv(
                f"{output_dir}/combined_workforce_data_{timestamp}.csv",
                index=False
            )

            # Analysis: Count of employees per month
            employees_per_month = combined_df.groupby(['year', 'month']).size().reset_index(name='employee_count')
            logger.info("\nEmployee counts by month:")
            for _, row in employees_per_month.iterrows():
                logger.info(f"  {row['month']}/{row['year']}: {row['employee_count']} employees")

            # Analysis: Changes in employee roster between months
            if len(all_workforce_data) > 1:
                # Get unique employee IDs for each month
                first_month_employees = set(all_workforce_data[0]['Local_HRID'].unique())
                last_month_employees = set(all_workforce_data[-1]['Local_HRID'].unique())

                # Find new and departed employees
                new_employees = last_month_employees - first_month_employees
                departed_employees = first_month_employees - last_month_employees

                logger.info("\nWorkforce changes:")
                logger.info(f"  New employees in latest month: {len(new_employees)}")
                logger.info(f"  Employees who left since first month: {len(departed_employees)}")

                if len(new_employees) > 0:
                    logger.info(f"  Sample of new employees: {list(new_employees)[:5]}")
                if len(departed_employees) > 0:
                    logger.info(f"  Sample of departed employees: {list(departed_employees)[:5]}")

        elapsed_time = time.time() - start_time
        logger.info(f"Test completed in {elapsed_time:.2f} seconds")
        return True

    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)
        return False


if __name__ == "__main__":
    run_test()
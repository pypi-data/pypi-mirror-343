# test_gatherer.py
from tria_hr_data_gatherer import TriaHRDataGatherer
import json

# Configure your test credentials
BASE_URL = "https://stage.company.triahr.com"
CLIENT_ID = "your_test_client_id"
CLIENT_SECRET = "your_test_client_secret"

# Initialize the gatherer
gatherer = TriaHRDataGatherer(
    base_url="https://decasport.triahr.com",
    client_id="13_61ev6jlbu6ko8sgk4cg0cg0scss4oc8sg8wkwsokoowo48gooo",
    client_secret="4jqizm9xg1kwk8c88gkow0w0owkcss4sk8kg4c0kkwwwwo0gos",
    debug=True
)

# First, test the connection
try:
    print("Testing API connection...")
    gatherer.test_connection()
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {str(e)}")
    exit(1)

# Now try a different endpoint to debug the issue
try:
    print("\nTesting a different endpoint: /api/v1/companies/")
    companies = gatherer._make_request('/api/v1/companies/')
    print(f"Success! Got {len(companies.get('data', []))} companies")
except Exception as e:
    print(f"Error testing companies endpoint: {str(e)}")

# Test getting data by email
try:
    print("\nTesting get_data_by_email...")
    user_data = gatherer.get_data_by_email("dan.simanek@seznam.cz", month=3, year=2025)
    print(f"Success! Got data for user: {user_data['workforce_data']['Local_HRID']}")

    # Print the complete formatted data structure
    print("\nComplete data structure:")
    print(json.dumps(user_data, indent=2))
except Exception as e:
    print(f"Error testing get_data_by_email: {str(e)}")

try:
    print("\nTesting get_data_by_unit...")
    unit_data = gatherer.get_data_by_unit(120, month=3, year=2025)

    # Print the complete formatted data structure
    print("\nComplete data structure:")
    print(json.dumps(unit_data, indent=2))

    pandas_df = gatherer.to_dataframes(unit_data)
    print(pandas_df)
except Exception as e:
    print(f"Error testing get_data_by_unit: {str(e)}")
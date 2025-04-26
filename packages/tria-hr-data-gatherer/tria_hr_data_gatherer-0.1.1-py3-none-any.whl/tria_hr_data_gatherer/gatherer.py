"""
Main implementation of the TriaHRDataGatherer class.
"""

from typing import Optional, Dict, List, Any, Set, Tuple, Union
import calendar
import json
import urllib.parse
from dateutil.parser import parse as date_parse
import datetime

import pandas as pd

from tria_hr_api import TriaHRAPI  # Importing your existing library


class TriaHRDataGatherer:
    """
    Extended TriaHR client that collects and processes employee data from TriaHR API.
    """

    def __init__(self, tria_client: Optional[TriaHRAPI] = None, debug: bool = False, **kwargs):
        """
        Initialize with either an existing TriaHRAPI instance or parameters to create one.

        Args:
            tria_client: Optional existing TriaHRAPI instance
            debug: Enable detailed debugging output
            **kwargs: Parameters to initialize a new TriaHRAPI if tria_client not provided
        """
        self.debug = debug

        if tria_client:
            self.client = tria_client
        else:
            self.client = TriaHRAPI(**kwargs)

        # Cache for basic work positions to avoid multiple requests
        self.work_positions_cache = None

        # Lazy loading cache for detailed work position data
        self.detailed_positions_cache = {}

        # Cache for organization units
        self.organization_units_cache = {}

    def _debug_log(self, message: str):
        """Log debug messages if debug mode is enabled"""
        if self.debug:
            print(f"[DEBUG] {message}")

    @classmethod
    def from_config(cls, config_path: str = 'config.ini', environment: str = 'stage', debug: bool = False):
        """Create an instance from a configuration file"""
        tria_client = TriaHRAPI.from_config(config_path, environment)
        return cls(tria_client=tria_client, debug=debug)

    @classmethod
    def from_json(cls, base_url: str, credentials_json: dict, debug: bool = False):
        """Create an instance from parsed JSON credentials dictionary"""
        tria_client = TriaHRAPI.from_json(base_url, credentials_json)
        return cls(tria_client=tria_client, debug=debug)

    def _make_request(self, endpoint: str, method: str = 'GET', params: Optional[Dict] = None,
                      data: Optional[Dict] = None):
        """
        Make an API request with debug logging

        Args:
            endpoint: API endpoint
            method: HTTP method (default: GET)
            params: Optional query parameters
            data: Optional request body for POST/PUT requests

        Returns:
            API response
        """
        # Get the full URL that will be used
        base_url = self.client.base_url.rstrip('/')
        full_url = f"{base_url}{endpoint}"

        self._debug_log(f"Making {method} request to endpoint: {endpoint}")
        self._debug_log(f"Full URL: {full_url}")

        if params:
            self._debug_log(f"Request parameters: {params}")
        if data:
            self._debug_log(f"Request data: {data}")

        # Check if we have a valid token (this is important)
        if not hasattr(self.client, 'access_token') or not self.client.access_token:
            self._debug_log("WARNING: No access token available - authentication might fail")
        else:
            token_preview = f"{self.client.access_token[:10]}...{self.client.access_token[-10:]}"
            self._debug_log(f"Using access token: {token_preview}")

        try:
            response = self.client.undefined_request(endpoint, method=method, params=params, force_trailing_slash=False)

            if self.debug:
                # Log a truncated version of the response
                if isinstance(response, dict):
                    keys = list(response.keys())
                    status = response.get('status', 'unknown')
                    data_content = response.get('data', [])
                    data_length = len(data_content) if isinstance(data_content, list) else 'object'
                    self._debug_log(f"Response status: {status}, keys: {keys}, data length: {data_length}")
                else:
                    self._debug_log(f"Response type: {type(response)}")

            return response

        except Exception as e:
            self._debug_log(f"Request failed: {str(e)}")

            # Get more details about the error
            if hasattr(e, 'response'):
                status_code = e.response.status_code if hasattr(e.response, 'status_code') else 'unknown'
                content = e.response.text if hasattr(e.response, 'text') else 'unknown'
                self._debug_log(f"Error details: status_code={status_code}, content={content[:500]}")

                # Log request headers if available
                if hasattr(e.response.request, 'headers'):
                    headers = e.response.request.headers
                    # Remove sensitive info before logging
                    if 'Authorization' in headers:
                        auth = headers['Authorization']
                        if auth.startswith('Bearer '):
                            token = auth[7:]  # Remove 'Bearer ' prefix
                            headers['Authorization'] = f"Bearer {token[:10]}...{token[-10:]}"
                    self._debug_log(f"Request headers: {dict(headers)}")

            raise

    def test_connection(self):
        """
        Test the API connection by making a simple request

        Returns:
            True if connection successful, raises exception otherwise
        """
        self._debug_log("Testing API connection...")
        try:
            # Try a simple ping or companies endpoint
            response = self._make_request('/api/v1/ping/')
            self._debug_log(f"Connection test successful: {response}")
            return True
        except Exception as e:
            self._debug_log(f"Connection test failed: {str(e)}")
            raise

    def get_data_by_email(self, email: str, month: int, year: int) -> Dict[str, Any]:
        """
        Get employee data by email for a specific month and year.

        Args:
            email: Employee email address
            month: Month (1-12)
            year: Year (YYYY)

        Returns:
            Dictionary with processed employee data
        """
        self._debug_log(f"Getting data for email: {email}, month: {month}, year: {year}")

        # Get user info by email
        user_info = self._get_user_by_email(email)

        if not user_info.get('data') or not user_info['data'].get('id'):
            error_msg = f"User with email {email} not found"
            self._debug_log(error_msg)
            raise ValueError(error_msg)

        user_id = user_info['data']['id']
        self._debug_log(f"Found user_id: {user_id}")

        # Call the process method
        return self.process(user_id, month, year)

    def get_data_by_unit(self, unit_id: int, month: int, year: int, company_id: int = 1) -> List[Dict[str, Any]]:
        """
        Get data for all employees in an organizational unit.

        Args:
            unit_id: Organization unit ID
            month: Month (1-12)
            year: Year (YYYY)
            company_id: Company ID (default: 1)

        Returns:
            List of processed data for each user
        """
        self._debug_log(f"Getting data for unit_id: {unit_id}, month: {month}, year: {year}, company_id: {company_id}")

        # Get first and last day of the month
        first_day, last_day = self._get_month_range(month, year)
        self._debug_log(f"Date range: {first_day} to {last_day}")

        # Get attendance plan for the unit
        params = {
            'date_from': first_day,
            'date_to': last_day,
            'unit_id': unit_id,
            'company_id': company_id,
            'include_explicit_unit_id': 'false',
            'mode': 'plan'
        }

        attendance_plan = self._make_request('/api/v1/attendance-plan/', params=params)

        # Extract unique user IDs and organize attendance data by user ID
        user_ids, attendance_data_by_user = self._extract_user_data_from_attendance(attendance_plan)

        self._debug_log(f"Found {len(user_ids)} unique users in the unit")

        # Process data for each user
        results = []
        for user_id in user_ids:
            self._debug_log(f"Processing user_id: {user_id}")
            # Pass the pre-fetched attendance data to the process function
            user_attendance_data = attendance_data_by_user.get(user_id, [])
            try:
                user_data = self.process(user_id, month, year, attendance_data=user_attendance_data)
                results.append(user_data)
            except Exception as e:
                self._debug_log(f"Error processing user_id {user_id}: {str(e)}")
                # Continue with next user if one fails

        return results

    def get_data_by_company(self, month: int, year: int, company_id: int = 1,
                            interactive: bool = False, check_duplicates: bool = False) -> Dict[str, Any]:
        """
        Get data for all employees in all units of a company for a specific month.

        Args:
            month: Month (1-12)
            year: Year (YYYY)
            company_id: Company ID (default: 1)
            interactive: If True, prompt user for deduplication decisions (default: False)
            check_duplicates: If False, skip duplicate checking entirely (default: True)

        Returns:
            Dictionary with:
                'employees': List of processed data for each user across all units
                'duplicates': List of duplicate employees that were merged (empty if check_duplicates=False)
        """
        self._debug_log(f"Getting data for company_id: {company_id}, month: {month}, year: {year}")
        self._debug_log(f"Duplicate checking is {'enabled' if check_duplicates else 'disabled'}")

        # Get all organization units (active and inactive)
        all_units = self._get_organization_units(company_id, include_inactive=True)

        unit_ids = [unit['id'] for unit in all_units]
        self._debug_log(f"Processing {len(unit_ids)} units")

        # Process all units and collect results
        all_results = []
        unit_results_count = {}  # Track how many employees were found in each unit

        for unit_id in unit_ids:
            try:
                self._debug_log(f"Processing unit_id: {unit_id}")
                unit_results = self.get_data_by_unit(unit_id, month, year, company_id)
                all_results.extend(unit_results)

                # Store the count for reporting
                unit_name = next((unit['name'] for unit in all_units if unit['id'] == unit_id), f"Unit {unit_id}")
                unit_results_count[unit_name] = len(unit_results)

                self._debug_log(f"Completed unit_id: {unit_id}, found {len(unit_results)} employees")
            except Exception as e:
                self._debug_log(f"Error processing unit_id {unit_id}: {str(e)}")
                # Continue with next unit if one fails

        # Enhanced reporting before deduplication
        self._debug_log("Employee counts by unit:")
        for unit_name, count in unit_results_count.items():
            self._debug_log(f"  {unit_name}: {count} employees")

        # Skip deduplication if requested
        if not check_duplicates:
            self._debug_log(f"Skipping duplicate checking as requested. Total employees: {len(all_results)}")
            return {
                'employees': all_results,
                'duplicates': []  # Empty list since we didn't check
            }

        # Otherwise, perform duplicate checking as normal
        unique_results, duplicates = self._deduplicate_results(all_results, interactive=interactive)

        # Generate summary of duplicates by unit
        if duplicates:
            duplication_by_unit = {}
            for dup in duplicates:
                first_unit = dup.get('first_unit') or 'Unknown'
                dup_unit = dup.get('duplicate_unit') or 'Unknown'

                key = f"{first_unit} → {dup_unit}"
                duplication_by_unit[key] = duplication_by_unit.get(key, 0) + 1

            self._debug_log("Duplication patterns by unit:")
            for pattern, count in sorted(duplication_by_unit.items(), key=lambda x: x[1], reverse=True):
                self._debug_log(f"  {pattern}: {count} duplicates")

        self._debug_log(f"Total employees after deduplication: {len(unique_results)}")

        return {
            'employees': unique_results,
            'duplicates': duplicates
        }

    def get_data_time_segment_by_company(
            self,
            month_from: int,
            year_from: int,
            month_to: int,
            year_to: int,
            company_id: int = 1,
            interactive: bool = False,
            check_duplicates: bool = False
    ) -> Dict[str, Any]:
        """
        Get data for all employees in all units of a company for a range of months.

        Args:
            month_from: Starting month (1-12)
            year_from: Starting year (YYYY)
            month_to: Ending month (1-12)
            year_to: Ending year (YYYY)
            company_id: Company ID (default: 1)
            interactive: If True, prompt user for deduplication decisions (default: False)
            check_duplicates: If False, skip duplicate checking entirely (default: True)

        Returns:
            Dictionary with:
                'months': Dict mapping (year, month) tuples to lists of employee data
                'duplicates': Dict mapping (year, month) tuples to lists of duplicate info
        """
        self._debug_log(
            f"Getting data for company_id: {company_id} from {month_from}/{year_from} to {month_to}/{year_to}")
        self._debug_log(f"Duplicate checking is {'enabled' if check_duplicates else 'disabled'}")

        # Generate list of all month/year combinations in the range
        months = self._generate_month_year_range(month_from, year_from, month_to, year_to)
        self._debug_log(f"Processing {len(months)} months")

        # Process each month and store results
        results_by_month = {}
        duplicates_by_month = {}

        for year, month in months:
            self._debug_log(f"Processing month: {month}/{year}")
            try:
                month_result = self.get_data_by_company(
                    month=month,
                    year=year,
                    company_id=company_id,
                    interactive=interactive,
                    check_duplicates=check_duplicates
                )

                results_by_month[(year, month)] = month_result['employees']
                duplicates_by_month[(year, month)] = month_result['duplicates']

                self._debug_log(f"Completed month: {month}/{year}, found {len(month_result['employees'])} employees " +
                                f"({len(month_result['duplicates'])} duplicates)")

            except Exception as e:
                self._debug_log(f"Error processing month {month}/{year}: {str(e)}")
                # Store empty lists for failed months to maintain the structure
                results_by_month[(year, month)] = []
                duplicates_by_month[(year, month)] = []

        return {
            'months': results_by_month,
            'duplicates': duplicates_by_month
        }

    def _get_organization_units(self, company_id: int = 1, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """
        Get all organization units for a company with caching.

        Args:
            company_id: Company ID
            include_inactive: Whether to include deactivated units

        Returns:
            List of organization unit dictionaries
        """
        # Check if we have this company's units in cache
        cache_key = f"company_{company_id}"
        if cache_key in self.organization_units_cache:
            all_units = self.organization_units_cache[cache_key]
            self._debug_log(f"Using cached organization units for company_id {company_id}")
        else:
            # Fetch organization units
            self._debug_log(f"Fetching organization units for company_id {company_id}")
            params = {'company_id': company_id}

            response = self._make_request('/api/v1/attendance-organization-units/', params=params)
            all_units = response.get('data', [])

            # Cache the results
            self.organization_units_cache[cache_key] = all_units
            self._debug_log(f"Cached {len(all_units)} organization units for company_id {company_id}")

        # Filter units based on include_inactive parameter
        if include_inactive:
            return all_units
        else:
            active_units = [unit for unit in all_units if not unit.get('deactivated', False)]
            self._debug_log(f"Filtered to {len(active_units)} active units")
            return active_units

    def _extract_user_data_from_attendance(self, attendance_plan: Dict[str, Any]) -> Tuple[Set[Any], Dict[Any, List[Dict[str, Any]]]]:
        """
        Extract user IDs and attendance data from attendance plan response.

        Args:
            attendance_plan: Response from attendance-plan endpoint

        Returns:
            Tuple of (set of user IDs, dict mapping user IDs to their attendance data)
        """
        user_ids = set()
        attendance_data_by_user = {}

        for item in attendance_plan.get('data', []):
            if (plannable_employment := item.get('plannable_employment')) and \
                    (employee := plannable_employment.get('employee')) and \
                    (employee_id := employee.get('id')):
                user_id = employee_id
                user_ids.add(user_id)

                # Store the attendance data for this user
                if user_id not in attendance_data_by_user:
                    attendance_data_by_user[user_id] = []
                attendance_data_by_user[user_id].append(item)

        return user_ids, attendance_data_by_user

    def _calculate_absence_hours(self, absences: List[Dict[str, Any]]) -> float:
        """
        Calculate total hours of absences from absence records.

        Args:
            absences: List of absence records

        Returns:
            Total hours of absences
        """
        total_hours = 0.0

        for absence in absences:
            if 'date_time_from' in absence and 'date_time_to' in absence:
                try:
                    start_time = datetime.datetime.fromisoformat(absence['date_time_from'].replace('Z', '+00:00'))
                    end_time = datetime.datetime.fromisoformat(absence['date_time_to'].replace('Z', '+00:00'))

                    # Calculate duration in hours
                    duration = (end_time - start_time).total_seconds() / 3600
                    total_hours += duration

                    self._debug_log(f"Absence from {start_time} to {end_time}: {duration:.2f} hours")
                except Exception as e:
                    self._debug_log(f"Error calculating absence time: {str(e)}")

        self._debug_log(f"Total absence hours: {total_hours:.2f}")
        return total_hours

    def _deduplicate_results(self, results: List[Dict[str, Any]], interactive: bool = False) -> Tuple[
        List[Dict[str, Any]], List[Dict]]:
        """
        Remove duplicate user entries from results with optional interactive mode
        and detailed tracking.

        Args:
            results: List of processed user data
            interactive: If True, ask user confirmation for each potential duplicate

        Returns:
            Tuple of (deduplicated list, duplication report)
        """
        # Track duplicate employees for reporting
        seen_hrids = {}  # Map HRID to first occurrence index
        duplicate_info = []  # List to track duplicates for reporting
        unique_results = []

        self._debug_log(f"Deduplicating {len(results)} results" +
                        (f" in interactive mode" if interactive else ""))

        for i, result in enumerate(results):
            # Extract workforce data for easier access
            workforce = result.get('workforce_data', {})
            debug_data = result.get('debug_data', {})

            hrid = workforce.get('Local_HRID')
            user_id = debug_data.get('user_id')

            # Skip entries without a valid HRID
            if not hrid:
                self._debug_log(f"Skipping result at index {i}: No valid HRID found")
                continue

            # Check if we've seen this HRID before AND it's the same person (check user_id)
            # We only consider it a duplicate if both HRID and user_id match
            if hrid in seen_hrids:
                first_idx = seen_hrids[hrid]
                first_result = unique_results[first_idx]
                first_user_id = first_result.get('debug_data', {}).get('user_id')

                # Only treat as duplicate if it's actually the same person (user_id matches)
                # Different people should not be considered duplicates even if they have the same HRID
                if user_id == first_user_id:
                    # Found a legitimate duplicate
                    duplicate = self._create_duplicate_record(hrid, result, first_result, first_idx, i)

                    # Always log detailed information about the duplicate, even in non-interactive mode
                    duplicate_info_str = (
                        f"DUPLICATE: HRID={hrid}, "
                        f"Name={duplicate['name']} {duplicate['surname']}, "
                        f"Units: {duplicate['first_unit']} → {duplicate['duplicate_unit']}"
                    )
                    self._debug_log(duplicate_info_str)

                    # If in interactive mode, ask user what to do
                    if interactive:
                        try:
                            # Print information about the duplicate
                            print("\n" + "=" * 60)
                            print(f"DUPLICATE EMPLOYEE FOUND: {hrid}")
                            print(f"Name: {duplicate['name']} {duplicate['surname']}")
                            print("-" * 60)
                            print("First occurrence:")
                            self._print_employee_summary(first_result)
                            print("-" * 60)
                            print("Duplicate occurrence:")
                            self._print_employee_summary(result)
                            print("-" * 60)

                            # Ask user what to do
                            action = input("What would you like to do?\n"
                                           "[k]eep first (default), [r]eplace with second, [b]oth: ").lower().strip()

                            if action.startswith('r'):
                                # Replace first occurrence with this one
                                self._debug_log(f"User chose to replace employee {hrid} with duplicate")
                                unique_results[first_idx] = result
                                duplicate['action'] = 'replaced_first'
                            elif action.startswith('b'):
                                # Keep both (append new with modified HRID to avoid confusion)
                                self._debug_log(f"User chose to keep both occurrences of employee {hrid}")
                                unique_results.append(result)
                                duplicate['action'] = 'kept_both'
                            else:
                                # Default: keep first occurrence, discard duplicate
                                self._debug_log(f"User chose to keep first occurrence of employee {hrid}")
                                duplicate['action'] = 'kept_first'
                        except Exception as e:
                            # If there's any error in interactive mode, default to keeping first
                            self._debug_log(
                                f"Error in interactive mode: {str(e)}. Defaulting to keeping first occurrence.")
                            duplicate['action'] = 'kept_first_error'
                    else:
                        # In non-interactive mode, provide more info about what was merged
                        self._debug_log(f"AUTO-MERGED: Keeping first occurrence from {duplicate['first_unit']}, "
                                        f"discarding duplicate from {duplicate['duplicate_unit']}")

                    # Record this duplicate
                    duplicate_info.append(duplicate)
                else:
                    # Different people with same HRID - this is a data issue but we'll keep both
                    self._debug_log(
                        f"Warning: Different employees with same HRID {hrid} (user_ids: {first_user_id}, {user_id})")
                    seen_hrids[hrid + f"_{user_id}"] = len(
                        unique_results)  # Use a compound key to avoid further collisions
                    unique_results.append(result)
            else:
                # First time seeing this HRID
                seen_hrids[hrid] = len(unique_results)
                unique_results.append(result)

        # Generate deduplication report
        if duplicate_info:
            self._debug_log(f"Found {len(duplicate_info)} duplicate employees")
            for dup in duplicate_info:
                self._debug_log(f"Duplicate: {dup['hrid']} ({dup['name']} {dup['surname']}), "
                                f"Units: {dup['first_unit']} → {dup['duplicate_unit']}, "
                                f"Action: {dup['action']}")
        else:
            self._debug_log("No duplicate employees found")

        return unique_results, duplicate_info

    def _create_duplicate_record(self, hrid: str, result: Dict, first_result: Dict, first_idx: int,
                                 duplicate_idx: int) -> Dict:
        """
        Create a record with details about a duplicate employee.

        Args:
            hrid: Employee HRID
            result: The duplicate record
            first_result: The first occurrence of this employee
            first_idx: Index of first occurrence
            duplicate_idx: Index of duplicate occurrence

        Returns:
            Dictionary with duplicate information
        """
        debug = result.get('debug_data', {})
        workforce = result.get('workforce_data', {})
        first_workforce = first_result.get('workforce_data', {})

        # Get unit info in a way that handles None values safely
        first_unit = first_workforce.get('site_name') or "Unknown"
        duplicate_unit = workforce.get('site_name') or "Unknown"

        return {
            'hrid': hrid,
            'user_id': debug.get('user_id'),
            'name': debug.get('name', 'Unknown'),
            'surname': debug.get('surname', 'Unknown'),
            'first_unit': first_unit,
            'duplicate_unit': duplicate_unit,
            'first_index': first_idx,
            'duplicate_index': duplicate_idx,
            'action': 'auto_merged'  # Default action, may be updated
        }

    def _print_employee_summary(self, employee_data: Dict[str, Any]) -> None:
        """
        Print a summary of employee data for interactive comparison.

        Args:
            employee_data: Single employee data dictionary
        """
        debug = employee_data.get('debug_data', {})
        workforce = employee_data.get('workforce_data', {})

        # Handle None values gracefully for display
        def format_value(value):
            if value is None:
                return "Not set"
            return value

        print(f"ID: {format_value(debug.get('user_id'))}, HRID: {format_value(workforce.get('Local_HRID'))}")
        print(f"Name: {format_value(debug.get('name'))} {format_value(debug.get('surname'))}")
        print(f"Unit: {format_value(workforce.get('site_name'))} (Code: {format_value(workforce.get('site_code'))})")
        print(f"Position: {format_value(workforce.get('worker_job_name'))} "
              f"(Is manager: {format_value(workforce.get('worker_is_direct_manager'))})")
        print(f"Job started: {format_value(workforce.get('teammate_job_starting_date'))}, "
              f"Seniority: {format_value(workforce.get('teammate_seniority_date'))}")
        print(f"Working time: {format_value(workforce.get('teammate_working_time'))} "
              f"({format_value(workforce.get('teammate_contractual_hours'))} hours/week)")

    def _generate_month_year_range(self, month_from: int, year_from: int, month_to: int, year_to: int) -> List[Tuple[int, int]]:
        """
        Generate a list of (year, month) tuples for the given date range.

        Args:
            month_from: Starting month (1-12)
            year_from: Starting year (YYYY)
            month_to: Ending month (1-12)
            year_to: Ending year (YYYY)

        Returns:
            List of (year, month) tuples
        """
        months = []

        # Validate input
        if year_to < year_from or (year_to == year_from and month_to < month_from):
            raise ValueError("End date must be after start date")

        # Generate all months in the range
        current_year, current_month = year_from, month_from

        while current_year < year_to or (current_year == year_to and current_month <= month_to):
            months.append((current_year, current_month))

            # Move to next month
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1

        return months

    def _get_user_by_email(self, email: str) -> Dict[str, Any]:
        """Get user information by email, with proper URL encoding"""
        # URL encode the email address to handle special characters like '@'
        encoded_email = urllib.parse.quote(email)
        endpoint = f'/api/v1/users/{encoded_email}'
        self._debug_log(f"Looking up user by email: {email} (encoded: {encoded_email})")
        return self._make_request(endpoint)

    def _get_month_range(self, month: int, year: int) -> tuple[str, str]:
        """Get first and last day of the month in YYYY-MM-DD format"""
        last_day = calendar.monthrange(year, month)[1]
        first_day_str = f"{year}-{month:02d}-01"
        last_day_str = f"{year}-{month:02d}-{last_day:02d}"
        return first_day_str, last_day_str

    def _get_work_positions(self, company_id: int = 1) -> Dict[int, Dict[str, Any]]:
        """
        Get all work positions and cache them for reuse

        Returns:
            Dictionary mapping position ID to position data
        """
        if self.work_positions_cache is not None:
            self._debug_log("Using cached work positions")
            return self.work_positions_cache

        self._debug_log(f"Fetching work positions for company_id: {company_id}")
        params = {'company_id': company_id}

        response = self._make_request('/api/v1/work-positions/', params=params)

        # Create a mapping of position ID to position data
        positions = {}
        for position in response.get('data', []):
            if 'id' in position:
                positions[position['id']] = position

        self._debug_log(f"Cached {len(positions)} work positions")
        self.work_positions_cache = positions
        return positions

    def _get_work_position_details(self, position_id: int) -> Dict[str, Any]:
        """
        Get detailed information for a specific work position using lazy loading.

        Args:
            position_id: Work position ID

        Returns:
            Dictionary with detailed position data
        """
        # Check if we already have the position details in the cache
        if position_id in self.detailed_positions_cache:
            self._debug_log(f"Using cached detailed position data for position_id: {position_id}")
            return self.detailed_positions_cache[position_id]

        # Otherwise, fetch the detailed data
        self._debug_log(f"Fetching detailed work position data for position_id: {position_id}")

        try:
            response = self._make_request(f'/api/v1/work-positions/{position_id}')
            position_data = response.get('data', {})

            # Add to cache
            self.detailed_positions_cache[position_id] = position_data
            self._debug_log(f"Added position_id: {position_id} to detailed positions cache")

            return position_data
        except Exception as e:
            self._debug_log(f"Error fetching detailed work position data: {e}")
            # Return an empty dict if there's an error
            return {}

    def _calculate_absence_hours(self, absences: List[Dict[str, Any]]) -> float:
        """
        Calculate total hours of absences

        Args:
            absences: List of absence records

        Returns:
            Total hours of absences
        """
        total_hours = 0.0

        for absence in absences:
            if 'date_time_from' in absence and 'date_time_to' in absence:
                try:
                    start_time = date_parse(absence['date_time_from'])
                    end_time = date_parse(absence['date_time_to'])

                    # Calculate the duration in hours
                    duration = (end_time - start_time).total_seconds() / 3600
                    total_hours += duration
                    self._debug_log(f"Absence from {start_time} to {end_time}: {duration:.2f} hours")
                except Exception as e:
                    self._debug_log(f"Error calculating absence time: {e}")

        self._debug_log(f"Total absence hours: {total_hours:.2f}")
        return total_hours

    def _process_employments(self, employment_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process multiple employments to extract necessary data.

        Args:
            employment_data: List of employment records

        Returns:
            Dictionary with processed employment data
        """
        if not employment_data:
            self._debug_log("No employment data to process")
            return {}

        # Sort employments by start_date
        sorted_employments = sorted(
            employment_data,
            key=lambda emp: emp.get('start_date', '9999-12-31'),
            reverse=False  # oldest first
        )

        # Get the oldest employment for seniority date
        oldest_employment = sorted_employments[0]
        seniority_date = oldest_employment.get('start_date')

        # Get the newest employment for current job details
        newest_employment = sorted_employments[-1]

        # Get contractual hours
        contractual_hours = newest_employment.get('working_hours_per_week')

        # Calculate working time ratio
        working_time = None
        if contractual_hours is not None:
            try:
                working_time = float(contractual_hours) / 40.0
                # Round to 3 decimal places
                working_time = round(working_time, 3)
            except (ValueError, TypeError):
                self._debug_log(f"Error calculating working time from contractual hours: {contractual_hours}")

        return {
            "current_employment": newest_employment,
            "seniority_date": seniority_date,
            "contractual_hours": contractual_hours,
            "working_time": working_time
        }

    def process(self, user_id: int, month: int, year: int, attendance_data: Optional[List[Dict[str, Any]]] = None) -> \
    Dict[str, Any]:
        """
        Process and collect data for a specific user.

        Args:
            user_id: User ID
            month: Month (1-12)
            year: Year (YYYY)
            attendance_data: Optional pre-fetched attendance data for this user

        Returns:
            Processed data in the required format
        """
        self._debug_log(f"Processing data for user_id: {user_id}, month: {month}, year: {year}")
        month_id = f"{year}{month:02d}"
        first_day, last_day = self._get_month_range(month, year)

        # Step 1: Get personal inquiries overview
        self._debug_log("Step 1: Getting personal inquiries")
        personal_inquiries = self._make_request(
            endpoint='/api/v1/personal-inquiries/',
            params={'user_id': user_id, 'limit': 100, 'offset': 0}
        )

        # Extract inquiry identifier from the first inquiry if available
        inquiry_data = personal_inquiries.get('data', [])
        if not inquiry_data:
            error_msg = f"No personal inquiries found for user_id {user_id}"
            self._debug_log(error_msg)
            raise ValueError(error_msg)

        inquiry_identifier = inquiry_data[0].get('inquiry_identifier')
        if not inquiry_identifier:
            error_msg = f"Invalid inquiry data for user_id {user_id}"
            self._debug_log(error_msg)
            raise ValueError(error_msg)

        self._debug_log(f"Found inquiry_identifier: {inquiry_identifier}")

        # Step 2: Get detailed personal inquiry data
        self._debug_log("Step 2: Getting detailed personal inquiry data")
        detailed_inquiry = self._make_request(
            endpoint=f'/api/v1/personal-inquiries/{inquiry_identifier}'
        )

        # Step 3: Get employment data
        self._debug_log("Step 3: Getting employment data")
        employments = self._make_request(
            endpoint='/api/v1/employments/',
            params={
                'company_id': 1,
                'user_id': user_id,
                'approved': 'true',
                'active_on_date': first_day,
                'limit': 100,
                'offset': 0
            }
        )

        employment_data = employments.get('data', [])
        if not employment_data:
            error_msg = f"No employment data found for user_id {user_id}"
            self._debug_log(error_msg)
            raise ValueError(error_msg)

        # Process the employment data
        processed_employment = self._process_employments(employment_data)
        current_employment = processed_employment.get('current_employment', employment_data[0])

        # Get the work position ID
        work_position_id = current_employment.get('work_position_id')

        # Step 4: Get work positions if not already cached
        self._debug_log("Step 4: Getting work positions")
        work_positions = self._get_work_positions()

        # Step 4b: Get detailed position information
        job_category = None
        if work_position_id:
            self._debug_log(f"Getting detailed position info for position_id: {work_position_id}")
            position_details = self._get_work_position_details(work_position_id)
            job_category = position_details.get('job_group')
            self._debug_log(f"Found job_category (job_group): {job_category}")

        # Step 5: Get attendance plan for time data (only if not provided)
        if attendance_data is None:
            self._debug_log("Step 5: Getting attendance plan")
            attendance_plan = self._make_request(
                endpoint='/api/v1/attendance-plan/',
                params={
                    'user_id': user_id,
                    'company_id': 1,
                    'include_explicit_unit_id': 'false',
                    'mode': 'plan',
                    'date_from': first_day,
                    'date_to': last_day
                }
            )
            attendance_data = attendance_plan.get('data', [])
        else:
            self._debug_log("Step 5: Using pre-fetched attendance data")

        self._debug_log("Step 5.1: Debug info about work position - the located ID is " + str(
            work_position_id) if work_position_id else None)

        position_info = work_positions.get(work_position_id, {})
        self._debug_log("... so the work position data are " + str(position_info) if position_info else None)

        is_manager = position_info.get('managing_position', False)
        self._debug_log(f"... so the work position is leader? {is_manager}")

        # Extract key values for the result
        self._debug_log("Step 6: Building result object")
        result = {
            "debug_data": {
                "name": inquiry_data[0].get('name'),
                "surname": inquiry_data[0].get('surname'),
                "user_id": inquiry_data[0].get('user_id')
            },
            "workforce_data": {
                "month_id": month_id,
                "country_code": "CZ",
                "worker_uuid": None,
                "worker_uid": None,
                "Local_HRID": current_employment.get('personal_number'),
                "worker_gender": detailed_inquiry.get('data', {}).get('personal_info', {}).get('gender'),
                "worker_birthdate": inquiry_data[0].get('birth_date') if inquiry_data else None,
                "fiscal_company_number": "0153",
                "worker_uuid_direct_manager": None,
                "worker_uid_direct_manager": None,
                "worker_is_direct_manager": is_manager,
                "site_code": None,
                "site_name": None,
                "cost_center_code": None,
                "teammate_nationality": detailed_inquiry.get('data', {}).get('personal_info', {}).get(
                    'nationality_country_code'),
                "teammate_job_starting_date": current_employment.get('start_date'),
                "teammate_job_end_date": current_employment.get('end_date'),
                "worker_job_code": None,
                "worker_job_name": None,
                "job_category": job_category,
                "teammate_hire_date": None,
                "teammate_last_working_date": None,
                "teammate_contract_type": current_employment.get('type'),
                "teammate_working_time": processed_employment.get('working_time'),
                "teammate_termination_date": None,
                "teammate_termination_reason": None,
                "teammate_seniority_date": processed_employment.get('seniority_date'),
                "teammate_contractual_hours": processed_employment.get('contractual_hours'),
                "teammate_with_disability": None,
                "Technical_date": None
            },
            "time_data": {
                "month_id": month_id,
                "country_code": "CZ",
                "worker_uuid": None,
                "worker_uid": None,
                "Local_HRID": current_employment.get('personal_number'),
                "total_theoretical_hours": None,
                "total_overtime_hours": None,
                "total_planned_absences": None,
                "total_unplanned_absences": None,
                "Technical_date": None
            },
            "c&b_data": {
                "month_id": month_id,
                "country_code": "CZ",
                "worker_uuid": None,
                "worker_uid": None,
                "Local_HRID": current_employment.get('personal_number'),
                "currency_code": "CZK",
                "base_salary_frequency": "monthly",
                "theoretical_base_salary": current_employment.get('basic_salary'),
                "basis_salary_periodicity_plan": 12,
                "monthly_bonus_rate": None,
                "monthly_bonus_maxi_rate": 10,
                "quarterly_bonus_rate": 0,
                "quarterly_bonus_maxi_rate": 0,
                "profit_sharing_rate": None,
                "theoretical_profit_sharing_amount": None,
                "theoretical_local_annual_bonus": None,
                "expensive_city_bonus_rate": None,
                "international_annual_bonus_rate": None,
                "international_annual_bonus_maxi_rate": None,
                "exceptional_bonus_from_salary_review": None,
                "exceptional_bonus_out_of_salary_review": None,
                "performance_related_bonus": None,
                "value_creation_bonus": None,
                "theoretical_asset_incentive_amount": None,
                "expansion_performance_bonus": None,
                "on_call_duty_bonus": None,
                "captain_bonus": None,
                "holiday_allowance": None,
                "meal_allowance": None,
                "car_allowance": None,
                "transportation_allowance": None,
                "allowance_required_seniority": None,
                "retirement": None,
                "private_healthcare_insurance": None,
                "accident_and_death_insurance": None,
                "product_discount_amount": None,
                "Technical_date": None
            }
        }

        # Extract time data from attendance data
        self._debug_log("Step 7: Processing attendance data")
        if attendance_data:
            first_item = attendance_data[0]
            month_key = f"{month:02d}/{year}"

            # Get theoretical hours from working_hours_funds
            if working_hours_funds := first_item.get('working_hours_funds', {}):
                result['time_data']['total_theoretical_hours'] = working_hours_funds.get(month_key)
                self._debug_log(f"Theoretical hours from working_hours_funds: {working_hours_funds.get(month_key)}")

            # Calculate overtime (planned_hours - working_hours_funds) or 0 if negative
            if planned_hours := first_item.get('planned_hours', {}):
                planned_value = planned_hours.get(month_key, 0)
                theoretical_value = working_hours_funds.get(month_key, 0) if working_hours_funds else 0

                # Only positive values are considered overtime
                overtime = max(0, planned_value - theoretical_value)
                result['time_data']['total_overtime_hours'] = overtime
                self._debug_log(
                    f"Planned hours: {planned_value}, Theoretical hours: {theoretical_value}, Overtime: {overtime}")

            # Calculate planned absences from absence records
            if absences := first_item.get('absences', []):
                absence_hours = self._calculate_absence_hours(absences)
                result['time_data']['total_planned_absences'] = absence_hours
                self._debug_log(f"Planned absences: {absence_hours} hours")

        # Step 8: Get paychecks data for additional fields
        self._debug_log("Step 8: Getting paychecks data")
        paychecks_fields = {
            'monthly_bonus_rate': None,
            'expensive_city_bonus_rate': 0,
            'exceptional_bonus_from_salary_review': 0
        }

        try:
            # Get the target date (middle of the month to ensure it falls within the month)
            target_date = datetime.date(year, month, 15)

            # Get the appropriate employment identifier for this date
            employment_identifier = self._get_employment_identifier_for_date(user_id, target_date)

            if employment_identifier:
                # Get the paychecks data
                paycheck_data = self._get_paychecks_data(employment_identifier, year, month)

                if paycheck_data:
                    # Process the paychecks data to extract fields
                    paychecks_fields = self._process_paychecks_data(paycheck_data)
        except Exception as e:
            self._debug_log(f"Error processing paychecks data: {str(e)}")

        # Update the C&B data with paychecks fields
        result['c&b_data']['monthly_bonus_rate'] = paychecks_fields['monthly_bonus_rate']
        result['c&b_data']['expensive_city_bonus_rate'] = paychecks_fields['expensive_city_bonus_rate']
        result['c&b_data']['exceptional_bonus_from_salary_review'] = paychecks_fields[
            'exceptional_bonus_from_salary_review']

        self._debug_log("Processing complete")
        return result

    def clear_caches(self):
        """
        Clear all cached data to force fresh requests on next API calls.
        Useful for long-running processes or when you need to refresh data.
        """
        self._debug_log("Clearing all caches")
        self.work_positions_cache = None
        self.detailed_positions_cache = {}
        self.organization_units_cache = {}

        # Clear employment and paychecks caches if they exist
        if hasattr(self, '_employment_cache'):
            self._employment_cache = {}
        if hasattr(self, '_paychecks_cache'):
            self._paychecks_cache = {}

        self._debug_log("All caches cleared")

    def to_dataframes(self, data):
        """
        Convert structured JSON output to pandas DataFrames.

        Args:
            data: Either a single result dictionary or a list of result dictionaries
                  from get_data_by_email or get_data_by_unit

        Returns:
            Tuple of DataFrames (debug_df, workforce_df, time_df, cb_df)
        """

        # Convert single result to list for consistent processing
        if isinstance(data, dict):
            data_list = [data]
        else:
            data_list = data

        # Extract each section into its own list of dictionaries
        debug_data = []
        workforce_data = []
        time_data = []
        cb_data = []

        for item in data_list:
            if 'debug_data' in item:
                debug_data.append(item['debug_data'])
            if 'workforce_data' in item:
                workforce_data.append(item['workforce_data'])
            if 'time_data' in item:
                time_data.append(item['time_data'])
            if 'c&b_data' in item:
                cb_data.append(item['c&b_data'])

        # Convert to DataFrames
        debug_df = pd.DataFrame(debug_data) if debug_data else pd.DataFrame()
        workforce_df = pd.DataFrame(workforce_data) if workforce_data else pd.DataFrame()
        workforce_df = pd.DataFrame(workforce_data) if workforce_data else pd.DataFrame()
        time_df = pd.DataFrame(time_data) if time_data else pd.DataFrame()
        cb_df = pd.DataFrame(cb_data) if cb_data else pd.DataFrame()

        return debug_df, workforce_df, time_df, cb_df


    def save_duplicate_report(self, duplicates: List[Dict[str, Any]],
                              filename: str = "duplicate_employees_report.csv") -> None:
        """
        Save duplicate employee information to a CSV file.

        Args:
            duplicates: List of duplicate employee information
            filename: Output filename
        """
        if not duplicates:
            self._debug_log("No duplicates to report")
            return

        import pandas as pd
        df = pd.DataFrame(duplicates)
        df.to_csv(filename, index=False)
        self._debug_log(f"Duplicate employee report saved to {filename}")

    def _get_employment_identifiers(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get and cache all employment identifiers with their date ranges for a user.

        Args:
            user_id: User ID

        Returns:
            List of employment data with identifiers and date ranges
        """
        # Check if we already have cached employments for this user
        cache_key = f"employments_{user_id}"
        if hasattr(self, '_employment_cache') and cache_key in self._employment_cache:
            self._debug_log(f"Using cached employment data for user_id {user_id}")
            return self._employment_cache[cache_key]

        # Initialize cache if not exists
        if not hasattr(self, '_employment_cache'):
            self._employment_cache = {}

        # Fetch employments for the user
        self._debug_log(f"Fetching employment data for user_id {user_id}")
        employments = self._make_request(
            endpoint='/api/v1/employments/',
            params={
                'company_id': 1,
                'user_id': user_id,
                'approved': 'true',
                'limit': 100,
                'offset': 0
            }
        )

        # Extract and store relevant employment data
        employment_data = []
        for emp in employments.get('data', []):
            if 'id' in emp and 'employment_identifier' in emp:
                # Parse dates
                start_date = datetime.datetime.strptime(emp['start_date'], "%Y-%m-%d").date() if emp.get(
                    'start_date') else None
                end_date = datetime.datetime.strptime(emp['end_date'], "%Y-%m-%d").date() if emp.get(
                    'end_date') else None

                employment_data.append({
                    'id': emp['id'],
                    'employment_identifier': emp['employment_identifier'],
                    'start_date': start_date,
                    'end_date': end_date,
                    'personal_number': emp.get('personal_number')
                })

        # Cache the result
        self._employment_cache[cache_key] = employment_data
        self._debug_log(f"Cached {len(employment_data)} employments for user_id {user_id}")

        return employment_data

    def _get_employment_identifier_for_date(self, user_id: int, date: datetime.date) -> Optional[str]:
        """
        Get the correct employment identifier for a user on a specific date.

        Args:
            user_id: User ID
            date: The date to check

        Returns:
            Employment identifier string or None if not found
        """
        employments = self._get_employment_identifiers(user_id)

        for emp in employments:
            # Check if the date falls within this employment's date range
            start_date = emp['start_date']
            end_date = emp['end_date']

            if (start_date is None or start_date <= date) and (end_date is None or end_date >= date):
                self._debug_log(
                    f"Found matching employment identifier for user_id {user_id} on {date}: {emp['employment_identifier']}")
                return emp['employment_identifier']

        self._debug_log(f"No matching employment identifier found for user_id {user_id} on {date}")
        return None

    def _get_paychecks_data(self, employment_identifier: str, year: int, month: int) -> Optional[Dict[str, Any]]:
        """
        Get paychecks data for an employment identifier.

        Args:
            employment_identifier: Employment identifier string
            year: Year
            month: Month

        Returns:
            Paychecks data or None if not available
        """
        # Check if we already have cached paychecks for this employment/month/year
        cache_key = f"paychecks_{employment_identifier}_{year}_{month}"
        if hasattr(self, '_paychecks_cache') and cache_key in self._paychecks_cache:
            self._debug_log(f"Using cached paychecks data for {employment_identifier}, {month}/{year}")
            return self._paychecks_cache[cache_key]

        # Initialize cache if not exists
        if not hasattr(self, '_paychecks_cache'):
            self._paychecks_cache = {}

        # Fetch paychecks data
        self._debug_log(f"Fetching paychecks data for {employment_identifier}, {month}/{year}")
        try:
            paychecks = self._make_request(
                endpoint='/api/v1/paychecks/',
                params={
                    'employment_identifier': employment_identifier,
                    'year': year,
                    'month': month,
                    'limit': 1,
                    'offset': 0
                }
            )

            # Extract the first paycheck data if available
            if paychecks.get('data') and len(paychecks['data']) > 0:
                paycheck_data = paychecks['data'][0]

                # Cache the result
                self._paychecks_cache[cache_key] = paycheck_data
                self._debug_log(f"Cached paychecks data for {employment_identifier}, {month}/{year}")

                return paycheck_data
            else:
                self._debug_log(f"No paychecks data found for {employment_identifier}, {month}/{year}")
                return None

        except Exception as e:
            self._debug_log(f"Error fetching paychecks data: {str(e)}")
            return None

    def _process_paychecks_data(self, paycheck_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract the required fields from paychecks data.

        Args:
            paycheck_data: Paychecks data from API

        Returns:
            Dictionary with extracted fields
        """
        result = {
            'monthly_bonus_rate': None,
            'expensive_city_bonus_rate': 0,
            'exceptional_bonus_from_salary_review': 0
        }

        # Get monthly_bonus_rate from extra_data.BonusPercentage
        if extra_data := paycheck_data.get('extra_data', {}):
            if bonus_percentage := extra_data.get('BonusPercentage'):
                try:
                    # Convert to percentage and round
                    result['monthly_bonus_rate'] = round(float(bonus_percentage) * 100, 2)
                    self._debug_log(f"Extracted monthly_bonus_rate: {result['monthly_bonus_rate']}%")
                except (ValueError, TypeError):
                    self._debug_log(f"Could not convert BonusPercentage to float: {bonus_percentage}")

        # Process the items array to find codes 175 and 342
        if items := paycheck_data.get('items', []):
            for item in items:
                # Code 175 - expensive_city_bonus_rate
                if item.get('code') == 175:
                    result['expensive_city_bonus_rate'] = item.get('rate', 0)
                    self._debug_log(
                        f"Found code 175, setting expensive_city_bonus_rate: {result['expensive_city_bonus_rate']}")

                # Code 342 - exceptional_bonus_from_salary_review
                if item.get('code') == 342:
                    result['exceptional_bonus_from_salary_review'] = item.get('total_amount', 0)
                    self._debug_log(
                        f"Found code 342, setting exceptional_bonus_from_salary_review: {result['exceptional_bonus_from_salary_review']}")

        return result
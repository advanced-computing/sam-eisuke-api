# CPI Data Integration
This document outlines the three strategies for loading Consumer Price Index (CPI) data into a DuckDB database. 

1. append_load	
When you only need to add new months and trust that historical data will never change.

2. incremental_load
When historical data might be revised (common in CPI releases) and new months need to be added.

3. trunc_and_load
When you want to reset the database and ensure it perfectly matches the source file.

* Manual Testing
Initial State: Table loaded with 24M1.csv (Jan 1947 – Jan 2024, 924 rows).
Test Input: 25M2.csv (Jan 1947 – Feb 2025, 937 rows).

1. Testing append_load
Expected Observation:
The table should now contain 937 rows.
Check the last 13 rows; they should correspond to Feb 2024 through Feb 2025.
Success Criteria: Historical data (pre-2024) remains unchanged, and only the missing 13 months are added to the end.

2. Testing incremental_load
Expected Observation:
The table should contain 937 rows and each value should be updated.
Verification: Check 1950:01. The value 999.9 should have been overwritten by the correct value from the CSV. New months (up to Feb 2025) should be present.

3. Testing trunc_and_load
Expected Observation:
The table should contain 937 rows.
The table is physically dropped and recreated.
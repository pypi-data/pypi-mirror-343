#!/usr/bin/env python3
"""
IBM Quantum Usage Report Script

This script connects to IBM Quantum using your API token (from .env),
fetches all jobs for the current week, sums their execution times,
and prints a usage report. It is designed for production use, with
extensive comments and notations for future reference and refactoring.

- Author: Quantum-AI Team
- Date: 2024-04-17

NOTES:
- This script uses QiskitRuntimeService.jobs() to fetch job history.
- Quantum usage is fetched via job.usage(), representing actual quantum seconds consumed.
- All API credentials are loaded securely from environment variables.
- This script is robust and ready for deployment.

HISTORY:
- 2024-04-17: Initial version for monthly usage reporting.
"""

import os
import sys
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import argparse

# Load environment variables from .env
load_dotenv()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="IBM Quantum Usage Report")
parser.add_argument("--all-time", action="store_true", help="Report usage across all-time records")
args = parser.parse_args()

# Extensive notation: Always use the correct env var for IBM Quantum
API_TOKEN_ENV_VAR = "IBM_QUANTUM_TOKEN"
token = os.environ.get(API_TOKEN_ENV_VAR)
if not token:
    print(f"Error: {API_TOKEN_ENV_VAR} not found in environment variables. Please set it in your .env file.")
    sys.exit(1)

try:
    from qiskit_ibm_runtime import QiskitRuntimeService
except ImportError as e:
    print("Error: qiskit_ibm_runtime is not installed. Please install it with: pip install qiskit-ibm-runtime")
    sys.exit(1)

# Connect to IBM Quantum
try:
    service = QiskitRuntimeService(channel="ibm_quantum", token=token)
except Exception as e:
    print(f"Error: Failed to connect to IBM Quantum: {e}")
    sys.exit(1)

# Get the current time (UTC)
now = datetime.now(timezone.utc)
if not args.all_time:
    # calculate one-week-ago timestamp
    week_start = now - timedelta(days=7)

# Fetch all jobs via pagination (limit can be increased if needed)
jobs = []
page_size = 100
skip = 0
while True:
    try:
        page = service.jobs(limit=page_size, skip=skip)
    except Exception as e:
        print(f"Error: Failed to fetch jobs from IBM Quantum: {e}")
        sys.exit(1)
    if not page:
        break
    jobs.extend(page)
    skip += len(page)

# Filter jobs based on period and sum usage (quantum seconds) via job.usage()
filtered_jobs = []
total_usage_seconds = 0.0
for job in jobs:
    # Fetch creation date metadata
    creation_date = getattr(job, 'creation_date', None)
    if not creation_date:
        continue  # Skip jobs without creation date
    if not args.all_time:
        # Filter for current week (last 7 days)
        if creation_date.astimezone(timezone.utc) < week_start:
            continue  # Skip jobs older than one week
    # Only consider completed jobs
    if not job.done():
        continue  # Skip jobs still running or queued
    # Fetch actual quantum usage in seconds
    try:
        usage_seconds = job.usage()
    except Exception:
        continue  # Skip if usage unavailable
    total_usage_seconds += usage_seconds
    filtered_jobs.append({
        'job_id': job.job_id(),
        'status': job.status(),
        'creation_date': creation_date,
        'usage_seconds': usage_seconds
    })

# Print the usage report
if args.all_time:
    # Compute timespan of records
    if filtered_jobs:
        dates = [job['creation_date'].astimezone(timezone.utc) for job in filtered_jobs]
        start_date = min(dates)
        end_date = max(dates)
        period_label = f"Records from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
    else:
        period_label = "No completed job records found"
    report_title = "IBM Quantum All-Time Usage Report"
else:
    report_title = "IBM Quantum Weekly Usage Report"
    period_label = f"Week: {week_start.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}"

print(f"\n================ {report_title} ================")
print(period_label)
print(f"Total jobs completed: {len(filtered_jobs)}")
print(f"Total quantum execution time: {total_usage_seconds/60:.2f} minutes ({total_usage_seconds:.2f} seconds)")
print("---------------------------------------------------------")
for job in filtered_jobs:
    print(f"Job ID: {job['job_id']}")
    print(f"  Status: {job['status']}")
    print(f"  Created: {job['creation_date'].strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"  Usage:   {job['usage_seconds']:.2f} quantum seconds")
    print("---------------------------------------------------------")

print("Report generated successfully. For cost details, see the IBM Cloud Billing portal or API.")
# END OF SCRIPT 
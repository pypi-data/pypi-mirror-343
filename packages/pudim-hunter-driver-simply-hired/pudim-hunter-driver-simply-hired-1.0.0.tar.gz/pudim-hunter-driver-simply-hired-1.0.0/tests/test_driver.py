"""
Tests for SimplyHiredScraperJobDriver
"""
from datetime import datetime
from pudim_hunter_driver.models import JobQuery, Job
from pudim_hunter_driver_simply_hired.driver import SimplyHiredScraperJobDriver

import pytest
import os

# Skip all tests in this module if running in CI
pytestmark = pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS") == "true",
    reason="Phantom scraper tests are skipped in CI environment due to IP blocking"
)

def test_fetch_jobs_integration():
    """Test the complete job fetching process with real Simply Hired website"""
    driver = SimplyHiredScraperJobDriver()
    
    # Create a job query
    query = JobQuery(
        keywords="python developer",
        location="remote",
        remote=True
    )
    
    # Fetch jobs from Simply Hired
    job_list = driver.fetch_jobs(query)
    
    # Basic validation of fetched jobs
    assert len(job_list.jobs) > 0, "Should find at least one job"
    
    # Verify structure and data types of returned jobs
    for job in job_list.jobs:
        assert isinstance(job, Job), "Each item should be a Job instance"
        assert isinstance(job.title, str) and len(job.title) > 0, "Job should have a title"
        assert isinstance(job.company, str) and len(job.company) > 0, "Job should have a company"
        assert isinstance(job.location, str) and len(job.location) > 0, "Job should have a location"
        assert isinstance(job.summary, str) and len(job.summary) > 0, "Job should have a summary"
        assert isinstance(job.url, str) and job.url.startswith("https://www.simplyhired.com/"), "Job should have valid Simply Hired URL"
        assert isinstance(job.remote, bool), "Remote should be a boolean"
        assert isinstance(job.posted_at, datetime), "Posted date should be a datetime"
        assert job.source == "simplyhired", "Source should be Simply Hired"
        
        # Optional field validation
        if job.salary_range:
            assert isinstance(job.salary_range, str), "If salary exists, it should be a string"
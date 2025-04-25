import pytest
import os

from unittest.mock import Mock, patch
from datetime import datetime, timezone
from typing import Dict, Any, List
from contextlib import contextmanager

from pudim_hunter_driver.models import JobQuery, Job, JobList
from pudim_hunter_driver_simply_hired import SimplyHiredScraperJobDriver

MAX_PAGES = 2  # Maximum number of pages to scrape

@pytest.fixture
def mock_job_data() -> List[Dict[str, Any]]:
    return [
        {
            "title": "Software Engineer",
            "company": "Tech Corp",
            "location": "San Francisco, CA",
            "url": "/job/123",
            "summary": "Looking for a software engineer...",
            "posted_at": "2024-03-20",
            "remote": True,
            "salary_range": "$100,000 - $150,000 per year"
        },
        {
            "title": "Senior Developer",
            "company": "Dev Inc",
            "location": "Remote",
            "url": "/job/456",
            "summary": "Senior developer position...",
            "posted_at": "2024-03-19",
            "remote": True,
            "salary_range": "$130,000 - $180,000 per year"
        }
    ]

@pytest.fixture
def mock_query() -> JobQuery:
    return JobQuery(
        keywords="python developer",
        location="San Francisco",
        page=1,
        items_per_page=20
    )

@pytest.fixture
def mock_driver():
    # Create a mock scraper with a page attribute and context manager methods
    mock_scraper = Mock()
    mock_scraper.page = Mock()
    mock_scraper.__enter__ = Mock(return_value=mock_scraper)
    mock_scraper.__exit__ = Mock(return_value=None)

    # Create a context manager to simulate fetch_jobs context
    @contextmanager
    def mock_fetch_context():
        driver._scraper = mock_scraper
        try:
            yield
        finally:
            driver._scraper = None

    # Patch the _create_scraper method and add the mock context
    with patch.object(SimplyHiredScraperJobDriver, '_create_scraper', return_value=mock_scraper):
        driver = SimplyHiredScraperJobDriver()
        driver._fetch_context = mock_fetch_context
        yield driver

def test_build_search_url(mock_driver, mock_query):
    url = mock_driver.build_search_url(mock_query)
    assert "simplyhired.com" in url
    assert "python+developer" in url
    assert "San+Francisco" in url

def test_get_selectors(mock_driver):
    selectors = mock_driver.get_selectors()
    assert isinstance(selectors, dict)
    assert "job_list" in selectors
    assert "job_title" in selectors
    assert "company_name" in selectors
    assert "job_location" in selectors
    assert "description" in selectors
    assert "salary" in selectors

def test_extract_raw_job_data(mock_driver, mock_job_data):
    with mock_driver._fetch_context():
        # Mock the page and element selectors
        mock_elements = []
        for job_data in mock_job_data:
            mock_element = Mock()
            def mock_query_selector(selector):
                selector_map = {
                    "h2 a": job_data["title"],
                    "[data-testid='companyName']": job_data["company"],
                    "[data-testid='searchSerpJobLocation']": job_data["location"],
                    "[data-testid='searchSerpJobSnippet']": job_data["summary"],
                    "[data-testid='searchSerpJobSalaryConfirmed']": job_data["salary_range"]
                }
                mock_result = Mock()
                mock_result.inner_text.return_value = selector_map.get(selector, "")
                mock_result.get_attribute.return_value = job_data["url"] if selector == "h2 a" else None
                return mock_result
            mock_element.query_selector.side_effect = mock_query_selector
            mock_elements.append(mock_element)
        
        mock_driver.scraper.page.query_selector_all.return_value = mock_elements
        
        raw_data = mock_driver.extract_raw_job_data()
        assert len(raw_data) == len(mock_job_data)

def test_transform_job(mock_driver, mock_job_data):
    with mock_driver._fetch_context():
        # Create a mock element that simulates a job listing
        mock_element = Mock()
        
        # Configure the mock element's query_selector method
        def mock_query_selector(selector):
            selector_map = {
                "h2 a": ("title", True),
                "[data-testid='companyName']": ("company", False),
                "[data-testid='searchSerpJobLocation']": ("location", False),
                "[data-testid='searchSerpJobSnippet']": ("summary", False),
                "[data-testid='searchSerpJobSalaryConfirmed']": ("salary_range", False)
            }
            
            if selector not in selector_map:
                return None
                
            field, has_href = selector_map[selector]
            mock_result = Mock()
            mock_result.inner_text.return_value = mock_job_data[0][field]
            if has_href:
                mock_result.get_attribute.return_value = mock_job_data[0]["url"]
            return mock_result
        
        mock_element.query_selector.side_effect = mock_query_selector
        
        job = mock_driver.transform_job(mock_element)
        assert isinstance(job, Job)
        assert job.title == mock_job_data[0]["title"]
        assert job.company == mock_job_data[0]["company"]
        assert job.location == mock_job_data[0]["location"]
        assert job.url == "https://www.simplyhired.com" + mock_job_data[0]["url"]
        assert job.summary == mock_job_data[0]["summary"]
        assert isinstance(job.posted_at, datetime)

def test_transform_job_with_invalid_data(mock_driver):
    with mock_driver._fetch_context():
        # Create a mock element that returns None for all selectors
        mock_element = Mock()
        mock_element.query_selector.return_value = None
        
        job = mock_driver.transform_job(mock_element)
        assert job is None

def test_fetch_jobs_integration(mock_driver, mock_query, mock_job_data):
    with mock_driver._fetch_context():
        # Configure mock behaviors
        mock_elements = []
        for job_data in mock_job_data:
            mock_element = Mock()
            def mock_query_selector(selector):
                selector_map = {
                    "h2 a": job_data["title"],
                    "[data-testid='companyName']": job_data["company"],
                    "[data-testid='searchSerpJobLocation']": job_data["location"],
                    "[data-testid='searchSerpJobSnippet']": job_data["summary"],
                    "[data-testid='searchSerpJobSalaryConfirmed']": job_data["salary_range"]
                }
                mock_result = Mock()
                mock_result.inner_text.return_value = selector_map.get(selector, "")
                mock_result.get_attribute.return_value = job_data["url"] if selector == "h2 a" else None
                return mock_result
            mock_element.query_selector.side_effect = mock_query_selector
            mock_elements.append(mock_element)
        
        mock_driver.scraper.page.query_selector_all.return_value = mock_elements
        
        # Fetch jobs
        job_list = mock_driver.fetch_jobs(mock_query)
        
        # Assertions
        assert isinstance(job_list, JobList)
        assert len(job_list.jobs) > 0

def test_pagination_limit(mock_driver, mock_query, mock_job_data):
    with mock_driver._fetch_context():
        # Configure mock behaviors for pagination
        mock_elements = []
        for job_data in mock_job_data:
            mock_element = Mock()
            def mock_query_selector(selector):
                selector_map = {
                    "h2 a": job_data["title"],
                    "[data-testid='companyName']": job_data["company"],
                    "[data-testid='searchSerpJobLocation']": job_data["location"],
                    "[data-testid='searchSerpJobSnippet']": job_data["summary"],
                    "[data-testid='searchSerpJobSalaryConfirmed']": job_data["salary_range"]
                }
                mock_result = Mock()
                mock_result.inner_text.return_value = selector_map.get(selector, "")
                mock_result.get_attribute.return_value = job_data["url"] if selector == "h2 a" else None
                return mock_result
            mock_element.query_selector.side_effect = mock_query_selector
            mock_elements.append(mock_element)
        
        mock_driver.scraper.page.query_selector_all.return_value = mock_elements
        mock_driver.scraper.page.query_selector.return_value = Mock(
            get_attribute=lambda x: "https://www.simplyhired.com/search?page=2"
        )
        
        # Set up a query with a high page number
        high_page_query = JobQuery(
            keywords=mock_query.keywords,
            location=mock_query.location,
            page=5,  # Page number higher than MAX_PAGES
            items_per_page=mock_query.items_per_page
        )
        
        # Fetch jobs with high page number
        job_list = mock_driver.fetch_jobs(high_page_query)
        
        # Verify that the page number was limited
        assert mock_driver.current_page <= MAX_PAGES
        assert isinstance(job_list, JobList)
        assert len(job_list.jobs) <= len(mock_job_data) * MAX_PAGES

def test_error_handling(mock_driver, mock_query):
    with mock_driver._fetch_context():
        # Test network error handling
        mock_driver.scraper.page.wait_for_selector.side_effect = Exception("Network error")
        raw_data = mock_driver.extract_raw_job_data()
        assert raw_data is None

        # Test empty results handling
        mock_driver.scraper.page.wait_for_selector.side_effect = None
        mock_driver.scraper.page.query_selector_all.return_value = []
        raw_data = mock_driver.extract_raw_job_data()
        assert raw_data == [] 
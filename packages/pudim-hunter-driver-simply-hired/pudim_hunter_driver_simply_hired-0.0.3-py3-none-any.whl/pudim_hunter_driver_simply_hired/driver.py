"""
Pudim Hunter Driver Scraper for Simply Hired
"""
from typing import Any, Dict, List

from pudim_hunter_driver.models import JobQuery
from pudim_hunter_driver_scraper.driver import ScraperJobDriver
from pudim_hunter_driver_scraper.driver import ScraperType
from pudim_hunter_driver.models import Job

from typing import Optional
from playwright.sync_api import ElementHandle
from urllib.parse import quote_plus 
from datetime import datetime

import logging


class SimplyHiredScraperJobDriver(ScraperJobDriver):
    """
    Pudim Hunter Driver Scraper for Simply Hired
    """

    BASE_URL = "https://www.simplyhired.com/search?"
    SOURCE = "simplyhired"
    MAX_PAGES = 2  # Maximum number of pages to scrape

    def __init__(self, headless: bool = True):
        super().__init__(headless=headless, scraper_type=ScraperType.PHANTOM)
        self.logger = logging.getLogger(__name__)
        self.current_page = 1

    def extract_raw_job_data(self) -> Optional[Any]:
        """
        Extract raw job data from the page
        """
        try:
            selectors = self.get_selectors()
            self.scraper.page.wait_for_selector(selector=selectors["job_list"], timeout=10000)
            job_elements = self.scraper.page.query_selector_all(selectors["job_list"])
            return job_elements
        except Exception as e:
            self.logger.error(f"Error extracting raw job data: {str(e)}")
            return None

    def transform_job(self, job_element: ElementHandle) -> Optional[Job]:
        """
        Transform a job element into a Job object
        """
        try:
            selectors = self.get_selectors()
            
            title_element =  job_element.query_selector(selectors["job_title"])
            company_element =  job_element.query_selector(selectors["company_name"])
            location_element =  job_element.query_selector(selectors["job_location"])
            salary_element =  job_element.query_selector(selectors["salary"])
            description_element =  job_element.query_selector(selectors["description"])

            title =  title_element.inner_text() if title_element else "N/A"
            description =  description_element.inner_text() if description_element else "N/A"
            link =  title_element.get_attribute("href") if title_element else None
            company =  company_element.inner_text() if company_element else "N/A"
            job_location =  location_element.inner_text() if location_element else "N/A"
            salary =  salary_element.inner_text() if salary_element else "N/A"

            if link:
                full_link = f"https://www.simplyhired.com{link}"
                job_data = {
                    "id": full_link.split("/")[-1],  # Unique ID from job link
                    "title": title,
                    "company": company,
                    "location": job_location,
                    "description": description,
                    "url": full_link,
                    "salary_range": salary,
                    "remote": "remote" in job_location.lower(),
                    "posted_at": datetime.now(),
                    "source": self.SOURCE
                }

                return Job(**job_data)
        except Exception as e:
            self.logger.error(f"Error scraping job: {str(e)}")
            return None

    def get_next_page_url(self, page: int) -> Optional[str]:
        """
        Get the next page url for the given page number
        """
        # Check if we've reached the maximum number of pages
        if self.current_page >= self.MAX_PAGES:
            self.logger.info(f"Reached maximum page limit ({self.MAX_PAGES})")
            return None

        next_page_button = self.scraper.page.query_selector(f"a[data-testid='paginationBlock{page}']")

        if next_page_button:
            next_page_url = next_page_button.get_attribute("href")
            if next_page_url:
                self.logger.info(f"➡️ Moving to page {page}: {next_page_url}")
                self.current_page += 1
                return next_page_url
            else:
                self.logger.info("❌ No more pages available.")
                return None
        else:
            self.logger.info("❌ No more pages available.")
            return None

    def build_search_url(self, query: JobQuery) -> str:
        """
        Build the search URL for the given query
        """
        # Reset current page counter when starting a new search
        self.current_page = 1
        
        url = self.BASE_URL

        if query.keywords:
            url += f"q={quote_plus(query.keywords)}"
            if query.remote:
                url += "+remote"

        if not query.location:
            url += f"&l=remote"
        else:
            url += f"&l={quote_plus(query.location)}"

        return url
    
    def get_selectors(self) -> Dict[str, str]:
        """
        Get the selectors for the job elements
        """
        return {
            "job_list": "#job-list li",
            "job_title": "h2 a",
            "job_location": "[data-testid='searchSerpJobLocation']",
            "company_name": "[data-testid='companyName']",
            "description": "[data-testid='searchSerpJobSnippet']",
            "salary": "[data-testid='searchSerpJobSalaryConfirmed']",
            "next_page_button": "a[data-testid='paginationBlock{next_page_number}']",
        }

    def has_pagination(self) -> bool:
        return True
    
    def has_pagination_items_per_page(self) -> bool:
        return False
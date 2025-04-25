"""
Base scraper job driver implementation.
"""
from enum import Enum
from typing import Dict, Any, Optional, Union, List
from abc import abstractmethod

from pudim_hunter_driver.driver import JobDriver
from pudim_hunter_driver.models import JobQuery, JobList, Job
from pudim_hunter_driver.exceptions import DriverError

from .scraper import PlaywrightScraper
from .scraper_phantom import PhantomPlaywrightScraper
from playwright.sync_api import ElementHandle

class ScraperType(Enum):
    """Enum for available scraper types."""
    BASIC = "basic"
    PHANTOM = "phantom"

class ScraperJobDriver(JobDriver):
    """Base class for scraper-based job drivers."""
    
    def __init__(self, headless: bool = True, scraper_type: Union[str, ScraperType] = ScraperType.BASIC):
        """Initialize the driver.
        
        Args:
            headless: Whether to run the browser in headless mode.
            scraper_type: Type of scraper to use ("basic" or "phantom")
        """
        self.headless = headless
        self._scraper: Optional[PlaywrightScraper] = None
        
        # Convert string to enum if needed
        if isinstance(scraper_type, str):
            try:
                scraper_type = ScraperType(scraper_type.lower())
            except ValueError:
                raise ValueError(f"Invalid scraper type: {scraper_type}. Valid types are: {[t.value for t in ScraperType]}")
        
        self.scraper_type = scraper_type

    def _create_scraper(self) -> PlaywrightScraper:
        """Create a scraper instance based on the configured type.
        
        Returns:
            An instance of the requested scraper type.
        """
        if self.scraper_type == ScraperType.PHANTOM:
            return PhantomPlaywrightScraper(headless=self.headless)
        return PlaywrightScraper(headless=self.headless)

    @property
    def scraper(self) -> PlaywrightScraper:
        """Get the current scraper instance.
        
        Returns:
            The current scraper instance.
            
        Raises:
            RuntimeError: If scraper is not initialized.
        """
        if not self._scraper:
            raise RuntimeError("Scraper not initialized. Use within fetch_jobs context.")
        return self._scraper
        
    @abstractmethod
    def build_search_url(self, query: JobQuery) -> str:
        """Build the search URL for the job board.
        
        Args:
            query: The job search query.
            
        Returns:
            The complete search URL.
        """
        pass
        
    @abstractmethod
    def get_selectors(self) -> Dict[str, str]:
        """Get the CSS selectors for job data extraction.
        
        Returns:
            Dictionary mapping field names to CSS selectors.
        """
        pass
        
    @abstractmethod
    def extract_raw_job_data(self) -> Optional[Any]:
        """Extract job data from the page using a CSS selector.
        
        Returns:
            List of raw job data or None if no jobs found.
        """
        pass
        
    @abstractmethod
    def transform_job(self, data: Dict[str, Any]) -> Optional[Job]:
        """Transform scraped data into a Job object.
        
        Args:
            data: Raw scraped data.
            
        Returns:
            Job object or None if data is invalid.
        """
        pass

    @abstractmethod
    def has_pagination(self) -> bool:
        """Check if the job board has pagination."""
        pass

    @abstractmethod
    def get_next_page_url(self, page_number: int) -> Optional[str]:
        """Get the URL for the next page of results."""
        pass

    @abstractmethod
    def has_pagination_items_per_page(self) -> bool:
        """Check if the job board has pagination items per page."""
        pass

    @abstractmethod
    def has_description_support_enabled(self) -> bool:
        """Check if the job board has description support."""
        pass

    @abstractmethod
    def get_description(self, element: ElementHandle) -> Optional[str]:
        """Get the description support for the job board."""
        pass

    @abstractmethod
    def has_qualifications_support_enabled(self) -> bool:
        """Check if the job board has qualifications support."""
        pass

    @abstractmethod
    def get_qualifications(self, element: ElementHandle) -> Optional[List[str]]:
        """Get the qualifications support for the job board."""
        pass


    def fetch_jobs(self, query: JobQuery) -> JobList:
        """Fetch jobs using Playwright scraper.
        
        Args:
            query: The job search query.
            
        Returns:
            List of jobs matching the query.
        """

        try:
            with self._create_scraper() as scraper:
                self._scraper = scraper  # Store the scraper instance
                page_number = 1
                url = self.build_search_url(query)

                jobs = []

                while True:
                    raw_jobs = self.fetch_raw_jobs_from_url(url)

                    if raw_jobs:
                        for raw_job in raw_jobs:
                            job = self.transform_job(raw_job)

                            if self.has_description_support_enabled() and job:
                                job.description = self.get_description(raw_job)

                            if self.has_qualifications_support_enabled() and job:
                                job.qualifications = self.get_qualifications(raw_job)

                            if job:
                                jobs.append(job)

                    if self.has_pagination():
                        next_page_number = page_number + 1                        
                        url = self.get_next_page_url(next_page_number)
                        if not url:
                            break

                        page_number = next_page_number
                    else:
                        break;                
                
                return JobList(
                    jobs=jobs,
                    total_results=len(jobs),
                    page=query.page,
                    items_per_page=query.items_per_page
                )

        except Exception as e:
            raise DriverError(f"Failed to create scraper: {str(e)}")
        finally:
            self._scraper = None 

        return None


    def fetch_raw_jobs_from_url(self, url: str) -> Optional[List[Any]]:
        """Fetch raw jobs from a given URL.
        
        Args:
            url: The URL to fetch jobs from.
            
        Returns:
            List of raw job data or None if no jobs found.
            
        Raises:
            DriverError: If job fetching fails.
        """
        self.scraper.navigate(url)        
        raw_jobs = self.extract_raw_job_data()
        return raw_jobs

            
    def validate_credentials(self) -> bool:
        """Validate driver credentials.
        
        Returns:
            True if credentials are valid, False otherwise.
        """
        # No credentials needed for basic scraping
        return True 
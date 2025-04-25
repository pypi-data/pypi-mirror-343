# Pudim Hunter Driver Scraper 🍮

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Pytest 7.4](https://img.shields.io/badge/pytest-7.4-brightgreen.svg)](https://docs.pytest.org/en/7.4.x/)
[![CI](https://github.com/luismr/pudim-hunter-driver-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/luismr/pudim-hunter-driver-scraper/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/luismr/pudim-hunter-driver-scraper/branch/main/graph/badge.svg)](https://codecov.io/gh/luismr/pudim-hunter-driver-scraper)
[![PyPI version](https://badge.fury.io/py/pudim-hunter-driver-scraper.svg)](https://pypi.org/project/pudim-hunter-driver-scraper/)

A Python package that provides a Playwright-based scraper implementation for The Pudim Hunter platform. This package extends the `pudim-hunter-driver` interface to provide a common base for implementing job board scrapers.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
   - [PyPI Installation](#pypi-installation)
   - [Development Installation](#development-installation)
3. [Usage](#usage)
   - [Interface Overview](#interface-overview)
   - [Example Implementation](#example-implementation)
   - [Usage Examples](#usage-examples)
4. [Development Setup](#development-setup)
   - [Virtual Environment](#virtual-environment)
   - [Prerequisites](#prerequisites)
   - [Setup Instructions](#setup-instructions)
5. [Project Structure](#project-structure)
6. [Testing](#testing)
7. [Contributing](#contributing)
   - [Getting Started](#getting-started)
   - [Pull Request Process](#pull-request-process)
8. [License](#license)

## Features

* Playwright-based web scraping
* Headless browser automation
* Easy-to-extend base classes for job board implementations
* Built-in error handling and resource management
* Type hints and validation using Pydantic
* Advanced anti-detection scraping with `PhantomPlaywrightScraper`
  - WebDriver detection evasion
  - WebGL vendor spoofing
  - Chrome properties emulation
  - Plugin spoofing
  - Language preferences customization
  - And more stealth features

## Installation

### PyPI Installation

You can install the package directly from PyPI:

```bash
pip install pudim-hunter-driver-scraper
```

Or add to your requirements.txt:
```
pudim-hunter-driver-scraper>=0.0.1  # Replace with the version you need
```

### Development Installation

For development:
```bash
git clone git@github.com:luismr/pudim-hunter-driver-scraper.git
cd pudim-hunter-driver-scraper
pip install -e .
```

## Usage

### Interface Overview

This package provides the base scraper implementation for job search drivers. To create a scraper for a specific job board, you'll need to extend the `ScraperJobDriver` class and implement the required methods.

1. `ScraperJobDriver` (ABC) - The base scraper class that implements `JobDriver`:
   * Required Methods:
     * `build_search_url(query: JobQuery) -> str` - Build the search URL for the job board
     * `get_selectors() -> Dict[str, str]` - Get CSS selectors for job elements
     * `extract_raw_job_data() -> Optional[Any]` - Extract raw job data from the page
     * `transform_job(data: Dict[str, Any]) -> Optional[Job]` - Transform raw data into Job model
     * `has_pagination() -> bool` - Check if the job board has pagination
     * `get_next_page_url(page_number: int) -> Optional[str]` - Get URL for next page
     * `has_pagination_items_per_page() -> bool` - Check if pagination supports items per page
     * `has_description_support_enabled() -> bool` - Check if description support is enabled
     * `get_description(job: Job) -> Optional[str]` - Get job description
     * `has_qualifications_support_enabled() -> bool` - Check if qualifications support is enabled
     * `get_qualifications(job: Job) -> Optional[List[str]]` - Get job qualifications

2. `PlaywrightScraper` - The base scraper implementation:
   * Handles browser lifecycle
   * Provides navigation and data extraction methods
   * Context manager support with `with` statement

3. `PhantomPlaywrightScraper` - Enhanced scraper with anti-detection:
   * All features of base PlaywrightScraper
   * Advanced bot detection evasion
   * Stealth mode configurations

4. Exceptions:
   * Inherits all exceptions from `pudim-hunter-driver`
   * Adds scraper-specific error handling

### Example Implementation

```python
from typing import Dict, Any, Optional, List
from datetime import datetime
from pudim_hunter_driver.models import JobQuery, Job
from pudim_hunter_driver_scraper import ScraperJobDriver
from pudim_hunter_driver_scraper.driver import ScraperType

class MyPhantomJobDriver(ScraperJobDriver):
    def __init__(self):
        super().__init__(scraper_type=ScraperType.PHANTOM)
    
    def build_search_url(self, query: JobQuery) -> str:
        """Build the search URL for the job board."""
        return f"https://example.com/jobs?q={query.keywords}&l={query.location}"
    
    def get_selectors(self) -> Dict[str, str]:
        """Define CSS selectors for job elements."""
        return {
            "job_list": ".job-listing",
            "title": ".job-title",
            "company": ".company-name",
            "location": ".job-location"
        }
    
    def extract_raw_job_data(self) -> Optional[List[Dict[str, Any]]]:
        """Extract job data from the page."""
        jobs_data = []
        job_elements = self.scraper._page.query_selector_all(self.get_selectors()["job_list"])
        
        for job in job_elements:
            title = job.query_selector(self.get_selectors()["title"])
            company = job.query_selector(self.get_selectors()["company"])
            
            if title and company:
                jobs_data.append({
                    "title": title.inner_text(),
                    "company": company.inner_text()
                })
        
        return jobs_data
    
    def transform_job(self, data: Dict[str, Any]) -> Optional[Job]:
        """Transform raw job data into Job model."""
        if not data.get("title"):
            return None
            
        return Job(
            id=f"job-{hash(data['title'])}",
            title=data["title"],
            company=data["company"],
            location="",
            summary="",
            url="",
            remote=False,
            source="Example",
            posted_at=datetime.now()
        )
    
    def has_pagination(self) -> bool:
        """Check if the job board has pagination."""
        return True
    
    def get_next_page_url(self, page_number: int) -> Optional[str]:
        """Get URL for next page of results."""
        return f"https://example.com/jobs?page={page_number}"
    
    def has_pagination_items_per_page(self) -> bool:
        """Check if pagination supports items per page."""
        return True
    
    def has_description_support_enabled(self) -> bool:
        """Check if description support is enabled."""
        return True
    
    def get_description(self, job: Job) -> Optional[str]:
        """Get job description."""
        # Implement description extraction logic
        return None
    
    def has_qualifications_support_enabled(self) -> bool:
        """Check if qualifications support is enabled."""
        return True
    
    def get_qualifications(self, job: Job) -> Optional[List[str]]:
        """Get job qualifications."""
        # Implement qualifications extraction logic
        return None
```

### Usage Examples

```python
# Using the driver
driver = MyPhantomJobDriver()
query = JobQuery(
    keywords="software engineer",
    location="San Francisco",
    page=1,
    items_per_page=20
)

job_list = driver.fetch_jobs(query)
for job in job_list.jobs:
    print(f"{job.title} at {job.company}")
```

For more detailed examples, check the test files:
- `tests/test_driver_phantom.py`: Complete job driver implementation example
- `tests/test_scraper_phantom.py`: Anti-detection features testing
- `tests/test_scraper_phantom_sites.py`: Real-world site scraping examples

## Development Setup

### Virtual Environment

We strongly recommend using a virtual environment for development and testing.

### Prerequisites

* Python 3.9 or higher
* pip (Python package installer)
* venv module (usually comes with Python 3)

### Setup Instructions

1. Create and activate virtual environment:
```bash
python3.9 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

## Project Structure

```
pudim-hunter-driver-scraper/
├── src/
│   └── pudim_hunter_driver_scraper/
│       ├── __init__.py          # Package initialization
│       ├── scraper.py           # PlaywrightScraper implementation
│       └── driver.py            # ScraperJobDriver implementation
├── tests/                       # Test directory
│   └── __init__.py
├── README.md                    # This file
├── requirements.txt             # Direct dependencies
├── setup.py                     # Package setup
└── pyproject.toml              # Project configuration
```

## Testing

Run the tests:
```bash
pytest tests/
```

Key test files:
- `test_driver_phantom.py`: Tests for phantom job driver implementation
- `test_scraper_phantom.py`: Tests for anti-detection capabilities
- `test_scraper_phantom_sites.py`: Tests for real-world site scraping

## Contributing

### Getting Started

1. Fork and clone the repository:
```bash
git clone git@github.com:luismr/pudim-hunter-driver-scraper.git
cd pudim-hunter-driver-scraper
```

2. Create your feature branch:
```bash
git checkout -b feature/amazing-feature
```

3. Set up development environment:
```bash
python3.9 -m venv venv
source venv/bin/activate
pip install -e .
```

### Pull Request Process

1. Update documentation as needed
2. Add/update tests as needed
3. Ensure all tests pass
4. Submit PR for review

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

Copyright (c) 2024-2025 Luis Machado Reis 
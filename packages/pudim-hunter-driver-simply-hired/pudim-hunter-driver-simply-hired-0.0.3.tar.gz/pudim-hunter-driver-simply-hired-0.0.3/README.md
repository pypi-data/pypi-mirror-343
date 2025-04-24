# pudim-hunter-driver-simply-hired

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Pytest 7.4](https://img.shields.io/badge/pytest-7.4-brightgreen.svg)](https://docs.pytest.org/en/7.4.x/)
[![CI](https://github.com/luismr/pudim-hunter-driver-simply-hired/actions/workflows/ci.yml/badge.svg)](https://github.com/luismr/pudim-hunter-driver-simply-hired/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/luismr/pudim-hunter-driver-simply-hired/branch/main/graph/badge.svg)](https://codecov.io/gh/luismr/pudim-hunter-driver-simply-hired)
[![PyPI version](https://badge.fury.io/py/pudim-hunter-driver-simply-hired.svg)](https://pypi.org/project/pudim-hunter-driver-simply-hired/)

A specialized Simply Hired job scraper package built on top of `pudim-hunter-driver`. This package provides a robust implementation for scraping job listings from Simply Hired while effectively avoiding bot detection mechanisms.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- Specialized Simply Hired job scraping implementation
- Advanced anti-bot detection using PhantomPlaywrightScraper
- Headless browser automation with Playwright
- Robust error handling and retry mechanisms
- Clean job data extraction and transformation

## Installation

### From PyPI
```bash
pip install pudim-hunter-driver-simply-hired
```

### For Development
```bash
git clone git@github.com:luismr/pudim-hunter-driver-simply-hired.git
cd pudim-hunter-driver-simply-hired
pip install -e .
```

## Usage

```python
from pudim_hunter_driver.models import JobQuery
from pudim_hunter_driver_simply_hired import SimplyHiredJobDriver

# Initialize the driver
driver = SimplyHiredJobDriver()

# Create a job search query
query = JobQuery(
    keywords="software engineer",
    location="San Francisco",
    page=1,
    items_per_page=20
)

# Fetch jobs
job_list = driver.fetch_jobs(query)
for job in job_list.jobs:
    print(f"{job.title} at {job.company}")
```

### Anti-Bot Detection

The SimplyHiredJobDriver uses PhantomPlaywrightScraper internally to implement advanced anti-bot detection measures, ensuring reliable scraping from Simply Hired. This includes:

- Browser fingerprint randomization
- Stealth mode configurations
- Automated request pattern variation
- Advanced header management

## Project Structure

```
pudim-hunter-driver-simply-hired/
├── src/
│   └── pudim_hunter_driver_simply_hired/
│       ├── __init__.py
│       └── driver.py            # SimplyHiredJobDriver implementation
├── tests/
│   ├── __init__.py
│   └── test_simply_hired.py     # SimplyHiredJobDriver tests
├── README.md
├── requirements.txt
├── setup.py
└── pyproject.toml
```

## Development Setup

### Prerequisites

* Python 3.9 or higher
* pip (Python package installer)
* venv module

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

## Testing

Run the tests:
```bash
pytest tests/
```

The main test file:
- `test_simply_hired.py`: Tests for SimplyHiredJobDriver implementation and its anti-bot capabilities

## Contributing

### Getting Started

1. Fork and clone the repository:
```bash
git clone git@github.com:luismr/pudim-hunter-driver-simply-hired.git
cd pudim-hunter-driver-simply-hired
```

2. Create your feature branch:
```bash
git checkout -b feature/amazing-feature
```

3. Set up development environment as described above

### Pull Request Process

1. Update documentation as needed
2. Add/update tests as needed
3. Ensure all tests pass
4. Submit PR for review

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

Copyright (c) 2024-2025 Luis Machado Reis 
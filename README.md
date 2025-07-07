# greenfrog-automation

This repository implements an automation framework for end-to-end testing and API validation for JFrog repository creation with validating scan violations using UI automation

### What was my framework design thought process

1. I aimed to make the framework as scalable as possible, so it can easily accommodate future requirements and additional test modules.
2. I used the factory pattern to manage data such as payload requests and web elements, which enhances scalability for both backend and UI automation.
3. A centralized configuration space is provided for both UI and API tests, making it easy to manage and update environment-specific settings.
4. I integrated `flake8` for Python linting to ensure code quality and maintain consistent styling across the project.
5. All helper functions are currently under the `utils` directory. While I considered creating a separate `helpers` directory, for this automation’s current scope, it was unnecessary. In a larger framework, I would separate helpers for better organization.
6. All environment-related configurations are sourced from a `.env` file, allowing for easy scaling to multiple environments by simply changing environment variable values.
7. For demonstration purposes, username and password are stored in the `.env` file. In a production-grade automation framework, I recommend using secure storage solutions like AWS Secrets Manager or GitHub Secrets, especially for CI/CD pipelines.
8. The `setup.py` file is enabled to make the framework easily shareable and installable as a package.
9. There are two `conftest.py` files: one inside the `tests` directory for test-specific fixtures, and another under the `src` directory for global fixtures. This structure supports scalability if you add multiple test modules (e.g., `module1`, `module2`, etc.).
10. Logging is implemented extensively, with logs generated under the `logs` directory to aid in debugging and traceability.
11. The framework supports both API and UI automation, making it suitable for end-to-end validation scenarios.
12. Test data and page object management are modular, allowing for easy updates and maintenance as application features evolve.
13. The framework is compatible with both local and CI/CD execution, supporting seamless integration into automated pipelines.
14. Reporting is enabled via Allure, providing detailed and visually appealing test execution reports.
15. The project structure follows best practices for Python automation frameworks, ensuring maintainability and ease of onboarding for new contributors.
16. The codebase is designed to be extensible, so new features or test types can be added with minimal refactoring.

## Understanding the Automation Framework Structure

1. [`.github`](.github) directory

   - This directory has the [pull_request_template.md](.github/pull_request_template.md) and [`workflows`](.github/workflows) configured for this repository
   - Currently i have enabled `flake8` checks for formatting and other syntaxing checks for python.
 

2. [`allure-results`](allure-results) directory

   - Stores Allure report files generated during test execution.
   - Created automatically when running pytest with the `--alluredir=allure-results` option.

3. [`logs`](logs) directory

   - Contains logs generated during test execution for debugging and traceability.
   - Logging configuration is managed via [`pytest.ini`](pytest.ini).
   - Example: [`logs/execution.log`](logs/execution.log) is generated automatically when running tests.

4. [`screenshots`](screenshots) directory

   - Contains screenshots generated during the execution of UI automation

5. [`src`](src) directory

   - Main source code for the automation framework, organized as follows:

     - [`src/config`](src/config):
       - Configuration and constants for the framework ([`constants.py`](src/config/constants.py)).

     - [`src/factories`](src/factories):
       - Factory classes for creating test data and page objects.
       - [`data/payload_factory.py`](src/factories/data/payload_factory.py): Data payload factories for API tests.
       - [`pages/login_page_factory.py`](src/factories/pages/login_page_factory.py): Login page object factory.
       - [`pages/scan_page_factory.py`](src/factories/pages/scan_page_factory.py): Scan page object factory.

     - [`src/utils`](src/utils):
       - Utility modules for API helpers, base clients, scan utilities, and screenshot utilities.
       - [`api_helpers.py`](src/utils/api_helpers.py): API helper functions.
       - [`base_api_client.py`](src/utils/base_api_client.py): Base API client class.
       - [`scan_utils.py`](src/utils/scan_utils.py): Utilities for scan-related operations.
       - [`screenshot_utils.py`](src/utils/screenshot_utils.py): Screenshot capture utilities.

     - [`src/validators`](src/validators):
       - Response and data validation utilities.
       - [`response_validators.py`](src/validators/response_validators.py): Response validation logic.

     - [`src/tests`](src/tests):
       - Contains test files and test-specific fixtures.
       - [`conftest.py`](src/tests/conftest.py): Test fixtures for pytest.
       - [`test_e2e_xray_flow.py`](src/tests/test_e2e_xray_flow.py): The artifact creation to UI validation end-to-end test flow.

     - [`src/conftest.py`](src/conftest.py):
       - Global pytest fixtures for the framework.

     - [`src/greenfrog_automation.egg-info`](src/greenfrog_automation.egg-info):
       - Packaging metadata for the framework (auto-generated).

6. [`pytest.ini`](pytest.ini) file

   - Controls pytest options, logging configuration, and report generation.
   - I have enabled allure reporting for this so you can see adopts params for the same. `addopts = -v --alluredir=allure-results`

7. [`requirements.txt`](requirements.txt) file

   - Lists all Python package dependencies required for the framework.
   - Install these in your virtual environment before running tests.

8. [`setup.py`](setup.py) file

   - Packaging script for the automation framework.

9. [`README.md`](README.md) file

   - This file. Contains setup, usage, and framework structure documentation.

10. [`.flake8`](.flake8) file
   - Python styling and syntaxing file

11. [`.gitignore`](.gitignore) file
   - Typical gitignore file for python with some custom additions

12. [`.env`](.env) file
   - Environment specific configurations

> Note: `__init__.py` is present in every package directory to enable proper Python module resolution.

## Setup Instructions for Automation Framework

1. Verify if Python is installed (Python 3.11 or later required):

   ```bash
   which python3
   ```

2. If Python isn't installed, download and install it from [Python website](https://www.python.org/downloads/).

3. Clone the repository: [`Github Repository Link`](https://github.com/siddharthagout/greenfrog-automation)
   
   ```bash
   git clone <repo-url>
   cd greenfrog-automation
   ```

4. Create and activate a virtual environment:

   ```bash
   # For Mac/Linux
   python3 -m venv venv
   source venv/bin/activate

   # incase you want to run tests without any IDE
   MYDIR=`pwd`/venv/bin/activate
   source $MYDIR
   # For Windows
   # .\venv\Scripts\activate
   ```
   Note incase 

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Install the framework locally in editable mode:

   ```bash
   pip install -e .
   ```

   This allows you to import project modules without needing absolute paths.

## Running Automation Tests

1. Run all tests:

   ```bash
   pytest src
   ```

2. Or Running specific test file :

   ```bash
   pytest src/tests/test_e2e_xray_flow.py
   ```

## Allure Reporting

### 1. Install Allure CLI on macOS (via Homebrew)

```bash
brew install allure
allure --version
```

For other OS installation instructions, refer to: [https://allurereport.org/docs/install/](https://allurereport.org/docs/install/)

### 2. Generate and View the Report

```bash
# execute tests
pytest src

# generate report
allure serve allure-results
```

This will launch a browser window with the test report.

---

## Notes

- Logging is enabled across all tests to help in debugging.
- Fixtures are reusable and help abstract log reading and data setup.
- The framework is designed with modularity and scalability in mind for future expansion.
- For any issues or questions, please contact me via siddharthagout@gmail.com.

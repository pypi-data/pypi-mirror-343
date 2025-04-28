# 🚀🔬 vipentium: A Comprehensive Python Testing Framework

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python Versions](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-brightgreen.svg)](https://www.python.org/dev/peps/pep-0008/)

vipentium is a robust and user-friendly Python testing framework engineered to streamline your testing process. It provides a rich set of features to facilitate efficient test creation and execution.

## ✨ Key Features

* **🔍 Auto Test Discovery:** Automatically identifies test files (prefixed with `test_`), modules, and directories within a specified path, simplifying test organization and execution.
* **⚙️ Parameterized Testing (`@parameters`):** Enables running a single test function with multiple sets of input data. You can provide tuples of arguments or dictionaries of keyword arguments, optionally naming each parameter set for clearer reporting.
* **⏳ Asynchronous Test Support (`async`/`await`):** Fully supports testing asynchronous Python code written using `async` and `await` keywords, ensuring compatibility with modern Python concurrency.
* **⏰ Timeout Control (`@timeout`):** Allows setting a maximum execution time (in seconds) for individual test methods. If a test exceeds this limit, it's automatically marked as failed, preventing indefinite hangs.
* **🔄 Test Retries (`@retry`):** Provides a mechanism to automatically re-run failing tests a specified number of times. This is particularly useful for handling tests that might occasionally fail due to external factors or non-deterministic behavior.
* **💨 Parallel Execution (`--parallel`, `--process`):** Significantly reduces test execution time by running tests concurrently. The `--parallel` flag uses threads, while the `--process` flag utilizes separate processes for better isolation (requires `--parallel`).
* **🔌 Plugin Architecture:** Offers a flexible plugin system that allows you to extend the framework's functionality. You can create custom plugins to hook into various stages of the test lifecycle (e.g., before/after tests, suite start/end).
* **🛠️ Enhanced Fixture Management (`@fixture`):** Introduces a powerful fixture system for managing test dependencies and setup/cleanup operations. Fixtures support dependency injection, allowing test methods to receive required resources as arguments. Fixture scopes (`function`, `session`) control their lifecycle.
* **🏷️ Test Filtering with Markers (`@mark`, `--mark`):** Enables tagging test methods with descriptive labels using the `@mark` decorator. You can then use the `--mark` command-line option to selectively run tests based on these markers.
* **🗣️ Verbose Output (`--verbose`):** Provides more detailed output during test execution, including the names of discovered tests, the status of each test (pass/fail), execution times, and any error messages, enhanced with ANSI color codes for better readability.
* **📊 Advanced Reporting (`--report-json`, `--report-html`):** Supports generating comprehensive test reports in two formats:
    * **JSON (`--report-json <filename>`):** Creates a structured JSON file containing a summary of the test run and detailed results for each test.
    * **HTML (`--report-html <filename>`):** Generates a user-friendly HTML report with a summary and detailed test results presented in a web browser.

## 🕹️ Getting Started


```
pip install vipentium

---
vipentium <test_path> [options] 
````

Replace `<test_path>` with the path to the directory, file, or module containing your tests.

### Command-Line Options

| Option          | Description                                                                                                |
| :-------------- | :--------------------------------------------------------------------------------------------------------- |
| `<test_path>`   | The path to the directory, file, or module where vipentium should discover and run tests.                   |
| `--parallel`    | Enable parallel test execution using threads for potentially faster test runs.                             |
| `--process`     | Use separate processes for parallel test execution (requires `--parallel`). Provides better isolation.       |
| `--verbose`     | Enable verbose output, showing more details about the test execution process.                               |
| `--report-json <filename>` | Generate a test report in JSON format and save it to the specified filename.                       |
| `--report-html <filename>` | Generate a test report in HTML format and save it to the specified filename.                       |
| `--mark <marker>` | Only run tests that are decorated with the specified marker. This option can be used multiple times.      |

## 🧪 Writing Test Cases

1.  **Test File Naming:** Name your test files with the prefix `test_` (e.g., `test_utils.py`).
2.  **Test Class Definition:** Create classes that inherit from the `TestCase` base class provided by vipentium.
3.  **Test Method Definition:** Define individual test methods within your test classes. These methods must start with the prefix `test_` (e.g., `test_calculate_sum`).
4.  **Assertions:** Use the `assert_equal(a, b)` method provided by the `TestCase` class to compare expected and actual results. You can also use standard Python `assert` statements.
5.  **Decorators for Enhanced Testing:**
      * `@parameters(*args, **kwargs)`: Apply this decorator to a test method to run it with multiple sets of arguments. You can provide individual tuples or a list of tuples. For named parameters, use a dictionary with keys `"args"`, `"kwargs"`, and optionally `"name"`.
      * `@timeout(seconds)`: Decorate a test method to set a maximum execution time in seconds.
      * `@retry(times)`: Decorate a test method to specify the number of times it should be automatically retried upon failure.
      * `@mark(*tags)`: Decorate a test method with one or more marker tags (strings).
      * `@fixture(scope="function"|"session")`: Decorate a function to define a test fixture. The `scope` argument determines the fixture's lifecycle.

<!-- end list -->

```python
from vipentium import TestCase, parameters, timeout, retry, mark, fixture

@fixture
def setup_data():
    return {"user_id": 123, "username": "testuser"}

@mark("user", "integration")
class TestUserOperations(TestCase):
    def setUp(self):
        self.api_client = ... # Initialize an API client

    def tearDown(self):
        pass # Clean up resources

    @parameters((1, 2, 3, "positive"), (-1, 1, 0, "negative_zero"), name="addition_cases")
    def test_add(self, a, b, expected, case_name):
        self.assert_equal(a + b, expected)

    @timeout(3)
    @retry(2)
    def test_api_request(self, setup_data):
        user = self.api_client.get_user(setup_data["user_id"])
        self.assert_equal(user["username"], setup_data["username"])

    @mark("database")
    def test_database_connection(self):
        db = ... # Connect to database
        self.assertTrue(db.is_connected())
        db.close()
```

## 🔌 Extending with Plugins

vipentium's plugin system allows you to customize and extend its behavior. To create a plugin:

1.  Create a class that inherits from the `Plugin` base class provided by `vipentium`.
2.  Override the available hook methods (`before_test`, `after_test`, `on_start_suite`, `on_end_suite`) to implement your desired actions.
3.  Register your plugin using the `register_plugin()` function.

<!-- end list -->

```python
from vipentium import Plugin, register_plugin

class CustomReportPlugin(Plugin):
    def after_test(self, test_name, test_class, method_name, parameters, success, message, duration):
        if success:
            print(f"[CUSTOM REPORT] Test '{test_name}' passed in {duration:.2f}s")
        else:
            print(f"[CUSTOM REPORT] Test '{test_name}' failed: {message}")

def load_my_plugins():
    register_plugin(CustomReportPlugin())

# Make sure to call load_my_plugins() before running your tests.
```

## 📊 Reporting

vipentium can generate detailed reports of your test execution:

  * **JSON Report:** A structured `.json` file containing a summary of the test run (total, passed, failed, duration) and a list of individual test results with their names, status, duration, and any failure messages.
  * **HTML Report:** A human-readable `.html` file presenting the test summary and detailed results in a well-formatted web page.

Use the `--report-json <filename>` and `--report-html <filename>` command-line options to specify the names of the generated report files.

## 📜 License

MIT | @vipentium

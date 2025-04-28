#!/usr/bin/env python3
"""
vipentium: A Comprehensive Python Testing Framework

Features:
  • Auto test discovery (module, file, or directory)
  • Parameterized testing via @parameters decorator with optional names
  • Asynchronous test support (async/await tests)
  • Timeouts and retries via @timeout and @retry decorators
  • Parallel test execution (--parallel flag) with option for process-based execution (--process)
  • Enhanced fixture management with dependency injection via @fixture
  • Test filtering via markers (@mark and --mark)
  • Advanced reporting: JSON and HTML reports (--report-json / --report-html)

"""

import sys, os, argparse, time, traceback, importlib, importlib.util, json, asyncio, inspect, logging
import concurrent.futures

import os
import sys

# Add the parent directory to sys.path so that the "vipentium" folder is recognized.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Global configuration dictionary
config = {
    'parallel': False,
    'process': False,  # If True, use ProcessPoolExecutor for parallelism.
    'verbose': False,
    'report_json': None,
    'report_html': None,
    'coverage': False,  # Placeholder for coverage integration
    'markers': None     # Marker filter (list)
}

# Global plugin registry
PLUGINS = []

def register_plugin(plugin):
    PLUGINS.append(plugin)

# Setup logging
logger = logging.getLogger("vipentium")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# ANSI color codes for colorized output
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

def color_text(text, color):
    return f"{color}{text}{RESET}"

# --------------------------------------------------------------
# Fixture Management and Dependency Injection
# --------------------------------------------------------------

# Global registry for fixtures.
FIXTURES = {}

def fixture(scope="function"):
    """
    Decorator to register a fixture.
    Supported scopes: "function" (default), "session"
    """
    def decorator(func):
        FIXTURES[func.__name__] = {"func": func, "scope": scope, "value": None}
        return func
    return decorator

# --------------------------------------------------------------
# Marker decorator for test filtering
# --------------------------------------------------------------
def mark(*tags):
    """
    Decorator to tag tests with marker labels.
    """
    def decorator(func):
        setattr(func, "markers", tags)
        return func
    return decorator

# --------------------------------------------------------------
# Decorators for Parameterized Tests, Timeout and Retry
# --------------------------------------------------------------
def parameters(*args, **kwargs):
    """
    Decorator for parameterized tests.
    Accepts either a tuple (args, kwargs) or a dict with keys: "args", "kwargs", "name"
    """
    def decorator(func):
        if not hasattr(func, "parameters"):
            func.parameters = []
        # If a single dict is passed with keys "args" (and optionally "kwargs" and "name")
        if len(args) == 1 and isinstance(args[0], dict) and "args" in args[0]:
            func.parameters.append((args[0]["args"], args[0].get("kwargs", {}), args[0].get("name", None)))
        else:
            func.parameters.append((args, kwargs, None))
        return func
    return decorator

def timeout(seconds):
    """
    Decorator to set a timeout (in seconds) for a test method.
    """
    def decorator(func):
        func.timeout = seconds
        return func
    return decorator

def retry(times):
    """
    Decorator to set the number of retry attempts for a failing test.
    """
    def decorator(func):
        func.retry = times
        return func
    return decorator

# --------------------------------------------------------------
# Plugin Architecture
# --------------------------------------------------------------
class Plugin:
    def before_test(self, test_name, test_class, method_name, parameters):
        pass

    def after_test(self, test_name, test_class, method_name, parameters, success, message, duration):
        pass

    def on_start_suite(self):
        pass

    def on_end_suite(self, summary):
        pass

# --------------------------------------------------------------
# TestCase Base Class (Enhanced with Fixture Injection)
# --------------------------------------------------------------
class TestCase:
    """
    Base class for test cases.
    Override:
      - setUp() and tearDown() for per-test initialization and cleanup.
      - Optionally, setUpClass() and tearDownClass() as classmethods for fixture management.
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assert_equal(self, a, b):
        if a != b:
            raise AssertionError(f"Expected {a} to equal {b}")

# --------------------------------------------------------------
# Auto-discovery Helpers
# --------------------------------------------------------------
# def discover_test_files(root):
#     """
#     Recursively discover all .py files in the directory whose names start with 'test_'.
#     """
#     test_files = []
#     for dirpath, _, filenames in os.walk(root):
#         for filename in filenames:
#             if filename.startswith("test_") and filename.endswith(".py"):
#                 test_files.append(os.path.join(dirpath, filename))
#     return test_files
# def discover_test_files(root):
    # test_files = []
    # for dirpath, _, filenames in os.walk(root):
    #     for filename in filenames:
    #         print(f"DEBUG: Checking file: {filename}")  # Debug print
    #         if filename.startswith("test_") and filename.endswith(".py"):
    #             full_path = os.path.join(dirpath, filename)
    #             print(f"DEBUG: Found test file: {full_path}")  # Debug print
    #             test_files.append(full_path)
    # return test_files

def discover_test_files(root):
    test_files = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            print(f"DEBUG: Checking file: {filename}")  # Debug print
            if filename.startswith("test_") and filename.endswith(".py"):
                full_path = os.path.join(dirpath, filename)
                print(f"DEBUG: Found test file: {full_path}")  # Debug print
                test_files.append(full_path)
    return test_files


def load_module_from_file(filepath):
    """
    Load a Python module from a given file path.
    """
    module_name = os.path.splitext(os.path.basename(filepath))[0]
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_test_classes_from_module(module):
    import inspect
    classes = []
    for name, obj in module.__dict__.items():
        if inspect.isclass(obj) and name != "TestCase" and name.startswith("Test"):
            if any(base.__name__ == "TestCase" for base in inspect.getmro(obj)):
                classes.append(obj)
    return classes


def discover_tests(path):
    """
    Discover all test classes that are subclasses of TestCase.
    'path' may be a directory, a .py file, or a module name.
    """
    test_classes = []
    if os.path.isdir(path):
        files = discover_test_files(path)
        if config.get('verbose', False):
            logger.debug(color_text(f"Discovered test files: {files}", CYAN))
        for f in files:
            try:
                mod = load_module_from_file(f)
                test_classes.extend(get_test_classes_from_module(mod))
            except Exception as e:
                if config['verbose']:
                    logger.error(color_text(f"Error loading {f}: {e}", RED))
    else:
        if path.endswith(".py"):
            try:
                mod = load_module_from_file(path)
                test_classes.extend(get_test_classes_from_module(mod))
            except Exception as e:
                if config.get('verbose', False):
                    logger.error(color_text(f"Error loading module from file {path}: {e}", RED))
        else:
            try:
                mod = importlib.import_module(path)
                test_classes.extend(get_test_classes_from_module(mod))
            except Exception as e:
                logger.error(color_text(f"Error importing module {path}: {e}", RED))
    return test_classes

# --------------------------------------------------------------
# Core test execution (with fixture injection, timeouts, retries, and async support)
# --------------------------------------------------------------
def run_test_method(test_class, method_name, param_data, retry_count):
    """
    Execute a single test method and return (success, message, duration)
    Supports dependency injection with fixtures if no param_data is provided.
    """
    attempts = 0
    last_error = ""
    start_time = time.time()
    while attempts <= retry_count:
        instance = test_class()  # fresh instance for each attempt
        try:
            instance.setUp()
            method = getattr(instance, method_name)
            # If parameterized data is provided, then use it and skip fixture injection.
            if param_data is not None:
                args, kwargs = param_data
            else:
                # Dependency Injection: Inspect the method's signature for fixture injection
                argspec = inspect.getfullargspec(method)
                if len(argspec.args) > 1:
                    injected = []
                    for fixture_name in argspec.args[1:]:
                        if fixture_name in FIXTURES:
                            info = FIXTURES[fixture_name]
                            if info["scope"] == "session":
                                if info.get("value") is None:
                                    if inspect.iscoroutinefunction(info["func"]):
                                        info["value"] = asyncio.run(info["func"]())
                                    else:
                                        info["value"] = info["func"]()
                                injected.append(info["value"])
                            else:  # function scope
                                if inspect.iscoroutinefunction(info["func"]):
                                    injected.append(asyncio.run(info["func"]()))
                                else:
                                    injected.append(info["func"]())
                        else:
                            raise Exception(f"Fixture '{fixture_name}' not found")
                    args, kwargs = tuple(injected), {}
                else:
                    args, kwargs = (), {}
            # Execute the test method (handle async methods appropriately)
            if inspect.iscoroutinefunction(method):
                asyncio.run(method(*args, **kwargs))
            else:
                method(*args, **kwargs)
            instance.tearDown()
            duration = time.time() - start_time
            return True, "", duration
        except Exception:
            last_error = traceback.format_exc()
            attempts += 1
            try:
                instance.tearDown()
            except Exception:
                pass
    duration = time.time() - start_time
    return False, f"Failed after {attempts} attempts: {last_error}", duration

def execute_task(test_class, method_name, param_data, timeout_val, retry_count):
    """
    Wrapper to execute a test method with an optional timeout.
    """
    if timeout_val is not None:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(run_test_method, test_class, method_name, param_data, retry_count)
            try:
                result = future.result(timeout=timeout_val)
                return result
            except concurrent.futures.TimeoutError:
                return False, f"Timeout after {timeout_val} seconds", timeout_val
    else:
        return run_test_method(test_class, method_name, param_data, retry_count)

# --------------------------------------------------------------
# TestSuite: Aggregates discovered test classes & runs all tests
# --------------------------------------------------------------
class TestSuite:
    def __init__(self, test_classes):
        self.test_classes = test_classes  # list of test class types
        self.results = []  # list of dict entries (one per test)
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.total_duration = 0

    def run(self):
        for plugin in PLUGINS:
            plugin.on_start_suite()
        max_workers = os.cpu_count() if config['parallel'] else 1
        # Choose executor: thread-based by default, or process-based if specified.
        if config['parallel'] and config['process']:
            executor = concurrent.futures.ProcessPoolExecutor(max_workers=max_workers)
        else:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        future_to_test = {}
        # Process each test class
        for test_class in self.test_classes:
            # Call class-level setup if defined
            if hasattr(test_class, "setUpClass") and callable(getattr(test_class, "setUpClass")):
                try:
                    test_class.setUpClass()
                except Exception as e:
                    logger.error(color_text(f"Error in setUpClass of {test_class.__name__}: {e}", RED))
            # Discover test methods (names starting with "test_")
            methods = [m for m in dir(test_class) if m.startswith("test_") and callable(getattr(test_class, m))]
            for m in methods:
                method_obj = getattr(test_class, m)
                # If marker filter is enabled, check for method markers.
                if config.get("markers"):
                    method_markers = getattr(method_obj, "markers", [])
                    # Only run test if it has at least one marker that matches the filter.
                    if not any(tag in config["markers"] for tag in method_markers):
                        continue
                param_list = getattr(method_obj, "parameters", None)
                timeout_val = getattr(method_obj, "timeout", None)
                retry_count = getattr(method_obj, "retry", 0)
                if param_list is not None:
                    for idx, params in enumerate(param_list):
                        # Support named parameter sets if provided as a dict.
                        if isinstance(params, tuple) and len(params) == 3:
                            args_tuple, kwargs_dict, name = params
                            test_name = f"{test_class.__name__}.{m}[{name if name is not None else idx}]"
                            new_params = (args_tuple, kwargs_dict)
                        else:
                            # Expecting params as tuple (args, kwargs)
                            test_name = f"{test_class.__name__}.{m}[{idx}]"
                            new_params = params
                        for plugin in PLUGINS:
                            plugin.before_test(test_name, test_class, m, new_params)
                        future = executor.submit(execute_task, test_class, m, new_params, timeout_val, retry_count)
                        future_to_test[future] = (test_name, test_class, m, new_params)
                        self.total += 1
                else:
                    test_name = f"{test_class.__name__}.{m}"
                    for plugin in PLUGINS:
                        plugin.before_test(test_name, test_class, m, None)
                    future = executor.submit(execute_task, test_class, m, None, timeout_val, retry_count)
                    future_to_test[future] = (test_name, test_class, m, None)
                    self.total += 1
            # Call class-level teardown if defined
            if hasattr(test_class, "tearDownClass") and callable(getattr(test_class, "tearDownClass")):
                try:
                    test_class.tearDownClass()
                except Exception as e:
                    logger.error(color_text(f"Error in tearDownClass of {test_class.__name__}: {e}", RED))
        # Collect and log results as tasks complete
        for future in concurrent.futures.as_completed(future_to_test):
            test_name, test_class, method_name, params = future_to_test[future]
            try:
                success, message, duration = future.result()
            except Exception as exc:
                success = False
                message = str(exc)
                duration = 0
            self.total_duration += duration
            if success:
                self.passed += 1
                display = color_text(f"✅ [PASS] {test_name} ({duration:.2f}s)", GREEN)
            else:
                self.failed += 1
                display = color_text(f"❌ [FAIL] {test_name} ({duration:.2f}s) - {message}", RED)
            self.results.append({
                "test": test_name,
                "success": success,
                "message": message,
                "duration": duration
            })
            print(display)
            for plugin in PLUGINS:
                plugin.after_test(test_name, test_class, method_name, params, success, message, duration)
        summary = {
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "duration": self.total_duration
        }
        for plugin in PLUGINS:
            plugin.on_end_suite(summary)
        summary_text = (
            f"\n🌟 Test Summary 🌟\n"
            f"🧪 Total: {self.total} | ✅ Passed: {self.passed} | ❌ Failed: {self.failed} | ⏱ Duration: {self.total_duration:.2f}s"
        )
        print(color_text(summary_text, CYAN))
        return summary

# --------------------------------------------------------------
# Advanced Reporting: JSON and HTML reports
# --------------------------------------------------------------
def generate_json_report(report_file, suite_summary, results):
    report = {
        "summary": suite_summary,
        "results": results
    }
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
    print(color_text(f"JSON report generated at {report_file}", MAGENTA))

def generate_html_report(report_file, suite_summary, results):
    html = "<html><head><title>vipentium Report</title></head><body>\n"
    html += "<h1>Test Summary</h1>\n"
    html += f"<p>Total: {suite_summary['total']}, Passed: {suite_summary['passed']}, Failed: {suite_summary['failed']}, Duration: {suite_summary['duration']:.2f}s</p>\n"
    html += "<h2>Test Details</h2>\n<table border='1' cellpadding='5'><tr><th>Test</th><th>Status</th><th>Duration(s)</th><th>Message</th></tr>\n"
    for r in results:
        status = "✅ PASS" if r["success"] else "❌ FAIL"
        row = f"<tr><td>{r['test']}</td><td>{status}</td><td>{r['duration']:.2f}</td><td>{r['message']}</td></tr>\n"
        html += row
    html += "</table></body></html>"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(color_text(f"HTML report generated at {report_file}", MAGENTA))

# --------------------------------------------------------------
# Main Runner: Parse arguments, initialize, discover tests, and run suite
# --------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="vipentium Test Runner - Comprehensive Python Testing Framework")
    parser.add_argument("path", help="Path to a test module, file, or directory containing tests")
    parser.add_argument("--parallel", action="store_true", help="Enable parallel test execution (thread-based by default)")
    parser.add_argument("--process", action="store_true", help="Use process-based parallelism (requires --parallel)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--report-json", type=str, default=None, help="Generate JSON report to specified file")
    parser.add_argument("--report-html", type=str, default=None, help="Generate HTML report to specified file")
    parser.add_argument("--coverage", action="store_true", help="Enable coverage integration (placeholder)")
    parser.add_argument("--mark", action="append", help="Only run tests that contain the specified marker. Can be used multiple times.")
    args = parser.parse_args()
    
    config['parallel'] = args.parallel
    config['process'] = args.process
    config['verbose'] = args.verbose
    config['report_json'] = args.report_json
    config['report_html'] = args.report_html
    config['coverage'] = args.coverage
    config['markers'] = args.mark if args.mark else None

    if config['coverage']:
        logger.info(color_text("Coverage integration is enabled (placeholder)", YELLOW))

    if config['verbose']:
        logger.info(color_text("Verbose mode enabled.", YELLOW))
    
    # Setup a loader spinner during initialization
    loader_start = time.time()
    spinner = ['|', '/', '-', '\\']
    spin_duration = 2  # seconds
    while time.time() - loader_start < spin_duration:
        for frame in spinner:
            if time.time() - loader_start >= spin_duration:
                break
            print(f"\r⌛ Initializing vipentium... {frame}", end='', flush=True)
            time.sleep(0.1)
    print("\r" + " " * 80, end="\r")
    print(color_text("🚀 Welcome to vipentium! Let's run the tests! 🚀\n", CYAN))
    
    # Discover tests automatically from the given path
    test_classes = discover_tests(args.path)
    if not test_classes:
        logger.error(color_text("No tests found.", RED))
        sys.exit(1)
    if config['verbose']:
        logger.info(color_text(f"Discovered {len(test_classes)} test classes.", YELLOW))
    
    suite = TestSuite(test_classes)
    summary = suite.run()

    # Generate reports if requested
    if config['report_json']:
        generate_json_report(config['report_json'], summary, suite.results)
    if config['report_html']:
        generate_html_report(config['report_html'], summary, suite.results)
    
    sys.exit(0 if summary['failed'] == 0 else 1)

if __name__ == "__main__":
    main()

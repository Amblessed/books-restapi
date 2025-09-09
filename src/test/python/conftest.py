import subprocess
import time
import pytest
import os, shutil, sys
import socket
import platform

# --- Configuration ---


# Pick the right executable name depending on OS
MVN_EXEC = "mvn.cmd" if platform.system() == "Windows" else "mvn"

MAVEN_HOME = os.environ.get("MVN_HOME", r"C:\apache-maven-3.9.5")  # default if not set
MAVEN_CMD = os.path.join(MAVEN_HOME, "bin", MVN_EXEC)
SPRING_BOOT_CMD = [MAVEN_CMD, "spring-boot:run"]
SERVER_PORT = 8080
BASE_URL = f"http://localhost:{SERVER_PORT}/api/v1/"
STARTUP_WAIT = 120  # seconds
POLL_INTERVAL = 1  # seconds
LOG_FILE = "springboot.log"
PROJECT_PATH = os.getcwd()
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
RESULTS_DIR = os.path.join(PROJECT_ROOT, "allure-results")
PATH_PROJECT=r"C:\Users\okeyb\Documents\Java\books"

def is_port_open(port, host="localhost"):
    """Check if a TCP port is open on a host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)  # quick timeout to avoid blocking
        try:
            sock.connect((host, port))
            return True
        except (ConnectionRefusedError, socket.timeout):
            return False

def wait_for_port(port, host="localhost", timeout=60, interval=0.5):
    """
    Wait until a TCP port is open or until timeout.

    Args:
        port (int): Port number to check.
        host (str): Hostname or IP.
        timeout (float): Maximum seconds to wait.
        interval (float): Seconds to wait between checks.

    Returns:
        True if port opens within timeout.

    Raises:
        TimeoutError: If port is not open within timeout.
    """
    start = time.time()
    while True:
        if is_port_open(port, host):
            return True
        elapsed = time.time() - start
        if elapsed >= timeout:
            raise TimeoutError(f"Server not available on {host}:{port} after {timeout}s")
        time.sleep(min(interval, timeout - elapsed))


@pytest.fixture(scope="session", autouse=True)
def spring_boot_server():

    """
    Start Spring Boot only if running locally.
    On CI (GitHub Actions), the server is started by the workflow.
    """
    if os.getenv("CI", "false").lower() == "true":
        print("CI environment detected — assuming Spring Boot is already running.")
        yield
        return

    # Start Spring Boot
    print("\nStarting Spring Boot server...")
    with open(LOG_FILE, "w") as log:
        process = subprocess.Popen(SPRING_BOOT_CMD, cwd=PATH_PROJECT, stdout=log, stderr=log)

    # Wait until server is up
    print(f"Waiting for Spring Boot to start on port {SERVER_PORT}...")
    wait_for_port(SERVER_PORT, timeout=STARTUP_WAIT)

    # Run tests
    yield

    # Teardown: stop Spring Boot
    print("\nStopping Spring Boot server...")
    if os.name == 'nt':  # Windows
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(process.pid)])
    else:  # Unix/Linux/Mac
        process.terminate()
    process.wait()


def run_command(cmd, description: str):
    """Run a subprocess command and print stdout/stderr."""
    print(description)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print("STDOUT:\n", result.stdout)
    if result.stderr:
        print("STDERR:\n", result.stderr)
    return result.returncode

def pytest_sessionstart(session):
    """Clean allure-results and create environment.properties before tests start."""

    # Clean previous results
    if os.path.exists(RESULTS_DIR):
        print("Cleaning old Allure results...")
        shutil.rmtree(RESULTS_DIR)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Create environment.properties
    env_file = os.path.join(RESULTS_DIR, "environment.properties")
    os_name = f"{platform.system()} {platform.release()}"
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    with open(env_file, "w") as f:
        f.write(f"OS={os_name}\n")
        f.write(f"Python={python_version}\n")
        f.write("Project=BooksApp\n")
        f.write(f"API_BASE_URL={BASE_URL}\n")

def pytest_sessionfinish(session, exitstatus):
    """After tests finish, generate and open Allure report automatically."""

    if os.getenv("CI", "false").lower() == "true":
        return

    report_dir = os.path.join(PROJECT_ROOT, "allure-report")
    allure_cmd = r"C:\allure\allure-2.35.1\bin\allure.bat"

    # Generate report
    generate_cmd = [allure_cmd, "generate", RESULTS_DIR, "--clean", "-o", report_dir]
    if run_command(generate_cmd, description="Generating Allure report...") != 0:
        print("Allure report generation failed!")
        return

    # Open report
    print("Opening Allure report in browser...")
    subprocess.Popen([allure_cmd, "open", report_dir])


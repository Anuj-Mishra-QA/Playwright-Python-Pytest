from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import subprocess
import sys
import os
import shutil


app = FastAPI(title="QA Automation Portal")


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

ALLURE_RESULT_DIR = os.path.join(
    REPORTS_DIR,
    "allure-result"
)

ALLURE_REPORT_DIR = os.path.join(
    REPORTS_DIR,
    "allure-report"
)


# ---------------------------------------------------------
# Test Status
# ---------------------------------------------------------

test_status = {
    "status": "Not Started",
    "output": "",
    "error": ""
}


# ---------------------------------------------------------
# Allure Report
# ---------------------------------------------------------

if os.path.exists(ALLURE_REPORT_DIR):

    app.mount(
        "/report",
        StaticFiles(
            directory=ALLURE_REPORT_DIR,
            html=True
        ),
        name="allure-report"
    )


# ---------------------------------------------------------
# Run Tests
# ---------------------------------------------------------

def run_tests():

    global test_status

    test_status["status"] = "Running"
    test_status["output"] = ""
    test_status["error"] = ""

    try:

        # ---------------------------------------------
        # Run existing Playwright test suite
        # ---------------------------------------------

        result = subprocess.run(
            [sys.executable, "run_all.py"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )

        test_status["output"] = result.stdout
        test_status["error"] = result.stderr


        # ---------------------------------------------
        # Generate Allure Report
        # ---------------------------------------------

        if result.returncode == 0:

            allure_executable = shutil.which("allure")

            if not allure_executable:

                test_status["status"] = "Failed"
                test_status["error"] = (
                    "Allure command was not found."
                )
                return


            allure_result = subprocess.run(
                [
                    allure_executable,
                    "generate",
                    ALLURE_RESULT_DIR,
                    "-o",
                    ALLURE_REPORT_DIR,
                    "--clean"
                ],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True
            )


            if allure_result.returncode == 0:

                test_status["status"] = "Completed"

            else:

                test_status["status"] = "Failed"

                test_status["error"] += (
                    "\n\nAllure Generation Error:\n"
                    + allure_result.stderr
                )

        else:

            test_status["status"] = "Failed"


    except Exception as e:

        test_status["status"] = "Failed"
        test_status["error"] = str(e)


# ---------------------------------------------------------
# Home Page
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>QA Automation Portal</title>

        <style>

            body {

                font-family: Arial, sans-serif;

                margin: 0;

                padding: 50px;

                background: #f5f5f5;

            }


            .container {

                max-width: 750px;

                margin: auto;

                background: white;

                padding: 40px;

                border-radius: 10px;

                box-shadow: 0 2px 10px rgba(0,0,0,0.1);

            }


            h1 {

                margin-bottom: 10px;

            }


            .project {

                font-size: 18px;

                margin-bottom: 30px;

            }


            button {

                padding: 12px 25px;

                font-size: 16px;

                cursor: pointer;

                border-radius: 5px;

                border: 1px solid #999;

            }


            button:disabled {

                cursor: not-allowed;

                opacity: 0.6;

            }


            #status {

                margin-top: 25px;

                font-size: 18px;

                font-weight: bold;

            }


            #report {

                display: none;

                margin-top: 25px;

            }


            .report-button {

                display: inline-block;

                padding: 12px 25px;

                background: #222;

                color: white;

                text-decoration: none;

                border-radius: 5px;

            }


            #error {

                margin-top: 20px;

                color: #b00020;

                white-space: pre-wrap;

            }

        </style>

    </head>


    <body>

        <div class="container">

            <h1>QA Automation Portal</h1>

            <div class="project">
                Project: Odoo Automation
            </div>


            <button
                id="runButton"
                onclick="runTests()">

                RUN TESTS

            </button>


            <div id="status">

                Status: Not Started

            </div>


            <div id="report">

                <a
                    href="/report"
                    target="_blank"
                    class="report-button">

                    VIEW ALLURE REPORT

                </a>

            </div>


            <div id="error"></div>

        </div>


        <script>

            async function runTests() {

                const button =
                    document.getElementById("runButton");

                const status =
                    document.getElementById("status");

                const report =
                    document.getElementById("report");

                const error =
                    document.getElementById("error");


                button.disabled = true;

                report.style.display = "none";

                error.innerText = "";


                status.innerText =
                    "Status: Starting Tests...";


                const response = await fetch(
                    "/run-tests",
                    {
                        method: "POST"
                    }
                );


                const data = await response.json();


                status.innerText =
                    "Status: " + data.status;


                checkStatus();

            }


            async function checkStatus() {

                const status =
                    document.getElementById("status");

                const button =
                    document.getElementById("runButton");

                const report =
                    document.getElementById("report");

                const error =
                    document.getElementById("error");


                const response =
                    await fetch("/status");


                const data =
                    await response.json();


                status.innerText =
                    "Status: " + data.status;


                if (data.status === "Running") {

                    setTimeout(
                        checkStatus,
                        2000
                    );

                    return;

                }


                button.disabled = false;


                if (data.status === "Completed") {

                    report.style.display = "block";

                }


                if (data.status === "Failed") {

                    error.innerText =
                        data.error || "Test execution failed.";

                }

            }

        </script>

    </body>

    </html>
    """


# ---------------------------------------------------------
# Start Test Execution
# ---------------------------------------------------------

@app.post("/run-tests")
def start_tests(background_tasks: BackgroundTasks):

    if test_status["status"] == "Running":

        return {
            "status": "Tests are already running"
        }


    background_tasks.add_task(run_tests)


    return {
        "status": "Running"
    }


# ---------------------------------------------------------
# Test Status
# ---------------------------------------------------------

@app.get("/status")
def get_status():

    return test_status


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "running"
    }
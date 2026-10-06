pipeline {

    agent any

    environment {
        PYTHONUNBUFFERED = '1'
        ENV = 'QA'
        BROWSER = 'chrome'
    }

    stages {

        stage('Verify Environment') {
            steps {
                bat '''
                    echo ==============================
                    echo Checking Environment
                    echo ==============================
                    python --version
                    python -m pip --version
                    git --version
                    allure --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    echo ==============================
                    echo Installing Python Dependencies
                    echo ==============================

                    python -m pip install --upgrade pip
                    python -m pip install pytest
                    python -m pip install playwright
                    python -m pip install allure-pytest
                    python -m pip install pytest-html
                    python -m pip install pytest-xdist

                    python -m playwright install
                '''
            }
        }

        stage('Run Automation Tests') {
            steps {
                bat '''
                    echo ==============================
                    echo Running Playwright Automation
                    echo ==============================

                    if exist reports\\allure-result (
                        rmdir /s /q reports\\allure-result
                    )

                    python -m pytest test ^
                        -v ^
                        -s ^
                        --alluredir=reports/allure-result ^
                        --clean-alluredir ^
                        --html=reports/report.html ^
                        --self-contained-html
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                bat '''
                    echo ==============================
                    echo Generating Allure Report
                    echo ==============================

                    if exist reports\\allure-report (
                        rmdir /s /q reports\\allure-report
                    )

                    allure generate reports/allure-result ^
                        -o reports/allure-report ^
                        --clean
                '''
            }
        }
    }

    post {

        always {
            echo 'Publishing test reports...'

            archiveArtifacts artifacts: 'reports/report.html', allowEmptyArchive: true
            archiveArtifacts artifacts: 'reports/screenshots/**/*', allowEmptyArchive: true

            allure(
                includeProperties: false,
                results: [
                    [path: 'reports/allure-result']
                ]
            )
        }

        success {
            echo 'Playwright automation completed successfully.'
        }

        failure {
            echo 'Playwright automation failed. Check the test and Allure reports.'
        }
    }
}
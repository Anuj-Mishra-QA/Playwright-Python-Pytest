pipeline {

    agent any

    environment {
        PYTHON = 'C:\\Users\\anuj.mishra\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
        GIT = 'C:\\Users\\anuj.mishra.BRAINVIRE\\AppData\\Local\\Programs\\Git\\cmd\\git.exe'

        ENV = 'QA'
        BROWSER = 'chrome'
        PYTHONUNBUFFERED = '1'
    }

    stages {

        stage('Verify Environment') {
            steps {
                bat '''
                    echo ==============================
                    echo Checking Environment
                    echo ==============================

                    "%PYTHON%" --version
                    "%PYTHON%" -m pip --version
                    "%GIT%" --version
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

                    "%PYTHON%" -m pip install --upgrade pip
                    "%PYTHON%" -m pip install pytest
                    "%PYTHON%" -m pip install playwright
                    "%PYTHON%" -m pip install allure-pytest
                    "%PYTHON%" -m pip install pytest-html
                    "%PYTHON%" -m pip install pytest-xdist

                    "%PYTHON%" -m playwright install
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

                    "%PYTHON%" -m pytest test ^
                        -v ^
                        -s ^
                        --alluredir=reports/allure-result ^
                        --clean-alluredir ^
                        --html=reports/report.html ^
                        --self-contained-html
                '''
            }
        }
    }

    post {

        always {
            echo 'Publishing test reports...'

            archiveArtifacts artifacts: 'reports/report.html', allowEmptyArchive: true

            archiveArtifacts artifacts: 'reports/screenshots/**/*', allowEmptyArchive: true

            script {
                if (fileExists('reports/allure-result')) {
                    allure(
                        includeProperties: false,
                        results: [
                            [path: 'reports/allure-result']
                        ]
                    )
                } else {
                    echo 'Allure results directory not found. Skipping Allure report.'
                }
            }
        }

        success {
            echo 'Playwright automation completed successfully.'
        }

        failure {
            echo 'Playwright automation failed. Check the console output and reports.'
        }
    }
}
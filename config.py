# URL = "https://edu-anujmishra.odoo.com/web/login"
#
import os
ENV = os.getenv("ENV", "QA")
BROWSER = os.getenv("BROWSER", "chrome")
# USERNAME = "anuj.mishra@brainvire.com"
# PASSWORD = "admin123"
URL = "https://edu-nilesh-brainvire.odoo.com/web/login"

# Credentials
USERNAME = "anuj.mishra@brainvire.com"
PASSWORD = "anuj.mishra@brainvire.com"

# Base URL (Automatically derived from login URL)
BASE_URL = URL.replace("/web/login", "")

# Browser Settings
BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = False
SLOW_MO = 500

# Video Recording
VIDEO = False
VIDEO_PATH = "reports/videos"
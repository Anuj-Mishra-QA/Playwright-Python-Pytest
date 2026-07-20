import pytest

pytest.main([
    "test",
    "-v",
    "--html=reports/report.html",
    "--self-contained-html"
])
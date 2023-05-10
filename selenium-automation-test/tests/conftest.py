from datetime import datetime
from pathlib import Path
import pytest
import pytest_html

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if not config.option.htmlpath:
        now = datetime.now()
        reports_dir = Path('../reports', now.strftime('%Y%m%d'))
        reports_dir.mkdir(parents=True, exist_ok=True)
        test_file_path = Path(config.option.file_or_dir[0])
        report_filename = f"{test_file_path.stem + '-' + now.strftime('%Y%m%d_%H%M%S')}_report.html"
        report_path = reports_dir / report_filename
        config.option.htmlpath = report_path
        config.option.self_contained_html = True
        config.option.html_show_steps = True
        
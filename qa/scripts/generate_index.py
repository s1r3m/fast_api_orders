from pathlib import Path

PROJECT_ROOT = Path().absolute().parent
REPORT_DIR = PROJECT_ROOT / 'reports'
INDEX_FILE = PROJECT_ROOT / 'index.html'


def main() -> None:
    if not REPORT_DIR.exists():
        print(f'{REPORT_DIR} directory does not exist. {PROJECT_ROOT=}')
        return

    reports = [file_obj.parts[-1] for file_obj in REPORT_DIR.iterdir() if file_obj.is_dir()]

    with INDEX_FILE.open('w') as f:
        f.write('<html><body><h1>Allure Reports</h1><ul>')
        for report in reports:
            f.write(f'<li><a href="reports/{report}/index.html">{report}</a></li>')
        f.write('</ul></body></html>')
    print(f'Index generated: {INDEX_FILE}')


if __name__ == '__main__':
    main()

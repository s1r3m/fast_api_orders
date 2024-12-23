from pathlib import Path

REPORT_DIR = Path().absolute().parent / 'reports'
INDEX_FILE = REPORT_DIR.parent / ('index.html')


def main() -> None:
    if not REPORT_DIR.exists():
        print(f'{REPORT_DIR.absolute()} directory does not exist.')
        return

    reports = [file_obj for file_obj in REPORT_DIR.iterdir() if file_obj.is_dir()]

    with INDEX_FILE.open('w') as f:
        f.write('<html><body><h1>Allure Reports</h1><ul>')
        for report in reports:
            f.write(f'<li><a href="{report}/index.html">{report}</a></li>')
        f.write('</ul></body></html>')
    print(f'Index generated: {INDEX_FILE}')


if __name__ == '__main__':
    main()

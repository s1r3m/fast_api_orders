from pathlib import Path

REPORT_DIR = Path() / 'reports'
INDEX_FILE = Path('index.html')

def main():
    if not REPORT_DIR.exists():
        print(f'{REPORT_DIR} directory does not exist.')
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

# Apache Camel Issue Report Crawler

## Running the program
This program uses the `requests` and `lxml.html` packages to download and parse the HTML of the issue reports. A virtual environment is included with these libraries. Ensure you have `pip` installed following the instructions [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

To activate the virtual environment, type the following command:
```bash
source env/bin/activate
```

To run the program, which by default scrapes the issue CAMEL-10597, run the following command.
```bash
python crawl_camel_issue_report.py
```

You can specify a specific issue to crawl with the `-i` flag, like so:
```bash
python crawl_camel_issue_report.py -i CAMEL-10600
```

If the extraction was successful, a CSV file will have been created in your working directory with the details of the Camel issue report.

To deactivate the virtual environment, type the following command:
```bash
deactivate
```
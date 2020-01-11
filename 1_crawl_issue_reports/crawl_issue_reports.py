import requests
import lxml.html as lhtml

def main():
    csv_headers = list()
    base_tree = get_html_tree()
    issue_details = scrape_issue_details(base_tree, csv_headers)


def get_html_tree():
    url = 'https://issues.apache.org/jira/browse/CAMEL-10597'
    response = requests.get(url)
    return lhtml.fromstring(response.content)

def scrape_issue_details(base_tree, headers):
    issue_details = dict()
    issue_details_list = base_tree.xpath('//*[@id="issuedetails"]')[0]
    for list_element in issue_details_list.iterchildren():
        name = list_element.xpath('.//*[contains(@class, "name")]')[0].text_content().strip()
        name = name.replace(':', '')
        name = name.replace(',', r'\,')
        name = name.replace(' ', '')
        value = list_element.xpath('.//*[contains(@class, "value")]')[0].text_content().strip()
        value = value.replace(',', r'\,')
        value = value.replace(' ', '')
        print('{} - {}'.format(name, value))
        headers.append(name)
        issue_details[name] = value
    return issue_details


if __name__ == '__main__':
    main()
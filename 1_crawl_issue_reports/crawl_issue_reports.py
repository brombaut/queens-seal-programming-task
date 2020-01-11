import requests
import lxml.html as lhtml
import datetime

def main():
    csv_headers = list()
    base_tree = get_html_tree()
    issue_details = scrape_issue_details(base_tree, csv_headers)
    people_details = scrape_people_details(base_tree, csv_headers)
    dates_details = scrape_dates_details(base_tree, csv_headers)
    all_issue_details = dict()
    all_issue_details.update(issue_details)
    all_issue_details.update(people_details)
    all_issue_details.update(dates_details)
    print(all_issue_details)


def get_html_tree():
    url = 'https://issues.apache.org/jira/browse/CAMEL-10597'
    response = requests.get(url)
    return lhtml.fromstring(response.content)


def scrape_issue_details(base_tree, headers):
    issue_details = dict()
    issue_details_list = base_tree.xpath('//*[@id="issuedetails"]')[0]
    for list_element in issue_details_list.iterchildren():
        name = get_name_attribute_from_list_element(list_element)
        value = get_value_attribute_from_list_element(list_element)
        print('{} - {}'.format(name, value))
        headers.append(name)
        issue_details[name] = value
    return issue_details


def get_name_attribute_from_list_element(list_element):
    name_el = list_element.xpath('.//*[contains(@class, "name")]')[0]
    name = get_cleaned_text(name_el)
    return name


def get_value_attribute_from_list_element(list_element):
    value_el = list_element.xpath('.//*[contains(@class, "value")]')[0]
    value = get_cleaned_text(value_el)
    return value


def scrape_people_details(base_tree, headers):
    people_details = dict()
    people_details_list = base_tree.xpath('//*[@id="peopledetails"]')[0]
    for list_element in people_details_list.iterchildren():
        for description_list in list_element.iterchildren():
            name_el = description_list.xpath('.//dt')[0]
            name = get_cleaned_text(name_el)
            value_el = description_list.xpath('.//dd')[0]
            value = get_cleaned_text(value_el)
            print('{} - {}'.format(name, value))
            headers.append(name)
            people_details[name] = value
    return people_details


def scrape_dates_details(base_tree, headers):
    dates_details = dict()
    dates_details_list = base_tree.xpath('//*[@id="datesmodule"]//ul[contains(@class, "item-details")]/li')[0]
    for description_list in dates_details_list:
        name_el = description_list.xpath('.//dt')[0]
        name = get_cleaned_text(name_el)
        value_el = description_list.xpath('.//dd//time')[0]
        value = value_el.get('datetime')
        print('{} - {}'.format(name, value))
        headers.append(name)
        dates_details[name] = value
        headers.append('{}_Epoch'.format(name))
        dates_details['{}_Epoch'.format(name)] = get_epoch_from_date_string(value)
        print('{}_Epoch - {}'.format(name, get_epoch_from_date_string(value)))
    return dates_details


def get_epoch_from_date_string(date_string):
    date_time_obj = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')
    return int(date_time_obj.timestamp())


def get_cleaned_text(html_el):
    text = html_el.text_content().strip()
    text = text.replace(':', '')
    text = text.replace(',', r'\,')
    text = ' '.join(text.split())
    return text

if __name__ == '__main__':
    main()
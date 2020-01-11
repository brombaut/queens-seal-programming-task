import requests
import lxml.html as lhtml
import datetime
import os
import sys
from lxml import etree


def main(ticket):
    print('Beginning data extraction for issue report {}...'.format(ticket))
    try:
        raw_document = get_raw_document(ticket)
        base_tree = parse_html_tree(raw_document)
        print('Extracting issue details from HTML tree...')
        all_issue_details = parse_all_issue_details(base_tree)
        write_issue_to_csv(ticket, all_issue_details)
        print('Sucess for {}'.format(ticket))
    except Exception as e:
        print('ERROR: Failed to complete crawl for {} - error={}'.format(ticket, e))


def get_raw_document(ticket):
    url = 'https://issues.apache.org/jira/browse/{}'.format(ticket)
    print("Downloading issue report from {}".format(url))
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"
        }
        response = requests.get(url, headers)
        return response.content
    except Exception as e:
        raise Exception('Request error: {}'.format(e))


def parse_html_tree(raw_docuemnt):
    print("Parsing Document Tree...")
    try:
        return lhtml.fromstring(raw_docuemnt)
    except Exception as e:
        raise Exception('Document parsing error: {}'.format(e))


def parse_all_issue_details(base_tree):
    issue_details = scrape_issue_details(base_tree)
    people_details = scrape_people_details(base_tree)
    dates_details = scrape_dates_details(base_tree)
    description_details = scrape_description_details(base_tree)
    comment_details = scrape_comment_details(base_tree)
    issue_summary = scrape_issue_summary(base_tree)
    all_issue_details = dict()
    all_issue_details.update(issue_details)
    all_issue_details.update(people_details)
    all_issue_details.update(dates_details)
    all_issue_details.update(description_details)
    all_issue_details.update(comment_details)
    all_issue_details.update(issue_summary)
    return all_issue_details


def scrape_issue_details(base_tree):
    try:
        issue_details = dict()
        issue_details_list = base_tree.xpath('//*[@id="issuedetails"]')[0]
        for list_element in issue_details_list.iterchildren():
            name = get_name_attribute_from_list_element(list_element)
            value = get_value_attribute_from_list_element(list_element)
            issue_details[name] = value
        return issue_details
    except Exception as e:
        raise Exception('Scrape issue details error: {}'.format(e))


def get_name_attribute_from_list_element(list_element):
    name_el = list_element.xpath('.//*[contains(@class, "name")]')[0]
    name = get_cleaned_text(name_el)
    return name


def get_value_attribute_from_list_element(list_element):
    value_el = list_element.xpath('.//*[contains(@class, "value")]')[0]
    value = get_cleaned_text(value_el)
    return value


def scrape_people_details(base_tree):
    try:
        people_details = dict()
        people_details_list = base_tree.xpath('//*[@id="peopledetails"]')[0]
        for list_element in people_details_list.iterchildren():
            for description_list in list_element.iterchildren():
                name_el = description_list.xpath('.//dt')[0]
                name = get_cleaned_text(name_el)
                value_el = description_list.xpath('.//dd')[0]
                value = get_cleaned_text(value_el)
                people_details[name] = value
        return people_details
    except Exception as e:
        raise Exception('Scrape people details error: {}'.format(e))


def scrape_dates_details(base_tree):
    try:
        dates_details = dict()
        dates_details_list = base_tree.xpath('//*[@id="datesmodule"]//ul[contains(@class, "item-details")]/li')[0]
        for description_list in dates_details_list:
            name_el = description_list.xpath('.//dt')[0]
            name = get_cleaned_text(name_el)
            value_el = description_list.xpath('.//dd//time')[0]
            value = value_el.get('datetime')
            dates_details[name] = value
            dates_details['{}_Epoch'.format(name)] = get_epoch_from_date_string(value)
        return dates_details
    except Exception as e:
        raise Exception('Scrape dates error: {}'.format(e))


def get_epoch_from_date_string(date_string):
    date_time_obj = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')
    return int(date_time_obj.timestamp())


def scrape_description_details(base_tree):
    try:
        description_details = dict()
        description_container_el_list = base_tree.xpath('//*[@id="descriptionmodule"]')
        if len(description_container_el_list) == 0:
            return {
                'Description': "NO DESCRIPTION"
            }
        description_container_el = description_container_el_list[0]
        description_name_el = description_container_el.xpath('.//*[@id="descriptionmodule_heading"]')[0]
        description_name = get_cleaned_text(description_name_el)
        descrption_value_el = description_container_el.xpath('.//*[@id="description-val"]')[0]
        description_value = get_cleaned_text(descrption_value_el)
        description_details[description_name] = description_value
        return description_details
    except Exception as e:
        print('Scrape description error: {}'.format(e))
        return {
            'Description': "ERROR: COULD NOT PARSE DESCRIPTION"
        }


def scrape_comment_details(base_tree):
    comment_details = dict()
    # NOTE: This function doesn't work. Just return en empty dict for now, and hopefully figure it out later
    # comments_tree = build_correct_comments_html_tree(base_tree)
    # all_comments = comments_tree.xpath('.//*[contains(@class, activity-comment)]')
    # for comment_el in all_comments:
    #     verbose_comment_el = comment_el.xpath('.//*[contains(@class, verbose)]')[0]
    #     comment_head = verbose_comment_el.xpath('.//*[contains(@class, action-head)]')
    #     print(comment_head.text_content())
    return comment_details


def build_correct_comments_html_tree(base_tree):
    '''
    TODO: Get this function working
    Since the html for the comments section is returned as a string in a variable in a 
    script tag, the raw string has to be found in the javascript, decoded so that special
    HTML characters are no longer encoded, and then passed into lxml to build the HTML tree.
    Currently, I am not sure if I am correctly decoding the string so that it can be parsed
    correctly. Additionally, all this code is commented out because it increases the 
    execution time of the program
    '''
    # script = base_tree.xpath('//script[contains(., "activity-panel-pipe-id")]/text()')[0]
    # search_string = '["activity-panel-pipe-id"]='
    # start_index = script.index(search_string)
    # comments_html = script[start_index + len(search_string):]
    # end_index = comments_html.index('";')
    # comments_html = comments_html[:end_index + 1]
    # comments_html = comments_html.encode('utf-8').decode('unicode-escape')
    # comments_tree = lhtml.fromstring(comments_html)
    # print(etree.tostring(comments_tree, pretty_print=True))
    # return comments_tree


def scrape_issue_summary(base_tree):
    try:
        issue_summary = dict()
        summary_container_el_list = base_tree.xpath('//*[@id="summary-val"]')
        if (len(summary_container_el_list) == 0):
            return {
                'Summary': "NO SUMMARY"
            }
        summary_container_el = summary_container_el_list[0]
        summary_value = get_cleaned_text(summary_container_el)
        issue_summary['Summary'] = summary_value
        return issue_summary
    except Exception as e:
        print('Scrape summary error: {}'.format(e))
        return {
            'Summary': "ERROR: COULD NOT PARSE SUMMARY"
        }


def get_cleaned_text(html_el):
    text = html_el.text_content().strip()  # Remove tab and newline characters
    text = text.replace(':', '')
    text = text.replace(',', ' ')  # Replace comma with space, as the comma character is the delimiter in the csv file
    text = ' '.join(text.split())  # Remove extra spaces
    return text


def write_issue_to_csv(ticket, details):
    try:
        headers_string = ''
        values_string = ''
        for key, value in details.items():
            headers_string += str(key)
            headers_string += ','
            values_string += str(value)
            values_string += ','
        headers_string = headers_string[:-1]  # Remove last trailing comma
        values_string = values_string[:-1]  # Remove last trailing comma
        lines = [
            headers_string,
            values_string
        ]
        file_name = '{}.csv'.format(ticket)
        full_file_path = ''
        with open(file_name, 'w') as f: 
            f.write('\n'.join(lines))
            full_file_path = os.path.realpath(f.name)
        print('Issue report details for {} have been written to {}'.format(ticket, full_file_path))
    except Exception as e:
        raise Exception('Writing file error: {}'.format(e))


if __name__ == '__main__':
    ticket = 'CAMEL-10597'
    if len(sys.argv) > 1:
        if sys.argv[1] == '-i' and len(sys.argv) == 3:
            ticket = sys.argv[2]
    main(ticket)
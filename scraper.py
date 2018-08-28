from HTMLParser import HTMLParser
import urllib
import argparse
import sys
import re


class MyHTMLParser(HTMLParser):
    def __init__(self):
        # HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for i in attrs:
                if i[0] == 'src':
                    self.links.append(i[1])
        
        if tag == 'a':
            for i in attrs:
                if i[0] == 'href':
                    self.links.append(i[1])

        return

def get_emails(content):
    email_add = re.findall(r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+'''
                           r'''(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*'''
                           r'|"(?:[\x01-\x08\x0b\x0c\x0e-'
                           r'\x1f\x21\x23-\x5b\x5d-\x7f]'
                           r'|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@'
                           r'(?:(?:[a-z0-9]'
                           r'(?:[a-z0-9-]*[a-z0-9])?\.)'
                           r'+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?'
                           r'|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.)'
                           r'{3}(?:25[0-5]|2[0-4][0-9]'
                           r'|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:'
                           r'(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]'
                           r'|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])', content)
    email_add = list(set(email_add))
    print '\nEmails'
    for email in email_add:
        print email
    return

def get_phone(content):
    phone_nums = re.findall(r'1?\W*([2-9][0-8][0-9])'
                            r'\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?',
                            content)
    phone_nums = list(set(phone_nums))
    print '\nPhone Numbers'
    for phone in phone_nums:
        fin_phone = '-'.join(phone[0:3])
        print fin_phone

    return


def get_urls(content):
    print 'Urls'

    parser = MyHTMLParser()

    parser.reset()
    parser.feed(content)

    link_list = list(set(parser.links))
    for link in link_list:
        print link

    return


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url destination to extract data from")

    return parser

def extract_html(url):
    html_page = urllib.urlopen(url)
    content = html_page.read()

    get_urls(content)

    get_phone(content)

    get_emails(content)

    return content


def main(args):
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)
    content = extract_html(parsed_args.url)


if __name__ == "__main__":
    main(sys.argv[1:])



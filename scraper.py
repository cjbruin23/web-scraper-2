import argparse
import requests
import re
import sys


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
    pass


def get_phone(content):
    phone_nums = re.findall(r'1?\W*([2-9][0-8][0-9])'
                            r'\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?',
                            content)
    phone_nums = list(set(phone_nums))
    print '\nPhone Numbers'
    for phone in phone_nums:
        fin_phone = '-'.join(phone[0:3])
        print fin_phone

    pass


def get_urls(content):
    print 'Urls'
    link_matches = re.findall(r'http[s]?://(?:[a-zA-Z]'
                              r'|[0-9]|[$-_@.&+]|[!*\(\),]'
                              r'|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
    link_matches = list(set(link_matches))
    for link in link_matches:
        print link

    pass


def extract_html(url):
    req = requests.get(url)
    content = req.content

    get_urls(content)

    get_phone(content)

    get_emails(content)
    return


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url destination to extract data from")

    return parser


def main(args):
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)
    extract_html(parsed_args.url)


if __name__ == "__main__":
    main(sys.argv[1:])

# -*- coding: utf-8 -*-

# Handles user interaction with maicroft program. User passes their
# Reddit/Twitter username and program attempts to find a matching account.
from __future__ import print_function
import argparse
from builtins import input
import json
import logging
import sys
import datetime

from maicroft.users.reddit_user import RedditUser
from maicroft.users.twitter_user import TwitterUser
from maicroft.maicroft_exceptions import NoDataError, UserNotFoundError


def setup_logging(debug=False, logging_level=None):
    # create logger
    logger = logging.getLogger('maicroft')

    if not debug and not logging_level:
        logger.addHandler(logging.NullHandler())
        return logger

    if debug or logging_level == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif logging_level == "WARN":
        logger.setLevel(logging.WARN)
    elif logging_level == "INFO":
        logger.setLevel(logging.INFO)
    elif logging_level == "ERROR":
        logger.setLevel(logging.ERROR)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger


def run_menu():
    ans = 0
    while ans != "2":
        print("""
            1. Process a Reddit user
            2. Process a Twitter user
            3. Exit
        """)
        ans = input("Enter Choice: ")
        process_menu_choice(int(ans))


def process_menu_choice(choice):
    if choice == 1:
        username = input("Enter a reddit username: ")
        process_social_user(username)
    elif choice == 2:
        username = input("Enter a twitter id/screen-name")
        process_social_user(username, platform="twitter")
    elif choice == 3:
        sys.exit()
    else:
        print("invalid input. please try again")


def process_social_user(username, platform="Reddit", prettyprint=False):
    u = None
    print("Processing " + platform + " user: %s" % username)
    start = datetime.datetime.now()
    try:
        if platform.lower() == "reddit":
            u = RedditUser(username)
        elif platform.lower() == "twitter":
            u = TwitterUser(username)
        else:
            print("Invalid platform specified.")
            exit(1)

        if prettyprint:
            print(json.dumps(u, indent=4))
        else:
            print(u)
    except UserNotFoundError:
        print("User %s not found" % sys.argv[1])
    except NoDataError:
        print("No data available for user %s" % sys.argv[1])

    print("Processing complete... %s" % (datetime.datetime.now() - start))
    return u


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('platform', type=str,
                        help='which social platform the account is attached to (Reddit or Twitter)')
    parser.add_argument('username', type=str,
                        help='the account id')
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='output debugging logs from program')
    parser.add_argument('--prettyprint', dest='prettyprint', action='store_true',
                        help='output json is prettyprint (default: False)')
    parser.add_argument('--logging-level',
                        dest='logging_level',
                        type=str,
                        choices=set(["DEBUG", "INFO", "WARN", "ERROR"]),
                        default=None,
                        help='set the logging level for the program. one of {DEBUG, INFO, WARN, ERROR}')

    parser.set_defaults(prettyprint=False, debug=False)
    if len(sys.argv) == 1:
        run_menu()
    else:
        args = parser.parse_args()

    if (args.platform and not args.username) or (not args.platform and args.username):
        sys.exit("Usage: python <program> <SOCIAL PLATFORM> <USERNAME> [--prettyprint]")
    else:
        plat = args.platform
        username = args.username

    logger = setup_logging(args.debug, args.logging_level)

    process_social_user(username, platform=plat, prettyprint=args.prettyprint)


if __name__ == '__main__':
    main()

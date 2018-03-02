# -*- coding: utf-8 -*-

# Handles user interaction with maicroft program. User passes their
# Reddit/Twitter username and program attempts to find a matching account.
from __future__ import print_function
import argparse
from builtins import input
import json
import sys
import datetime

from maicroft.users.reddit_user import RedditUser
from maicroft.users.twitter_user import TwitterUser
from maicroft.maicroft_exceptions import NoDataError, UserNotFoundError


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

    process_social_user(username, platform=plat, prettyprint=args.prettyprint)


if __name__ == '__main__':
    main()

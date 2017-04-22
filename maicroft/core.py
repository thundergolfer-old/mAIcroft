# -*- coding: utf-8 -*-

# Handles user interaction with sherlock program. User passes their reddit username
# and program attempts to find a reddit matching it.
from __future__ import print_function
import sys
import datetime
import getopt

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
        ans = raw_input("Enter Choice: ")
        process_menu_choice(int(ans))

def process_menu_choice( choice ):
    if choice == 1:
        username = raw_input("Enter a reddit username: ")
        process_social_user(username)
    elif choice == 2:
        username = raw_input("Enter a twitter id/screen-name")
        process_social_user(username, platform="twitter")
    elif choice == 3:
        sys.exit()
    else:
        print("invalid input. please try again")

def process_social_user( username, platform="Reddit", prettyprint=False ):
    u = None
    print("Processing " + platform + " user: %s" % username)
    start = datetime.datetime.now()
    try:
        if platform.lower() == "reddit": u = RedditUser(username)
        elif platform.lower() == "twitter": u = TwitterUser(username)
        else: print("Invalid platform specified.")

        if prettyprint: print(json.dumps(u, indent=4))
        else:           print(u)
    except UserNotFoundError:
        print("User %s not found" % sys.argv[1])
    except NoDataError:
        print("No data available for user %s" % sys.argv[1])

    print("Processing complete... %s" % (datetime.datetime.now() - start))
    return u

def main():
    prettyPrint = False
    if len(sys.argv) > 2:
        plat = sys.argv[1]
        username = sys.argv[2]
    elif len(sys.argv) == 4 and sys.argv[3] == 'prettyprint':
        prettyPrint = True
    elif len(sys.argv) == 1:
        run_menu()
    else:
        sys.exit("Incorrect number of arguments\nUsage: python <program> <SOCIAL PLATFORM> <USERNAME>")
    process_social_user( username, platform=plat, prettyprint=prettyPrint)

if __name__ == '__main__':
    main()

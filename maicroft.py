# -*- coding: utf-8 -*-

# Handles user interaction with sherlock program. User passes their reddit username
# and program attempts to find a reddit matching it.

import sys
import datetime
import getopt

from reddit_user import RedditUser, UserNotFoundError, NoDataError

def runMenu():
    ans = 0
    while ans != "2":
        print ("""
            1. Process a Reddit user
            2. Exit
        """)
        ans = raw_input("Enter Choice: ")
        processMenuChoice(int(ans))

def processMenuChoice( choice ):
    if choice == 1:
        username = raw_input("Enter a reddit username: ")
        processRedditUser(username)
    elif choice == 2:
        sys.exit()

def processRedditUser( username ):
    u = None
    print "Processing user %s" % username
    start = datetime.datetime.now()
    try:
        u = RedditUser(username)
        print u
    except UserNotFoundError:
        print "User %s not found" % sys.argv[1]
    except NoDataError:
        print "No data available for user %s" % sys.argv[1]

    print "Processing complete... %s" % (datetime.datetime.now() - start)
    return u

def main():
    if len(sys.argv) > 1:
        username = sys.argv[1]
    elif len(sys.argv) == 1:
        runMenu()
    else:
        sys.exit("Incorrect number of arguments")
    processRedditUser( username )

if __name__ == '__main__':
    main()

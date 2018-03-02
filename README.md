<p align="center">
  <img src="images/text_logo_400.png">
</p>

# mAIcroft [![Build Status](https://travis-ci.org/thundergolfer/mAIcroft.svg?branch=master)](https://travis-ci.org/thundergolfer/mAIcroft) [![Code Climate](https://codeclimate.com/github/thundergolfer/mAIcroft/badges/gpa.svg)](https://codeclimate.com/github/thundergolfer/mAIcroft) [![Test Coverage](https://codeclimate.com/github/thundergolfer/mAIcroft/badges/coverage.svg)](https://codeclimate.com/github/thundergolfer/mAIcroft/coverage)

Extract interesting information about redditors from their submissions, comments, and subs. Outputs data in JSON format. Brother project to [Orionmelt's Sherlock](https://github.com/orionmelt/sherlock), adapting and expanding its functionality and generality.

[Documentation - Read The Docs](http://maicroft.readthedocs.io/en/latest/) [In Progress]
-------------------

### Currently working on:
*Detecting anti-social users by measuring their number of insulting comments. User comments are classified with machine learning as neutral [0] or insulting [1].* In progress at [thundergolfer/insults](https://github.com/thundergolfer/insults)

Dependencies
------------
* [requests](http://docs.python-requests.org/en/master/)
* [pytz](https://pypi.python.org/pypi/pytz/)
* [TextBlob 0.9.0](http://textblob.readthedocs.org/en/dev/)

Setup
-----
* Run `pip install -r requirements.txt` to install dependencies.
* Run `python -m textblob.download_corpora` to download TextBlob corpora.

Usage
-----
    python -m maicroft.core <social-platform (reddit|twitter)> <username> [--prettyprint] [--debug]

Example
-------
Command:

    python -m maicroft.core reddit thundergolfer

Output (truncated in parts for brevity):
```

Processing user thundergolfer
{
  "username": "thundergolfer",
  "summary": {
    "first_post_date": 1407428328,
    "submissions": {
      "count": 15,
      "gilded": 0,
      "average_karma": 63,
      "computed_karma": 1832,
      "type_domain_breakdown": {
        "name": "All",
        "children": [
          {
            "name": "Self",
            "children": [
              {
                "name": "TheoryOfReddit",
                "size": 1
              },
              ....
            ]
          },
        ]
      },
      "worst": {
        "permalink": "http:\/\/www.reddit.com\/r\/sandbox\/comments\/3ej437rl\/test_post_please_ignore\/",
        "title": "Test post, please ignore"
      },
      "best": { ... },
      "all_time_karma": 1070
    },
    "signup_date": 1404973258,
    "comments": {
      "worst": {
        "text": "fake worst comment ayylamo. :)",
        "permalink": "http:\/\/www.reddit.com\/r\/thedeathlyhallows\/comments\/46xd0w\/_\/d0bb25n"
      },
      "best": { ... },
      "average_karma": 3,
      "count": 431,
      "gilded": 1,
      "hours_typed": 5.98,
      "unique_word_count": 1963,
      "total_word_count": 14344,
      "karma_per_word": 0.09
    },
  },
  "metrics": { ... },
    "recent_karma": [0,1,22,0,...,0],
    "weekday": [ ... ],
    "hour": [ ... ],
    "recent_activity_heatmap": "000100...1010",
    "date": [
      {
        "submission_karma": 0,
        "posts": 1,
        "comments": 1,
        "comment_karma": 1,
        "karma": 1,
        "date": "2014-07-01",
        "submissions": 0
      },
      {
        "submission_karma": 4,
        "posts": 12,
        "comments": 11,
        "comment_karma": 16,
        "karma": 20,
        "date": "2014-08-01",
        "submissions": 1
      },
      ...
    ],
    "common_words": [
      {
        "text": "feedback",
        "size": 76
      },
      {
        "text": "data",
        "size": 58
      },
      ...
    ],
    "recent_posts": [],
    "subreddit": { ... }
  },
  "synopsis": {
    "television": {
      "data": [
        {
          "count": 3,
          "value": "psych"
        }
      ]
    },
    "lifestyle": {
      "data": [
        {
          "count": 36,
          "value": "gifts and charity"
        },
        {
          "count": 7,
          "value": "self-help and motivation"
        },
        {
          "count": 6,
          "value": "relationships"
        }
      ]
    },
    "possessions": {
      "data_extra": [
        {
          "count": 12,
          "sources": [
            "http:\/\/www.reddit.com\/r\/funny\/comments\/3gd7to\/_\/ctx75ih",
            ...
          ],
          "value": "site"
        },
        ...
      ]
    },
    "business": {
      "data": [
        {
          "count": 36,
          "value": "entrepreneurship"
        }
      ]
    },
    "books": {
      "data": [
        {
          "count": 3,
          "value": "harry potter"
        }
      ]
    },
    "favorites": {
      "data": [
        {
          "count": 1,
          "sources": [
            "http:\/\/www.reddit.com\/r\/misc\/comments\/2qzz64\/_\/cnbbvee"
          ],
          "value": "redditinvestigator"
        },
        ...
      ]
    },
    "attributes": {
      "data": [
        {
          "count": 3,
          "sources": [
            "http:\/\/www.reddit.com\/r\/UsefulWebsites\/comments\/328vgb\/_\/cq9edg0",
            "http:\/\/www.reddit.com\/r\/InternetIsBeautiful\/comments\/2wstiw\/_\/cou7p6f",
            "http:\/\/www.reddit.com\/r\/programming\/comments\/2qx5ij\/_\/cnaueqc"
          ],
          "value": "winner"
        },
        ...
        {
          "count": 1,
          "sources": [
            "http:\/\/www.reddit.com\/r\/snoovatars\/comments\/2xr0dy\/i_created_an_api_to_get_your_snoovatar_as_a_png\/"
          ],
          "value": "creator"
        }
      ]
    },
    "technology": {
      "data": [
        {
          "count": 127,
          "value": "internet"
        },
        ...
      ]
    }
  },
  "version": 8,
  "metadata": {
    "latest_submission_id": "4263aj",
    "latest_comment_id": "d0bb25n",
    "reddit_id": "hc427"
  }
}
Processing complete... 0:00:06.084066
```

License
-------
[LICENSE.txt](/LICENSE.txt) MIT License

The MIT License (MIT)
Copyright (c) 2016

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

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

Output:
```

Processing user thundergolfer
{
  "username": "thundergolfer",
  "summary": {
    "first_post_date": 1407428328,
    "submissions": {
      "count": 15,
      "gilded": 0,
      "worst": {
        "permalink": "http:\/\/www.reddit.com\/r\/sandbox\/comments\/3ej437rl\/test_post_please_ignore\/",
        "title": "Test post, please ignore"
      },
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
          {
            "name": "Image",
            "children": [

            ]
          },
          {
            "name": "Video",
            "children": [

            ]
          },
          {
            "name": "Other",
            "children": [
              {
                "name": "snoopsnoo.com",
                "size": 7
              },
              {
                "name": "triviusgame.com",
                "size": 1
              },
              {
                "name": "blog.snoopsnoo.com",
                "size": 5
              }
            ]
          }
        ]
      },
      "best": {
        "permalink": "http:\/\/www.reddit.com\/r\/dataisbeautiful\/comments\/2r3jnk\/your_reddit_activity_analyzed_and_visualized_oc\/",
        "title": "Your reddit activity, analyzed and visualized [OC]"
      },
      "all_time_karma": 1070
    },
    "signup_date": 1404973258,
    "comments": {
      "worst": {
        "text": "Just refreshed your SnoopSnoo profile, and it looks like it is now caught up with most of what you mentioned. :)",
        "permalink": "http:\/\/www.reddit.com\/r\/dataisbeautiful\/comments\/46xd0w\/_\/d0bb25n"
      },
      "average_karma": 3,
      "best": {
        "text": "I built this site and posted on \/r\/dataisbeautiful and someone suggested that I crosspost it here. Feedback and criticism are welcome!",
        "permalink": "http:\/\/www.reddit.com\/r\/secretsanta\/comments\/2r7xhr\/_\/cnd9lyd"
      },
      "count": 431,
      "gilded": 1,
      "hours_typed": 5.98,
      "unique_word_count": 1963,
      "total_word_count": 14344,
      "karma_per_word": 0.09
    },
    "lurk_period": {
      "to": 1428638447,
      "from": 1426913740
    }
  },
  "metrics": {
    "topic": {
      "name": "All",
      "children": [
        {
          "name": "Technology",
          "children": [
            {
              "name": "Internet",
              "children": [
                {
                  "name": "Generic",
                  "size": 129
                }
              ]
            },
            {
              "name": "Data",
              "children": [
                {
                  "name": "Data Visualization",
                  "size": 37
                }
              ]
            },
            {
              "name": "Programming",
              "children": [
                {
                  "name": "Python",
                  "size": 28
                },
                {
                  "name": "Generic",
                  "size": 11
                },
                {
                  "name": "Web Development",
                  "size": 2
                }
              ]
            },
            {
              "name": "Software",
              "children": [
                {
                  "name": "Chrome",
                  "size": 2
                }
              ]
            }
          ]
        },
        {
          "name": "Other",
          "size": 49
        },
        {
          "name": "Lifestyle",
          "children": [
            {
              "name": "Gifts and Charity",
              "children": [
                {
                  "name": "Generic",
                  "size": 37
                }
              ]
            },
            {
              "name": "Self-help and Motivation",
              "children": [
                {
                  "name": "Generic",
                  "size": 7
                }
              ]
            },
            {
              "name": "Relationships",
              "children": [
                {
                  "name": "Generic",
                  "size": 6
                }
              ]
            }
          ]
        },
        {
          "name": "News and Politics",
          "children": [
            {
              "name": "Generic",
              "children": [
                {
                  "name": "Generic",
                  "size": 3
                }
              ]
            },
            {
              "name": "World News",
              "children": [
                {
                  "name": "Generic",
                  "size": 2
                }
              ]
            }
          ]
        },
        {
          "name": "Entertainment",
          "children": [
            {
              "name": "Television",
              "children": [
                {
                  "name": "Psych",
                  "size": 3
                },
                {
                  "name": "Seinfeld",
                  "size": 2
                },
                {
                  "name": "British TV",
                  "size": 1
                }
              ]
            },
          ]
        },
        {
          "name": "Locations",
          "children": [
            {
              "name": "World",
              "children": [
                {
                  "name": "Singapore",
                  "size": 1
                }
              ]
            }
          ]
        },
        {
          "name": "Sports",
          "children": [
            {
              "name": "Hockey",
              "children": [
                {
                  "name": "New Jersey Devils",
                  "size": 1
                }
              ]
            }
          ]
        }
      ]
    },
    "recent_karma": [0,1,22,0,...,0],
    "weekday": [
      {
        "submission_karma": 28,
        "posts": 103,
        "comments": 99,
        "comment_karma": 229,
        "weekday": "Sun",
        "submissions": 4,
        "karma": 257
      },
      ...
      {
        "submission_karma": 6,
        "posts": 56,
        "comments": 54,
        "comment_karma": 171,
        "weekday": "Sat",
        "submissions": 2,
        "karma": 177
      }
    ],
    "hour": [
      {
        "submission_karma": 0,
        "hour": 0,
        "posts": 24,
        "comments": 24,
        "comment_karma": 96,
        "karma": 96,
        "submissions": 0
      },
      ...
      {
        "submission_karma": 3,
        "hour": 23,
        "posts": 24,
        "comments": 23,
        "comment_karma": 54,
        "karma": 57,
        "submissions": 1
      }
    ],
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

        "size": 17
      },
      ...
    ],
    "recent_posts": [],
    "subreddit": {
      "name": "All",
      "children": [
        {
          "name": "Gaming",
          "children": [
            {
              "submission_karma": 0,
              "name": "IndieGaming",
              "posts": 1,
              "comments": 1,
              "comment_karma": 1,
              "karma": 1,
              "submissions": 0
            },
            ...
            {
              "submission_karma": 1,
              "name": "DestinyTheGame",
              "posts": 1,
              "comments": 0,
              "comment_karma": 0,
              "karma": 1,
              "submissions": 1
            }
          ]
        },
        {
          "name": "Lifestyle",
          "children": [
            {
              "submission_karma": 0,
              "name": "Mydaily3",
              "posts": 7,
              "comments": 7,
              "comment_karma": 14,
              "karma": 14,
              "submissions": 0
            },
            ...
            {
              "submission_karma": 1,
              "name": "Favors",
              "posts": 1,
              "comments": 0,
              "comment_karma": 0,
              "karma": 1,
              "submissions": 1
            }
          ]
        },
        ...
        {
          "name": "Entertainment",
          "children": [
            {
              "submission_karma": 179,
              "name": "harrypotter",
              "posts": 3,
              "comments": 2,
              "comment_karma": 8,
              "karma": 187,
              "submissions": 1
            },
            ...
            {
              "submission_karma": 7,
              "name": "blackmirror",
              "posts": 1,
              "comments": 0,
              "comment_karma": 0,
              "karma": 7,
              "submissions": 1
            }
          ]
        },
      ]
    }
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
        {
          "count": 11,
          "sources": [
            "http:\/\/www.reddit.com\/r\/InternetIsBeautiful\/comments\/33fepc\/_\/cqkjp9g",
            "http:\/\/www.reddit.com\/r\/AdviceAnimals\/comments\/30hxhr\/_\/cpt4b4l",
            ...
          ],
          "value": "program"
        },
        {
          "count": 1,
          "sources": [
            "http:\/\/www.reddit.com\/r\/SnoopSnoo\/comments\/3yp4n8\/_\/cyfhqw7"
          ],
          "value": "cc"
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
        {
          "count": 1,
          "sources": [
            "http:\/\/www.reddit.com\/r\/EVEX\/comments\/2ztguf\/_\/cpr5v4c"
          ],
          "value": "web development"
        }
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
          "value": "developer of this site"
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

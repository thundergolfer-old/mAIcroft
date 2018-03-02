"""
Activity Metrics Processing File
--------------------------------
'Activity Metrics' are metrics related to the amount of interactions a user
has with a social network platform, and also the characteristics of those
interactions (frequency, long-form, seasonal, recreation-vs-professional etc..)

Some of these metrics are unrelated to the focus of this project, which is to
understand the personality, goals, and beliefs of a user. Some of these metrics
are vaguely related.

They are kept separately from the 'core' of the project here in this file.
"""

import datetime
import pytz


def process_metrics(user, comment):
    """
    Process the part of a comment that relates to metrics.
    """

    comment_timestamp = datetime.datetime.fromtimestamp(
        comment.created_utc, tz=pytz.utc
    )

    user.commented_dates.append(comment_timestamp)
    user.comments_gilded += comment.gilded

    days_ago_60 = user.today - datetime.timedelta(60)
    if (comment_timestamp.date() - days_ago_60).days > 0:
        user.metrics["heatmap"][
            (comment_timestamp.date() - days_ago_60).days*24 +
            comment_timestamp.hour
        ] += 1
        user.metrics["recent_karma"][
            (comment_timestamp.date() - days_ago_60).days
        ] += comment.score
        user.metrics["recent_posts"][
            (comment_timestamp.date() - days_ago_60).days
        ] += 1

    # Update metrics
    for i, d in enumerate(user.metrics["date"]):
        if d["date"] == (
            comment_timestamp.date().year,
            comment_timestamp.date().month
        ):
            d["comments"] += 1
            d["comment_karma"] += comment.score
            user.metrics["date"][i] = d
            break

    for i, h in enumerate(user.metrics["hour"]):
        if h["hour"] == comment_timestamp.hour:
            h["comments"] += 1
            h["comment_karma"] += comment.score
            user.metrics["hour"][i] = h
            break

    for i, w in enumerate(user.metrics["weekday"]):
        if w["weekday"] == comment_timestamp.date().weekday():
            w["comments"] += 1
            w["comment_karma"] += comment.score
            user.metrics["weekday"][i] = w
            break

    if comment.score > user.best_comment.score:
        user.best_comment = comment
    elif comment.score < user.worst_comment.score:
        user.worst_comment = comment


def process_submission_metrics(user, submission):
    """
    Process the part of a submission that relates to metrics
    """
    submission_timestamp = datetime.datetime.fromtimestamp(
        submission.created_utc, tz=pytz.utc
    )

    user.submitted_dates.append(submission_timestamp)
    user.submissions_gilded += submission.gilded
    if submission.score > user.best_submission.score:
        user.best_submission = submission
    elif submission.score < user.worst_submission.score:
        user.worst_submission = submission

    days_ago_60 = user.today - datetime.timedelta(60)
    if (submission_timestamp.date() - days_ago_60).days > 0:
        user.metrics["heatmap"][
            ((submission_timestamp.date() - days_ago_60).days-1) * 24 + submission_timestamp.hour
        ] += 1
        user.metrics["recent_karma"][
            (submission_timestamp.date() - days_ago_60).days
        ] += submission.score
        user.metrics["recent_posts"][
            (submission_timestamp.date() - days_ago_60).days
        ] += 1

    for i, d in enumerate(user.metrics["date"]):
        if d["date"] == (
            submission_timestamp.date().year,
            submission_timestamp.date().month
        ):
            d["submissions"] += 1
            d["submission_karma"] += submission.score
            user.metrics["date"][i] = d
            break

    for i, h in enumerate(user.metrics["hour"]):
        if h["hour"] == submission_timestamp.hour:
            h["submissions"] += 1
            h["submission_karma"] += submission.score
            user.metrics["hour"][i] = h
            break

    for i, w in enumerate(user.metrics["weekday"]):
        if w["weekday"] == submission_timestamp.date().weekday():
            w["submissions"] += 1
            w["submission_karma"] += submission.score
            user.metrics["weekday"][i] = w
            break

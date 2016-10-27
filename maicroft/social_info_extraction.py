import datetime
import urlparse
import pytz
import calendar

from maicroft.reddit_user import Util
from maicroft.activity_metric_proc import process_metrics, process_submission_metrics

"""
Generalising the information extraction processing of social media content.
Currently only Reddit social content is supported, but we want the code to be
reusable for other major social media content eg. Twitter, Facebook, LinkedIn...
"""

parser = TextParser()

def antisocial_rating( user ):
    raise NotImplementedError

def insult_or_not( user, comment ):
    raise NotImplementedError

def process_comment(user, comment):
    """
    Process a single comment.

    * Updates metrics
    * Sanitizes and extracts chunks from comment.
    """

    text = Util.sanitize_text(comment.text) # Sanitize comment text.

    user.corpus += text.lower() # Add comment text to corpus.

    comment_timestamp = datetime.datetime.fromtimestamp(
        comment.created_utc, tz=pytz.utc
    )

    process_metrics(user, comment): # Process the comment for metrics

    # If comment is in a subreddit in which comments/user text
    # are to be ignored (such as /r/jokes, /r/writingprompts, etc), do not process it further.
    if comment.subreddit in ignore_text_subs:
        return False

    # TODO: This is dodgy behaviour
    # If comment text does not contain "I" or "my", why even bother?
    if not re.search(r"\b(i|my)\b", text, re.I):
        return False

    # Now, this is a comment that needs to be processed.
    (chunks, sentiments) = parser.extract_chunks(text)
    user.sentiments += sentiments

    for chunk in chunks:
        user.load_attributes(chunk, comment)

    return True

def process_submission(user, submission):
    """
    Process a single submission.

    * Updates metrics
    * Sanitizes and extracts chunks from user text.
    """

    if(submission.is_user):
        text = Util.sanitize_text(submission.text)
        user.corpus += text.lower()

    process_submission_metrics(user, submission) # add metrics info to user

    submission_type = None
    submission_domain = None
    submission_url_path = urlparse(submission.url).path

    if submission.domain.startswith("user."):
        submission_type = "Self"
        submission_domain = submission.subreddit
    elif (
        submission_url_path.endswith(tuple(user.IMAGE_EXTENSIONS)) or
        submission.domain.endswith(tuple(user.IMAGE_DOMAINS))
    ):
        submission_type = "Image"
        submission_domain = submission.domain
    elif submission.domain.endswith(tuple(user.VIDEO_DOMAINS)):
        submission_type = "Video"
        submission_domain = submission.domain
    else:
        submission_type = "Other"
        submission_domain = submission.domain
    t = [
        x for x in user.submissions_by_type["children"] if x["name"]==submission_type
    ][0]
    d = (
        [x for x in t["children"] if x["name"]==submission_domain] or [None]
    )[0]
    if d:
        d["size"] += 1
    else:
        t["children"].append({
            "name" : submission_domain,
            "size" : 1
        })

    # If submission is in a subreddit in which comments/user text
    # are to be ignored (such as /r/jokes, /r/writingprompts, etc),
    # do not process it further.
    if submission.subreddit in ignore_text_subs:
        return False

    # Only process user texts that contain "I" or "my"
    if not submission.is_user or not re.search(r"\b(i|my)\b",text,re.I):
        return False

    (chunks, sentiments) = parser.extract_chunks(text)
    user.sentiments += sentiments

    for chunk in chunks:
        user.load_attributes(chunk, submission)

    return True

def load_attributes(user, chunk, post):
    """
    Given an extracted chunk, load appropriate attributes from it.

    """

    # Is this chunk a possession/belonging?
    if chunk["kind"] == "possession" and chunk["noun_phrase"]:
        # Extract noun from chunk
        noun_phrase = chunk["noun_phrase"]
        noun_phrase_text = " ".join([w for w, t in noun_phrase])
        norm_nouns = " ".join([
            parser.normalize(w, t) \
                for w,t in noun_phrase if t.startswith("N")
        ])

        noun = next(
            (w for w, t in noun_phrase if t.startswith("N")), None
        )
        if noun:
            # See if noun is a pet, family member or a relationship partner
            pet = parser.pet_animal(noun)
            family_member = parser.family_member(noun)
            relationship_partner = parser.relationship_partner(noun)

            if pet:
                user.pets.append((pet, post.permalink))
            elif family_member:
                user.family_members.append((family_member, post.permalink))
            elif relationship_partner:
                user.relationship_partners.append(
                    (relationship_partner, post.permalink)
                )
            else:
                user.possessions_extra.append((norm_nouns, post.permalink))

    # Is this chunk an action?
    elif chunk["kind"] == "action" and chunk["verb_phrase"]:
        verb_phrase = chunk["verb_phrase"]
        verb_phrase_text = " ".join([w for w, t in verb_phrase])

        # Extract verbs, adverbs, etc from chunk
        norm_adverbs = [
            parser.normalize(w,t) \
                for w, t in verb_phrase if t.startswith("RB")
        ]
        adverbs = [w.lower() for w, t in verb_phrase if t.startswith("RB")]

        norm_verbs = [
            parser.normalize(w,t) \
                for w, t in verb_phrase if t.startswith("V")
        ]
        verbs = [w.lower() for w, t in verb_phrase if t.startswith("V")]

        prepositions = [w for w, t in chunk["prepositions"]]

        noun_phrase = chunk["noun_phrase"]

        noun_phrase_text = " ".join(
            [w for w, t in noun_phrase if t not in ["DT"]]
        )
        norm_nouns = [
            parser.normalize(w,t) \
                for w, t in noun_phrase if t.startswith("N")
        ]
        proper_nouns = [w for w, t in noun_phrase if t == "NNP"]
        determiners = [
            parser.normalize(w, t) \
                for w, t in noun_phrase if t.startswith("DT")
        ]

        prep_noun_phrase = chunk["prep_noun_phrase"]
        prep_noun_phrase_text = " ".join([w for w, t in prep_noun_phrase])
        pnp_prepositions = [
            w.lower() for w, t in prep_noun_phrase if t in ["TO", "IN"]
        ]
        pnp_norm_nouns = [
            parser.normalize(w, t) \
                for w, t in prep_noun_phrase if t.startswith("N")
        ]
        pnp_determiners = [
            parser.normalize(w, t) \
                for w, t in prep_noun_phrase if t.startswith("DT")
        ]

        full_noun_phrase = (
            noun_phrase_text + " " + prep_noun_phrase_text
        ).strip()

        # TODO - Handle negative actions (such as I am not...),
        # but for now:
        if any(
            w in ["never", "no", "not", "nothing"] \
                for w in norm_adverbs+determiners
        ):
            return

        # I am/was ...
        if (len(norm_verbs) == 1 and "be" in norm_verbs and
            not prepositions and noun_phrase):
            # Ignore gerund nouns for now
            if (
                "am" in verbs and
                any(n.endswith("ing") for n in norm_nouns)
            ):
                user.attributes_extra.append(
                    (full_noun_phrase, post.permalink)
                )
                return

            attribute = []
            for noun in norm_nouns:
                gender = None
                orientation = None
                if "am" in verbs:
                    gender = parser.gender(noun)
                    orientation = parser.orientation(noun)
                if gender:
                    user.genders.append((gender, post.permalink))
                elif orientation:
                    user.orientations.append(
                        (orientation, post.permalink)
                    )
                # Include only "am" phrases
                elif "am" in verbs:
                    attribute.append(noun)

            if attribute and (
                (
                    # Include only attributes that end
                    # in predefined list of endings...
                    any(
                        a.endswith(
                            parser.include_attribute_endings
                        ) for a in attribute
                    ) and not (
                        # And exclude...
                        # ...certain lone attributes
                        (
                            len(attribute) == 1 and
                            attribute[0] in parser.skip_lone_attributes and
                            not pnp_norm_nouns
                        )
                        or
                        # ...predefined skip attributes
                        any(a in attribute for a in parser.skip_attributes)
                        or
                        # ...attributes that end in predefined
                        # list of endings
                        any(
                            a.endswith(
                                parser.exclude_attribute_endings
                            ) for a in attribute
                        )
                    )
                ) or
                (
                    # And include special attributes with different endings
                    any(a in attribute for a in parser.include_attributes)
                )
            ):
                user.attributes.append(
                    (full_noun_phrase, post.permalink)
                )
            elif attribute:
                user.attributes_extra.append(
                    (full_noun_phrase, post.permalink)
                )

        # I live(d) in ...
        elif "live" in norm_verbs and prepositions and norm_nouns:
            if any(
                p in ["in", "near", "by"] for p in prepositions
            ) and proper_nouns:
                user.places_lived.append(
                    (
                        " ".join(prepositions) + " " + noun_phrase_text,
                        post.permalink
                    )
                )
            else:
                user.places_lived_extra.append(
                    (
                        " ".join(prepositions) + " " + noun_phrase_text,
                        post.permalink
                    )
                )

        # I grew up in ...
        elif "grow" in norm_verbs and "up" in prepositions and norm_nouns:
            if any(
                p in ["in", "near", "by"] for p in prepositions
            ) and proper_nouns:
                user.places_grew_up.append(
                    (
                        " ".join(
                            [p for p in prepositions if p != "up"]
                        ) + " " + noun_phrase_text,
                        post.permalink
                    )
                )
            else:
                user.places_grew_up_extra.append(
                    (
                        " ".join(
                            [p for p in prepositions if p != "up"]
                        ) + " " + noun_phrase_text,
                        post.permalink
                    )
                )

        elif(
            len(norm_verbs) == 1 and "prefer" in norm_verbs and
            norm_nouns and not determiners and not prepositions
        ):
            user.favorites.append((full_noun_phrase, post.permalink))

        elif norm_nouns:
            actions_extra = " ".join(norm_verbs)
            user.actions_extra.append((actions_extra, post.permalink))

def derive_attributes(user):
    """
    Derives attributes using activity data.
    """

    for name, count in user.commented_subreddits():
        subreddit = subreddits_dict[name] if name in subreddits_dict else None
        if (
            subreddit and subreddit["attribute"] and
            count >= user.MIN_THRESHOLD
        ):
            user.derived_attributes[subreddit["attribute"]].append(
                subreddit["value"].lower()
            )

    for name, count in user.submitted_subreddits():
        subreddit = subreddits_dict[name] if name in subreddits_dict else None
        if (
            subreddit and subreddit["attribute"] and
            count >= user.MIN_THRESHOLD
        ):
            user.derived_attributes[subreddit["attribute"]].append(
                subreddit["value"].lower()
            )

    # If someone mentions their wife,
    # they should be male, and vice-versa (?)
    # TODO: This is faulty logic and should be changed/removed - 25/07/16
    if "wife" in [v for v, s in user.relationship_partners]:
        user.derived_attributes["gender"].append("male")
    elif "husband" in [v for v, s in user.relationship_partners]:
        user.derived_attributes["gender"].append("female")

    commented_dates = sorted(user.commented_dates)
    submitted_dates = sorted(user.submitted_dates)
    active_dates = sorted(user.commented_dates + user.submitted_dates)

    min_date = datetime.datetime(datetime.MINYEAR, 1, 1, tzinfo=pytz.utc)
    first_comment_date = \
        min(commented_dates) if commented_dates else min_date
    first_submission_date = \
        min(submitted_dates) if submitted_dates else min_date


    user.first_post_date = max(first_comment_date, first_submission_date)

    active_dates += [datetime.datetime.now(tz=pytz.utc)]
    commented_dates += [datetime.datetime.now(tz=pytz.utc)]
    submitted_dates += [datetime.datetime.now(tz=pytz.utc)]

    # Find the longest period of inactivity
    comment_lurk_period = max(
        [
            {
                "from" : calendar.timegm(d1.utctimetuple()),
                "to" : calendar.timegm(d2.utctimetuple()),
                "days" : (d2 - d1).seconds,
            } for d1, d2 in zip(
                commented_dates[:-1], commented_dates[1:]
            )
        ], key=lambda x:x["days"]
    ) if len(commented_dates) > 1 else {"days":-1}

    submission_lurk_period = max(
        [
            {
                "from" : calendar.timegm(d1.utctimetuple()),
                "to" : calendar.timegm(d2.utctimetuple()),
                "days" : (d2 - d1).seconds,
            } for d1, d2 in zip(
                submitted_dates[:-1], submitted_dates[1:]
            )
        ], key=lambda x:x["days"]
    ) if len(submitted_dates) > 1 else {"days":-1}

    post_lurk_period = max(
        [
            {
                "from" : calendar.timegm(d1.utctimetuple()),
                "to" : calendar.timegm(d2.utctimetuple()),
                "days" : (d2 - d1).seconds,
            } for d1, d2 in zip(
                active_dates[:-1], active_dates[1:] # compares 1st with 2nd, 2nd with 3rd, 3rd with...
            )
        ], key=lambda x:x["days"]
    )

    user.lurk_period = min(
        [
            x for x in [
                comment_lurk_period,
                submission_lurk_period,
                post_lurk_period
            ] if x["days"]>=0
        ],
        key=lambda x:x["days"]
    )
    del user.lurk_period["days"]

import re


class Util:
    """
    Contains a collection of common utility methods.

    """

    @staticmethod
    def sanitize_text(text):
        """
        Returns text after removing unnecessary parts.

        """

        MAX_WORD_LENGTH = 1024

        _text = " ".join([
            l for l in text.strip().split("\n") if (
                not l.strip().startswith("&gt;")
            )
        ])
        substitutions = [
            (r"\[(.*?)\]\((.*?)\)", r""),   # Remove links from Markdown
            (r"[\"](.*?)[\"]", r""),        # Remove text within quotes
            (r" \'(.*?)\ '", r""),          # Remove text within quotes
            (r"\.+", r". "),                # Remove ellipses
            (r"\(.*?\)", r""),              # Remove text within round brackets
            (r"&amp;", r"&"),               # Decode HTML entities
            (r"http.?:\S+\b", r" ")         # Remove URLs
        ]
        for pattern, replacement in substitutions:
            _text = re.sub(pattern, replacement, _text, flags=re.I)

        # Remove very long words
        _text = " ".join(
            [word for word in _text.split(" ") if len(word) <= MAX_WORD_LENGTH]
        )
        return _text

    @staticmethod
    def coalesce(lst):
        """
        Given a list, returns the last element that is not equal to "generic".

        """

        lst = [x for x in lst if x.lower() != "generic"]
        return next(iter(lst[::-1]), "")

    @staticmethod
    def humanize_days(days):
        """
        Return text with years, months and days given number of days.

        """
        y = days/365 if days > 365 else 0
        m = (days - y*365)/31 if days > 30 else 0
        d = (days - m*31 - y*365)
        yy = str(y) + " year" if y else ""
        if y > 1:
            yy += "s"
        mm = str(m) + " month" if m else ""
        if m > 1:
            mm += "s"
        dd = str(d) + " day"
        if d > 1 or d == 0:
            dd += "s"
        return (yy + " " + mm + " " + dd).strip()

    @staticmethod
    def scale(val, src, dst):
        """
        Scale the given value from the scale of src to the scale of dst.
        """
        return ((val - src[0])/(src[1] - src[0])) * (dst[1]-dst[0]) + dst[0]

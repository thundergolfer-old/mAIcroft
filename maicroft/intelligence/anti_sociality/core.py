from insults import Insults

# TODO: this takes a while to load, might want to handle this loading better
Insults.load_model()


class Antisociality():
    def __init__(self):
        self.comment_ratings = []
        self.most_likely_insult = (0, "")
        self.insults_threshold = 0.5

    def percentage_comments_that_are_insults(self):
        num_ratings = len(self.comment_ratings)
        if num_ratings == 0:
            return 0

        num_insults = sum([x for x in self.comment_ratings if x > self.insults_threshold])
        return (num_insults / num_ratings) * 100

    def update(self, comment):
        insult_likelihood = Insults.rate_comment(comment)
        self.comment_ratings.append(insult_likelihood)

        if insult_likelihood > self.most_likely_insult[0]:
            self.most_likely_insult = (insult_likelihood, comment)

    def __repr__(self):
        dict_repr = {
            "percentage_insults": self.percentage_comments_that_are_insults(),
            "highest_likelihood_insulting_comment": self.most_likely_insult
        }
        return str(dict_repr)

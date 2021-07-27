import requests
import json
import webbrowser


def getstrquestion():
    strquestion = json.loads(
        requests.get("https://scibowldb.com/api/questions/random").text
    )["question"]

    del strquestion["id"]
    del strquestion["source"]
    del strquestion["search_vector"]
    return strquestion


class ask_bowl_internal_question_class:
    def __init__(
        self,
        question_type: str,
        question: str,
        answer: str,
    ):
        self.qtype = question_type
        self.isSA = question_type == "Short Answer"
        self.isMC = not self.isSA
        self.q = question
        self.ans = answer


class internal_tossup(ask_bowl_internal_question_class):
    def __init__(
        self,
        question_type: str,
        question: str,
        answer: str,
    ):
        super(internal_tossup, self).__init__(
            question_type,
            question,
            answer,
        )
        self.time = 7
        self.warning = None


class internal_bonus(ask_bowl_internal_question_class):
    def __init__(
        self,
        question_type: str,
        question: str,
        answer: str,
    ):
        super(internal_bonus, self).__init__(question_type, question, answer)
        self.time = 22
        self.warning = 5


class internal_question:
    def __init__(self, tossup: internal_tossup, bonus: internal_bonus, link: str):
        self.tossup = tossup
        self.bonus = bonus
        self.link = link
        self.listform = [tossup, bonus]


def make_new_question():
    raw = getstrquestion()
    return internal_question(
        internal_tossup(
            raw["tossup_format"],
            raw["tossup_question"].replace("^", " to the power of  "),
            raw["tossup_answer"].replace("^", " to the power of  "),
        ),
        internal_bonus(
            raw["bonus_format"],
            raw["bonus_question"].replace("^", " to the power of  "),
            raw["bonus_answer"].replace("^", " to the power of  "),
        ),
        raw["uri"],
    )

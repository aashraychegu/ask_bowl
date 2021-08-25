import requests
import json
import webbrowser
import shelve
from shelve import Shelf
from random import choice
from sys import exit, getsizeof
import os


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

    def __repr__(self):
        return f"\nTossup:\n{self.tossup.q}\n\nAnswer:\n{self.tossup.ans}\n\n\nBonus:\n{self.bonus.q}\n{self.bonus.ans}\n\n\n{self.link}"


def make_str_question(strquestion):

    del strquestion["id"]
    del strquestion["source"]
    del strquestion["search_vector"]
    del strquestion["api_url"]
    return internal_question(
        internal_tossup(
            strquestion["tossup_format"],
            strquestion["tossup_question"].replace("^", " to the power of  "),
            strquestion["tossup_answer"].replace("^", " to the power of  "),
        ),
        internal_bonus(
            strquestion["bonus_format"],
            strquestion["bonus_question"].replace("^", " to the power of  "),
            strquestion["bonus_answer"].replace("^", " to the power of  "),
        ),
        strquestion["uri"],
    )


def load_file():
    try:
        json.dump(
            json.loads(requests.get("https://scibowldb.com/api/questions").text),
            (x := open("dbs/main.json", "r+")),
        )
        x.close()
    except:
        pass


def read_file_into_memory():
    obj = json.load((x := open("dbs/main.json")))["questions"]
    x.close()
    return obj, type(obj), getsizeof(obj)


def get_question_from_memory(l):
    return make_str_question(choice(l))


load_file()
questions_file = (read_file_into_memory())[0]


def make_new_question():
    return get_question_from_memory(questions_file)

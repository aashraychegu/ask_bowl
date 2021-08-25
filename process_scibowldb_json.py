from shelve import Shelf
from ask_bowl_web_retrieval import *
from os.path import isfile
from random import randint


class question_db:
    sill: Shelf
    sill = None
    number: int
    number = None


qdb = question_db()


def make_meta_file(xn):

    with open("dbs/metafile.txt", "r+") as metafile:
        raw = metafile.read()
        if raw:
            qdb.number = int(raw)
        else:
            metafile.write(str(xn))
            qdb.number = xn
        if qdb.number != xn:
            metafile.seek(0, 0)
            metafile.write(str(xn) + "     ")
            return False
        return True


def get_data():

    x = json.loads(requests.get("https://scibowldb.com/api/questions").text)[
        "questions"
    ]

    return len(x), x


def make_neat_json(x):

    for v, strquestion in enumerate(x):
        del strquestion["id"]
        del strquestion["source"]
        del strquestion["search_vector"]
        del strquestion["api_url"]
        i = internal_question(
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
        qdb.sill[str(v)] = i
    return len(x)


def get_random_question(v):
    x = str(randint(0, v))
    while x not in qdb.sill.keys():
        x = str(randint(0, v))
    return qdb.sill[x]


def _init():
    qdb.sill = shelve.open("dbs/offline")
    qdb.number, source = get_data()
    if not make_meta_file(qdb.number):
        make_neat_json(source)


_init()
if __name__ == "__main__":
    print("asdf")
    for i in range(1000000):
        print(get_random_question(qdb.number))

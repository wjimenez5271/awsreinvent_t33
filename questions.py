import db


class Question(object):
    def __init__(self):
        qid = None
        qstring = None
        point_val = int
        answers = {"answer_key": "value"}
        child_questions = {'answer_key': "qid"}
        last_updated = None



def process_question():
    db.get('questions', qid="1")


def get_next_question():
    raise NotImplementedError



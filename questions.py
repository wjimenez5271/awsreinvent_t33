import db
import uuid
import db


class Question(object):
    def __init__(self, qstring):
        self.qid = uuid.uuid4()
        self.qstring = qstring
        self.point_val = int
        self.answers = {"answer_key": "value"}
        self.child_questions = {'answer_key': "qid"}
        self.last_updated = None

    def __str__(self):
        return self.qid

    def set_answers(self, answers):
        assert type(answers) == dict
        self.answers = answers
        return True

    def set_child_questions(self, child_questions):
        assert type(child_questions) == dict
        self.child_questions = child_questions

    def write(self):
        db.put(
        {"qid": self.qid,
         "qstring": self.qstring,
         "point_val": self.point_val,
         "answers": self.answers
         "child_questions": self.child_questions,
         "last_updated": self.last_updated}, table_name='questions', overwrite=True)


def process_question():
    db.get('questions', qid="1")


def get_next_question():
    raise NotImplementedError


def write_question_to_db(question_string, question_answers, child_questions):
    new_question = Question(question_string)
    new_question.set_answers(question_answers)
    new_question.set_child_questions(child_questions)
    return new_question.qid




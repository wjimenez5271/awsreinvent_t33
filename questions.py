import uuid
import db


class Question(object):
    def __init__(self, qstring, qid=None):
        if qid is None:
            self.qid = str(uuid.uuid4())
        else:
            self.qid = qid
        self.qstring = qstring
        self.point_val = 0
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
         "answers": self.answers,
         "child_questions": self.child_questions,
         "last_updated": self.last_updated}, table_name='questions', overwrite=True)


def get_question(qid):
    r = db.get('questions', qid=qid)
    q = Question(r['qstring'], qid=qid)
    q.set_answers(r['answers'])
    q.set_child_questions(r['child_questions'])
    return q



def get_next_question():
    raise NotImplementedError


def write_question_to_db(question_string, question_answers, child_questions):
    new_question = Question(question_string)
    new_question.set_answers(question_answers)
    new_question.set_child_questions(child_questions)
    new_question.write()
    return new_question.qid


def get_first_question():
     return get_question(qid='0588ebb9-f0a6-46c8-9a33-ec3c83c56945')

def test():
     print write_question_to_db('Why is the sky blue',{'1':'Because I said so',
                                                  '2': 'I dont know'}, {'1':'guid of another question',
                                                                        '2':'guid of another question'})
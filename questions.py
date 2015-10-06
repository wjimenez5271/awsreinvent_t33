import db

def process_question():
    db.get('questions', qid="1")

def get_next_question():
    raise NotImplementedError


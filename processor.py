import questions
import users
import db
import queue
import json
import unicodedata

from boto.dynamodb2.exceptions import ItemNotFound

def main():
    # get new message from queue
    events = queue.get_queue('IngressQueue')
    for event in events:
        d = event.get_body()
        d = d.encode('ascii','ignore')
        d = d.replace('\\','')
        d = d.split(':')
        message = d[1].split(',')[0]
        uid = d[2]
        message = message.split("'")[1]
        uid = uid.split("'")[1]

        # lookup user

        try:
            curr_user = users.get_user(uid)
        except ItemNotFound:
            curr_user = users.EndUser(uid)

        # process question
        if curr_user.last_question is None:
            question = questions.get_first_question()
        else:
            question = questions.get_question(curr_user.last_question)

        for q, v in question.answers.iteritems():
            if message == v:
                next_question_id = question.child_questions[q]
            else:
                raise Exception
        # create response message & publish to queue

        next_question = questions.get_question(next_question_id)
        queue.put_queue({'to': uid,
                         'message': next_question.qstring}, 'EgressQueue')


if __name__ == '__main__':
    main()
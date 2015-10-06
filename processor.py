import questions
import users
import db
import queue
import json

def main():
    # get new message from queue
    events = queue.get_queue('IngressQueue')
    for event in events:
        d = event.get_body()
        d = json.loads(d)

        uid = d['from']
        # lookup user

        user = users.get_user(uid)
        # process question
        question = questions.get_question(user.last_question)

        for q,v in question.answers.iteritems():
            if d['message'] == v:
                next_question_id = question.child_questions[q]
            else:
                raise Exception
        # create response message & publish to queue

        next_question = questions.get_question(next_question_id)
        queue.put_queue({'to':uid,
                         'message':next_question.qstring}, 'EgressQueue')


if __name__ == '__main__':
    main()
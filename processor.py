import questions
import users
import queue
import json
from time import sleep

from boto.dynamodb2.exceptions import ItemNotFound


def send_first_question(uid, event):
    question = questions.get_first_question()
    print question.qstring
    queue.put_queue(json.dumps({'to': uid,
                     'message': question.qstring}), 'EgressQueue')
    queue.delete_from_queue(event, 'IngressQueue')

def main():
    # get new message from queue
    events = queue.get_queue('IngressQueue')
    for event in events:
        d = event.get_body()
        d = json.loads(d)
        uid = d['from']
        message = d['message']

        # lookup user

        try:
            curr_user = users.get_user(uid)
        except ItemNotFound:
            curr_user = users.EndUser(uid)

        # process question
        if curr_user.last_question is None:
            send_first_question(uid, event)
            break
        else:
            question = questions.get_question(curr_user.last_question)

        for q, v in question.answers.iteritems():
            if message.lower() == v[1].lower():
                next_question_id = question.child_questions[q]
            else:
                # invalid response
                queue.put_queue(json.dumps({'to': uid,
                 'message': "Sorry, that wasn't a valid response"}), 'EgressQueue')
                queue.delete_from_queue(event, 'IngressQueue')
                break
        # create response message & publish to queue
        next_question = questions.get_question(next_question_id)
        queue.put_queue(json.dumps({'to': uid,
                         'message': next_question.qstring}), 'EgressQueue')
        queue.delete_from_queue(event, 'IngressQueue')



if __name__ == '__main__':
    try:
        while True:
            main()
            sleep(5)
    except KeyboardInterrupt:
        print 'exiting'
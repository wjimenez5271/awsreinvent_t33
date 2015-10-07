import questions
import users
import queue
import json
from time import sleep

from boto.dynamodb2.exceptions import ItemNotFound


def send_first_question(uid, event, curr_user):
    question = questions.get_first_question()
    print question.qstring
    queue.put_queue(json.dumps({'to': uid,
                     'message': question.qstring}), 'EgressQueue')
    queue.delete_from_queue(event, 'IngressQueue')
    print str(question.qid)
    curr_user.last_question = str(question.qid)
    curr_user.write()

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
            curr_user.write()

        print curr_user
        print curr_user.last_question
        # process question
        if curr_user.last_question is None:
            send_first_question(uid, event, curr_user)
            break
        else:
            question = questions.get_question(curr_user.last_question)

        for q, v in question.answers.iteritems():

            v_json = json.loads(v)

            print v[1].lower()
            if message.lower() == v_json.values()[0].lower():
                print "response match found"
                next_question_id = json.loads(question.child_questions[q])
                print next_question_id.values()[0]
                # create response message & publish to queue
                next_question = questions.get_question(next_question_id.values()[0])
                queue.put_queue(json.dumps({'to': uid,
                                            'message': next_question.qstring}), 'EgressQueue')
                queue.delete_from_queue(event, 'IngressQueue')
            else:
                print "unable to find a response match"
                # invalid response
                queue.put_queue(json.dumps({'to': uid,
                 'message': "Sorry, that wasn't a valid response"}), 'EgressQueue')
                queue.delete_from_queue(event, 'IngressQueue')
                break




if __name__ == '__main__':
    try:
        while True:
            main()
            sleep(2)
    except KeyboardInterrupt:
        print 'exiting'
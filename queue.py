import boto.sqs

region = 'us-east-1'
conn = boto.sqs.connect_to_region(region)
queue_name = "AnswersQueue"


def process_events(events, queue_name):
    for event in events:
        process_events(event)  # process events
        # if no exceptions were raised, we can assume all's good and we can remove from queue
        queue = conn.get_queue(queue_name)
        resp = queue.delete_message(event)
        if resp:
            print "Cleanup completed successfully, removing message from queue."


def get_queue(queue_name):
    queue = conn.get_queue(queue_name)
    events = queue.get_messages()
    if len(events) == 0:
        print "No events found, nothing to do. Bye."
    return events

def delete_from_queue(event, queue_name):
    queue = conn.get_queue(queue_name)
    resp = queue.delete_message(event)
    if resp:
        print "Cleanup completed successfully, removing message from queue."

def put_queue(data, queue_name):
    queue = conn.get_queue(queue_name)
    print queue.id
    conn.send_message(queue, data)

#put_queue({'id':'bar'})
for i in get_queue('AnswersQueue'):
    print i.get_body()

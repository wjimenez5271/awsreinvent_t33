import boto.sqs

region = 'us-east-1'
conn = boto.sqs.connect_to_region(region)
queue_name = "AnswersQueue"


def process_events(event):
    raise NotImplementedError


def get_queue():
    queue = conn.get_queue(queue_name)
    events = queue.get_messages()
    if len(events) == 0:
        print "Nothing to do. Bye."
    for event in events:
        process_events(event)  # process events
        # if no exceptions were raised, we can assume all's good and we can remove from queue
        resp = queue.delete_message(event)
        if resp:
            print "Cleanup completed successfully, removing message from queue."


def put_queue(data):
    queue = conn.get_queue(queue_name)
    print queue.id
    conn.send_message(queue, data)

put_queue({'id':'bar'})
get_queue()

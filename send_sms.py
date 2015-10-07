import queue
import json
from time import sleep
from twilio.rest import TwilioRestClient
import os


send_sms_from = "+1650-549-1180"
egressQueue = 'EgressQueue'


def main():
    events = queue.get_queue(egressQueue)
    print 'Processing EgressQueue...'
    for event in events:
        d = event.get_body()
        d = json.loads(d)


        client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

        client.messages.create(
                to= d['to'],
                from_= send_sms_from,
                body= d['message'],
        )
        queue.delete_from_queue(event,egressQueue)


if __name__ == '__main__':
    ACCOUNT_SID = os.environ.get('twilio_sid')
    AUTH_TOKEN = os.environ.get('twilio_token')
    if ACCOUNT_SID or AUTH_TOKEN is None:
        raise Exception('Unable to get Twilio credentials ')
    try:
        while True:
            main()
            sleep(5)
    except KeyboardInterrupt:
        print 'exiting'


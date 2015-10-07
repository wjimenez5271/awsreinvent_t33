import queue
import json
from time import sleep
from twilio.rest import TwilioRestClient

send_sms_from = "+14693400604"
egressQueue = 'EgressQueue'


def main():
    events = queue.get_queue(egressQueue)
    print 'Processing EgressQueue...'
    for event in events:
        d = event.get_body()
        d = json.loads(d)

        ACCOUNT_SID = "ACebf8f6d8ce6a55a53e72dc0d1dcc0137"
        AUTH_TOKEN = "6167baeb1791cea76df2d82e163c2f6b"

        client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

        client.messages.create(
                to= d['to'],
                from_= send_sms_from,
                body= d['message'],
        )


if __name__ == '__main__':
    try:
        while True:
            main()
            sleep(20)
    except KeyboardInterrupt:
        print 'exiting'


from flask import Flask, request, redirect
import argparse
import twilio.twiml
import json
import logging
import queue

ingressQueue = 'IngressQueue'
egressQueue = 'EgressQueue'

app = Flask(__name__)

@app.route("/incoming", methods=['GET', 'POST'])
def receive_sms():

    from_number = request.values.get('From', None)
    message_body = request.values.get('Body', None)
    message_sid = request.values.get('MessageSid', None)
    queue.put_queue(json.dumps({'from': from_number, 'message': message_body}), ingressQueue)
    return True

def setup_logging(loglevel, logfile):
    #Setup Logger
    numeric_log_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_log_level, int):
         raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(filename=logfile, level=numeric_log_level,
                        format="%(asctime)s - [ignite-chat] - "
                          "%(levelname)s - %(message)s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--loglevel', help='logging level', type=str, default='INFO')
    parser.add_argument('--logfile', help='path to write logfile to', type=str, default='sms-receiver.log')
    args = parser.parse_args()

    setup_logging(args.loglevel, args.logfile)
    logging.info('Starting server')
    if args.loglevel.upper() == 'DEBUG':
        floglevel=True
    else:
        floglevel=False

    app.run(debug=floglevel, host='0.0.0.0')


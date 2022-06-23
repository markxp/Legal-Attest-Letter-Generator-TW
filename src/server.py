from base64 import b64decode
from collections import namedtuple
from io import open as io_open
from json import JSONEncoder
from os import getenv
from uuid import uuid4 as uuid

from flask import Flask, abort, make_response, request
from lal_modules import core

app = Flask(__name__)


class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __jsonencode__(self):
        return {'name': self.name, 'address': self.address}


class Config:
    def __init__(self, senders, receivers, carbon_copies):
        self.senders = senders[:]
        self.receivers = receivers[:]
        self.carbonCopy = carbon_copies[:]

    def __jsonencode__(self):
        return {'senders': self.senders[:], 'receivers': self.receivers[:], 'carbonCopy': self.carbonCopy[:]}


class Content:
    def __init__(self, encoded_content):
        self.data = encoded_content

    def __jsonencode__(self):
        return {'data': self.data}


class Req:
    def __init__(self, config, data):
        self.config = config
        self.data = data

    def __jsonencode__(self):
        return {'config': self.config, 'content': self.data}


class MyJSONEncoder(JSONEncoder):
    def default(self, obj):  # pylint: disable=E0202
        if hasattr(obj, '__jsonencode__'):
            return obj.__jsonencode__()
        return JSONEncoder.default(self, obj)


@app.route("/", methods=['POST'])
def handler():
    data = request.get_json(silent=True)
    if data == None:
        abort(400)
    conf = data['config']
    encoded = data['content']['data']

    # transform to same form as CLI tool used
    _senders = conf['senders']
    _receivers = conf['receivers']
    _cc = conf['carbonCopy']

    senders = []
    senderAddrs = []
    receivers = []
    receiverAddrs = []
    ccs = []
    ccAddrs = []

    for _sender in _senders:
        senders.append(_sender['name'])
        senderAddrs.append(_sender['address'])

    for _r in _receivers:
        receivers.append(_r['name'])
        receiverAddrs.append(_r['address'])

    for _c in _cc:
        ccs.append(_c['name'])
        ccAddrs.append(_c['address'])

    text = bytes.decode(b64decode(encoded), encoding='utf-8')
    fname = core.gen_filename()

    text, letter = core.generate_text_and_letter(
        senders, senderAddrs, receivers, receiverAddrs, ccs, ccAddrs, text)
    core.merge_text_and_letter(text, letter, fname)

    with io_open(fname, 'rb') as f:
        resp = make_response(f.read())
        resp.headers['content-type'] = 'application/pdf'
        resp.headers['content-disposition'] = 'attachment'
    core.clean_temp_files(text, letter)
    return resp

# run in production with gunicorn
if __name__ == '__main__':
    port = getenv('PORT', 5000)
    app.run(host="0.0.0.0", port=port)

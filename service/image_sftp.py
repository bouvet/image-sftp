from flask import Flask, request, Response
import os
import logging
import json
import base64
import pysftp

app = Flask(__name__)
logger = None
format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger('images-sftp')

host = os.environ.get('host')
username = os.environ.get('username')
password = os.environ.get('password')

# Log to stdout
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(logging.Formatter(format_string))
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)


@app.route("/decode", methods=["POST"])
def decode():
    json_data = request.get_json()
    for entity in json_data:
        for k,v in entity.items():
            if k == "employeenumber" and not None:
                filename = v + ".png"
            else:
                pass
            if k == "image" and entity["image"] is not None:
                img_data = v.encode()
                logger.info("encoding image...")
                # try disabling host key check
                cnopts = pysftp.CnOpts()
                cnopts.hostkeys = None
                try:
                    with pysftp.Connection(host, username=username, password=password, cnopts=cnopts) as sftp:
                        try:
                            with sftp.open("/" + filename, mode="rwb") as remote_file:
                                remote_file.write(base64.decodebytes(img_data))
                                sftp.close()
                        except Exception as e:
                            logger.error(e.args)
                except Exception as e:
                    logger.error(e.args)
            else:
                logger.info('no content in image')

    return Response(
        print("sent encoded images to sFTP"),
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=os.environ.get('port',5000))

from flask import Flask, request, Response
import os
import logging
import json
import base64
import io
from paramiko import SSHClient, AutoAddPolicy
from PIL import Image


app = Flask(__name__)
logger = None
format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger('images-sftp')

host = os.environ.get('host')
username = os.environ.get('username')
password = os.environ.get('password')
port = os.environ.get('ftp-port', 22)

# Log to stdout
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(logging.Formatter(format_string))
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)

# Get POSTed images, and put them on an sftp
@app.route("/decode", methods=["POST"])
def decode():
    entities = request.get_json()

    logger.info("Received %s entities from Sesam", len(entities))

    for entity in entities:

        for k, v in entity.items():
            if k == os.environ.get('filename') and v is not None:
                filename = v
            else:
                pass
            if k == os.environ.get('imagedata') and v is not None:
                logger.info("encoding image...")
                img_data = v.encode()
                image_stream = io.BytesIO(base64.decodebytes(img_data))
                image = Image.open(image_stream)
                filetype = image.format
                client = SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(AutoAddPolicy())
                try:
                    client.connect(hostname=host, port=port, username=username, password=password)
                    logger.info('connected')
                    sftp = client.open_sftp()
                    full_filename = filename + "." + filetype
                    with sftp.open("/" + full_filename, mode="wb") as remote_file:
                        remote_file.write(base64.decodebytes(img_data))
                        logger.info('sent file %s', full_filename)
                        client.close()

                except Exception as e:
                    logger.info("could not connect to " + os.environ.get('host') + ":  %s" % e)
                    raise Exception("Problem connecting : '%s'" % e)

            else:
                pass
    return Response(
        print("sent encoded images to sFTP"),
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=os.environ.get('port',5000))

from flask import Flask, request, Response
import os
import logging
import json
import base64
from paramiko import SSHClient, AutoAddPolicy


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
    entities = request.get_json()

    logger.info("Received %s entities from Sesam", len(entities))

    for entity in entities:

        for k, v in entity.items():
            if k == "employeenumber" and v is not None:
                filename = v + ".png"
            else:
                pass
            if k == "image" and v is not None:
                logger.info("encoding image...")
                img_data = v.encode()
                client = SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(AutoAddPolicy())
                try:
                    client.connect(hostname=host, username=username, password=password)
                    logger.info('connected')
                    sftp = client.open_sftp()
                    with sftp.open("/" + filename, mode="wb") as remote_file:
                        remote_file.write(base64.decodebytes(img_data))
                        logger.info('sent file %s', filename)
                        client.close()

                except Exception as e:
                    logger.info("could not connect to " + os.environ.get('host') + ":  %s" % e)
                    raise Exception("Problem connecting : '%s'" % e)
                #try:
                    # try disabling host key check
                    # cnopts = pysftp.CnOpts()
                    # cnopts.hostkeys = None

                #     with pysftp.Connection(host, username=username, password=password, cnopts=cnopts) as sftp:
                #         try:
                #             with sftp.open("/" + filename, mode="rwb") as remote_file:
                #                 remote_file.write(base64.decodebytes(img_data))
                #                 sftp.close()
                #                 logger.info('sent file %s', filename)
                #         except Exception as e:
                #             logger.error(e.args)
                # except Exception as e:
                #     logger.error(e.args)
            else:
                pass
    return Response(
        print("sent encoded images to sFTP"),
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=os.environ.get('port',5000))

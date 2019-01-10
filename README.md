# image-sftp
Small service to send images to an sftp from base64 encoded images in Sesam

System config:
```json
{
  "_id": "image-sftp",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "host": "$ENV(sftp-hostname)",
      "password": "$SECRET(sftp-password)",
      "username": "$ENV(sftp-username)",
      "filename": "what property should be used as filename",
      "imagedata": "Property of your image data"
    },
    "image": "sesam-community/image-sftp:latest",
    "port": 5000
  }
}
```


It's set to add missing hostkeys if missing.

Set fileextension to what is supported o to what the images where before encoding. Imagedata is the source property for the encoded image and filename is what the file should be called once it has been decoded.


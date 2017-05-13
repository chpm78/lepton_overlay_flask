# lepton_overlay_flask
Stream lepton + picamera overlay with flask

Experiments in streaming with flask a picamera image + Flir Lepton Overlay

Lepton is accessed using pylepton (https://github.com/groupgets/pylepton)

## Progress

Up to now I'm able to capture the image from Flir Lepton, add a palette with opencv functions, increase the resolution to match the picamera image, overlay (with adjustable weights) it to the picamera image and then stream the images to a web client using Flask.

The Flir and Picamera capture is triggered from a web request. This only works if there is one web request at a time.

## TO DO

Flask is accepting only one connection at a time and this makes things very easy. 

To accept more than one connection the capture part must be moved somewhere else. I'm going to experiment Celery with RabbitMQ

All the parameters are now set in the source code. I'm going to make a web interface that allows the user to:
- Choose which palette to use
- Choose the overlay weight
- Choose the image resolution



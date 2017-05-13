import time
import picamera
import picamera.array
import cv2

from flask import Flask, render_template, Response
#from camera import Camera

import sys
import numpy as np
from pylepton import Lepton

old_frame=0

RES_X=1024
RES_Y=768

app = Flask(__name__)

def capture(device = "/dev/spidev0.0"):
  with Lepton(device) as l:
    a, frame = l.capture()
  
  #cv2.flip(a,0)
  cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
  np.right_shift(a, 8, a)
  return np.uint8(a)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    while True:
        thermal = capture(device = "/dev/spidev0.0")  
        thermal_big = cv2.resize(thermal, (RES_X, RES_Y))
        
        im_color = cv2.applyColorMap(thermal_big, cv2.COLORMAP_HOT)
      
        with picamera.PiCamera() as camera:
          camera.resolution = (RES_X, RES_Y)

          with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='bgr')

            # At this point the image is available as stream.array
            src = stream.array
                                  
            dst = src.astype('uint8')
            
            result = cv2.addWeighted(dst,0.7,im_color,0.3,0)            
            
            img_str = cv2.imencode('.jpg', result)[1].tostring()
      
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img_str + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


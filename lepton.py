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

def blend_transparent(face_img, overlay_t_img):
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
    overlay_mask = overlay_t_img[:,:,3:]  # And the alpha plane

    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image    
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))


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
        #cv2.imwrite("thermal_big.jpg", thermal_big)
        
        im_color = cv2.applyColorMap(thermal_big, cv2.COLORMAP_HOT)
        #cv2.imwrite("thermal_color.jpg", im_color)
      
        with picamera.PiCamera() as camera:
          camera.resolution = (RES_X, RES_Y)
          #camera.start_preview()
          #time.sleep(2)
          with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='bgr')
            # At this point the image is available as stream.array
            src = stream.array
            #cv2.imwrite("camera.jpg", image)
            
            #Edge Detection
            #dst = cv2.Canny(src,50,200)
            
            #img = cv2.GaussianBlur(src,(3,3),0)

            # convolute with proper kernels
            #dst = cv2.Laplacian(img,cv2.CV_64F)
            
            
            #dst = cv2.detailEnhance(src, sigma_s=20, sigma_r=0.15)
            #dst = cv2.stylization(src, sigma_s=60, sigma_r=0.07)
            
            dst=src
            
            #dst = cv2.adaptiveThreshold(src,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
            
            #result_1  = cv2.addWeighted(dst,0.8,im_color,0.2,0)
            #cv2.imwrite("merged.jpg", result_1)
                      
            dst_1 = dst.astype('uint8')
            
            result_1 = cv2.addWeighted(dst_1,0.7,im_color,0.3,0)            
            
            img_str = cv2.imencode('.jpg', result_1)[1].tostring()

      
        #frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img_str + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)




#if __name__ == '__main__':

#  thermal = capture(device = "/dev/spidev0.0")  
#  cv2.imwrite("thermal.jpg", thermal)
  
#  thermal_big = cv2.resize(thermal, (RES_X, RES_Y))
#  cv2.imwrite("thermal_big.jpg", thermal_big)
  
#  im_color = cv2.applyColorMap(thermal_big, cv2.COLORMAP_JET)
#  cv2.imwrite("thermal_color.jpg", im_color)

#  with picamera.PiCamera() as camera:
#    camera.resolution = (RES_X, RES_Y)
    #camera.start_preview()
    #time.sleep(2)
#    with picamera.array.PiRGBArray(camera) as stream:
#      camera.capture(stream, format='bgr')
      # At this point the image is available as stream.array
#      image = stream.array
#      cv2.imwrite("camera.jpg", image)

      #result_1 = blend_transparent(image, im_color)
#      result_1  = cv2.addWeighted(image,0.8,im_color,0.2,0)
#      cv2.imwrite("merged.jpg", result_1)


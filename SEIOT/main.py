# Fall detection main

import video
import time
import sys
import numpy as np
import cv2
import time
import settings

video = video.Video()
time.sleep(1.0)   #let camera autofocus + autosaturation settle
video.nextFrame()
video.testBackgroundFrame()

settings = settings.Settings()
debug = settings.debug

while 1:
    #get next frame of video
    video.nextFrame()
    video.testBackgroundFrame() #press n to delete background?
    video.updateBackground()
    video.compare()
    video.showFrame()
    if debug:
        video.testSettings()
    
    k = cv2.waitKey(1) & 0xff
    if video.testDestroy():
        if k == 27:
            break

#video.release()
cv2.destroyAllWindows()
sys.exit()

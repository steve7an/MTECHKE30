# Fall detector settings class
#
#
# Kim Salmi, kim.salmi(at)iki(dot)fi
# http://tunn.us/arduino/falldetector.php
# License: GPLv3

class Settings(object):
	
	def __init__(self):
		self.debug = 0 # boolean
		self.source = './storedvideos/stand.avi'#0 # camera source
		self.bsMethod = 1 #1 # listed in bs.py
		self.MOG2learningRate = 0.001 #0.001 #0 means that the background model is not updated at all, 1 means that the background model is completely reinitialized from the last frame.
		self.MOG2shadow = 0 #shadow detection boolean
		self.MOG2history = 100 #the number of last frames that affect the background model.
		self.MOG2thresh = 20 #the variance threshold for the pixel-model match.
		self.minArea = 100 * 100 #50*50 # minimum area to be considered as a person
		self.thresholdLimit = 75 #50
		self.dilationPixels = 30 # dilate thresh
		self.useGaussian = 1 #1 # boolean
		self.useBw = 1 # boolean
		self.useResize = 1 # boolean
		self.gaussianPixels = 31 #31
		self.movementMaximum = 75 # amount to move to still be the same person
		self.movementMinimum = 1 # minimum amount to move to not trigger alarm
		self.movementTime = 45 # 50 # number of frames after the alarm is triggered
		self.location = 'NUS Lab'
		self.phone = '01010101010'
		self.email = 'student@u.nus.edu'
		self.email_cc = 'student@gmail.com'
		self.apiKey = ""
		self.alarmImagesFolder = "alarms"
		self.triggerEmail = 1 #send alarm email or not
		self.alarmSound = 'Loud-Alarm-08-loud.mp3'
		self.channel = 4
		self.mailbody = "Help!!"
		self.url = 'https://api.mailgun.net/v3/sandbox09688ba028104ae0bec1d690ebc67a37.mailgun.org/messages'
		self.fromMail = "Mailgun Sandbox <postmaster@sandbox09688ba028104ae0bec1d690ebc67a37.mailgun.org>"
		self.windowMode = 0
		self.videoErrorCount = 0
		self.videoAlertLog = []
		self.videoFrameCount = 1
		self.videoWaitKey = 1 #25
		self.person_w_ratio = 1.2
		self.person_h_ratio = 1.2
		self.person_keep_last_count = 30

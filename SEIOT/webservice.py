# Fall detector webservice
#
# Kim Salmi, kim.salmi(at)iki(dot)fi
# http://tunn.us/arduino/falldetector.php
# License: GPLv3
import requests
import os
import time
import settings
import RPi.GPIO as GPIO # calling header file for GPIO’s of PI


class Webservice(object):
	
	def __init__(self, place, phone, email, apiKey):
		self.settings = settings.Settings()
		self.url = self.settings.url
		self.recipients = email
		self.apiKey = apiKey
		self.mailbody = self.settings.mailbody
		self.fromMail = self.settings.fromMail
		#self.data = '' #attach the image to be shown in the body

	def send_email(self, subject, attachment):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		file_path = os.path.join(dir_path,attachment)

		return requests.post(
			self.url,
			auth=("api", self.apiKey),
			files=[("attachment", (attachment, open(file_path, "rb").read()))],
			data={"from": self.fromMail,
			      "to": self.recipients,
			      "subject": subject,
				  "text": self.mailbody})


	def sound_alarm(self, alarm_sound):
		audio_length = 120
		os.system("mpg123 -n {0} -q {1}".format(audio_length, alarm_sound))


	def mail_alarm(self, detectiontype, personid, attachment):
		subject = 'Alarm triggered due to '+detectiontype+' by person id '+str(personid)
		print (subject + ' with attachment: ' + attachment)
		self.send_email(subject, attachment)


	def blink_alarm(self, channel):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(channel, GPIO.OUT)
		light_duration = 3

		GPIO.output(channel, GPIO.HIGH)
		time.sleep(light_duration)
		
		GPIO.cleanup()
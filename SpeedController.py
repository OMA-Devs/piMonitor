#!/usr/bin/env python3

#Logging Python
import logging
#Control GPIO
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

class SpeedController():
	def __init__(self, OUTpin):
		##LOG##
		self.name = "SpeedController"
		self.log = logging.getLogger(self.name)
		self.fHandler = logging.FileHandler(self.name+".log")
		self.SHandler = logging.StreamHandler()
		self.fFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		self.fHandler.setFormatter(self.fFormat)
		self.SHandler.setFormatter(self.fFormat)
		self.log.addHandler(self.fHandler)
		self.log.addHandler(self.SHandler)
		self.log.setLevel(logging.WARNING)
		##
		'''Clase generica para instanciar un generador de PWM asociado a un pin de salida.
		Diseñada con el control de un transistor 2n2222 en mente, pero sirve para cualquier
		otro tipo de control PWM con pocas o ninguna modificación.'''
		#self.OUTpin = OUTpin
		#gpio.setup(self.OUTpin, gpio.OUT)
		self.speed = 0
		#self.pwm = gpio.PWM(self.OUTpin, 5) #100 es la frecuencia en HERTZIOS
		#self.pwm.start(0)
		self.log.warning("SPEED CONTROLLER STARTED")
	def setSpeed(self, duty):
		'''Determina el ciclo de trabajo PWM'''
		#self.pwm.ChangeDutyCycle(duty)
		#self.speed = duty
		self.log.info("setSpeed()- SPEED SET TO: "+str(duty))
	def setSpeedMAP(self, min, max, act):
		'''Mapea una velocidad de 0-100 dado un par MIN-MAX y una variable ACT(ual)'''
		n = (max-min)/100
		#self.log.info("N: "+str(n))
		z = round((act-min)/n)
		self.log.info("setSpeedMAP()- MAPPED SPEED TO: "+str(z))
		##Manejo de posibles CICLOS menores a 0
		if z < 0:
			self.setSpeed(0)
		elif z > 100:
			self.setSpeed(100)
		else:
			self.setSpeed(z)
	def clearController(self):
		'''Destrucción del objeto y liberación de los GPIO correspondientes.'''
		#self.pwm.stop()
		#gpio.cleanup()
		self.log.warning("clearController()- SPEED CONTROLLER INHABILITED")

if __name__ == "__main__":
	ctrl = SpeedController(12)
	while True:
		try:
			spd = int(input())
			ctrl.setSpeed(spd)
		except KeyboardInterrupt:
			ctrl.clearController()
			ctrl.log.warning("INVALID SPEED. SHUTTING OFF")
			break
		except ValueError:
			ctrl.clearController()
			ctrl.log.warning("INVALID SPEED. SHUTTING OFF")
			break
		except EOFError:
			ctrl.clearController()
			ctrl.log.warning("INVALID SPEED. SHUTTING OFF")
			break
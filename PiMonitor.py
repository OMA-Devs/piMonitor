#!/usr/bin/env python3
#Aqui se usa para ejecutar comandos de shell
import subprocess
#Vamos a ser serios.
import logging
#Librería de interfaz
from tkinter import Tk
from tkinter import filedialog
from tkinter.font import Font
from tkinter import messagebox
from tkinter import ttk
from tkinter import IntVar

#Utilizado solo para mostrar los logos.
from PIL import Image, ImageTk

#Utilizado para gestionar log.
from datetime import datetime

##CONFIGURACION
from SpeedController import SpeedController

class Aplicacion():
	''' Clase monolitica que encapsula la interfaz y las funciones necesarias para su
	correcto desarrollo.'''
	def __init__(self):
		##LOG##
		self.name = "GUI"
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
		''' Creación de la interfaz y todas sus variables asociadas'''
		self.raiz = Tk()
		self.raiz.geometry('')		#La línea de geometría sin definir ningún tamaño hace que la interfaz sea autoadaptable.
		self.fontTITLE = Font(size = 30)
		self.font = Font(size = 16)
		buttStyle = ttk.Style()
		buttStyle.configure("size.TButton", font = ("Helvetica",16))
		self.raiz.title('PiMonitor')
		##Variables de la aplicacion
		self.minTEMP = 30 #CONFIG.minTEMP sera usada en versiones posteriores
		self.normTEMP = 50 #CONFIG.normTEMP sera usada en versiones posteriores
		self.maxTEMP = 70 #CONFIG.maxTEMP sera usada en versiones posteriores
		##Variable de controlador
		self.control = SpeedController(19)
		##################
		##LOGOS y TITULO##
		##################
		LOGO = ImageTk.PhotoImage(Image.open("logo.png").resize((120,120)))
		self.LOGO = ttk.Label(self.raiz, image = LOGO)
		self.LOGO.grid(column=0, row = 0, columnspan = 2)
		self.titleLABEL = ttk.Label(self.raiz, text= "PiMonitor", font = self.fontTITLE)
		self.titleLABEL.grid(column = 3, row = 0, columnspan = 3)
		##############################
		#######DISPLAY DE ESTADO######
		##############################
		self.tempLAB = ttk.Label(self.raiz, text = "Temp: ", font = self.font)
		self.tempLAB.grid(column = 0, row = 1, columnspan = 1, pady = 20)
		self.temp = ttk.Label(self.raiz, text = "XX", font = self.font)
		self.temp.grid(column = 1, row = 1, columnspan = 2, pady = 20)
		self.range = ttk.Label(self.raiz, text = "Rango Cº: ", font = self.font)
		self.range.grid(column = 3, row = 1, columnspan = 1, pady = 20)
		self.minVAR = IntVar()
		self.minVAR.set(self.minTEMP)
		self.minRange = ttk.Entry(self.raiz, text = self.minVAR, width = 2)
		self.minRange.grid(column = 4, row = 1, columnspan = 1, pady = 20)
		self.LAB = ttk.Label(self.raiz, text = "MIN-MAX", font = self.font)
		self.LAB.grid(column = 5, row = 1, columnspan = 1, pady = 20)
		self.maxVAR = IntVar()
		self.maxVAR.set(self.maxTEMP)
		self.maxRange = ttk.Entry(self.raiz, text = self.maxVAR, width = 2)
		self.maxRange.grid(column = 6, row = 1, columnspan = 1, pady = 20)

		self.fanSPDlab = ttk.Label(self.raiz, text="Speed: ", font = self.font)
		self.fanSPDlab.grid(column = 0, row = 3, columnspan = 1, pady = 20)
		self.fanSPD = ttk.Label(self.raiz, text="XX", font = self.font)
		self.fanSPD.grid(column = 1, row = 3, columnspan = 1, pady = 20)

		self.raiz.after(500, self.PID)
		self.log.info("GUI INITIALIZED")
		self.raiz.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.raiz.mainloop()
	def overTemperature(self, temp):
		'''Chequea la temperatura otorgada y la compara con la máxima admitida.
		Efectua operaciones según corresponda, apagando o manteniendo el sistema encendido.'''
		if temp >= self.maxTEMP:
			self.log.warning("overTemperature()- OVERTEMPERATURE: SHUTING OFF")
			messagebox.showwarning("ALERTA","RPI VA A APAGARSE")
			self.control.clearController()
			subprocess.run("sudo shutdown -h now", shell= True)
		else:
			self.log.info("overTemperature()- TEMPERATURE IN RANGE")
	def getColor(self, temp):
		'''Devuelve una cadena de color para decorar la interfaz dependiendo del margen de temperatura establecido.'''
		if temp < self.normTEMP:
			return "blue"
		elif temp >= self.normTEMP and temp < self.maxTEMP-10:
			return "green"
		elif temp >= self.maxTEMP-10 and temp < self.maxTEMP:
			return "yellow"
		elif temp >= self.maxTEMP:
			return "red"
	def getTemp(self):
		'''Se obtiene la temperatura del procesador mediante un comando de shell y se trata
		la cadena de salida correspondiente. Este comando hace que el programa sea especifico
		de RPI.'''
		#Obtenemos la temperatura mediante el proceso del sistema correspondiente
		proc = subprocess.run("vcgencmd measure_temp", shell=True, stdout=subprocess.PIPE)
		#Tratamos y convertimos la cadena en un número para trabajar con ella
		temp = int(proc.stdout.decode("utf-8").split("=")[1][:-5])
		self.temp["text"] = temp
		self.temp.config(background = self.getColor(temp))
		#Se devuelve la cadena
		return temp
	def PID(self):
		'''Ciclo de actualización y comprobación de las variables relevantes. Se actualiza la temperatura
		y esta se pasa a todas las funciones necesarias para actualizar los labels, el color de estos y
		la velocidad del controlador.'''
		temp = self.getTemp()
		self.control.setSpeedMAP(self.minTEMP,self.maxTEMP,temp)
		self.log.info("PID()- MIN: "+str(self.minTEMP)+"| MAX: "+str(self.maxTEMP)+"| ACT: "+str(temp))
		self.overTemperature(temp)
		self.fanSPD["text"] = round(self.control.speed)
		self.raiz.after(2000, self.PID)
	def on_closing(self):
		'''Esta función detiene correctamente el controlador de velocidad y libera los GPIO correspondientes.'''
		if messagebox.askokcancel("Salir", "¿Quieres Salir?"):
			self.control.clearController()
			self.log.warning("GUI- STOPPING GUI")
			self.raiz.destroy()

if __name__ == "__main__":
	Aplicacion()

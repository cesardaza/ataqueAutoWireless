import RPi.GPIO as GPIO
import time
import threading
from logica import controlador,ap,wep,wpa,wpa2

#poner modo BCH
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#definir pines como salida
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

def apagarleds():
	GPIO.output(18, GPIO.LOW)
	GPIO.output(23, GPIO.LOW)
	GPIO.output(22, GPIO.LOW)
	GPIO.output(25, GPIO.LOW)
	GPIO.output(12, GPIO.LOW)
	
def clearLeds():	
	GPIO.cleanup()

def prenderVerde():
	GPIO.output(18, GPIO.HIGH)

def prenderAmarillo():
	GPIO.output(23, GPIO.HIGH)

def prenderAzul():
	GPIO.output(22, GPIO.HIGH)
	
def prenderRojo():
	GPIO.output(25, GPIO.HIGH)
	
def prenderBlanco():
	GPIO.output(12, GPIO.HIGH)	
	
def parpadear(arg):
	t = threading.currentThread() 
	cont = 0
	while getattr(t,"do_run",True):
		if cont%2 == 0:
			GPIO.output(arg, GPIO.HIGH)
		else:
			GPIO.output(arg, GPIO.LOW)
		cont = cont + 1
		time.sleep(0.5)	

if __name__ == '__main__':

	#Escaneo y creacion de directorios y registro en firebase de las redes wifi
	ledVerde = threading.Thread(target=parpadear,args=(18,))
	ledVerde.start()
	control = controlador.Controlador()
	control.obtenerAps()
	control.crearDirectorios()
	control.guardarEnFirebase()
	ledVerde.do_run = False
	ledVerde.join()
	prenderVerde()

	#Ataque a redes WEP
	ledAmarillo = threading.Thread(target=parpadear,args=(23,))
	ledAmarillo.start()
	redeswep = control.getRedesWep()
	for x in redeswep:
		ataqueWep = wep.Wep(x)
		ataqueWep.atacar()
	ledAmarillo.do_run = False
	ledAmarillo.join()
	prenderAmarillo()

	#Ataque a redes WPA
	ledAzul = threading.Thread(target=parpadear,args=(22,))
	ledAzul.start()
	redesWpa = control.getRedesWpa()
	for x in redesWpa:
		ataqueWpa = wpa.Wpa(x)
		ataqueWpa.atacar()
	ledAzul.do_run = False
	ledAzul.join()
	prenderAzul()
	
	#Ataque a redes WPA2
	ledRojo = threading.Thread(target=parpadear,args=(25,))
	ledRojo.start()
	redesWpa2 = control.getRedesWpa2()
	for x in redesWpa2:
		ataqueWpa2 = wpa2.Wpa2(x)
		ataqueWpa2.atacar()
	ledRojo.do_run = False
	ledRojo.join()
	prenderRojo()
	
	ledBlanco = threading.Thread(target=parpadear,args=(12,))
	ledBlanco.start()
	ledBlanco.do_run = False
	ledBlanco.join()
	prenderBlanco()
	time.sleep(30)
	apagarleds()
	
	
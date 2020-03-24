import commands
import ap 
from firebase import firebase
from wifi import Cell

class Controlador:
	"""docstring for Controlador"""
	def __init__(self):
		self._aps = []
		self._firebase = firebase.FirebaseApplication("https://redes-wireless.firebaseio.com/",None)

	def firebase(self):
		return self._firebase

	def aps(self):
		return self._aps

	def addAp(self,ap):
		self._aps.append(ap)

	#Determina si un AP ya esta guardado en firebase
	def buscarRedFirebase(self,essid):
		redes = self.firebase().get('/redes-wireless/Redes','')
		if not redes == None:
			for x in redes:
				if redes[x]['essid'] == str(essid):
					return True
		return False

	#Guarda las las redes que estan en self._aps no guarda de nuevo las que ya se hayan registrado en firebase	
	def guardarEnFirebase(self):
		for x in self.aps():
			if not self.buscarRedFirebase(x.essid()):
				datos = {'essid':x.essid(),'channel':x.channel(),'bssid':x.bssid(),'tipo':x.tipo(),'contrasena':'sin descifrar'}
				self.firebase().post('/redes-wireless/Redes',datos)

	#escanea las redes wifi disponibles y las cuarda en self._aps
	def obtenerAps(self):
		cell = Cell.all('wlan0')
		for x in xrange(0,len(cell)):
			if self.buscarRedFirebase(str(cell[x].address)) == False:
				essid = str(cell[x].address)
				channel = str(cell[x].channel)
				bssid = str(cell[x].ssid)
				tipo = str(cell[x].encryption_type)
				red = ap.Ap(essid,channel,bssid,tipo)
				self.addAp(red)
	
	#Crea los directorios para los archivos de escaneo para cada AP
	def crearDirectorios(self):	
		for x in self.aps():
			nom = str(x.bssid())
			nom =  nom.replace(" ","_")
			folder = str(nom)
			comando = 'mkdir ./datos/'+folder
			direc = commands.getoutput(comando)
		commands.getoutput('rm -r ./temp/*')	

	#Retorna todas las redes wep cargadas en self._aps
	def getRedesWep(self):
		redesWep = []
		for x in self.aps():
			if x.tipo() == 'wep':
				redesWep.append(x)
		return redesWep

	def getRedesWpa(self):
		redesWep = []
		for x in self.aps():
			if x.tipo() == 'wpa':
				redesWep.append(x)
		return redesWep

		

from firebase import firebase

class Ap:

	def __init__(self,essid,channel,bssid,tipo):
		self._essid = essid
		self._channel = channel
		self._bssid = bssid
		self._tipo = tipo
		self._contrasena = None

	def essid(self):
		return self._essid
		
	def channel(self):
		return self._channel

	def bssid(self):
		return self._bssid

	def tipo(self):
		return self._tipo

	def contrasena(self):
		return self._contrasena
	
	def set_contrasena(self,contrasena):
		self._contrasena = contrasena
		self.guardarContrasenaFirebase()		
	

	def apEqual(self,ap):
		if bssid == ap.bssid:
			return True
		return False

	def guardarContrasenaFirebase(self):
		fire = firebase.FirebaseApplication("https://redes-wireless.firebaseio.com/",None)
		redes = fire.get('/redes-wireless/Redes','')
		for x in redes:
			if str(redes[x]['essid']) == self.essid():
				comando = '/redes-wireless/Redes/'+str(x)
				fire.put(comando,'contrasena',self.contrasena())
				break
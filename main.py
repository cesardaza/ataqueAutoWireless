from logica import controlador,ap,wep,wpa,wpa2

if __name__ == '__main__':
	control = controlador.Controlador()
	control.obtenerAps()
	control.crearDirectorios()
	control.guardarEnFirebase()
	redeswep = control.getRedesWep()
	"""
	for x in redeswep:
		ataqueWep = wep.Wep(x)
		ataqueWep.atacar()

	redesWpa = control.getRedesWpa()
	for x in redesWpa:
		ataqueWpa = wpa.Wpa(x)
		ataqueWpa.atacar()
	"""
	redesWpa2 = control.getRedesWpa2()
	print(len(redesWpa2))
	for x in redesWpa2:
		ataqueWpa2 = wpa2.Wpa2(x)
		ataqueWpa2.atacar()
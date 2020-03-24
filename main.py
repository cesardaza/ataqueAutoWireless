import controlador
import ap
import wep
import wpa

if __name__ == '__main__':
	control = controlador.Controlador()
	control.obtenerAps()
	control.crearDirectorios()
	control.guardarEnFirebase()
	redesWpa = control.getRedesWpa()
	for x in redesWpa:
		ataqueWpa = wpa.Wpa(x)
		ataqueWpa.atacar()
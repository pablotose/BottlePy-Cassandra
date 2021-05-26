from bottle import run, route, get, post, hook, request, redirect, template

from cassandra.cluster import Cluster

cluster = Cluster(['84.122.138.226'])

@hook('before_request')
def strip_trailing_slash():
	request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')


@route('/')
def index():
	session = cluster.connect()
	session.set_keyspace("db")
	q = request.GET.get('q')
	if q:
		query = session.execute("SELECT * from animales where nombre_animal like '{}%'".format(q))
		return template('templates/layout.html', animals = query) 
	else:
		data = session.execute("SELECT * from animales")
		return template('templates/layout.html', animals = data)

@post('/add_animal', method='POST')
def add_animal():
	if request.method == 'POST':
		nombre_animal = str(request.params.get('name_animal'))
		print (nombre_animal)
		localidad = str(request.params.get('localidad'))
		edad_animal = int(request.params.get('edad'))
		tipo_animal = str(request.params.get('tipo'))
		raza_animal = str(request.params.get('raza'))
		telefono_duenno = int(request.params.get('telefono'))
		session = cluster.connect()
		session.set_keyspace("db")
		session.execute("INSERT INTO animales (id_animal, nombre_animal, localidad, edad_animal, tipo_animal, raza_animal, telefono_duenno ) values (now(), '{}','{}',{},'{}','{}',{})".format(nombre_animal, localidad, edad_animal, tipo_animal, raza_animal, telefono_duenno))
	
		return redirect('/')




run(host='localhost', port=8080, debug=True, reloader=True)
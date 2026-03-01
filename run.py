from my_server import app		# importera "app" från huvudpaketet

if __name__ == '__main__':
	app.run(host='localhost', port=8070, debug=True)
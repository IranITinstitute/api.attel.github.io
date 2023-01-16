import qrcode
import base64
from io import BytesIO
from db import loggined



# статик логин по логину и паролю

def static_login(id):
	try:
		if loggined[id] == 'False':
			loggined[id] = 'True'
			return {'status': 'loggined'}

	except:
		return {'status': 'id not exists'}

# создание qr кода для входа

def qr_login(id):
	
	# допилить создание из памяти сразу а не из хеширования файла
	 
	data = f'http://127.0.0.1:42069/api/logon/{id}/confirm/QR?q=confirmation'
	#qrObj = qrcode.QRCode()
	#qrObj.add_data(data)
	#qrObj.make()
	#img = qrObj.make_image(fill_color="red")
	#buffered = BytesIO()
	#img.save(buffered, format="PNG")
	#qrhash = base64.b64encode(buffered.getvalue()).decode("utf-8")
	img = qrcode.make(data)
	img.save("qrc.jpg")	

	with open("qrc.jpg", "rb") as img_qr:
		qrhash = base64.b64encode(img_qr.read()).decode('utf-8')
	s = qrhash
	l = s.split()
	s1 = '+'.join(l)  
	
	return s1
	
# создание статуса активации

def qr_confirm(id, status):
	try:
		if status == 'confirmation':
			if loggined[id] == 'False':
				loggined[id] = 'True'
				return 'confirmed'
	except:
		return {'status': 'confirmation error'}

# фукнция возврата данных логина

def db_list():
	return loggined

# функция логаута

def account_logout(id):
	
	if loggined[id] == 'True':
		loggined[id] = 'False'
		return {id: 'logouts'}


#!/usr/bin/python
# coding: utf-8



# Задание 2: 
# 1) Правильно ли я понимаю что скрипт должен отправлять на сервер методом POST, по пути “server_name/images”, все картинки из переданной ему папки ? 
# 2) Какое количество картинок ожидается в папке ? 
# 3) У всех изображений один формат ? Или могут быть разные форматы ? 

#2.1) да
# 2.2) может много, а может мало. а может их там и нету
# 2.3) можно условиться что там jpg и gif, а остальные не интересны


from flask import Flask
from flask import request
from flask import Response
app = Flask(__name__)

@app.route('/images', methods=['GET', 'POST'])
def entry_point():
	if request.method == 'POST':
		print(request.files.keys())
		return Response(status=201)
	else: 
		return Response(status=201)
	


if __name__ == '__main__':
    app.run(debug=True, port=8001)

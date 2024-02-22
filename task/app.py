from flask import Flask
import redis

app = Flask(__name__)

r = redis.Redis(host='redis', port=6379)

@app.route('/')
def show_info():
    shifr = '20Б0633'
    fullname = r.get(shifr).decode('utf-8')
    
    html_content = f"""
    <html>
    <head><title>Информация о ФИО и шифре</title></head>
    <body>
        <h1>Информация о ФИО и шифре</h1>
        <p>Имя: {fullname}</p>
        <p>Шифр: {shifr}</p>
    </body>
    </html>
    """
    
    return html_content

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
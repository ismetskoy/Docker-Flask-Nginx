from flask import Flask, render_template, request
import requests


app = Flask(__name__)


def check_website(url):
    try:
        full_url = f"https://{url}"
        response = requests.get(full_url)
        if response.status_code == 200:
            return '📡 Online'
        else:
            return f'👿 Ofline: {response.status_code}'
    except requests.exceptions.RequestException as e:
        return f'👿 Ofline: {e}'

@app.route('/')
def monitor():
    websites = ["xatavpn.ru" , "xatadocker.ru" , "xata-grafana.ru"]
    status_list = []
    for url in websites:
        status = check_website(url)
        status_list.append((url, status))
    return render_template('index.html', status_list=status_list)

if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, render_template, request
import requests
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.mail.ru'
app.config['MAIL_PORT'] = 465  
app.config['MAIL_USE_SSL'] = True  


mail = Mail(app)

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
    websites = ["xata-vpn.ru" , "xata-docker.ru" , "xatagrafana.ru"]
    status_list = []
    for url in websites:
        status = check_website(url)
        status_list.append((url, status))
    return render_template('index.html', status_list=status_list)

def send_email(subject, sender, recipients, body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = body
    mail.send(msg)

@app.route('/send_email', methods=['POST'])
def send_email_route():
    subject = request.form['subject']
    sender = request.form['sender']
    recipients = [request.form['recipients']]
    body = request.form['body']
    
    send_email(subject, sender, recipients, body)
    
    back_mail = render_template('email.html', name='Jerry')
    
    return back_mail

if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', port=5000)
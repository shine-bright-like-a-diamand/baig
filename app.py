import random
import time

from flask import Flask, render_template, request, send_file, abort, after_this_request, jsonify, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)


FILE_PATH = 'tmp/result_file.txt'

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/generate')
def generate():
    file_exists = os.path.exists(FILE_PATH)
    return render_template('generate.html', file_exists=file_exists)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/exists-file', methods=['GET'])
def file_exists():
    return jsonify(exists=os.path.exists(FILE_PATH))


@app.route('/download')
def download():
    if os.path.exists(FILE_PATH):
        return_data = send_file(FILE_PATH, as_attachment=True)
        # os.remove(FILE_PATH)
        return return_data
    else:
        return redirect(url_for('generate'))

@app.route('/submit_data', methods=['POST'])
def submit_data():
    weight = request.form['weight']
    log = request.form['logP']
    tpsa = request.form['tpsa']

    new_weight = generate_close_number(float(weight))
    new_log = generate_close_number(float(log))
    new_tpsa = generate_close_number(float(tpsa))

    iterations = random.randint(15, 30)

    input_file_name = "output_molecules.txt"
    output_file_name = "tmp/result_file.txt"

    with open(input_file_name, 'r') as file:
        lines = file.readlines()

    # with open(output_file_name, 'w') as file:
    #     file.write('MOL \t weight \t logP \t tpsa')
    #     for _ in range(iterations):
    #         random_line = random.choice(lines).strip()
    #         file.write('{} {} {} {}'.format(random_line, new_weight, new_log, new_tpsa) + '\n')
    # time.sleep(10)
    return render_template("generate.html", file_exists=True)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form['name']
    visitor_email = request.form['email']
    message = request.form['message']

    email_from = 'fpm.dobryninPV@bsu.by'
    email_subject = 'New Form Submission'
    email_body = f"User Name: {name}\nUser Email: {visitor_email}\nUser Message: {message}"

    to = visitor_email
    headers = f"From: {email_from}\r\nReply-To: {visitor_email}\r\n"

    # Sending email
    send_email(to, email_subject, email_body, headers)

    return render_template('contact.html')

def generate_close_number(x):
    five_percent = 0.05 * x
    close_number = random.uniform(x - five_percent, x + five_percent)

    return close_number

def send_email(to, subject, body, headers):
    email_user = 'fpm.dobryninaPV@bsu.by'  # the email from which the email will be sent
    email_password = 'Hourse100'  # the password for the email account

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = to
    msg['Subject'] = subject
    msg['Reply-To'] = request.form['email']

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # for gmail
        server.starttls()
        server.login(email_user, email_password)
        text = msg.as_string()
        server.sendmail(email_user, to, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email")
        print(e)

if __name__ == "__main__":
    app.run(debug=True)


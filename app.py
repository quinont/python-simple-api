from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)
SERVER_MESSAGES = os.getenv('SERVER_MESSAGES', "localhost:9090")


@app.route('/')
def index():
    messages, err = get_messages()
    if err != "":
        return err, 500
    return render_template('index.html', messages=messages)


@app.route('/add_message', methods=['POST'])
def add_message():
    message = request.form['message']
    response = requests.post(f'http://{SERVER_MESSAGES}/api/messages', data=message)
    if response.status_code == 200:
        return redirect(url_for('index'))
    else:
        return "Error adding message", response.status_code


@app.route('/delete_message/<int:index>', methods=['POST'])
def delete_message(index):
    response = requests.delete(f'http://{SERVER_MESSAGES}/api/messages/{index}')
    if response.status_code == 200:
        return redirect(url_for('index'))
    else:
        return "Error deleting message", response.status_code


@app.route('/update_message/<int:index>', methods=['POST'])
def update_message(index):
    updated_message = request.form['updated_message']
    response = requests.put(f'http://{SERVER_MESSAGES}/api/messages/{index}', data=updated_message)
    if response.status_code == 200:
        return redirect(url_for('index'))
    else:
        return "Error updating message", response.status_code


def get_messages():
    try:
        response = requests.get(f'http://{SERVER_MESSAGES}/api/messages')
        if response.status_code == 200:
            return (response.json(), "")
        return ([], f"ERROR: respuesta del servidor {response.status_code}")
    except Exception as err:
        return ([], f"ERROR: {err}, el server esta prendido?")


if __name__ == '__main__':
    app.run(port=8080, debug=False)

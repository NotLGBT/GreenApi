from flask import Flask, current_app, render_template, request, jsonify, redirect, session, url_for
import requests, os
import json, sql_script

ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.secret_key = "byby"


@app.route('/welcome')
def welcome():
    response = app.make_response(render_template('welcome_page.html'))
    response.headers["Refresh"] = "15; url=http://10.96.0.54:5000/"
    return response

@app.route('/')
def home():
    if session.get('redirected'):
        return render_template('index.html')
    else:
        session['redirected'] = True
        return redirect(url_for('welcome'))
    
@app.route('/api/request', methods=['POST'])
def api_request():
    try:
        data = request.json

        idInstance = os.getenv("idInstance", "----")
        apiTokenInstance = os.getenv("apiTokenInstance", "---------------------------")
        apiUrl = os.getenv("apiUrl", "https://7103.api.greenapi.com")
        currentRequest = data.get("currentRequest", "ErrorRequest")
        payload = data.get("payload", {})
        method = data.get("method", "GET").upper()

        if not all([currentRequest, idInstance, apiTokenInstance, apiUrl]):
            return jsonify({"error": "Missing required parameters"}), 400

        url = f"{apiUrl}/waInstance{idInstance}/{currentRequest}/{apiTokenInstance}"
        print(f"Request URL: {url}")
        print(f"Payload: {payload}")

        response = requests.request(
            method=method,
            url=url,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")


        log_file_path = "./log.json"
        try:

            if os.path.exists(log_file_path):
                with open(log_file_path, "r") as file:
                    try:
                        logs = json.load(file)
                        if not isinstance(logs, list):
                            logs = []  
                    except json.JSONDecodeError:
                        logs = []  
            else:
                logs = []

            logs.append(response.json())

            with open(log_file_path, "w") as file:
                json.dump(logs, file, indent=4, separators=(',', ': '))
        except Exception as log_error:
            print(f"Error logging response: {log_error}")

        
        
        try:
            return jsonify(response.json()), response.status_code
        except ValueError:
            return jsonify({"error": "Invalid JSON in API response", "response": response.text}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500    
    
if __name__ == "__main__":
    context = ('local.crt', 'local.key')  
    app.run(host='0.0.0.0', ssl_context=context)

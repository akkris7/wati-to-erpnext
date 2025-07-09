from flask import Flask, request
import requests
import os

app = Flask(__name__)

@app.route('/wati-webhook', methods=['POST'])
def wati_webhook():
    data = request.json
    print("Received data:", data)

    name = data.get('profile', {}).get('name', 'WhatsApp Lead')
    phone = data.get('waId', 'Unknown')
    message = data.get('text', {}).get('body', 'No message')

    # Payload to send to ERPNext
    payload = {
        "lead_name": name,
        "email_id": f"{phone}@whatsapp.com",
        "phone": phone
    }

    # Headers with ERPNext API key and secret
    headers = {
        "Authorization": "token 24d8381cbb074e5:52a7b6f1b55fc3f",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Send data to ERPNext
    response = requests.post(
        "https://laeldesign-erp.daddara.in/api/method/create_lead",
        json=payload,
        headers=headers
    )

    return {
        "status": "sent to ERP",
        "erp_status": response.status_code,
        "erp_response": response.json()
    }

# Render-compatible server start
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

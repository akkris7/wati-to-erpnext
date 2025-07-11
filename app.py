from flask import Flask, request
import requests
import os

app = Flask(__name__)

@app.route('/wati-webhook', methods=['POST'])
def wati_webhook():
    try:
        data = request.json
        print("✅ Received data from WATI:", data)

        name = data.get('profile', {}).get('name', 'WhatsApp Lead')
        phone = data.get('waId', 'Unknown')

        text_data = data.get('text')
        if isinstance(text_data, dict):
            message = text_data.get('body', 'No message')
        else:
            message = str(text_data) or 'No message'

        payload = {
            "lead_name": name,
            "subject": message,
            "mobile_no": phone,
            "source": "WhatsApp",
            "email_id": f"{phone}@whatsapp.com"
        }

        headers = {
            "Authorization": "token 24d8381cbb074e5:52a7b6f1b55fc3f",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        response = requests.post(
            "https://laeldesign-erp.daddara.in/api/method/create_lead",
            json=payload,
            headers=headers
        )

        print("📤 Sent to ERPNext. Status:", response.status_code)
        print("📨 ERPNext Response:", response.text)

        return {
            "status": "sent to ERP",
            "erp_status": response.status_code,
            "erp_response": response.json()
        }

    except Exception as e:
        print("🔥 Error occurred:", str(e))
        return {"error": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

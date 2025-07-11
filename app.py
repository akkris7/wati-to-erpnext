from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 🔁 Health check route for UptimeRobot and Render
@app.route('/', methods=['GET'])
def health():
    return "OK", 200

# 🔗 Webhook endpoint to receive messages from WATI
@app.route('/wati-webhook', methods=['POST'])
def wati_webhook():
    try:
        data = request.json
        print("✅ Received data from WATI:", data)

        # Extract correct fields from actual WATI payload
        name = data.get('senderName', 'WhatsApp Lead')
        phone = data.get('waId', 'Unknown')
        message = data.get('text', 'No message')

        # Prepare payload for ERPNext lead creation
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

        # Send to ERPNext API
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

# 🌐 Run the app on Render (port binding)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

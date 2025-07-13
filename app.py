from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Health check route to keep the app alive (used by UptimeRobot)
@app.route('/', methods=['GET'])
def health():
    return "OK", 200

# Webhook endpoint for WATI
@app.route('/wati-webhook', methods=['POST'])
def wati_webhook():
    try:
        data = request.json
        print("✅ Received data from WATI:", data)

        # Extract name and phone
        name = data.get('senderName') or data.get('profile', {}).get('name', 'WhatsApp Lead')
        phone = data.get('waId', '').strip()

        # Safety fallback
        if not phone:
            return {"error": "Phone number missing"}, 400

        # ERPNext payload
        payload = {
            "lead_name": name,
            "first_name": name,
            "mobile_no": phone,
            "phone": phone,  # explicitly fill both fields
            "source": "WhatsApp"
        }

        headers = {
            "Authorization": "token 24d8381cbb074e5:52a7b6f1b55fc3f",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Send to ERPNext
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
        print("🔥 Error:", str(e))
        return {"error": str(e)}, 500

# Run the Flask app (for Render compatibility)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

from flask import Blueprint, render_template, request, jsonify
from controller import CoreController

class ChatbotController:
    def __init__(self):
        self.view_base = 'chatbot'

    def index(self):
        return render_template(f'{self.view_base}.html')
    
    @staticmethod
    def send_message():
        core_controller = CoreController()
        print("Headers:", request.headers)
        print("Raw data received:", request.data)

        try:
            data = request.get_json(force=True)
            print("Parsed JSON:", data)
        except Exception as e:
            print("JSON parsing failed:", str(e))
            return jsonify({'error': 'Invalid JSON format'}), 400

        message = data.get('message', '').strip()
        if not message:
            return jsonify({'error': 'No message provided'}), 400

        response = core_controller.conv(message)
        print("Response generated:", response)
        return jsonify({'response': response})

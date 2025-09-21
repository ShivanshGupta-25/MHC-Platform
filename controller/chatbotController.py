from flask import Blueprint, render_template, request, jsonify
from controller import CoreController

class ChatbotController:
    def __init__(self):
        self.core_controller = CoreController()
        self.view_base = 'chatbot'

    def index(self):
        return render_template(f'{self.view_base}.html')
    
    def send_message(self):
        message = request.json.get('message', '')
        print(message)
        print("Received message:", message)
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        response = self.core_controller.conv(message)
        return jsonify({'response': response})

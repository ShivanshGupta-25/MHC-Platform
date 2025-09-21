from flask import Blueprint, render_template, request, jsonify
from controller import CoreController

class ChatbotController:
    def __init__(self):
        self.view_base = 'chatbot'
        self.core_controller = CoreController()  # Initialize CoreController once when the class is instantiated

    def index(self):
        # Renders the main HTML page
        return render_template(f'{self.view_base}.html')
    
    def send_message(self):

        # Log request headers and raw data for debugging
        print("Headers:", request.headers)
        print("Raw data received:", request.data)

        # Try to parse the incoming JSON
        try:
            data = request.get_json(force=True)  # force=True will ignore any content-type issues
            print("Parsed JSON:", data)
        except Exception as e:
            print("JSON parsing failed:", str(e))
            return jsonify({'error': 'Invalid JSON format'}), 400

        # Get the message from the parsed data
        message = data.get('message', '').strip()

        # Check if the message is empty
        if not message:
            return jsonify({'error': 'No message provided'}), 400

        try:
            # Generate response using the CoreController
            response = self.core_controller.conv(message)
            print("Response generated:", response)
        except Exception as e:
            # If there's any issue during message processing, return an error
            print(f"Error during model response generation: {str(e)}")
            return jsonify({'error': 'Error generating response from model'}), 500

        # Return the generated response as a JSON object
        return jsonify({'response': response})

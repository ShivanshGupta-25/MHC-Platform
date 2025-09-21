from controller import (
    HomeController,
    SignupController,
    LoginController,
    DashboardController,
    ChatbotController
)
home_controller = HomeController()
signup_controller = SignupController()
login_controller = LoginController()
dashboard_controller = DashboardController()
chatbot_controller = ChatbotController()

def setupRoute(app):
    app.add_url_rule('/',endpoint='home',view_func=home_controller.index,methods=['GET'])
    app.add_url_rule('/signup',endpoint='signup',view_func=signup_controller.index,methods=['GET'])
    app.add_url_rule('/signup',endpoint='signup.create',view_func=signup_controller.create,methods=['POST'])
    app.add_url_rule('/login',endpoint='login',view_func=login_controller.index,methods=['GET'])
    app.add_url_rule('/login',endpoint='login.store',view_func=login_controller.store,methods=['POST'])
    app.add_url_rule('/dashboard',endpoint='dashboard',view_func=dashboard_controller.index,methods=['GET'])
    app.add_url_rule('/chat',endpoint='chatbot',view_func=chatbot_controller.index,methods=['GET'])
    app.add_url_rule('/chat', endpoint='send_message', view_func=chatbot_controller.send_message, methods=['POST'])


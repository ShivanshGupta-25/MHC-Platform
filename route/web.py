from controller import (
    HomeController,
    SignupController,
    LoginController
)
home_controller = HomeController()
signup_controller = SignupController()
login_controller = LoginController()

def setupRoute(app):
    app.add_url_rule('/',endpoint='home',view_func=home_controller.index,methods=['GET'])
    app.add_url_rule('/signup',endpoint='signup',view_func=signup_controller.index,methods=['GET'])
    app.add_url_rule('/signup',endpoint='signup.create',view_func=signup_controller.create,methods=['POST'])
    app.add_url_rule('/login',endpoint='login',view_func=login_controller.index,methods=['GET'])
    app.add_url_rule('/login',endpoint='login.store',view_func=login_controller.store,methods=['POST'])
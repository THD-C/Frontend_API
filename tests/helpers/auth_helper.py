from src.router.access import Credentials, RegisterData

register_user_1 = RegisterData(username="testTest", password="test321password123", email="x1@gmail.com")

login_user_1 = Credentials(login="testTest", password="test321password123")
email_login_user_1 = Credentials(login="x1@gmail.com", password="test321password123")

login_invalid_login_1 = Credentials(login="tst", password="test321password123")
login_invalid_email_login_1 = Credentials(login="tst@gmail.com", password="test321password123")
login_invalid_password_1 = Credentials(login="testTest", password="testpassword123")

# services.py
from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email, name, otp):
    subject = "Welcome to Flashfund!!!"
    message = f"""Dear {name},

    Thank you for registering with us.

    Please verify your email by entering this OTP:

    Your OTP is: {otp}

    Thank You!!!

    Team FlashFund"""

    from_email = settings.EMAIL_HOST_USER 
    recipient_list = [email]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )

def login_otp_email(email, name, otp):
    subject = "Welcome to Flashfund!!!"
    message = f"""Dear {name},

    Thank you for logging in with us.

    Please enter the OTP for login:

    Your OTP is: {otp}

    Thank You!!!

    Team FlashFund"""

    from_email = settings.EMAIL_HOST_USER 
    recipient_list = [email]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )

# utils/auth_decorators.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

def jwt_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('access_token')
        if not token:
            raise AuthenticationFailed("Authorization token missing in cookies.")

        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            request.user = user
        except Exception as e:
            raise AuthenticationFailed("Invalid or expired token.")

        return view_func(request, *args, **kwargs)
    return _wrapped_view

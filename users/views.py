from .permissions import IsAdminUser
from rest_framework import viewsets,permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from django.core.cache import cache
from django.contrib.auth import authenticate
import random
from .services import send_otp_email,login_otp_email,jwt_login_required
from rest_framework.response import Response
from .models import User, Role,UserPAN
from .serializer import *
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth.hashers import make_password
import requests
import logging
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.utils.decorators import method_decorator

def landing_page(request):
    return render(request, 'landing.html')

def login(request):
    return render(request, 'login.html')

@jwt_login_required
def index(request):
    return render(request, 'index.html')

@jwt_login_required
def schemes(request):
    return render(request, 'scheme.html')

@csrf_exempt
@jwt_login_required
def schemeviewer(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            payload = data.get("payload", {})
            context = payload.get("context")
            message = payload.get("message")
            print("Received context:", context)
            print("Received message:", message) 

            return render(request, "schemeviewer.html", {"context": context, "message": message})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # permission_classes = [IsAdminUser]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsAdminUser()]  # Only admins can list/retrieve/update/delete users

class UserPANViewSet(viewsets.ModelViewSet):
    queryset = UserPAN.objects.all()
    serializer_class = UserPANSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return UserPAN.objects.none()
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return UserPAN.objects.all()  # Admins see all
        return UserPAN.objects.filter(user=user)

    def perform_create(self, serializer):
        # Automatically set the user to the current user
        serializer.save(user=self.request.user)

class SendOTPView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view
    def post(self, request):
        email = request.data.get('email'    )
        name = request.data.get('name')
        password = request.data.get('password')
        username = request.data.get('username')
        phone = request.data.get('phone')

        if not email or not name or not password or not username or not phone:
            return Response({"error": "All Fieds are required."}, status=400)
        
        try:
            user=User.objects.get(email=email)
            return Response({"error": "User already exists."}, status=400)
        except User.DoesNotExist:
            
            otp = str(random.randint(100000, 999999))
            cache.set(f'otp_{email}', otp, timeout=300)
            user_data = {
                "email": email,
                "name": name,
                "password": make_password(password),
                "username": username,
                "phone": phone,
                "role": 1,  # Assuming role ID 1 is for 'client'
            }
            cache.set(f'data_{email}', json.dumps(user_data), timeout=300)
           
            print(f"OTP for {email}: {otp}")

            try:
                send_otp_email(email=email, name=name, otp=otp)
                return Response({"message": "OTP sent successfully."}, status=200)
            except Exception as e:
                return Response({"error": str(e)}, status=500)

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_input = request.data.get('otp')

        if not email or not otp_input:
            return Response({"error": "Email and OTP are required."}, status=400)

        cached_otp = cache.get(f'otp_{email}')
        user_data_json = cache.get(f'data_{email}')

        if not cached_otp or cached_otp != otp_input:
            return Response({"error": "Invalid or expired OTP."}, status=400)

        if not user_data_json:
            return Response({"error": "User data expired or missing."}, status=400)

        user_data = json.loads(user_data_json)

        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f'otp_{email}')
            cache.delete(f'data_{email}')
            return Response({"message": "User registered successfully.", "user": serializer.data}, status=201)
        else:
            return Response(serializer.errors, status=400)

#Login
@method_decorator(csrf_exempt, name='dispatch')
class LoginOTPView(APIView):
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({"error": "Email and password are required."}, status=400)
        
        
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({"error": "Invalid email or password."}, status=401)
        
        name=user.name

        # Generate and cache OTP (expires in 5 minutes)
        otp = str(random.randint(100000, 999999))
        cache.set(f'login_otp_{email}', otp, timeout=300)
        cache.set(f'login_email_{otp}', email, timeout=300)
        print(f"OTP for {email}: {otp}")

        try:
            login_otp_email(email=email, name=name, otp=otp)
            return Response({"message": "OTP sent successfully"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        



User = get_user_model()

class VerifyLoginOTPView(APIView):
    def post(self, request):
        otp_input = request.data.get('otp')

        if not otp_input:
            return Response({"error": "OTP is required."}, status=400)

        email = cache.get(f'login_email_{otp_input}')
        if not email:
            return Response({"error": "Invalid or expired OTP."}, status=400)

        cached_otp = cache.get(f'login_otp_{email}')
        if cached_otp != otp_input:
            return Response({"error": "Incorrect OTP."}, status=400)

        try:
            user = User.objects.get(email=email)

            # Generate JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Clean up
            cache.delete(f'login_email_{otp_input}')
            cache.delete(f'login_otp_{email}')

            response=JsonResponse({
                "message": "Login successful.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name
                },
                "access_token": access_token,
                "refresh_token": str(refresh)
            })
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # Set to True in production (HTTPS)
                samesite='Lax'
            )
            return response
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)
        
# views.py



class PANRegisterView(APIView):
    def post(self, request):
        serializer = UserPANSerializer(data=request.data)
        if serializer.is_valid():
            # Save PAN to DB
            pan_record = serializer.save(user=request.user)
            transaction_id = str(uuid.uuid4())
            message_id = str(uuid.uuid4())  
            # Step 1: Hit API 1
            ondc_url = 'https://investment.preprod.vyable.in/ondc/search/'
            api_1_response = requests.post(ondc_url, json={"transaction_id": transaction_id,"message_id":message_id})
            if api_1_response.status_code != 200:
                return Response({"error": "Failed at API 1"}, status=400)
            
            

            # Extract bpp_id and bpp_uri from response
            try:
                context = api_1_response.json()["context"]
                bpp_id = context["bpp_id"]
                bpp_uri = context["bpp_uri"]
            except (KeyError, TypeError):
                return Response({"error": "Invalid ONDC response structure"}, status=500)


            ondc_2_url = "https://investment.preprod.vyable.in/ondc/select/"
            api_2_payload = {
                "transaction_id": transaction_id,
                "bpp_id": bpp_id,
                "bpp_uri": bpp_uri,
            }
            api_2_response = requests.post(ondc_2_url, json=api_2_payload)

            if api_2_response.status_code != 200:
                return Response({"error": "Failed at API 2"}, status=400)

            api_2_json = api_2_response.json()

            try:
                form_link = api_2_json["message"]["order"]["xinput"]["form"]["url"]
            except KeyError:
                return Response({"error": "Form link not found in API 2 response"}, status=500)
            return Response({"form_link": form_link}, status=200)

        return Response(serializer.errors, status=400)



class PersonalDetailsViewSet(viewsets.ModelViewSet):
    queryset = PersonalDetails.objects.all()
    serializer_class = PersonalDetailsSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
                 return UserPAN.objects.none()
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return PersonalDetails.objects.all()
        return PersonalDetails.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NomineeViewSet(viewsets.ModelViewSet):
    queryset = Nominee.objects.all()
    serializer_class = NomineeSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        
        user = self.request.user
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class PayoutBankAccountViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PayoutBankAccountSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
             return UserPAN.objects.none()
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return PayoutBankAccount.objects.all()
        return PayoutBankAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class CommunicationPhoneViewSet(viewsets.ModelViewSet):
    serializer_class = CommunicationPhoneSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return UserPAN.objects.none()
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return CommunicationPhone.objects.all()
        return CommunicationPhone.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommunicationEmailViewSet(viewsets.ModelViewSet):
    serializer_class = CommunicationEmailSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return UserPAN.objects.none()
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return CommunicationEmail.objects.all()
        return CommunicationEmail.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommunicationDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = CommunicationDetailsSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return UserPAN.objects.none()
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return  CommunicationDetails.objects.all()
        return CommunicationDetails.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#ondc search

class SearchView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        ondc_url = 'https://investment.preprod.vyable.in/ondc/search/'
        try:
            response=requests.post(ondc_url, json=request.data)
            return Response(response.json(), status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
class SearchDataView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        ondc_url = 'https://investment.preprod.vyable.in/ondc/on_searchdata'
        try:
            response=requests.post(ondc_url,json=request.data,headers={'Authorization': request.headers.get('Authorization'),
                'Content-Type': 'application/json'})
            response.raise_for_status() 
            return Response(response.json(), status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"ONDC API error: {str(e)}"}, status=502)
        except Exception as e:
            return Response({'error': f'Server error: {str(e)}'}, status=500)
    


class SIPView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        ondc_url = 'https://investment.staging.flashfund.in/ondc/select/'
        try:
            response=requests.post(ondc_url, json=request.data)
            return Response(response.json(), status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
        

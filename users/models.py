from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.core.validators import RegexValidator

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not role:
            raise ValueError("User must have a role")  # <- raise error if not supplied

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, role=role, **extra_fields)  # <- assign role here
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None,phone=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('phone', phone)

        if not phone:
            raise ValueError('Superuser must have a phone number')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        try:
            role = Role.objects.get(name='admin')
        except Role.DoesNotExist:
            raise ValueError("Role 'admin' does not exist. Create it first.")

        extra_fields['phone'] = phone
        extra_fields['role'] = role  # ✅ pass role here

        return self.create_user(email=email, username=username, password=password, **extra_fields)


pan_validator = RegexValidator(
    regex=r'^[A-Z]{5}[0-9]{4}[A-Z]$',
    message="Enter a valid PAN number (e.g., ABCDE1234F)."
)



class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True, db_index=True)
    phone = models.BigIntegerField()
    name = models.CharField(max_length=30, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users',default=None)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone']

    def __str__(self):
        return self.username


    

class UserPAN(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_pan')
    pan_number = models.CharField(max_length=10, validators=[pan_validator], unique=True)
    dob= models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.pan_number}"
    

class Gender(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class MaritalStatus(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Occupation(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class SourceOfWealth(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class IncomeRange(models.Model):
    range = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=50)  # optional for display label

    def __str__(self):
        return self.label


class Country(models.Model):
    code = models.CharField(max_length=2, unique=True)  # e.g., 'IN', 'US'
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    




class PersonalDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_personal')
    pan=models.CharField(max_length=10, validators=[pan_validator], unique=True,db_index=True)
    dob=models.DateField()
    last_4_digis=models.CharField(max_length=4)

    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.SET_NULL, null=True)
    occupation = models.ForeignKey(Occupation, on_delete=models.SET_NULL, null=True)
    source_of_wealth = models.ForeignKey(SourceOfWealth, on_delete=models.SET_NULL, null=True)
    income_range = models.ForeignKey(IncomeRange, on_delete=models.SET_NULL, null=True)

    father_name = models.CharField(max_length=255, blank=True)
    spouse_name = models.CharField(max_length=255, blank=True)
    mother_name = models.CharField(max_length=255, blank=True)

    cob =  models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='personaldetails_cob')
    pob = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True,related_name='personaldetails_pob')
    nationality =  models.ForeignKey(Country, on_delete=models.SET_NULL, null=True,related_name='personaldetails_nationality')
    citizenships = models.JSONField(default=list)

    def __str__(self):
        return self.user.name
    
class AddressNature(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class BelongsTo(models.Model):
    label = models.CharField(max_length=50, unique=True)  # e.g., Self, Spouse, Guardian, etc.

    def __str__(self):
        return self.label

class CommunicationPhone(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='comm_phone')
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE)
    number = models.BigIntegerField()
    belongs_to = models.ForeignKey(BelongsTo, on_delete=models.SET_NULL, null=True)

class CommunicationEmail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='comm_email')
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE)
    email = models.EmailField()
    belongs_to = models.ForeignKey(BelongsTo, on_delete=models.SET_NULL, null=True)

class CommunicationDetails(models.Model):
    user=  models.OneToOneField(User, on_delete=models.CASCADE, related_name='communication_detail')
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE)
    address=models.CharField(max_length=255)
    pincode=models.CharField(max_length=6)
    address_country=models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    address_nature=models.ForeignKey(AddressNature, on_delete=models.SET_NULL, null=True)

class Relationship(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., Spouse, Child, etc.

    def __str__(self):
        return self.name


class Guardian(models.Model):
    name = models.CharField(max_length=100)
    pan = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Nominee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nominees')
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pan = models.CharField(max_length=10)
    dob = models.DateField()
    relationship = models.ForeignKey(Relationship, on_delete=models.SET_NULL, null=True)
    guardian = models.ForeignKey(Guardian, on_delete=models.SET_NULL, null=True, blank=True)
    allocation_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Example: 33.33

    def __str__(self):
        return f"{self.name} ({self.allocation_percentage}%)"
    


class BankAccountType(models.Model):
    name = models.CharField(max_length=30, unique=True)  # e.g., 'Savings', 'Current'

    def __str__(self):
        return self.name

class PayoutBankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payout_accounts')
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=30)
    primary_holder_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=11,validators=[RegexValidator(regex=r'^[A-Z]{4}0[A-Z0-9]{6}$',message='Enter a valid 11-character IFSC code.')])
    account_type = models.ForeignKey(BankAccountType, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.primary_holder_name} - {self.account_number}"
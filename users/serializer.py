from rest_framework import serializers
from .models import *

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'name', 'role','password','is_active', 'is_staff']
        read_only_fields = ['id', 'is_staff']

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        user = User(role=role, **validated_data)
        user.set_password(password)  # ✅ Hash the password
        user.save()
        return user
    
class UserPANSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserPAN
        fields = ['user', 'pan_number', 'dob']

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'name']

class MaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaritalStatus
        fields = ['id', 'name']

class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = ['id', 'name']

class SourceOfWealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceOfWealth
        fields = ['id', 'name']

class IncomeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeRange
        fields = ['id', 'range', 'label']


class PersonalDetailsSerializer(serializers.ModelSerializer):
    gender = GenderSerializer(read_only=True)
    gender_id = serializers.PrimaryKeyRelatedField(
        queryset=Gender.objects.all(), source='gender', write_only=True
    )
    marital_status = MaritalStatusSerializer(read_only=True)
    marital_status_id = serializers.PrimaryKeyRelatedField(
        queryset=MaritalStatus.objects.all(), source='marital_status', write_only=True
    )
    occupation = OccupationSerializer(read_only=True)
    occupation_id = serializers.PrimaryKeyRelatedField(
        queryset=Occupation.objects.all(), source='occupation', write_only=True
    )
    source_of_wealth = SourceOfWealthSerializer(read_only=True)
    source_of_wealth_id = serializers.PrimaryKeyRelatedField(
        queryset=SourceOfWealth.objects.all(), source='source_of_wealth', write_only=True
    )
    income_range = IncomeRangeSerializer(read_only=True)
    income_range_id = serializers.PrimaryKeyRelatedField(
        queryset=IncomeRange.objects.all(), source='income_range', write_only=True
    )

    user = serializers.StringRelatedField()  # shows user.__str__ (likely username)

    class Meta:
        model = PersonalDetails
        fields = [
            'user', 'pan', 'dob', 'last_4_digis',
            'gender', 'gender_id',
            'marital_status', 'marital_status_id',
            'occupation', 'occupation_id',
            'source_of_wealth', 'source_of_wealth_id',
            'income_range', 'income_range_id',
            'father_name', 'spouse_name', 'mother_name',
            'cob', 'pob', 'nationality', 'citizenships',
        ]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['code', 'name']


class AddressNatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressNature
        fields = ['id', 'name']


class BelongsToSerializer(serializers.ModelSerializer):
    class Meta:
        model = BelongsTo
        fields = ['id', 'label']


class CommunicationPhoneSerializer(serializers.ModelSerializer):
    belongs_to = BelongsToSerializer()

    class Meta:
        model = CommunicationPhone
        fields = ['number', 'belongs_to']

    def create(self, validated_data):
        belongs_to_data = validated_data.pop('belongs_to')
        belongs_to, _ = BelongsTo.objects.get_or_create(**belongs_to_data)
        return CommunicationPhone.objects.create(belongs_to=belongs_to, **validated_data)


class CommunicationEmailSerializer(serializers.ModelSerializer):
    belongs_to = BelongsToSerializer()

    class Meta:
        model = CommunicationEmail
        fields = ['address', 'belongs_to']

    def create(self, validated_data):
        belongs_to_data = validated_data.pop('belongs_to')
        belongs_to, _ = BelongsTo.objects.get_or_create(**belongs_to_data)
        return CommunicationEmail.objects.create(belongs_to=belongs_to, **validated_data)


class CommunicationDetailsSerializer(serializers.ModelSerializer):
    address_country = CountrySerializer()
    address_nature = AddressNatureSerializer()

    class Meta:
        model = CommunicationDetails
        fields = ['address', 'pincode', 'address_country', 'address_nature']

    def create(self, validated_data):
        country_data = validated_data.pop('address_country')
        nature_data = validated_data.pop('address_nature')

        country, _ = Country.objects.get_or_create(**country_data)
        nature, _ = AddressNature.objects.get_or_create(**nature_data)

        return CommunicationDetails.objects.create(
            address_country=country,
            address_nature=nature,
            **validated_data
        )

class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = ['id', 'name', 'pan']


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['id', 'name']


class NomineeSerializer(serializers.ModelSerializer):
    guardian = GuardianSerializer(required=False, allow_null=True)
    relationship = RelationshipSerializer()

    class Meta:
        model = Nominee
        fields = [
            'id',
            'user',
            'name',
            'pan',
            'dob',
            'relationship',
            'guardian',
            'allocation_percentage',
        ]

    def create(self, validated_data):
        relationship_data = validated_data.pop('relationship')
        guardian_data = validated_data.pop('guardian', None)

        # Retrieve or create Relationship instance
        relationship, _ = Relationship.objects.get_or_create(**relationship_data)

        # Retrieve or create Guardian instance if provided
        guardian = None
        if guardian_data:
            guardian, _ = Guardian.objects.get_or_create(**guardian_data)

        nominee = Nominee.objects.create(
            relationship=relationship,
            guardian=guardian,
            **validated_data
        )
        return nominee

    def update(self, instance, validated_data):
        relationship_data = validated_data.pop('relationship', None)
        guardian_data = validated_data.pop('guardian', None)

        if relationship_data:
            relationship, _ = Relationship.objects.get_or_create(**relationship_data)
            instance.relationship = relationship

        if guardian_data is not None:
            if guardian_data:
                guardian, _ = Guardian.objects.get_or_create(**guardian_data)
                instance.guardian = guardian
            else:
                instance.guardian = None

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    

class BankAccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccountType
        fields = ['id', 'name']

class PayoutBankAccountSerializer(serializers.ModelSerializer):
    account_type = BankAccountTypeSerializer()

    class Meta:
        model = PayoutBankAccount
        fields = ['id', 'account_number', 'primary_holder_name', 'ifsc_code', 'account_type']

    def create(self, validated_data):
        account_type_data = validated_data.pop('account_type')
        account_type, _ = BankAccountType.objects.get_or_create(**account_type_data)
        return PayoutBankAccount.objects.create(account_type=account_type, **validated_data)

    def update(self, instance, validated_data):
        account_type_data = validated_data.pop('account_type', None)
        if account_type_data:
            account_type, _ = BankAccountType.objects.get_or_create(**account_type_data)
            instance.account_type = account_type
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class BankAccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccountType
        fields = ['id', 'name']

class PayoutBankAccountSerializer(serializers.ModelSerializer):
    account_type = BankAccountTypeSerializer()

    class Meta:
        model = PayoutBankAccount
        fields = ['id', 'account_number', 'primary_holder_name', 'ifsc_code', 'account_type']

    def create(self, validated_data):
        account_type_data = validated_data.pop('account_type')
        account_type, _ = BankAccountType.objects.get_or_create(**account_type_data)
        return PayoutBankAccount.objects.create(account_type=account_type, **validated_data)

    def update(self, instance, validated_data):
        account_type_data = validated_data.pop('account_type', None)
        if account_type_data:
            account_type, _ = BankAccountType.objects.get_or_create(**account_type_data)
            instance.account_type = account_type
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class AddressNatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressNature
        fields = ['id', 'name']

class BelongsToSerializer(serializers.ModelSerializer):
    class Meta:
        model = BelongsTo
        fields = ['id', 'label']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'code', 'name']

class CommunicationPhoneSerializer(serializers.ModelSerializer):
    belongs_to = BelongsToSerializer(read_only=True)
    belongs_to_id = serializers.PrimaryKeyRelatedField(
        queryset=BelongsTo.objects.all(), source='belongs_to', write_only=True
    )
    
    class Meta:
        model = CommunicationPhone
        fields = ['id', 'user', 'number', 'belongs_to', 'belongs_to_id']
        read_only_fields = ['user']

class CommunicationEmailSerializer(serializers.ModelSerializer):
    belongs_to = BelongsToSerializer(read_only=True)
    belongs_to_id = serializers.PrimaryKeyRelatedField(
        queryset=BelongsTo.objects.all(), source='belongs_to', write_only=True
    )
    
    class Meta:
        model = CommunicationEmail
        fields = ['id', 'user', 'address', 'belongs_to', 'belongs_to_id']
        read_only_fields = ['user']

class CommunicationDetailsSerializer(serializers.ModelSerializer):
    address_nature = AddressNatureSerializer(read_only=True)
    address_nature_id = serializers.PrimaryKeyRelatedField(
        queryset=AddressNature.objects.all(), source='address_nature', write_only=True
    )
    address_country = CountrySerializer(read_only=True)
    address_country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), source='address_country', write_only=True
    )
    
    class Meta:
        model = CommunicationDetails
        fields = ['id', 'user', 'address', 'pincode', 'address_country', 'address_country_id', 'address_nature', 'address_nature_id']
        read_only_fields = ['user']
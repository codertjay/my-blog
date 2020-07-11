from random import Random
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    ModelSerializer, EmailField, CharField
)
from django.contrib.auth import get_user_model

User = get_user_model()


# we are using the serializer in our comment detail serializer
class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
    email2 = EmailField(label='Confirm Email')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',

        ]
        # this is to prevent us from seeing the password
        extra_kwargs = {'password': {'write_only': True}}


    def validate_email(self, value):
        data = self.get_initial()
        email2 = data.get('email2')
        email1 = value
        if email2 != email1:
            raise ValidationError('Emails must match. ')
        user_qs = User.objects.filter(email=email1)
        if user_qs.exists():
            raise ValidationError('This user has been registered.  ')
        return value

    """ we are validating the email2 """

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value
        if email1 != email2:
            raise ValidationError('Emails must match. ')
        return value

    """ in here we are getting the validated data before we create the user"""

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username,
            email=email,
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    username = CharField(required=False, allow_blank=True)
    email = EmailField(required=False, allow_blank=True)
    token = CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',

        ]
        # this is to prevent us from seeing the password
        extra_kwargs = {'password': {'write_only': True}}

    """ he did this last this is another way of doing validation
    and below is another method  i prefer this method """

    def validate(self, data):
        user_obj = None
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password')
        if not email and not username:
            raise ValidationError('A username or email must be required. ')

        # to pck only one meaning of distinct
        user = User.objects.filter(
            Q(email=email) |
            Q(username=username)).distinct()
        # to prevent error from users with no email
        user = user.exclude(email__isnull=True).exclude(email__iexact='')

        if user.exists() and user.count() == 1:
            user_obj = user.first()
            print(user_obj)
        else:
            raise ValidationError('This username/email is not valid  ')
        if user_obj:
            if not user_obj.check_password(password):
                # checking if the user have input his password
                raise ValidationError("Incorrect credentials please try again ")
        data['token'] = "some random token "
        return data

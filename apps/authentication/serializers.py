from rest_framework import serializers 
from .models import User 
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""
    # Ensure email is provided and is unique
    email = serializers.EmailField(
        required=True,
        allow_null=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Email already exist",
            )
        ],
        error_messages={
            'required': "Email is a required field",
        }
    )
 
    # characters, and can not be read by the client.
    password = serializers.CharField(
            required=True,
            allow_null=False,
            write_only=True,
            min_length=6,
    )
    confirm_password = serializers.CharField(
            write_only=True,
            required=True,
            allow_null=False,
            min_length=6,)
    user_name = serializers.CharField(
            required=True,
            allow_null=False,
            min_length=2,
            validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Username already exist",
            )
        ],
        error_messages={
            'required': "Username is a required field",
        }
    )
    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(read_only=True)

    @staticmethod
    def validate_password_(data):
        password = data.get('password', None)
        confirm_password = data.get('password', None)
        # As mentioned above, an user_name is required. Raise an exception if an
        # user_name is not provided.
        # As mentioned above, a password is required. Raise an exception if a
        # password is not provided.
        if confirm_password != password:
            raise serializers.ValidationError(
                'Confirmed Password and Password should match .'
            )
        return data 

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['user_name', 'email',
                  'password','confirm_password','is_supervisor','is_manager','is_reportee',  'token']
    @classmethod
    def create(self, data):
        del data["confirm_password"]
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**data)

class LoginSerializer(serializers.Serializer):
    """Login serializer Class"""
    user_name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    @staticmethod
    def validate(data):
        user_name = data.get('user_name', None)
        password = data.get('password', None)
        # As mentioned above, an user_name is required. Raise an exception if an
        # user_name is not provided.
        if user_name is None:
            raise serializers.ValidationError(
                'An user_name is required to log in.'
            )
        # As mentioned above, a password is required. Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this user_name/password combination. Notice how
        # we pass `user_name` as the `username` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `user_name`.
        user = authenticate(user_name=user_name, password=password)
        # If no user was found matching this user_name/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this user_name and password was not found.'
            )
        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'user_name': user.user_name,
            'email':user.email,
            'token': user.token,
        }
         
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny  # Import AllowAny for open access to login
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from api.dto.user_dto import UserDTO  # Assuming you are using DTOs for user

class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]  # Allows access without authentication

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        # Extract username and password from the request
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        # If authentication fails
        if user is None:
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Prepare user data for the response
        user_data = {
            'username': user.username,
            'user_type': user.user_type,  # Ensure the user model has this field
            # Add any other fields you want to return, such as email, first_name, etc.
        }

        # Return the response with the access token, refresh token, and user info
        return Response({
            'access_token': access_token,
            'refresh_token': str(refresh),
            'user': user_data
        }, status=status.HTTP_200_OK)

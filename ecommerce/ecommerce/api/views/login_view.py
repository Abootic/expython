from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from api.dto.user_dto import UserDTO

class LoginViewSet(viewsets.ViewSet):
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
            'user_type': user.user_type,  # Include any additional user data here
        }

        # Return the response with the access token and user info
        return Response({
            'access_token': access_token,
            'refresh_token': str(refresh),
            'user': user_data
        }, status=status.HTTP_200_OK)

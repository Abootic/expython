from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.factories.service_factory import create_user_service
from api.dto.user_dto import UserDTO
from api.permissions.permissions import RoleRequiredPermission
from rest_framework import status
from rest_framework.decorators import action


class UserViewSet(viewsets.ViewSet):
    required_roles = ['ADMIN']  # Define required roles for this view

    def get_permissions(self):
        permission_classes = [IsAuthenticated, RoleRequiredPermission]
        return [permission() for permission in permission_classes]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = create_user_service()

    def list(self, request):
        # List all users
        users = self.user_service.all()
        return Response([user.to_dict() for user in users])

    def retrieve(self, request, pk=None):
        user_dto = self.user_service.get_user_by_id(pk)
        if user_dto:
            return Response(user_dto.to_dict())
        return Response({"error": "User not found"}, status=404)

    def create(self, request):
        user_dto = UserDTO(
            username=request.data.get('username'),
            user_type=request.data.get('user_type'),
            email=request.data.get('email'),
            password=request.data.get('password')
        )
        created_user = self.user_service.create_user(user_dto)
        return Response(created_user.to_dict(), status=201)

    def update(self, request, pk=None):
        user_dto = UserDTO(
            id=pk,
            username=request.data.get('username'),
            user_type=request.data.get('user_type'),
            email=request.data.get('email'),
            password=request.data.get('password')
        )
        updated_user = self.user_service.update_user(user_dto)
        if updated_user:
            return Response(updated_user.to_dict())
        return Response({"error": "User not found"}, status=404)

    def destroy(self, request, pk=None):
        success = self.user_service.delete_user(pk)
        if success:
            return Response({"message": "User deleted"}, status=204)
        return Response({"error": "User not found"}, status=404)

    @action(detail=True, methods=['put'], url_path='update-role')
    def update_role(self, request, pk=None):
        new_role = request.data.get('user_type')
        if not new_role:
            return Response({"error": "Role is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Call the service to update the user's role (no role validation in view)
        try:
            updated_user = self.user_service.update_user_role(pk, new_role)
            return Response({"message": f"User role updated to {updated_user.user_type}"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

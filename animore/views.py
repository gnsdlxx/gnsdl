from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


User = get_user_model()

class SignupView(CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([AllowAny])
def Login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        # 'None' 문자열이 반환되는 경우에 대한 처리
        if serializer.validated_data['email'] == "None":
            return Response({"message": 'fail'}, status=status.HTTP_200_OK)
            
        response = {
            'success': True,
            'token': serializer.data['token']
        }
        return Response(response, status=status.HTTP_200_OK)
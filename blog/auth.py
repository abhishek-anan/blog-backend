from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
import jwt
from django.utils.timezone import datetime
from django.utils import timezone
from django.utils.timezone import timedelta
from django.contrib.auth.hashers import check_password


# check token
def validate_token(func):
    def inner(request, *args, **kwargs):
        if request.headers and request.headers.get('Authorization'):
            encoded = request.headers.get('Authorization')
            if encoded.startswith("Bearer "):
                token = encoded[7:len(encoded):1]
                header_data = jwt.get_unverified_header(token)
                try:
                    user = jwt.decode(
                        token, 'secret', algorithms=[header_data['alg']], options={'require': ['exp', 'iat']})
                    if User.objects.get(email=user['email']).token == token:
                        return func(request, *args, **kwargs)
                    return Response({'data': {"message": "Invalid Token"}, 'api_status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
                except jwt.ExpiredSignatureError:
                    return Response({'data': {"message": "Token expired"}, 'api_status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
                except Exception as e:
                    return Response({'data': {"message": "Invalid Token"}, 'api_status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'data': {"message": "Access token is not in correct format"}, 'api_status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'data': {"message": "Token not available"}, 'api_status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
    return inner


# login api
@api_view(['POST'])
def login_view(request):
    try:
        data = request.data
        email = data.get('email')
        password = data.get('password')
        if email and not password:
            return Response({'data': {"errors": {'password': 'password is required!'}}, }, status=status.HTTP_400_BAD_REQUEST)
        if not email and password:
            return Response({'data': {"errors": {'email': 'email is required!'}}, }, status=status.HTTP_400_BAD_REQUEST)
        if not (email and password):
            return Response({'data': {"errors": {'email': 'email is required!', 'password': 'password is required!'}}, }, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=email)
        pwd_valid = check_password(password, user.password)
        if pwd_valid:
            serializer = UserSerializer(user)
            dt = datetime.now(tz=timezone.utc)+timedelta(hours=11124)
            token = jwt.encode({'id': serializer.data['id'], 'name': serializer.data['name'],
                                'email': serializer.data['email'], 'mobile': serializer.data['mobile'], 'exp': dt, 'iat': datetime.now(tz=timezone.utc)}, "secret", algorithm="HS256")
            user.token = token
            user.save()
            return Response({'data': {"message": "login successfully!", 'token': token}, }, status=status.HTTP_200_OK)
        else:
            return Response({'data': {"message": "email/password not matched!"}, }, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'data': {'message': 'email not found!'}, }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'data': {"message": "Something went wrong!"}, }, status=status.HTTP_400_BAD_REQUEST)

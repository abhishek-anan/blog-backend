from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from .auth import validate_token
from django.core.exceptions import ValidationError


# user api
@api_view(['GET'])
@validate_token
def get_users(request):
    try:
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response({'data': {'data': serializer.data}, 'total': len(serializer.data), 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_user(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {"message": "User created successfully!", 'data': serializer.data}, 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({'data': {"message": "Something went wrong!", "errors": serializer.errors}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@validate_token
def update_user(request, id):
    try:
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {"message": "User detail update successfully!", 'data': serializer.data}, 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({'data': {"message": "Something went wrong!", 'errors': serializer.errors}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'data': {"message": "No user found"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError:
        return Response({'data': {"message": "Invalid id!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@validate_token
def remove_user(request, id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        return Response({'data': {"message": "User remove successfully!"}, 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'data': {"message": "No user found"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError:
        return Response({'data': {"message": "Invalid id!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

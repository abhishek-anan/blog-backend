from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TagSerializer
from .models import Tag
from .auth import validate_token
from rest_framework import status
from django.core.exceptions import ValidationError


# Tag api
@api_view(['GET'])
# @validate_token
def get_tags(request):
    try:
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response({'data': {'data': serializer.data}, 'total': len(serializer.data), 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@validate_token
def create_tag(request):
    try:
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {"message": "Tag created successfully!", 'data': serializer.data}, 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({'data': {"message": "Something went wrong!", 'errors': serializer.errors}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@validate_token
def update_tag(request, id):
    try:
        queryset = Tag.objects.get(id=id)
        serializer = TagSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {"message": "Tag detail update successfully!", 'data': serializer.data}, 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({'data': {"message": "Something went wrong!", 'errors': serializer.errors}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Tag.DoesNotExist:
        return Response({'data': {"message": "Tag not found", 'api_status': status.HTTP_400_BAD_REQUEST}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError:
        return Response({'data': {"message": "Invalid id!", 'api_status': status.HTTP_400_BAD_REQUEST}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@validate_token
def remove_tag(request, id):
    try:
        tag = Tag.objects.get(id=id)
        tag.delete()
        return Response({'data': {"message": "Tag removed successfully!"}, 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Tag.DoesNotExist:
        return Response({'data': {"message": "Tag not found", 'api_status': status.HTTP_400_BAD_REQUEST}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError:
        return Response({'data': {"message": "Invalid id!", 'api_status': status.HTTP_400_BAD_REQUEST}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

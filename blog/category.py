from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer
from .models import Category
from .auth import validate_token
from rest_framework import status
from django.core.exceptions import ValidationError


# caegory api
@api_view(['GET'])
# @validate_token
def get_categories(request):
    try:
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response({'data': {'data': serializer.data}, 'total': len(serializer.data), 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@validate_token
def create_category(request):
    try:
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {"message": "Category created successfully!", 'data': serializer.data}, 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({'data': {"message": "Something went wrong!", 'errors': serializer.errors}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@validate_token
def update_category(request, id):
    try:
        queryset = Category.objects.get(id=id)
        serializer = CategorySerializer(
            queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {"message": "Category detail update successfully!", 'data': serializer.data}, 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({'data': {"message": "Something went wrong!", 'errors': serializer.errors}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Category.DoesNotExist:
        return Response({'data': {"message": "category not found", 'api_status': status.HTTP_400_BAD_REQUEST}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError:
        return Response({'data': {"message": "Invalid id!", 'api_status': status.HTTP_400_BAD_REQUEST}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@validate_token
def remove_category(request, id):
    try:
        category = Category.objects.get(id=id)
        category.delete()
        return Response({'data': {"message": "Category removed successfully!"}, 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        return Response({'data': {"message": "Category not found", 'api_status': status.HTTP_400_BAD_REQUEST}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError:
        return Response({'data': {"message": "Invalid id!", 'api_status': status.HTTP_400_BAD_REQUEST}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

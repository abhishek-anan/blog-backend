from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BlogSerializer, BlogDetailSerializer
from .models import Blog, BlogDetail
from .auth import validate_token
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db.models import F
# from itertools import chain


# blog api
@api_view(['GET'])
# @validate_token
def get_blogs(request):
    try:
        print(request)
        data_obj = Blog.objects.filter().annotate(category_name=F('category__name'), user_name=F('user__name')).values(
            'id', 'title', 'image', 'sub_desc', 'created', 'category_name', 'user_name')
        data = data_obj.order_by('-created')
        data_count = data_obj.count()
        return Response({'data': {'data': data, 'total': data_count}, 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @validate_token
def get_curr_blog(request, id):
    try:
        data_obj = Blog.objects.filter(id=id).annotate(category_name=F('category__name'), user_name=F('user__name')).values(
            'id', 'title', 'image', 'sub_desc', 'created', 'category_name', 'user_name').get()
        return Response({'data': {'data': data_obj, }, 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@validate_token
def create_blog(request):
    try:
        data = request.data
        print(data['title'])
        if (Blog.objects.filter(title=data['title'])):
            return Response({'data': {"message": "Blog with this title already exists!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {"message": "Blog created successfully", 'data': serializer.data}, 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({'data': {"message": "Something went wrong!", 'data': {'errors': serializer.errors, }}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError:
        return Response({'data': {"message": "Invaid id!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@validate_token
def update_blog(request, id):
    try:
        queryset = Blog.objects.get(id=id)
        serializer = BlogSerializer(
            queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {"message": "Blog detail update successfully!", 'data': serializer.data}, 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({'data': {"message": "Something went wrong!", 'errors': serializer.errors}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Blog.DoesNotExist:
        return Response({'data': {"message": "Blog not found"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError:
        return Response({'data': {"message": "Invalid id!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@validate_token
def remove_blog(request, id):
    try:
        blog = Blog.objects.get(id=id)
        blog.delete()
        return Response({'data': {"message": "Blog removed successfully!"}, 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Blog.DoesNotExist:
        return Response({'data': {"message": "Blog not found"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError:
        return Response({'data': {"message": "Invalid id!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


# blog_detail api
@api_view(['POST'])
@validate_token
def create_blog_detail(request, id):
    try:
        data = request.data
        data['blog'] = id
        print(data)
        serializer = BlogDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {"message": "Blog detail created successfully!", 'data': serializer.data}, 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({'data': {"message": "Something went wrong!", 'errors': serializer.errors}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError:
        return Response({"data": {"message": "Invalid id!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'data': {"message": "Something went wrong", }, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @validate_token
def get_blog_detail(request, id):
    try:
        blog = Blog.objects.get(id=id)
        blog_serializer = BlogSerializer(blog)
        blogs = BlogDetail.objects.filter(blog=id).order_by('created')
        serializer = BlogDetailSerializer(blogs, many=True)
        return Response({'data': {"data": serializer.data}, 'total': len(serializer.data), 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except BlogDetail.DoesNotExist:
        return Response({'data': {"message": "Blog detail is not there!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError:
        return Response({"data": {"message": "Invalid id!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'data': {"message": "Something went wrong!", }, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

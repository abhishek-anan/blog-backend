from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BlogSerializer, TagSerializer, BlogTagSerializer
from .models import Blog, Tag, BlogTag
from .auth import validate_token
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db.models import F


# blog tag api
@api_view(['POST'])
@validate_token
def create_blog_tag(request):
    try:
        data = request.data
        blog = Blog.objects.get(id=data['blog_id'])
        blogs = BlogTag.objects.filter(blog=data['blog_id'])
        if blogs:
            for blog in blogs:
                blog.delete()
        # tags = set(data['tag_id'].replace(" ", "").split(","))
        for tag in data['tag_id']:
            request_data = {}
            request_data['tag_id'] = tag
            request_data['blog_id'] = data['blog_id']
            request_data['created_by_id'] = data['created_by_id']
            request_data['modified_by_id'] = data['modified_by_id']
            serializer = BlogTagSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({'data': {"message": "Something went wrong!", 'errors': serializer.errors}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'data': {"message": "Blog tag created successfully!", 'data': serializer.data}, 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Blog.DoesNotExist:
        return Response({'data': {"message": "Blog not found"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Tag.DoesNotExist:
        print(tag)
        return Response({'data': {"message": "Tag not found"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError:
        print("v")
        return Response({'data': {"message": "Invalid id!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    # except IntegrityError:
    #     print("i")
    #     return Response({'data': {"message": "Invalid id!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @validate_token
def get_blog_tag(request):
    try:
        queryset = BlogTag.objects.all()
        serializer = BlogTagSerializer(queryset, many=True)
        return Response({'data': {'data': serializer.data}, 'total': len(serializer.data), 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @validate_token
def get_blog_by_tag(request, id):
    try:
        queryset = BlogTag.objects.filter(tag=id).annotate(blog_title=F('blog__title'), blog_sub_desc=F('blog__sub_desc'), category_name=F('blog__category__name'), user_name=F('blog__user__name')).values(
            'category_name', 'user_name', 'blog_id', 'blog_title', 'blog_sub_desc')
        return Response({'data': {'data': queryset}, 'total': len(queryset), 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @validate_token
def get_tag_by_blog(request, id):
    try:
        queryset = BlogTag.objects.filter(blog_id=id).annotate(tag_name=F('tag__name'), blog_title=F('blog__title')).values(
            'id', 'blog_id', 'tag_id', 'blog_title', 'tag_name')
        return Response({'data': {'data': queryset}, 'total': len(queryset), 'api_status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data': {"message": "Something went wrong!"}, 'api_status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

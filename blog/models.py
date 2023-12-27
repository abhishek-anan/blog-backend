from django.db import models
import uuid


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=300)
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=60, unique=True)
    mobile = models.CharField(max_length=10)
    token = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=120, unique=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='category_created_by')
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='category_modified_by')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, unique=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tag_created_by')
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tag_modified_by')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    sub_desc = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_created_by')
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_modified_by')

    def __str__(self):
        return self.title


class BlogTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blogtag_created_by')
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blogtag_modified_by')


class BlogDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text_type = models.CharField(max_length=20)
    heading = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(
        upload_to='blog_images/', null=True, blank=True)
    text = models.CharField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blogdetail_created_by')
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blogdetail_modified_by')

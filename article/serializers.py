from rest_framework import serializers

from .models import Article


# Serializer is similar to Form
class ArticleSerializer(serializers.ModelSerializer):
    # specifying fields explicitly (https://www.django-rest-framework.org/api-guide/serializers/#specifying-fields-explicitly)
    author = serializers.CharField(max_length=100, default="hai")

    class Meta:
        model = Article
        fields = ["title", "content", "author"]


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
    pass

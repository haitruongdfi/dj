import io

from django.http import HttpResponse
from django.views import View
from rest_framework import generics, permissions
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .comments import Comment
from .models import Article
from .serializers import ArticleSerializer, CommentSerializer

xyz = "I should be removed by autoflake but not. Why?"


class ArticleView(generics.ListAPIView):

    serializer_class = ArticleSerializer
    # model = serializer_class.Meta.model
    queryset = Article.objects.all()
    # when we set 'rest_framework.permissions.IsAuthenticated' in settings.py

    # JUST WITH APIView, if there is not below line, this view is prevent from requesting
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentView(View):
    comments = []
    comments.append(
        Comment(
            email="haitruong1@datafluct.com", content="Hello, this is first comment"
        )
    )
    comments.append(
        Comment(
            email="haitruong2@datafluct.com", content="Hello, this is second comment"
        )
    )
    comments.append(
        Comment(
            email="haitruong3@datafluct.com", content="Hello, this is third comment"
        )
    )
    comments.append(
        Comment(
            email="haitruong4@datafluct.com", content="Hello, this is fourth comment"
        )
    )

    def get(self, req):
        # parse JSON to object
        # format of json string MUST be a byte string: b'' (single quote)
        json = b'{"email":"haha@gmail.com","content":"hello hahaha","created":""}'
        stream = io.BytesIO(json)  # buffer json string to memory
        data = JSONParser().parse(
            stream
        )  # parsing stream of data to Python native datatype
        for k, v in data.items():
            # print("{} is {}".format(k,v))
            # print("%s is %s" % (k,v))
            print(f"{k} is {v}")

        single_comment = Comment(
            email="hello@datafluct.com", content="Hello, this is single comment"
        )
        serializer = CommentSerializer(single_comment)
        # print(serializer)
        print(serializer.data)  # at this time, data is Python native datatype
        # render data to JSON bytes
        json_data = JSONRenderer().render(serializer.data)

        serializer = CommentSerializer(
            self.comments, many=True
        )  # dealing with multiple objects
        # print(serializer)
        print(serializer.data)  # at this time, data is Python native datatype
        # render data to JSON bytes
        json_data += JSONRenderer().render(serializer.data)
        print(type(json_data))
        print(type(json_data.decode()))
        self.sayHello(123)
        return HttpResponse(json_data)

    def sayHello(name: str) -> str:
        return "Hello " + name

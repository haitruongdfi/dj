import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Article
from .serializers import ArticleSerializer

"""This testing only for pytest => run command: pytest"""


@pytest.mark.django_db  # We first mark our test with django_db to tell PyTest that this test has access to the database.
def test_list_articles(client):
    #  Client class of Django which simulates a dummy browser so you can make HTTP requests and test how your Django API responds.
    url = reverse("list-articles")  # get url to prepare for client
    response = client.get(url)

    articles = Article.objects.all()
    expected_data = ArticleSerializer(articles, many=True).data

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data  # compare response data with serialized data


"""Testing using APITestCase => run command: python3 manage.py test"""


class ArticleAPITests(APITestCase):
    def test_listing_articles(self):
        url = reverse("list-articles")  # get url to prepare for client
        response = self.client.get(url)

        articles = Article.objects.all()
        expected_data = ArticleSerializer(articles, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(expected_data,response.data)
        print(response.data)

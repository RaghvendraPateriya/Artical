from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Artical, Vote

class UserSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(required=True, validators=[UniqueValidator(
                                 queryset=User.objects.all())])
  username = serializers.CharField(max_length=32, validators=[UniqueValidator(
                                   queryset=User.objects.all())])
  password = serializers.CharField(min_length=8)

  def create(self, validated_data):
    user = User.objects.create_user(validated_data['username'],
                    validated_data['email'],
                    validated_data['password'])
    return user

  class Meta:
    model = User
    fields = ('username', 'email', 'password')


class AuthorSerializer(serializers.ModelSerializer):
   class Meta:
     model = User
     fields = ('username',)


class ArticalSerializer(serializers.ModelSerializer):
  author = AuthorSerializer

  class Meta:
  	model = Artical
  	fields = ('author', 'content', 'title')


class VoteSerializer(serializers.ModelSerializer):
  class Meta:
  	model = Vote
  	fields = ('user', 'artical', 'up_vote')

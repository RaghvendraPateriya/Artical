from django.contrib.auth.models import User
from django.db.models import Count  
from django.shortcuts import render, get_object_or_404

from rest_framework.generics import CreateAPIView, ListAPIView

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Artical, Vote
from .serializers import ArticalSerializer, UserSerializer, VoteSerializer

class UserCreate(APIView):
  '''Creates the user.'''
  queryset = User.objects.all()
  
  def post(self, request, format='json'):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      if user:
        #TODO write a token for Auth module.
        return Response(status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateArtical(CreateAPIView):
  '''Create Artical.'''
  queryset = Artical.objects.all()
  serializer_class = ArticalSerializer

  def create(self, request):
    data = request.data
    auther = get_object_or_404(User, username=data.get('auther'))
    data['auther'] = auther
    serializer_obj = ArticalSerializer(data=data)
    if serializer_obj.is_valid():
      serializer_obj.save()
      return Response(status=status.HTTP_200_OK)
    else:
      return Response(data={'error': serializer_obj.errors},
                      status=status.HTTP_400_BAD_REQUEST)  


class ListArtical(ListAPIView):
  '''List Artical in decending order.'''
  serializer_class = ArticalSerializer
  model = Artical

  def get_queryset(self):
    query_set =  Artical.objects.values('title', 'content',
        'author__username').annotate(Count('vote'))
    return query_set


class UpVote(APIView):
  '''Makes up-vote for an Artical.'''
  queryset = Vote.objects.all()
  serializer_class = VoteSerializer

  def post(self, request, id=None):
    data = request.data
    user = get_object_or_404(User, username=data.get('user'))
    artical = get_object_or_404(Artical, id=data.get('artical'))
    serializer_obj = VoteSerializer(data={'user':user.id, 'artical':artical.id,
                                          'up_vote':True})
    if serializer_obj.is_valid():
      serializer_obj.save()
      return Response(status=status.HTTP_200_OK)
    else:
      return Response(data={'error': serializer_obj.errors},
                      status=status.HTTP_400_BAD_REQUEST)  
  

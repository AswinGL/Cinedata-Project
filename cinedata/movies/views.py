from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework.response import Response

from . models import Movies , Rating

import json

from .serializers import MoviesListRetrieveSerializer,MoviesCreateUpdateSerializer

from django .shortcuts import get_object_or_404

from rest_framework import authentication,permissions

from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from authentication.permissions import IsAdmin,IsUser

from rest_framework_simplejwt import authentication

from django.db.models import Avg

from .serializers import RatingSerializer

# Create your views here.

class MoviesListCreateView(APIView):

    http_method_names = ['get', 'post']

    authentication_classes = [authentication.JWTAuthentication]

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # thus seriallizer for get movies
    get_serializer_class = MoviesListRetrieveSerializer

    # this seriallizer for update and create movies
    post_serializer_class = MoviesCreateUpdateSerializer

    def get_permissions(self):

        if self.request.method == 'GET':

            return [AllowAny()]

        elif self.request.method == 'POST':

            return [IsAdmin()]

        return super().get_permissions()

    def get (self,request,*args,**kwargs):

        movies = Movies.objects.filter(active_status=True)

        serializer = self.get_serializer_class(movies,many=True)

        return Response(data=serializer.data,status=200)

    def post(self,request,*args,**kwargs):

        serializer = self.post_serializer_class(data=request.data)

        if serializer.is_valid():

            movie = serializer.save()

            cast_ids = json.loads(request.data.get('cast', '[]'))

            movie.cast.set(cast_ids) 

            return Response(data={'msg':'movie created successfully'},status=200)
        
        return Response(data=serializer.errors,status=400)


class MoviesRetrieveUpdateDestroyView(APIView):

    get_serializer_class = MoviesListRetrieveSerializer

    post_serializer_class = MoviesCreateUpdateSerializer   

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        movie = get_object_or_404(Movies,uuid=uuid)

        serializer = self.get_serializer_class(movie)

        return Response(data=serializer.data,status=200)
    
    def put(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        movie = get_object_or_404(Movies,uuid=uuid)

        serializer = self.post_serializer_class(instance=movie,data=request.data,partial=True)

        if serializer.is_valid():

            movie_obj = serializer.save()

            cast = request.data.get('cast')

            if cast:

                cast_ids = json.loads('cast', [] )

                movie_obj.cast.set(cast_ids)

            return Response(data={'msg':'movie updated successfully'},status=200)
        
        return Response(data=serializer.errors,status=400)
    
    def delete(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        movie = get_object_or_404(Movies,uuid=uuid)

        movie.active_status = False

        movie.save()

        return Response(data={'msg':'movie deleted successfully'},status=200)
    
class AddRatingView(APIView):

    http_method_names = ['post']

    authentication_classes = [authentication.JWTAuthentication]

    permission_classes = [IsUser()]

    def post(self, request, *args, **kwargs):

        user = request.user

        uuid = kwargs.get('uuid')

        movie = get_object_or_404(Movies, uuid=uuid)    

        rating = request.data.get('rating')

        Rating.objects.get_or_create(user=user, movie=movie, rating=rating )

        movie.rating_set.create(user=user, rating=rating)

        return Response(data={'msg': 'Rating added successfully'}, status=200)

        
       
class Top20MoviesListView(APIView):

    http_method_names = ['get']

    authentication_classes = [authentication.JWTAuthentication]

    permission_classes = [AllowAny]

    serializer_class = MoviesListRetrieveSerializer

    def get(self, request, *args, **kwargs):

        top_20_movies = Movies.objects.annotate(avg_rating=Avg('rating__rating')).filter(avg_rating__isnull=False) #.exclude(avg_rating__isnull=True)

        serializer = self.serializer_class(top_20_movies, many=True)
        
        return Response(data=serializer.data, status=200)



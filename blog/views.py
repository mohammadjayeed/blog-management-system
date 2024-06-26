from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from .models import Blog
from .serializers import BlogCreateUpdateSerializer, BlogRetrieveSerializer, BlogSerializer
from .permissions import (blog_create_view_permissions_by_action, blog_retrieveupdatedelete_permissions_by_action)

class BlogCreateViewSet(ViewSet):

    def get_permissions(self):

        return [permission() for permission in blog_create_view_permissions_by_action(self.action)]

    @swagger_auto_schema(request_body=BlogCreateUpdateSerializer)
    def create(self, request):
        
        
        serializer = BlogCreateUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"status": "error","message": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        
        
        serializer.save(author=request.user)
        return Response({"id": serializer.instance.id, "status": "success","message": "blog post created."}, status.HTTP_201_CREATED)
    

    def list(self, request):
        
        
        queryset = Blog.objects.all()
        serializer = BlogSerializer(queryset, many=True)
        return Response({"status": "success","results": serializer.data})
    
    @swagger_auto_schema(tags=['my_blog_posts'])
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def me(self,request):
        queryset = Blog.objects.filter(author= request.user.id)
        serializer = BlogSerializer(queryset, many=True)
        return Response({"status": "success","results": serializer.data})
   
        
class BlogRetrieveUpdateDeleteViewSet(ViewSet):

    def get_permissions(self):
        return [permission() for permission in blog_retrieveupdatedelete_permissions_by_action(self.action)]

    def retrieve(self, request, pk):
        
        try:
            queryset = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response({"status": "success","message": "No matching Blog post."}, status.HTTP_404_NOT_FOUND)
        
        # if queryset.author != request.user:
        #     return Response({"status": "error", "message": "You do not have permission to see details of this post."}, status=status.HTTP_403_FORBIDDEN)

        serializer = BlogRetrieveSerializer(queryset)
        
        return Response({"status": "success","results": serializer.data})

    @swagger_auto_schema(request_body=BlogCreateUpdateSerializer)
    def update(self, request, pk):
        
        
        try:
            queryset = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response({"status": "success","message": "Sorry, we couldn't find any matching post."}, status.HTTP_404_NOT_FOUND)
        
        if queryset.author != request.user:
            return Response({"status": "error", "message": "You do not have permission to update this post."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = BlogCreateUpdateSerializer(queryset, data=request.data)

        if not serializer.is_valid():
            return Response({"status": "error", "message": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response({"status": "success","message": "Blog updated successfully."}, status.HTTP_200_OK)


    def destroy(self, request, pk):
        
        
        try:
            queryset = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response({"status": "success","message": "Sorry, we couldn't find any matching post."}, status.HTTP_404_NOT_FOUND)
        
        if queryset.author != request.user:
            return Response({"status": "error", "message": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        
        queryset.delete()

        return Response({"status": "success","message": "Product deleted successfully."}, status.HTTP_204_NO_CONTENT)

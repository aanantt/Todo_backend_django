from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
# Create your views here.
from rest_framework import status, generics, permissions
from rest_framework.authtoken.admin import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import TodoSerializer, UserSerializer
from todo_app.models import ToDo


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class BillingRecordsView(generics.ListAPIView):
    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)

    queryset = get_queryset
    serializer_class = TodoSerializer
    pagination_class = LargeResultsSetPagination


class ToDoMaker(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = LargeResultsSetPagination

    def post(self, request):

        ToDo.objects.create(user=request.user, work=request.data['work'])
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        todo = ToDo.objects.filter(user=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(todo, request)
        todoSerializer = TodoSerializer(result_page, many=True)
        if todoSerializer:
            return paginator.get_paginated_response(todoSerializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        todo = ToDo.objects.get(id=id)
        if request.data.get('work'):
            todo.work = request.data.get('work')
        if request.data.get('isdone'):
            todo.isdone = request.data.get('isdone')
        todo.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, id):
        todo = ToDo.objects.filter(id=id)
        todo.delete()
        return Response(status=status.HTTP_200_OK)

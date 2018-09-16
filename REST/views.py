# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import permissions as dp


from . import models
from . import serializers
from . import permissions


# Create your views here.


# class ListCreateCourse(APIView):
#
#     def get(self, request, format=None):
#         courses = models.Course.objects.all()
#         serializer = serializers.CourseSerializer(courses, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = serializers.CourseSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class ListCreateCourse(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer


class RetrieveUpdateDestroyCourse(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer


class ListCreateReview(generics.ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return self.queryset.filter(course_id=self.kwargs.get('course_pk'))

    def perform_create(self, serializer):
        course = get_object_or_404(models.Course, pk=self.kwargs.get('course_pk'))
        serializer.save(course=course)


class RetrieveUpdateDestroyReview(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def get_object(self):
        return get_object_or_404(self.get_queryset(), course_id=self.kwargs.get('course_pk'), pk=self.kwargs.get('pk'))

# VERSION 2
###########


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsSuperUser,
        dp.DjangoModelPermissions)
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

    @detail_route(methods=['get'])
    def reviews(self, request, pk=None):
        self.pagination_class.page_size = 1
        reviews = models.Review.objects.filter(course_id=pk)
        page = self.paginate_queryset(reviews)

        if page is not None:
            serializer = serializers.ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
        # course = self.get_object()
        # serializer = serializers.ReviewSerializer(course.reviews.all(), many=True)


# class ReviewViewSet(viewsets.ModelViewSet):
#     queryset = models.Review.objects.all()
#     serializer_class = serializers.ReviewSerializer







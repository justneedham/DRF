from rest_framework import serializers
from django.db.models import Avg
from . import models


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        extra_kwargs = {
            'email': {'write_only': True}
        }
        fields = (
            'id',
            'course',
            'name',
            'email',
            'comment',
            'rating',
            'created_at'
        )
        model = models.Review

    def validate_rating(self, value):
        if value in range(1, 6):
            return value
        raise serializers.ValidationError(
            'Rating Must Be An Integer Between 1 and 5'
        )


class CourseSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    # reviews = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='apiV2:review-detail')
    reviews = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'title',
            'url',
            'reviews',
            'average_rating'
        )
        model = models.Course

    def get_average_rating(self, object):
        average = object.reviews.aggregate(Avg('rating')).get('rating__avg')

        if average is None:
            return 0
        else:
            return round(average * 2) / 2



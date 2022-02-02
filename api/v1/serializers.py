"""API v.1 serializers."""


from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models.aggregates import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    """Reviews.Review model serializer."""
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = "__all__"
        model = Review
        read_only_fields = ("author", "title")

    def validate(self, data):
        """Validate a specific review does not exists."""
        title = self.context["view"].kwargs.get("titles_id")
        request = self.context.get("request")
        if (
            request.method != "PATCH"
            and Review.objects.filter(
                author=self.context["request"].user, title_id=title
            ).exists()
        ):
            raise serializers.ValidationError(
                "You can send only one review for one title."
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Reviews.Comment model serializer."""
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = ("author", "review")


class CustomUserSerializer(serializers.ModelSerializer):
    """Reviews.User model custom serializer."""
    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User


class UserMeSerializer(serializers.ModelSerializer):
    """Reviews.User model serializer for an own account."""
    role = serializers.CharField(read_only=True)

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User


class SignUpSerializer(serializers.ModelSerializer):
    """Reviews.User model serializer for a sing up action."""
    class Meta:
        fields = ("username", "email")
        model = User

    def validate(self, data):
        """Validate username is not equal me."""
        if data["username"] == "me":
            raise validators.ValidationError("You can not use this username.")

        return data


class TokenCreateSerializer(serializers.ModelSerializer):
    """Reviews.User model serializer for a token creation."""
    confirmation_code = serializers.CharField(source="password")

    class Meta:
        fields = ("username", "confirmation_code")
        model = User

    def validate(self, data):
        """Validate confirmation code is equal to user's password."""
        current_user = get_object_or_404(User, username=data["username"])
        if data["confirmation_code"] != current_user.password:
            raise validators.ValidationError(
                "Confirmation code is not correct!"
            )


class CategorySerializer(serializers.ModelSerializer):
    """Reviews.Category model serializer."""
    class Meta:
        fields = ("name", "slug")
        model = Category
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class GenreSerializer(serializers.ModelSerializer):
    """Reviews.Genre model serializer."""
    class Meta:
        fields = ("name", "slug")
        model = Genre
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class RepresentCategory(serializers.SlugRelatedField):
    """Represented category field."""
    def to_representation(self, obj):
        serializer = CategorySerializer(obj)
        return serializer.data


class RepresentGenre(serializers.SlugRelatedField):
    """Represented genre field."""
    def to_representation(self, obj):
        serializer = GenreSerializer(obj)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    """Reviews.Title model serializer."""
    rating = serializers.SerializerMethodField()

    category = RepresentCategory(
        slug_field="slug", queryset=Category.objects.all(), required=False
    )
    genre = RepresentGenre(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True,
        required=False,
    )

    def get_rating(self, obj):
        """Method gets data for a rating field."""
        rating = Review.objects.filter(title=obj.id).aggregate(Avg("score"))
        if rating["score__avg"] is None:
            return None
        return rating["score__avg"]

    def validate_year(self, value):
        """Validate year is in range from 1000 to a current."""
        now_year = datetime.now().year
        if value in range(1000, now_year + 1):
            return value
        else:
            raise serializers.ValidationError(
                "Enter the year from 1000 to current."
            )

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        model = Title

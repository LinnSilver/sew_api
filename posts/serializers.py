from rest_framework import serializers
from posts.models import Post
from likes.models import Like


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    image = serializers.ImageField(required=False)
    url = serializers.URLField(required=False)
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def validate_image(self, value):
        """
        Validates the image field to ensure its size and dimensions are within limits.
        """
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError('Image height larger than 4096px!')
        if value.image.width > 4096:
            raise serializers.ValidationError('Image width larger than 4096px!')
        return value

    def get_is_owner(self, obj):
        """
        Determines if the requesting user is the owner of the post.
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_likes_count(self, obj):
        """
        Returns the number of likes for the post.
        """
        return obj.post_likes.count()

    def get_like_id(self, obj):
        """
        Returns the ID of the like made by the requesting user for the post, if any.
        """
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(owner=user, post=obj).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'content', 'image', 'url', 'like_id', 'likes_count'
        ]

from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'owner' , 'image']
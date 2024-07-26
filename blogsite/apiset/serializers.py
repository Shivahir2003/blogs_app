from django.contrib.auth.models import User

from rest_framework import serializers


from accounts.models import UserProfile
from blogapp.models import Blog,Category,Comments,Reply


class UserNameSerializer(serializers.ModelSerializer):
    """
        define username and user id 
    """
    id= serializers.IntegerField(required=False)

    class Meta:
        model=User
        fields= ['id','username']
        read_only_fields= ['username']


class BlogTitleSerializer(serializers.ModelSerializer):
    """
        define blog title
    """
    class Meta:
        model = Blog
        fields= ['title']


class CommentNameSerializer(serializers.ModelSerializer):
    """
        define comment name and comment id
    """
    id= serializers.IntegerField(required=False)

    class Meta:
        model = Comments
        fields = ['id','comment']
        read_only_fields =['comment']


class ReplySetSerializer(serializers.ModelSerializer):
    """
        define reply and user 
    """
    user =UserNameSerializer()

    class Meta:
        model = Reply
        fields = ['reply','user']


class UserSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, user):
        """
            calculate full name from first_name and last_name
        """
        return user.first_name + user.last_name

    class Meta:
        model= User
        fields= ['username','first_name','last_name','email','full_name']


class UserProfileSerializer(serializers.ModelSerializer):

    user= UserSerializer()

    class Meta:
        model = UserProfile
        fields= ['user','mobile_number']

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model= Category
        fields =['name']


class CommentSerializer(serializers.ModelSerializer):
    blog =BlogTitleSerializer()
    user = UserNameSerializer()
    reply= ReplySetSerializer(many=True)

    class Meta:
        model = Comments
        fields= ['id','comment','blog','user','reply', 'created']


class ReplySerializer(serializers.ModelSerializer):
    comment = CommentNameSerializer()
    user= UserNameSerializer()

    class Meta:
        model = Reply
        fields = ['reply','comment','user','created']
        read_only_fields=['created']

    def validate(self,data):
        """
            check if user and comments exists or does not exists
        """
        if not self.context['request'].method =="PATCH":
            if not User.objects.filter(pk=data['user']['id']).exists() :
                raise serializers.ValidationError("user not found")
            elif not Comments.objects.filter(pk=data['comment']['id']).exists():
                raise serializers.ValidationError("comment not found")
        return data

    def create(self, validated_data):
        """
            getting user and comment instance
        """
        user= User.objects.get(pk =validated_data['user']['id'])
        comment= Comments.objects.get(pk =validated_data['comment']['id'])
        reply= Reply.objects.create(
            reply=validated_data['reply'],
            user=user,
            comment=comment
        )
        return reply

    def update(self, instance, validated_data):
        """
            update reply field only
        """
        instance.reply = validated_data.get('reply',instance.reply)
        instance.save()
        return instance


class BlogSerializer(serializers.ModelSerializer):

    user = UserNameSerializer()
    categories = CategorySerializer()
    comments = CommentSerializer(many=True)

    class Meta:
        model= Blog
        fields = ['title','description','post','user','categories','created','comments']
        read_only_fields=['comments']


class BlogListSerializer(serializers.ModelSerializer):

    user = UserNameSerializer()

    class Meta:
        model= Blog
        fields=['title','description','created','user']

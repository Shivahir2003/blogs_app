import re
from django.contrib.auth.models import User

from rest_framework import serializers

from accounts.models import UserProfile
from blogapp.models import Blog,Category,Comments,Reply


class UserNameSerializer(serializers.ModelSerializer):
    """
        define username and user id 
    """
    id = serializers.IntegerField(required=False)

    class Meta:
        model=User
        fields= ['id','username']
        read_only_fields= ['username']


class BlogTitleSerializer(serializers.ModelSerializer):
    """
        define blog title
    """
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Blog
        fields = ['id','title']
        read_only_fields =['title']


class CommentNameSerializer(serializers.ModelSerializer):
    """
        define comment name and comment id
    """
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Comments
        fields = ['id','comment']
        read_only_fields = ['comment']


class ReplySetSerializer(serializers.ModelSerializer):
    """
        define reply and user 
    """
    user = UserNameSerializer()

    class Meta:
        model = Reply
        fields = ['id','reply','user']
        read_only_fields = ['reply']


class CategoryNameSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model= Category
        fields = ['id','name']
        read_only_fields = ['name']




class UserSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField('get_full_name')

    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def get_full_name(self, user):
        """
            calculate full name from first_name and last_name
        """
        return user.first_name + user.last_name

    class Meta:
        model = User
        fields = ['username','password','password2','first_name','last_name','email','full_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user','mobile_number']

    def validate(self,data):

        if data['user']['password'] != data['user']['password2']:
            raise serializers.ValidationError(
                {
                    "comfirm password": "password fields does not match"
                }
            )
        return data

    def create(self, validated_data):

        user = User.objects.create(
            username =validated_data['user']['username'],
            first_name=validated_data['user']['first_name'],
            last_name=validated_data['user']['last_name'],
            email=validated_data['user']['email']
        )
        user.set_password(validated_data['user']['password'])
        user.save()

        userprofile = UserProfile.objects.create(
            user=user,
            mobile_number = validated_data['mobile_number']
        )
        return userprofile


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model= Category
        fields = ['id','name']


class CommentSerializer(serializers.ModelSerializer):
    blog = BlogTitleSerializer()
    user = UserNameSerializer()
    reply = ReplySetSerializer(many=True,required=False)

    class Meta:
        model = Comments
        fields= ['id','comment','blog','user','reply', 'created']
        read_only_fields = ['created','reply',]

    def validate(self, data):
        if not self.context['request'].method == "PATCH":
            if not User.objects.filter(pk=data['user']['id']).exists() :
                raise serializers.ValidationError("User not found")
            elif not Blog.objects.filter(pk=data['blog']['id']).exists():
                raise serializers.ValidationError("Blog not found")
        return data

    def create(self, validated_data):
        blog = Blog.objects.get(pk = validated_data['blog']['id'])
        user = User.objects.get(pk =validated_data['user']['id'])
        comment = Comments.objects.create(
            comment=validated_data['comment'],
            blog=blog,
            user=user
        )
        return comment

    def update(self, instance, validated_data):
        instance.comment=validated_data.get('comment',instance.comment)
        instance.save()
        return instance


class ReplySerializer(serializers.ModelSerializer):
    comment = CommentNameSerializer()
    user = UserNameSerializer()

    class Meta:
        model = Reply
        fields = ['id','reply','comment','user','created']
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
        user = User.objects.get(pk =validated_data['user']['id'])
        comment = Comments.objects.get(pk =validated_data['comment']['id'])
        reply = Reply.objects.create(
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

    user = UserNameSerializer(required=False)
    categories = CategoryNameSerializer()
    comments = CommentSerializer(many=True, required=False)


    class Meta:
        model= Blog
        fields = ['id','title','description','post','user','categories','created','comments']
        read_only_fields = ['comments','created']

    def validate(self, data):
        return super().validate(data)

    def create(self, validated_data):

        user=User.objects.get(pk =validated_data['user']['id'])
        category=Category.objects.get(pk =validated_data['categories']['id'])
        blog = Blog.objects.create(
            user=user,
            title=validated_data['title'],
            description=validated_data['description'],
            post=validated_data['post'],
            categories=category,
        )
        return blog

    def update(self, instance, validated_data):
        instance.title=validated_data.get('title',instance.title)
        instance.description=validated_data.get('description',instance.description)
        instance.post=validated_data.get('post',instance.post)
        if 'categories' in validated_data.keys():
            category=Category.objects.get(pk=validated_data['categories']['id'])
            instance.categories=category
        instance.save()
        return instance


class BlogListSerializer(serializers.ModelSerializer):

    user = UserNameSerializer()
    categories = CategorySerializer()

    class Meta:
        model = Blog
        fields = ['id','title','description','created','user','categories']

from .models import Answer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import serpy
from django.utils import timezone

class UserSerializer(serpy.Serializer):
    id = serpy.Field()
    first_name = serpy.Field()
    last_name = serpy.Field()

class AnswerSerializer(serpy.Serializer):
    id = serpy.Field()
    title = serpy.Field()
    comment = serpy.Field()
    score = serpy.Field()
    status = serpy.Field()
    user = UserSerializer(required=False)

    score = serpy.Field()
    academy = serpy.Field()
    cohort = serpy.Field()
    mentor = serpy.Field()
    event = serpy.Field()

class AnswerPUTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ()

    def validate(self, data):
        utc_now = timezone.now()

        # the user cannot vote to the same entity within 5 minutes
        answer = Answer.objects.filter(user=self.context['request'].user,id=self.context['answer']).first()
        if answer is None:
            raise ValidationError('This survay does not exist for this user')

        if answer.status == 'ANSWERED':
            raise ValidationError('You have already voted')

        if int(data['score']) > 10 or int(data['score']) < 1:
            raise ValidationError('Score must be between 1 and 10')

        return data

    # def create(self, validated_data):
    def update(self, instance, validated_data):

        instance.score = validated_data['score']
        instance.status = 'ANSWERED'
        if 'comment' in validated_data:
            instance.comment = validated_data['comment']
        instance.save()
        return instance

        
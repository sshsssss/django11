from rest_framework import serializers
from .models import Question, TextContent
class TextContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextContent
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    info_content = TextContentSerializer()

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        question = Question.objects.create(**validated_data)
        return question

    def update(self, instance, validated_data):
        print("update")
        info_content_data = validated_data.pop('info_content')
        info_content = instance.info_content
        instance.question_type = validated_data.get('question_type', instance.question_type)
        instance.subject_id = validated_data.get('subject_id', instance.subject_id)
        instance.score = validated_data.get('score', instance.score)
        instance.level = validated_data.get('level', instance.level)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)
        instance.save()

        # Update the content field with the JSON representation of questionObject
        info_content.content = info_content_data.get('content', info_content.content)
        info_content.save()

        return instance

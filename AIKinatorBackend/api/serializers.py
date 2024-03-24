from rest_framework import serializers

class QuestionsSerializer(serializers.Serializer):
    question = serializers.CharField()
    answer = serializers.FloatField()
    session_id = serializers.CharField()

class AnswerSerializer(serializers.Serializer):
    answer = serializers.FloatField(required=False)

from rest_framework import serializers

class QuestionsSerializer(serializers.Serializer):
    question = serializers.CharField()


from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import QuestionsSerializer
from rest_framework import status
from django.contrib.sessions.models import Session
import uuid

# Create your views here.

# class QuestionView(APIView):
@api_view(('GET','POST'))
def create_session(request):
    session_key = request.session.session_key

    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    session = Session.objects.get(session_key = session_key)
    session_data = session.get_decoded()


    if request.method == 'GET':
        question = "do you experience headaches?"
        uid = uuid.uuid4
        request.session['id'] = uid
        data = [{
            "question": question,
            "session_id": request.session['id'],
            "answer": -1,
        }]


        res = QuestionsSerializer(data, many = "true").data
        return Response(res)

    if request.method == 'POST':
        serializer = QuestionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




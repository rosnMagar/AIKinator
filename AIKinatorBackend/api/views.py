from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import QuestionsSerializer, AnswerSerializer
from rest_framework import status
from django.contrib.sessions.models import Session
import uuid
import numpy as np
import pandas as pd
from multiprocessing import Process,Queue,Pipe
from .integrator import *
from waiting import wait

# Create your views here.

# class QuestionView(APIView):
@api_view(('POST','GET'))
def create_session(request):
    session_key = request.session.session_key

    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    session = Session.objects.get(session_key = session_key)
    session_data = session.get_decoded()
    uid = uuid.uuid4()
    request.session['id'] = str(uid)

    currentQuestion = ""
    questionsAsked = [] 

    integrator = Integrator()

    if request.method == 'GET':
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():

            wait(lambda: integrator.isQuestionReady(), timeout_seconds = 10, wait_for="question_to_be_ready")
            data = [
                {
                    "question": integrator.readQuestion()
                }
            ]
            if(len(questionsAsked) == 0):
                integrator.sendAnswer(serializer.data['answer'])
                integrator.setAnswerReady(True)

                questionsAsked.append(integrator.currentQuestion)
            else:
                wait(lambda: integrator.isQuestionReady(), timeout_seconds = 10, wait_for="question_to_be_ready")
                integrator.sendAnswer(serializer.data['answer'])
                integrator.setAnswerReady(True)
                questionsAsked.append(integrator.currentQuestion)

            # store all the questions and answer and run a NN to predict the disease
            integrator.setAnswerReady(False)
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

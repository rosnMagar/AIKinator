from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import QuestionsSerializer, AnswerSerializer
from rest_framework import status
from django.contrib.sessions.models import Session
import uuid
from multiprocessing import Process,Queue,Pipe
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from scipy.special import softmax
from django.contrib.staticfiles import finders


import torch
import torch.nn as nn
from torch.nn import functional as F
from torch.autograd import Variable


# Create your views here.
    

# Load the dataset
data_path= "diseases.csv"
df_train = pd.read_csv(data_path)

# Convert the 'Disease' column to dummy variables
Disease    = pd.get_dummies(df_train['Disease'],drop_first=True)
Diseases_columns=Disease.columns;
# Drop the 'Unnamed: 0' column
df_train.drop(['Unnamed: 0'],axis=1,inplace=True)

train_columns = df_train.columns[1:]
# Calculate the correlation matrix and adjust it
corr=df_train.iloc[:,1:].corr()
corr=corr.to_numpy()
corr=np.maximum(corr-0.1,-0.2)

# Define the neural network architecture
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__();
        self.fc1=nn.Linear(131,512);
        self.fc2=nn.Linear(512,512);
        self.fc3=nn.Linear(512,512);
        self.fc4=nn.Linear(512,41);
        self.dropout=nn.Dropout(0.2);
        #self.sm=nn.Softmax();
    def forward(self,x):
        x=F.relu(self.fc1(x));
        x=self.dropout(x);
        x=F.relu(self.fc2(x));
        x=self.dropout(x);
        x=F.relu(self.fc3(x));
        x=self.dropout(x);
        x=self.fc4(x);
        #x=self.sm(x);
        return x;

# Load the trained model
model1=Net();
model_path = 'model_params.pth'
model1.load_state_dict(torch.load(model_path))
model1.cuda(0)
model1.eval()

# Initialize arrays for correlation, answers, and mark
corrarr=np.full(131,0.3);
answers=np.full(131,0.0);
mark=np.full(131,0.0)
index=0;
countt = 0

# API endpoint to create a session and handle the GET and POST requests
@api_view(('POST','GET'))
def create_session(request):
    session_key = request.session.session_key

    #Verification of the key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    session = Session.objects.get(session_key = session_key)
    session_data = session.get_decoded()
    uid = uuid.uuid4()
    request.session['id'] = str(uid)

    #Call global variable
    global countt
    global index
    global Diseases_columns
    global train_columns
    global corr
    global corrarr
    global answers
    global mark
    global model1

    #User sending request
    if request.method == 'POST':
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            # website sending the data
            if request.data['answer'] == -1:
                #refresh the questions
                countt += 1
                if countt <=15:
                    for i in range(20):
                        index = np.argpartition(-corrarr, i)[i]
                        if corrarr[index]<0 :
                            break;
                        if mark[index]==1 :
                            continue;
                        return Response({
                            "type": "question",
                            "question" : train_columns[index],
                            "question_id" : index,
                            "countt" : countt
                        })
                
                
                #Make the final perdiction
                x_pd=Variable(torch.FloatTensor(answers.reshape((1,131))).cuda(0));
                output=model1(x_pd);
                cc=output.cpu().detach().numpy().reshape(-1)
                values,st=torch.sort(output,descending=True)
                ans=st[:,:3].cpu().numpy().reshape(-1)  
                return Response({
                        "type": "prediction", 
                        "value":[
                            {Diseases_columns[ans[0]]:softmax(cc)[ans[0]]},
                            {Diseases_columns[ans[1]]:softmax(cc)[ans[1]]},
                            {Diseases_columns[ans[2]]:softmax(cc)[ans[2]]}
                            ]
                    })
            # user sending the data
            elif request.data['answer'] >= 0:
                #update the arraies
                feel = request.data['answer']
                index = request.data['question_id'];
                answers[index]=feel;
                mark[index]=1;
                corrarr=corrarr+corr[index]*((feel)*1.1-0.09);
                return Response({"type": "debug", 
                        "value":[
                            index,feel,answers[index]
                            ]})
            # website reset
            elif request.data['answer'] == -2:
                # array reset
                corrarr=np.full(131,0.3);
                answers=np.full(131,0.0);
                mark=np.full(131,0.0)
                index=0;
                countt = 0
                return Response({})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Integrator:
    def __init__(self):
        self.currentAnswer = 0.0
        self.currentQuestion = ""
        self.questionProvided = False
        self.questionReady = False
        self.answerReady = False

    def isAnswerReady(self):
        return self.answerReady
    def isQuestionReady(self):
        return self.questionReady
    
    def setAnswerReady(self, value):
        self.answerReady = value

    def setQuestionReady(self, value):
        self.questionReady = value
    
    def sendQuestion(self, question):
        self.currentQuestion = question
    
    def sendAnswer(self, answer):
        self.currentAnswer = answer
    
    def readAnswer(self):
        return self.currentAnswer
    
    def readQuestion(self):
        return self.currentQuestion
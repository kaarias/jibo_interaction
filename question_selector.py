import random

#Positive
pos1 = 'What are three good things that happened today?'
pos2 = 'Is there someone you feel gratitude to?'
pos3 = 'Tell me about one kind act you did today.'
pos4 = 'Tell me three funny things that you experienced today.'
pos5 = 'What is something fun you did today?'
pos6 = 'Is there something you feel grateful for today?'
pos7 = 'What is something nice someone did for you today?'
pos8 = 'What was your favorite part of your day today?'

#Neutral
neut1 = 'How did you use one of your strengths in a new way today?'
neut2 = 'Is there anything youd like to talk about?'
neut3 = 'How did you use your gift of time to someone today? It could be helping someone, sharing meal, etc.'
neut4 = 'What is one skill that youre getting better at?'
neut5 = 'What is one skill that you want to get better at?'
neut6 = 'What is one goal that you have for tomorrow?'
neut7 = 'Tell me about a moment where you got carried away today.'

#Negative 
neg1 = 'Was there anything that made you angry today?'
neg2 = 'Is there someone you need to forgive?'
neg3 = 'Tell me about a moment today when something bad turned into something good.'
neg4 = 'Tell me about something that challenged you today.'
neg5 = 'Tell me about something that made you sad today. '
neg6 = 'Is there something that you regret today?'
neg7 = 'What is something you did today to distract you from negative thoughts?'

positive = [pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8]
negative = [neg1, neg2, neg3, neg4, neg5, neg6, neg7]
neutral = [neut1, neut2, neut3, neut4, neut5, neut6, neut7]

def random_selector():
    posq = random.choice(positive)
    negq = random.choice(negative)
    neutq = random.choice(neutral)
    questions = [posq, negq, neutq]
    questions = random.sample(questions, len(questions))   
    return questions



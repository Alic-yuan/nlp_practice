lines = open("test.txt","r",encoding='utf-8').readlines()
sec = [ line.strip() for line in lines]

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
Chinese_bot = ChatBot("Training")
Chinese_bot.set_trainer(ListTrainer)
Chinese_bot.train(sec)


# 测试一下
question = '挖机履带掉了怎么装上去'
print(question)
response = Chinese_bot.get_response(question)
print(response)
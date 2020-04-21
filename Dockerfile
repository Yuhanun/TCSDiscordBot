FROM docker.io/library/python:3
COPY . /TCSDiscordBot
RUN pip install -r /TCSDiscordBot/requirements.txt
CMD cd /TCSDiscordBot && python main.py
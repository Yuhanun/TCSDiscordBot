# Source it from the python dockerfile
FROM python:3.8.2
# Copy over the current directory structure, make sure token.txt exists!
COPY . /TCSDiscordBot

# Install the requirements
RUN pip install -r /TCSDiscordBot/requirements.txt

# Run the bot
ENTRYPOINT [ "/TCSDiscordBot/run.sh" ]

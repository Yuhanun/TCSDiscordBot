# TCSDiscordBot
Discord bot for the TCS UTwente discord server

## Working on TCSDiscordBot:
Clone the repository and set up virtualenv:

```sh
# clone the repository
git clone https://github.com/Yuhanun/TCSDiscordBot.git
cd TCSDiscordBot
# set up and activate the virtualenv in the correct spot
# You don't HAVE to do this, however it's recommended.
python3 -m virtualenv venv
source ./venv/bin/activate # for linux/macOS
.\venv\Scripts\activate # for windows
# install the dependencies
pip install -r requirements.txt

# Create a token.txt file containing your bot token, \n's and spaces don't matter at the end or begin, the token is .strip()'d

python main.py
```
to stop working on the project, just type `deactivate` in your terminal of choice

### Docker
Because using the above virtualenv might still impose compatibility problems related to `sqlite`, there is also a Dockerfile provided that you can use.
```sh
# Clone the repository:
git clone https://github.com/Yuhanun/TCSDiscordBot.git
cd TCSDiscordBot

# Create a token.txt file containing your bot token here

# Build the Docker image
docker build -t tcs-discord-bot .
# Run the Docker image (or run it differently)
docker run -it  --name tcs-discord-bot tcs-discord-bot:latest
```
To stop, press <kbd>Ctrl</kbd>+<kbd>P</kbd>, then <kbd>Ctrl</kbd>+<kbd>Q</kbd> and run `docker stop  tcs-discord-bot`

## Feel free to pull request any changes / improvements you make :) ##

# License #
This project is licensed under the MIT License (yay, free software) - see the [LICENSE](https://github.com/Yuhanun/TCSDiscordBot/blob/master/LICENSE) file for details

# Acknowledgments #
Thanks to @EyeDevelop for coding this bot with me.
Thanks to anyone whose code was used.

### Buy me a coffee ;) (BTC) ###
32dcJ31dsxj8BMD5oD3mWKTDFSzpFHuHP1

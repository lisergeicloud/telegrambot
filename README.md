# Practical AI - Telegram bot "Rick"
#### The bot can play with you in Tic-Tac-Toe and Matches games, solve math tasks, translate from English to Russian, identify person on the photo, and recognize objects on the image. You can use voice input to interact with the bot.
## Group M2:
* Anton Shilov
* Ivan Osadchiy
* Konstantin Kubrak
* Sergey Li
### 1. Specify your Telegram bot, Wolfram Alfa, Wit.ai, Yandex.Translate tokens and Microsoft Face.
In **mytokens.py** file replace placeholders with your tokens:
```python
telegram_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
wolfram_token = "yyyyyyyyyyyyyyyyyyyyyyyyyyyy"
wit_token = "zzzzzzzzzzzzzzzzzzzzzzzzzz"
ya_translate_token = "qqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
repo_directory = "yyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
cf_token = 'lllllllllllllllllllllllllllll'
```
### 2. Install requirements (Python3)
> pip3 install -r requirements.txt

> apt install ffmpeg

> git clone https://github.com/pjreddie/darknet (specify `repo_directory` in `mytokens.py`)

### 3. Download "docvectors.pickle" file (213.42 MB) from [here](https://drive.google.com/file/d/1ef1llYF35FSQhtE-xhlv3P0cBlPccrw9/view?usp=sharing) and put it into the project folder.
This is for the joker module. The file was too heavy to upload to GitHub.

### 4. Run the bot
> python3 tbot.py

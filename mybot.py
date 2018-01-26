import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from wolfram_api_client import ask

from matches_game import MatchesGame, ACTIVE_GAMES
from mytokens import telegram_token

bot = telegram.Bot(token=telegram_token)

updater = Updater(token=telegram_token)
dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def solve(bot, update, args):
    if not ''.join(args):
        result = 'You need to specify a task. For example, "\solve x+1=4"'
        bot.send_message(chat_id=update.message.chat_id, text=result)
        return
    print('Command solve')
    request = ' '.join(args)
    result = ask(request)
    if result is None:
        result = "I don't know!"
    print(result)
    bot.send_message(chat_id=update.message.chat_id, text=result)


def matches(bot, update):
    print('Game started!')
    game = ACTIVE_GAMES.get(update.message.chat_id, None)
    if game is None:
        game = MatchesGame(chat_id=update.message.chat_id)
        ACTIVE_GAMES[update.message.chat_id] = game
    bot.send_message(chat_id=update.message.chat_id, text=game.RULES)
    bot.send_message(chat_id=update.message.chat_id,
                     text="It's your turn. Pick 1-4 matches. Or /exit.".format(game.MATCHES_NUM))


def exit(bot, update):
    print('Game finished.')
    try:
        del ACTIVE_GAMES[update.message.chat_id]
    except KeyError:
        pass
    response = "The game is finished."
    bot.send_message(chat_id=update.message.chat_id, text=response)


def echo(bot, update):
    text = update.message.text
    game = ACTIVE_GAMES.get(update.message.chat_id, None)
    print(game)
    if game is not None:
        response = game.get_response(text)
        for r in response:
            bot.send_message(chat_id=update.message.chat_id, text=r)
    else:
        bot.send_message(chat_id=update.message.chat_id, text=text)



start_handler = CommandHandler('start', start)
solve_handler = CommandHandler('solve', solve, pass_args=True)
matches_handler = CommandHandler('matches', matches)
exit_handler = CommandHandler('exit', exit)
echo_handler = MessageHandler(Filters.text, echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(solve_handler)
dispatcher.add_handler(matches_handler)
dispatcher.add_handler(exit_handler)
dispatcher.add_handler(echo_handler)

if __name__ == '__main__':
    print("Starting bot ...")
    updater.start_polling()

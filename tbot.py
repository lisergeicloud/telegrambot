import logging
import re
import telegram

from telegram import InlineKeyboardMarkup
from telegram.ext import (Updater, Filters,
                          CommandHandler,
                          ConversationHandler,
                          CallbackQueryHandler,
                          MessageHandler, RegexHandler)

import alphabeta
import board
import console
import evaluation
import gomokuboard
import gomokuconsole
from matches_game import MatchesGame, ACTIVE_GAMES
from mytokens import *
from wolfram_api_client import ask
from joker import get_jokes
from filters import FilterJoke, FilterTranslate
from ya_translater import translate_this
from speech import voice_handler

joke_filter = FilterJoke()
translate_filter = FilterTranslate()

SECOND = 2

COMMANDS = [
    ('/tictactoe', 'Tic-Tac-Toe 3X3'),
    ('/matches', 'Matches Game'),
    ('/solve', 'Solve math tasks. Example: /solve x^3=27'),
    ('Ask for a joke: ', '"Tell me a joke about ..."'),
    ('Ask for a translation: ', '"Translate ..."'),
    ('', 'You can use voice input function.'),
]

GAME_COMMANDS = ['play', 'run']
SOLVE_COMMANDS = ['estimate', 'solve', 'calculate', 'compute', 'quantify', 'assess', 'evaluate']


class Tbot:
    """
    Telegram bot with the following functionalities:
    - It is self-explanatory.
    - It can solve simple equations and math tasks (integrate, derive, …)
    - It can play “tic-tac-toe” and “matches”
    - It can play XO 5-in-a-row
    """
    token = telegram_token
    board_size = 3

    def __init__(self):

        self.custom_kb = []
        self.updater = Updater(token=self.token)
        self.bot = self.updater.bot
        self.dispatcher = self.updater.dispatcher
        self.games = {}
        self.games5 = {}
        self.human = {}

    def start(self, bot, update):
        response = ['{} {}'.format(x, y) for x, y in COMMANDS]
        response.insert(0, 'Make Your Choice:')
        response = '\n'.join(response)
        bot.send_message(chat_id=update.message.chat_id, text=response)

    def plain_text_manager(self, bot, update):
        '''
        This function parses plain text messages and executes correspondent rules. 
        '''
        text = update.message.text.strip().lower()
        if re.search(r"(.*(play|run).*matches.*)", text, re.IGNORECASE) is not None:
            return self.matches(bot, update)
        elif re.search(r".*(play|run).*(tic.*tac.*toe.*|deductible.*)", text, re.IGNORECASE) is not None:
            return self.ttt_size(bot, update)
        elif 'joke' in text:
            about = text.split('joke')[-1].strip()
            update.message.reply_text("Oh, you want a joke {}. Let's see...".format(about))
            try:
                response = get_jokes(text)
            except Exception as e:
                response = str(e)
            update.message.reply_text(response)
        elif 'translate' in text:
            text = text.split('translate')[-1].strip()
            try:
                response = translate_this(text)
            except Exception as e:
                response = str(e)
            update.message.reply_text(response)
        else:
            text_list = text.split()
            for w in SOLVE_COMMANDS:
                if w in text_list:
                    text = text.split(w)[-1].strip()
                    self.solve(bot, update, text.split())
                    return -1
            update.message.reply_text('Did you say: \"' + text + '\"?')
        return -1

    def t3(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text='Choose board size: 3 or 5')
        return 2

    def ttt_size(self, bot, update):
        board_size = update.message.text.strip()
        if board_size not in ['3', '5']:
            bot.sendMessage(chat_id=update.message.chat_id, text='Choose board size: 3 or 5!')
            return 2
        else:
            custom_kb = [['X'], ['O']]
            reply = telegram.ReplyKeyboardMarkup(custom_kb)
            bot.sendMessage(chat_id=update.message.chat_id, text='Choose your side:', reply_markup=reply)
            return int(board_size)

    def t5(self, bot, update):
        custom_kb = [['X'], ['O']]
        reply = telegram.ReplyKeyboardMarkup(custom_kb)
        bot.sendMessage(chat_id=update.message.chat_id, text='Choose your side:', reply_markup=reply)
        return 0

    def voice_handler(self, bot, update):
        file = self.bot.getFile(update.message.voice.file_id)
        print("file_id: " + str(update.message.voice.file_id))
        text = voice_handler(file)
        print(text)
        update.message.text = text
        return self.plain_text_manager(bot, update)

    def ttt3(self, bot, update):
        try:
            if update.message.text == "X":
                human_move = board.State.X
            elif update.message.text == 'O':
                human_move = board.State.O
        except:
            pass
        reply = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text='Preparing...', reply_markup=reply)
        self.board_size = 3
        self.games[update.message.chat_id] = [console.Console(self.board_size), [], human_move]

        for i in range(0, 9, 3):
            self.games[update.message.chat_id][1].append([telegram.InlineKeyboardButton(' ', callback_data=str(i)),
                                                          telegram.InlineKeyboardButton(' ', callback_data=str(i + 1)),
                                                          telegram.InlineKeyboardButton(' ', callback_data=str(i + 2))])
        reply = InlineKeyboardMarkup(self.games[update.message.chat_id][1])

        if human_move == board.State.O:
            self.play_move(bot, update, update.message.chat_id)

        bot.send_message(chat_id=update.message.chat_id, text='Let\'s play, my dear opponent! ', reply_markup=reply)

        return 13

    def ttt5(self, bot, update):
        try:
            if update.message.text == "X":
                human_move = gomokuboard.State.X
            elif update.message.text == 'O':
                human_move = gomokuboard.State.O
        except:
            pass
        reply = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text='Preparing...', reply_markup=reply)
        self.board_size = 8
        self.games5[update.message.chat_id] = [gomokuconsole.Console(self.board_size), [], human_move]
        for i in range(0, 64, 8):
            self.games5[update.message.chat_id][1].append([telegram.InlineKeyboardButton(' ', callback_data=str(i)),
                                                           telegram.InlineKeyboardButton(' ', callback_data=str(i + 1)),
                                                           telegram.InlineKeyboardButton(' ', callback_data=str(i + 2)),
                                                           telegram.InlineKeyboardButton(' ', callback_data=str(i + 3)),
                                                           telegram.InlineKeyboardButton(' ', callback_data=str(i + 4)),
                                                           telegram.InlineKeyboardButton(' ', callback_data=str(i + 5)),
                                                           telegram.InlineKeyboardButton(' ', callback_data=str(i + 6)),
                                                           telegram.InlineKeyboardButton(' ',
                                                                                         callback_data=str(i + 7))])
        reply = InlineKeyboardMarkup(self.games5[update.message.chat_id][1])

        if human_move == gomokuboard.State.O:
            self.play_move5(bot, update, update.message.chat_id)

        bot.send_message(chat_id=update.message.chat_id, text='Let\'s play, my dear opponent! ', reply_markup=reply)

        return 15

    def tictac3(self, bot, update):

        id = update.callback_query.message.chat_id

        self.play_move(bot, update, id)

        if self.games[id][0].board.game_over:
            self.get_winner(bot, update, id)
            return -1

        self.play_move(bot, update, id)

        if self.games[id][0].board.game_over:
            self.get_winner(bot, update, id)
            return -1

        return 13

    def play_move(self, bot, update, id):
        mc = self.games[id][0].board.move_count

        if self.games[id][0].board.get_turn() == self.games[id][2]:
            self.get_player_move(bot, update, id)
        else:
            abp = alphabeta.AlphaBetaPruning(self.games[id][0].board.board_width ** 2 - 1)
            if self.games[id][0].board.board_width > 3:
                m_p = 5
            else:
                m_p = self.games[id][0].board.board_width ** 2 - 1
            abp.run(player=self.games[id][0].board.get_turn(), board=self.games[id][0].board, max_ply=m_p)

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.games[id][0].board.board[i][j] == board.State.X:
                    self.games[id][1][i][j] = telegram.InlineKeyboardButton("❌",
                                                                            callback_data=str(i * self.board_size + j))
                elif self.games[id][0].board.board[i][j] == board.State.O:
                    self.games[id][1][i][j] = telegram.InlineKeyboardButton('⭕️',
                                                                            callback_data=str(i * self.board_size + j))

        reply = InlineKeyboardMarkup(self.games[id][1])

        if self.games[id][0].board.move_count == 1 and self.games[id][2] == board.State.O:
            pass
        elif mc < self.games[id][0].board.move_count:
            bot.editMessageText(chat_id=update.callback_query.message.chat_id,
                                message_id=update.callback_query.message.message_id,
                                text='Let\'s play, my dear opponent! ',
                                reply_markup=reply)

    def get_player_move(self, bot, update, id):

        move = int(update.callback_query.data)
        if not self.games[id][0].board.move(move):
            try:
                query = update.callback_query
                reply = InlineKeyboardMarkup(self.games[id][1])
                bot.editMessageText(
                    chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text="Press on the blank box please",
                    reply_markup=reply
                )
            except telegram.error.BadRequest:
                pass

    def get_winner(self, bot, update, id):
        winner = self.games[id][0].board.get_winner()

        if winner == board.State.Blank:
            s = "The TicTacToe is a Draw."
        else:
            s = "Player " + str(winner.name) + " wins!"

        s += "\nTo start a new game press please /tictactoe"

        query = update.callback_query
        reply = InlineKeyboardMarkup(self.games[id][1])
        bot.editMessageText(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=s,
            reply_markup=reply
        )
        del self.games[id]

    def tictac5(self, bot, update):

        id = update.callback_query.message.chat_id

        self.play_move5(bot, update, id)

        if self.games5[id][0].board.game_over:
            self.get_winner5(bot, update, id)
            return -1

        self.play_move5(bot, update, id)

        if self.games5[id][0].board.game_over:
            self.get_winner5(bot, update, id)
            return -1

        return 15

    def play_move5(self, bot, update, id):
        mc = self.games5[id][0].board.move_count

        if self.games5[id][0].board.get_turn() == self.games5[id][2]:
            self.get_player_move5(bot, update, id)
        else:
            if self.games5[id][0].board.move_count == 0:
                pl_mv = evaluation.firstmove(self.games5[id][0].board)
            elif self.games5[id][0].board.move_count == 1:
                pl_mv = evaluation.secondmove(self.games5[id][0].board)
            else:
                pl_mv = evaluation.nextMove(self.games5[id][0].board, 2, 3)
            self.games5[id][0].board.move(pl_mv)

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.games5[id][0].board.board[i][j] == gomokuboard.State.X:
                    self.games5[id][1][i][j] = telegram.InlineKeyboardButton("❌",
                                                                             callback_data=str(i * self.board_size + j))
                elif self.games5[id][0].board.board[i][j] == gomokuboard.State.O:
                    self.games5[id][1][i][j] = telegram.InlineKeyboardButton('⭕️',
                                                                             callback_data=str(i * self.board_size + j))

        reply = InlineKeyboardMarkup(self.games5[id][1])

        if self.games5[id][0].board.move_count == 1 and self.games5[id][2] == gomokuboard.State.O:
            pass
        elif mc < self.games5[id][0].board.move_count:
            bot.editMessageText(chat_id=update.callback_query.message.chat_id,
                                message_id=update.callback_query.message.message_id,
                                text='Let\'s play, my dear opponent! ',
                                reply_markup=reply)

    def get_player_move5(self, bot, update, id):

        move = int(update.callback_query.data)
        if not self.games5[id][0].board.move(move):
            try:
                query = update.callback_query
                reply = InlineKeyboardMarkup(self.games5[id][1])
                bot.editMessageText(
                    chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text="Press on the blank box please",
                    reply_markup=reply
                )
            except telegram.error.BadRequest:
                pass

    def get_winner5(self, bot, update, id):
        winner = self.games5[id][0].board.get_winner()

        if winner == gomokuboard.State.Blank:
            s = "The TicTacToe is a Draw."
        else:
            if winner == self.games5[id][2]:
                s = "You won!"
            else:
                s = "AI won!"

        s += "\nTo start a new game press please /tictactoe"

        query = update.callback_query
        reply = InlineKeyboardMarkup(self.games5[id][1])
        bot.editMessageText(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=s,
            reply_markup=reply
        )
        del self.games5[id]

    def solve(self, bot, update, args):
        """
        Solve math tasks using Wolfram Alpha.
        """
        # if not ''.join(args):
        #     result = 'You need to specify a task. For example, "\solve x+1=4"'
        #     bot.send_message(chat_id=update.message.chat_id, text=result)
        #     return
        request = ' '.join(args)
        result = ask(request)
        if result is None:
            result = "I don't know!"
        bot.send_message(chat_id=update.message.chat_id, text=result)

    def matches(self, bot, update):
        """
        Matches Game. 
        """
        game = ACTIVE_GAMES.get(update.message.chat_id, None)
        if game is None:
            game = MatchesGame(chat_id=update.message.chat_id)
            ACTIVE_GAMES[update.message.chat_id] = game
        bot.send_message(chat_id=update.message.chat_id, text=game.RULES)
        bot.send_message(chat_id=update.message.chat_id, text='Do you want to make first move? (y/n)')
        return 1

    def exit(self, bot, update):
        """
        Exit Matches Game.
        """
        try:
            del ACTIVE_GAMES[update.message.chat_id]
        except KeyError:
            pass
        response = "The game is finished."
        bot.send_message(chat_id=update.message.chat_id, text=response)
        return -1

    def move(self, bot, update):
        """
        Handles Matches moves.
        """
        text = update.message.text.strip()
        game = ACTIVE_GAMES.get(update.message.chat_id, None)
        code = 1
        if game is not None:
            code, response = game.get_response(text)
            for r in response:
                bot.send_message(chat_id=update.message.chat_id, text=r)
        return code

    def handlers(self):

        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('help', self.start))
        self.dispatcher.add_handler(CommandHandler('solve', self.solve, pass_args=True))

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('matches', self.matches),
                          CommandHandler('tictactoe', self.t3),
                          MessageHandler(Filters.voice, self.voice_handler),
                          MessageHandler(Filters.text, self.plain_text_manager)],
            states={
                1: [MessageHandler(Filters.text, self.move), CommandHandler('exit', self.exit)],
                2: [MessageHandler(Filters.text, self.ttt_size)],
                13: [CallbackQueryHandler(self.tictac3)],
                15: [CallbackQueryHandler(self.tictac5)],
                3: [MessageHandler(Filters.text, self.ttt3), CallbackQueryHandler(self.ttt3)],
                5: [MessageHandler(Filters.text, self.ttt5), CallbackQueryHandler(self.ttt5)]
            },
            fallbacks=[CommandHandler('start', self.start)]
        )

        self.dispatcher.add_handler(conv_handler)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    bot = Tbot()
    bot.handlers()
    bot.updater.start_polling()
    bot.updater.idle()

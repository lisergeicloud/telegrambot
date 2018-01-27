import random

ACTIVE_GAMES = {}


class MatchesGame:
    CHAT_ID = None
    CHOOSE_ORDER_MODE = True
    MATCHES_NUM = 21
    RULES = "MATCHES GAME.\nTHE RULES:\n" \
            "- There are 21 Match Sticks.\n" \
            "- You and bot will pick up the sticks in turn.\n" \
            "- Sticks can be picked from 1 to 4.\n" \
            "- The who, picked up the last stick, is the loser."

    def __init__(self, chat_id):
        self.CHAT_ID = chat_id

    def get_response(self, text):
        response = []
        if self.CHOOSE_ORDER_MODE:
            if text.lower() in ['y', 'yes']:
                response.append("Ok, we have {} matches. Pick 1-4 matches.".format(self.MATCHES_NUM))
            elif text.lower() in ['n', 'no']:
                response.append("Ok, I'll start. We had {} matches.".format(self.MATCHES_NUM))
                TOTAL1, TOTAL2, bot_takes = self.process_move(0)
                response.append('I take {} matches --> {} matches left. Your turn.'.format(bot_takes, TOTAL2))
            self.CHOOSE_ORDER_MODE = False
            return response
        try:
            value = int(text)
        except ValueError:
            result = 'No. You can enter only a number from 1 to 4.'
            response.append(result)
            return response
        if not text.isdigit() or value not in [1, 2, 3, 4]:
            result = 'No. You can enter only a number from 1 to 4.'
            response.append(result)
            return response
        else:
            TOTAL1, TOTAL2, bot_takes = self.process_move(value)
            response.append('You took {} matches --> {} matches left.'.format(value, TOTAL1))
            response.append('I take {} matches --> {} matches left.'.format(bot_takes, TOTAL2))
            if TOTAL1 == 1:
                response.append('You win! :) Congratulations!')
                del ACTIVE_GAMES[self.CHAT_ID]
                return response
            if TOTAL2 == 1:
                response.append('YOU LOST. :( The game is finished.')
                del ACTIVE_GAMES[self.CHAT_ID]
            else:
                response.append('Your turn.')
            return response

    def process_move(self, matches_taken):
        TOTAL1 = self.MATCHES_NUM - matches_taken
        bot_takes = (TOTAL1 - 1) % 5
        if bot_takes == 0:
            bot_takes = random.choice([1, 2, 3, 4])
        TOTAL2 = TOTAL1 - bot_takes
        self.MATCHES_NUM = TOTAL2
        return TOTAL1, TOTAL2, bot_takes

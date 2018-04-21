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
                self.CHOOSE_ORDER_MODE = False
            elif text.lower() in ['n', 'no']:
                response.append("Ok, I'll start. We had {} matches.".format(self.MATCHES_NUM))
                TOTAL1, TOTAL2, bot_takes = self.process_move(0)
                response.append('I take {} matches --> {} matches left. Your turn.'.format(bot_takes, TOTAL2))
                self.CHOOSE_ORDER_MODE = False
            else:
                response.append('Yes or No? (y/n). This is so f*cking simple, Morty!')
            return 1, response
        try:
            value = int(text)
        except ValueError:
            result = 'No, Morty. Focus! You can enter only a number from 1 to 4.'
            response.append(result)
            return 1, response
        if not text.isdigit() or value not in [1, 2, 3, 4]:
            result = 'No, Morty. Focus! You can enter only a number from 1 to 4.'
            response.append(result)
            return 1, response
        else:
            TOTAL1, TOTAL2, bot_takes = self.process_move(value)
            response.append('You took {} matches --> {} matches left.'.format(value, TOTAL1))
            if TOTAL1 == 1:
                response.append('You won! But this happend just by accident, Morty.')
                del ACTIVE_GAMES[self.CHAT_ID]
                return -1, response
            if TOTAL2 == 1:
                response.append('I take {} matches --> {} matches left.'.format(bot_takes, TOTAL2))
                response.append('I won! Morty, I am not sure you are my grandson.')
                del ACTIVE_GAMES[self.CHAT_ID]
                return -1, response
            else:
                response.append('I take {} matches --> {} matches left.'.format(bot_takes, TOTAL2))
                response.append("Your turn. Don't make me wait long.")
                return 1, response

    def process_move(self, matches_taken):
        TOTAL1 = self.MATCHES_NUM - matches_taken
        bot_takes = (TOTAL1 - 1) % 5
        if bot_takes == 0:
            bot_takes = random.choice([1, 2, 3, 4])
        TOTAL2 = TOTAL1 - bot_takes
        self.MATCHES_NUM = TOTAL2
        return TOTAL1, TOTAL2, bot_takes

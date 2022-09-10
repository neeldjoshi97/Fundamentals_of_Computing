# Mini-project #6 - Blackjack
# Paste in CodeSkulptor and have Fun !!!

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = None
score = 0
pbusted = False
dbusted = False

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.hand_list = []

    def __str__(self):
        return 'Hand Object <list_of_Card_objects>'

    def add_card(self, card):
        self.hand_list.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # pass	# compute the value of the hand, see Blackjack video
        # global score
        value = 0
        cardlist = []

        for a_card in self.hand_list:
            # print('here', cardlist)
            cardlist.append(str(a_card)[1])
            # print('there', cardlist)
        cardlist.reverse()

        for a_value in cardlist:
            # b = VALUES[a_value]
            if a_value == 'A' and value + 11 < 21:
                value += 10
            value += VALUES[a_value]

        return value

    def draw(self, canvas, pos):
        # pass	# draw a hand on the canvas, use the draw method for cards
        for each_card in self.hand_list:
            card = Card(each_card[0], each_card[1])
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]



# define deck class
class Deck:
    def __init__(self):
        self.deck_cards = []
        for i in SUITS:
            for j in RANKS:
                self.deck_cards.append(i + j)

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.deck_cards)

    def deal_card(self):
        Deck.shuffle(self)
        dummy = self.deck_cards[0]
        self.deck_cards.remove(dummy)
        return dummy

    def __str__(self):
        return 'Deck of Cards <list_of_deck_cards_symbols>'



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, pbusted, dbusted, score

    if outcome == 'started':
        print('Player voluntarily lost. Starting new game...........')
    else:
        print('\nNew game started !!!')
        outcome = 'started'

    # your code goes here
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    for i in range(2):
        player_hand.add_card(deck.deal_card())

    dealer_hand = Hand()
    for i in range(2):
        dealer_hand.add_card(deck.deal_card())

    # print(len(player_hand.hand_list))
    # print(len(dealer_hand.hand_list))

    in_play = True
    pbusted = False
    dbusted = False


def hit():
    # pass	# replace with your code below
    global in_play, score, pbusted, dbusted, outcome

    outcome = None

    if dbusted:
        print('Dealer already busted!!! Tell the dealer to start new deal !!!')

    # if the hand is in play, hit the player
    if in_play == True and not pbusted and not dbusted:
        player_hand.add_card(deck.deal_card())

    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21 and in_play:
        print("Look who's busted... !!!")
        score -= 1
        pbusted = True
    in_play = False

def stand():
    global pbusted, dbusted, player_hand, dealer_hand, in_play, outcome, score
    # pass	# replace with your code below
    outcome = None
    in_play = True

    if pbusted or dbusted:
        print('Hey, you are already busted....... Start new deal !!!')
    else:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())

        if dealer_hand.get_value() > 17:
            print('Dealer got busted ...... ')
            score += 1
            dbusted = True
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                print("Player wins the deck !!! Hurray !!!")
                score += 1
                dbusted = True
            else:
                print("The dealer wins the deck !!!")
                score -= 1
                pbusted = True

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler
def draw(canvas):
    # pass #test to make sure that card.draw works, replace with your code below
    global score, in_play, pbusted, dbusted
    # card = Card("H", "K")
    # card.draw(canvas, [300, 300])

    player_hand.draw(canvas, [100, 400])
    canvas.draw_text('Player at ' + str(player_hand.get_value()), (100, 375), 30, 'White')

    dealer_hand.draw(canvas, [100, 100])
    canvas.draw_text('Dealer at ' + str(dealer_hand.get_value()), (100, 75), 30, 'White')

    canvas.draw_text("Net score on player's side: " + str(score), (100, 275), 30, 'White')

    if in_play and not (pbusted or dbusted):
        canvas.draw_text(str("Player's turn !"), (100, 320), 30, 'Red')
    elif not in_play and not (pbusted or dbusted):
        canvas.draw_text(str("Dealer's turn !"), (100, 320), 30, 'Red')
    elif pbusted:
        canvas.draw_text(str("Look who's busted... !!!"), (100, 320), 30, 'Red')
    elif dbusted:
        canvas.draw_text(str("Dealer got busted ......"), (100, 320), 30, 'Red')

    if not(pbusted or dbusted):
        canvas.draw_polygon([[100, 100], [172, 100], [172, 196], [100, 196]], 1, 'Black', 'Red')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric

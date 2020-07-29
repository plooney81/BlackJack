from sys import exit
import random
import time



class Card(object):
    numb_direct = {
        "Ace" : 1,
        "Two" : 2,
        "Three" : 3,
        "Four" : 4,
        "Five" : 5,
        "Six" : 6,
        "Seven" : 7,
        "Eight" : 8,
        "Nine" : 9,
        "Ten" : 10,
        "Jack" : 10,
        "Queen" : 10,
        "King" : 10,
    }


    def __init__(self, suit, val):
        self.suit = suit
        self.val = val
        #self.numb = None
        self.number_val()

    def show(self):
        print(f"{self.val} of {self.suit}")

    def number_val(self):
        self.numb = Card.numb_direct.get(self.val)

    def call_numb_val(self):
        return self.numb


#Creates a many_decks number of decks of cards, 4 suites, 13 cards per suite, ranging from ace to king.
class Deck(object):

    def __init__(self, many_decks):
        self.many_decks = many_decks
        self.cards = []
        self.build()

    #Automatically called when an instance is initiated.
    def build(self):
        all_suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
        all_val = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
        for i in range(1, self.many_decks + 1): #makes many_decks number of decks
            for s in all_suits:
                for v in all_val:
                    self.cards.append(Card(s, v))

    def show(self):
        for c in self.cards:
            c.show()

    def count(self):
        print(len(self.cards))
    
    def shuffle(self):
        print("\nShuffling...")
        time.sleep(3)
        #Starts at the furthest number and stops at zero, and iterates by -1 each time.
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            # Swap elements by index in a list. use list[index] to access the element
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]
        print("\nDone\n")

    def drawCard(self):
        return self.cards.pop()



class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.hand_score = 0

    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self
    
    def showHand(self):
        print("-"*8)
        print(f"{self.name}'s cards are the:")
        for card in self.hand:
            card.show()
            time.sleep(1)
        print("-"*8)
    
    def showTopCard(self):
        time.sleep(1)
        print(f"\nYou hit and got:")
        self.hand[-1].show()
    
    def addCards(self):
        print(f"\n{self.name}'s cards add up to:")
        total = 0
        for card in self.hand:
            total += card.call_numb_val()
            #print(card.call_numb_val())
        self.hand_score = total
        print(self.hand_score)

    def clear_hand(self):
        self.hand = []

class Dealer(object):
    def __init__(self):
        self.hand = []
        self.hand_score = 0
    
    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self
    
    def showHand(self):
        print("*" * 8)
        print("Dealers cards are: ")
        for card in self.hand:
            card.show()
            time.sleep(1)
        print("*" * 8)
    
    def showTopCard(self):
        print("Dealer is showing: ")
        self.hand[-1].show()
    
    def addCards(self):
        print("\nThe Dealer's cards add up to:")
        total = 0
        for card in self.hand:
            total += card.call_numb_val()
            #print(card.call_numb_val())
        self.hand_score = total
        print(self.hand_score)
    
    def clear_hand(self):
        self.hand = []


class PlayHand(object):
    score_board = {
        "player" : 0,
        "dealer" : 0
    }

    def __init__(self, numb_decks, player_name):
        self.numb_decks = numb_decks
        self.player_name = player_name
        self.deck = Deck(numb_decks)
        self.player = Player(player_name)
        self.dealer = Dealer()
        self.play()

    def play(self):
        self.player.clear_hand()
        self.dealer.clear_hand()
        self.deck.shuffle()
        #self.deck.show()
        #deal to player then dealer from the top of the deck, iterates twice. If modulus is 0 then it deals to player, if not, then it deals to the dealer
        for i in range(0,4):
            if i % 2 == 0:
                self.player.draw(self.deck)
            else:
                self.dealer.draw(self.deck)

        self.player.showHand()
        self.player.addCards()
        print("*" * 8)
        self.dealer.showTopCard()
        print("*" * 8)
        time.sleep(2)
        player_choice = ""
        while player_choice != "stay":
            player_choice = self.playerChoice()

    def playerChoice(self):
        print("\n\nWould you like to hit or stay?")
        decision = input("> ")
        decision = decision.lower()
        if decision == "hit":
            self.player.draw(self.deck)
            self.player.showTopCard()
            time.sleep(1)
            self.player.addCards()
            if self.player.hand_score > 21:
                time.sleep(1)
                print("\nYou busted. HOUSE WINS!\n\n")
                self.dealerwins()
            return "hit"
        elif decision == "stay":
            self.dealerChoice()
            return "stay"
        else:
            print("I don't recognize that")
    
    def dealerChoice(self):
        self.dealer.showHand()
        self.dealer.addCards()
        dealer_choice = ""
        while dealer_choice != "stay":
            if self.dealer.hand_score < 17:
                print("The dealer must hit:")
                self.dealer.draw(self.deck)
                self.dealer.showTopCard()
                self.dealer.addCards()
                if self.dealer.hand_score > 21:
                    print("Dealer busts! Congrats, YOU WIN THE HAND!\n\n")
                    self.playerwins()
                dealer_choice = "hit"
            elif self.dealer.hand_score >= 17:
                dealer_choice = "stay"
            else:
                print("something went wrong, look at line 199")
                exit(0)
        self.decide_who_wins()

    def decide_who_wins(self):
        if self.dealer.hand_score > self.player.hand_score:
            self.dealerwins()
        elif self.dealer.hand_score < self.player.hand_score:
            self.playerwins()
        else:
            print("The hand is pushed.\n\n")
            dec = input("Play again?\n\n> ")
            if dec == "yes":
                self.play()
            if dec == "no":
                exit(0)

    def playerwins(self):
        PlayHand.score_board["player"] += 1
        self.prn_score()

    def dealerwins(self):
        PlayHand.score_board["dealer"] += 1
        self.prn_score()

    def prn_score(self):
        player_score = PlayHand.score_board.get("player")
        dealer_score = PlayHand.score_board.get("dealer")
        total_hands = player_score + dealer_score
        time.sleep(3)
        print(f"\n\nAfter {total_hands} hands the score is:")
        print(f"{self.player_name} has won {player_score} hands")
        print(f"The Dealer has won {dealer_score} hands")
        time.sleep(2)
        print("\n\nWould you like to play another hand?")
        resp = input("> ")
        if resp == "yes":
            self.play()
        if resp == "no":
            exit(0)



print("What is your name?")
player_name = input("> ")
time.sleep(1)

print("\nHow many decks would you like to play black jack with?")
numb_decks = int(input("> "))
time.sleep(1)

PlayHand(numb_decks, player_name)

# deck = Deck(numb_decks)
# #deck.show()

# deck.shuffle()

# deck.show()

# #card = deck.drawCard()
# #card.show()

# pete = Player("pete")
# pete.draw(deck)
# pete.showHand()


# deck.show()
# #deck.count()
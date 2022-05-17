import random

class Deck:
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    card_values = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
    suits = [u"\u2666", u"\u2665", u"\u2663", u"\u2660"]

    def __init__(self):
        self.dealer_hand = []
        self.player_hand = []
        self.deck = []
        self.money = 500
        self.bet = 0

    @classmethod
    def convert_to_value(cls, hand):
        card = [i[0] for i in hand]
        if "1" in card:
            ind = card.index("1")
            card[ind] = "10"
        value = 0
        for i in card:
            num = cls.card_values.get(i)
            value += int(num)
        if value > 21 and "A" in card:
            value -= 10
        return value

    def fill_deck(self):
        for i in self.suits:
            for j in self.cards:
                self.deck.append(j + i)
        
    def hand_reset(self):
        self.dealer_hand = []
        self.player_hand = []
        
    def deck_reset(self):
        self.deck = []

    def shuffle_cards(self):
        random.shuffle(self.deck)

    def play(self):
        play = ""
        while not play.lower() == "yes":
            play = input(f"\nYou are starting with ${self.money}. Would you like to play a hand? ")
            if play.lower() == "no":
                print(f"You left the game with {self.money}")
                quit()
        while True:
            self.bet = input("Place your bet: ")
            if int(self.bet) > self.money:
                print("You do not have sufficient funds.")
            elif int(self.bet) <= 0:
                print("The minimum bet is $1.")
            else:
                break

    def deal(self):
        self.hand_reset()
        self.deck_reset()
        self.fill_deck()
        self.shuffle_cards()
        while len(self.player_hand) < 2:
            self.player_hand.append(self.deck[0])
            self.deck.pop(0)
            self.dealer_hand.append(self.deck[0])
            self.deck.pop(0)
        str = ", ".join(self.player_hand)
        print(f"You are dealt: {str}")
        print(f"The dealer is dealt: {self.dealer_hand[0]}, Unknown")

    def hit_stay(self):
        hit_stay = input("Would you like to hit or stay? ")
        while not hit_stay.lower() == "stay":
            if hit_stay.lower() == "hit":
                self.player_hand.append(self.deck[0])
                self.deck.pop(0)
                print(f"You are dealt: {self.player_hand[-1]}")
                new_player_hand = ", ".join(self.player_hand)
                print(f"You now have: {new_player_hand}")
                value = self.convert_to_value(self.player_hand)
            else:
                print("That is not a valid option")
            if value > 21:
                print(f"Your hand value is over 21 and you lose ${self.bet}")
                self.money -= int(self.bet)
                return "no"
            hit_stay = input("Would you like to hit or stay? ")

    def hit(self, hand):
        hand.append(self.deck[0])
        self.deck.pop(0)

    def dealer_hit_stay(self):
        dealer_hand = ", ".join(self.dealer_hand)
        print(f"The dealer has: {dealer_hand}")
        value = self.convert_to_value(self.dealer_hand)
        while int(value) <= 16:
            self.hit(self.dealer_hand)
            print(f"The dealer hits and is dealt: {self.dealer_hand[-1]}")
            hand = ", ".join(self.dealer_hand)
            print(f"The dealer has: {hand}")
            value = self.convert_to_value(self.dealer_hand)

    def calc_value(self):
        dealer_value = self.convert_to_value(self.dealer_hand)
        player_value = self.convert_to_value(self.player_hand)
        if dealer_value > 21:
            if player_value == 21:
                print("The dealer busts")
                print(f"Blackjack! You win ${self.bet}")
                self.money = (int(self.money) * 150) / 100
            else:
                print(f"The dealer busts, you win ${self.bet}")
                self.money += int(self.bet)

        elif dealer_value == player_value:
            print("The dealer stays.")
            print("You tie. Your bet has been returned.")
        elif player_value == 21:
            print("The dealer stays.")
            self.bet = (int(self.bet) * 150) / 100
            self.money += int(self.bet)
            print(f"Blackjack! You win ${self.bet}")
        elif dealer_value > player_value:
            print("The dealer stays.")
            print(f"The dealer wins, you lose ${self.bet}")
            self.money -= int(self.bet)
        elif player_value > dealer_value:
            print("The dealer stays.")
            print(f"You win ${self.bet}")
            self.money += int(self.bet)

d = Deck()
print("Welcome to Blackjack!")
while d.money > 0:
    d.play()
    d.deal()
    if d.hit_stay() == "no":
        continue
    else:
        d.dealer_hit_stay()
        d.calc_value()
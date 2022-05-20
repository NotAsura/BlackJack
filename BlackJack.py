import random

# Deck Object that is used for blackjack
class Deck:
    # Class variables that contain everything used to make each card and their values
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    card_values = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
    suits = [u"\u2666", u"\u2665", u"\u2663", u"\u2660"]

    # Creates object variables when intialized
    def __init__(self):
        self.dealer_hand = []
        self.player_hand = []
        self.deck = []
        self.money = 500
        self.bet = 0

    # Outputs the value of the hand when either the hand of the player or the dealer is inputted
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

    # Fills the deck variable with the 52 cards present in a normal deck
    def fill_deck(self):
        for i in self.suits:
            for j in self.cards:
                self.deck.append(j + i)
    
    # Sets the dealer and players hand to an empty array
    def hand_reset(self):
        self.dealer_hand = []
        self.player_hand = []
    
    # Sets the deck to an empty array
    def deck_reset(self):
        self.deck = []

    # Randomizes the order of the cards in the deck variable
    def shuffle_cards(self):
        random.shuffle(self.deck)

    """Asks if the player would like to play a hand. If player answers so they walk away
    with the amount of money they have. Otherwise the script asks the player for a amount to bet.
    This amount is then checked to see if it is less than the amount of money they have and 
    that it isn't a negative number. If the bet is either one of these the script asks the amount
    the player wants to bet again."""
    def play(self):
        play = ""
        while not play.lower() == "yes":
            play = input(f"\nYou are starting with ${self.money}. Would you like to play a hand? ")
            if play.lower() == "no":
                print(f"You left the game with ${self.money}")
                quit()
        while True:
            self.bet = input("Place your bet: ")
            if int(self.bet) > self.money:
                print("You do not have sufficient funds.")
            elif int(self.bet) <= 0:
                print("The minimum bet is $1.")
            else:
                break

    """Resets the hand and deck, fills the deck and shuffles it. Then deals the player and dealer alternating cars
    until they both have 2 cards in their hand. After that the script outputs the cards that the player has
    and the first card the dealer has"""
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

    """Asks if the player would like to hit or stay. If player hits they are dealt a card from the
    top of the deck and told what card they drew. If the value of the cards in the players hand is bigger
    than 21 then they bust and lose their bet. """
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

    #Removes the top card from the deck and adds it to the hand imputed into the function
    def hit(self, hand):
        hand.append(self.deck[0])
        self.deck.pop(0)

    """If the dealer has a value below or equal to 16 they dealer has to hit and if the dealer
    has a value above 16 then the dealer hits"""
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

    """This function compares the values of the players hand and the dealers hand to determine who wins
    and who loses. Then changes the value of the players money depending on if they drew won or lost. If the player
    gets Blackjack (hand value of 21) they win and 1.5x their bet and that is added to their total money"""
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

"""Calls the methods of the deck object and uses it to make the game progress"""
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
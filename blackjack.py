import random
from colorama import Fore, Style

__author__ = "Adeola Odusola"
__date__ = "2023-01-31"
__version__ = "1.0.2"


def pick_card(all_cards):
    # pick from top of deck
    card = all_cards[0]
    # remove from deck
    all_cards.remove(card)
    return card


def deal_cards(p, d, deck):
    card = pick_card(deck)
    p.append(card)
    print("dealing first card for player...", card)
    card = pick_card(deck)
    d.append(card)
    print("dealing first card for dealer...", card)
    card = pick_card(deck)
    p.append(card)
    print("dealing second card for player...", card)
    card = pick_card(deck)
    d.append(card)
    print("dealing second card for dealer... *")


def display_process(card, card_array, suit):
    if card_array[0] == "1" or card_array[0] == "11":
        card_for_display = "A" + suit
    elif not card_array[0].isnumeric():
        card_for_display = card[0] + suit
    else:
        card_for_display = card_array[0] + suit
    return card_for_display


def display_cards(cs):
    cards_for_display = []
    suits = {"clubs": "\u2663", "diamonds": "\u2666", "hearts": "\u2665", "spades": "\u2660"}
    for card in cs:
        card = str(card)
        card_array = card.split()
        if "clubs" in card:
            card_for_display = display_process(card, card_array, suits["clubs"])
            cards_for_display.append(card_for_display)
        if "diamonds" in card:
            card_for_display = display_process(card, card_array, suits["diamonds"])
            cards_for_display.append(card_for_display)
        if "hearts" in card:
            card_for_display = display_process(card, card_array, suits["hearts"])
            cards_for_display.append(card_for_display)
        if "spades" in card:
            card_for_display = display_process(card, card_array, suits["spades"])
            cards_for_display.append(card_for_display)
    return cards_for_display


def view_player_cards(p):
    display = display_cards(p)
    print("player's cards: ", display)


def view_dealer_cards(d, ini=False):
    display = display_cards(d)
    if ini:
        # hide dealer's second card
        print("dealer's cards: ['", display[0], ", '*']")
    else:
        print("dealer's cards: ", display)


def player_hint(total, deck):
    # first peek at the card, then return decision
    next_card = deck[0]
    print("peeking at next card in deck...", display_cards([next_card]))
    if "Ace" in next_card:
        # using 11
        next_card = "11"
    potential_total = total + get_total([next_card])
    if potential_total > 21:
        # stand - do not pick another card - it will be over 21
        hint = 1
    else:
        # pick another card
        hint = 2
    return hint


def player_decision(p_cards, deck):
    choice = 0
    index = 0
    for p_card in p_cards:
        p_card = str(p_card)
        if "Ace" in p_card:
            suit = p_card.replace("Ace", "")
            while True:
                try:
                    ace = int(input("What is your Ace value? Enter 1 or 11:\n"))
                    if ace != 1 and ace != 11:
                        print("Enter 1 or 11!")
                    else:
                        break
                except Exception as ex:
                    print("Input Exception! Enter 1 or 11: ", ex)
            p_cards[index] = str(ace) + suit
        index += 1
    # get total
    total = get_total(p_cards)
    print("player's current total is: ", total)
    if total > 21:
        print("Player is busted!")
        return 0, p_cards
    # add HINT for player - peek at deck, see if deck[0] + total is far from 21 or close
    while True:
        try:
            ask_for_hint = int(input("Do you need a hint?\n"
                                     "Enter 1 for Yes\n"
                                     "Enter 0 for No\n"))
            if ask_for_hint != 0 and ask_for_hint != 1:
                print("Enter 0 or 1!")
            else:
                if ask_for_hint == 1:
                    hint = player_hint(total, deck)
                    if hint == 1:
                        print(Fore.RED + "You are advised to stand!")
                    else:
                        print(Fore.RED + "You are advised to pick another card!")
                    print(Style.RESET_ALL)
                break
        except Exception as ex:
            print("Input Exception! Enter 1 or 2: ", ex)
    # player makes decision
    while True:
        try:
            choice = int(input("Do you stand on your cards or want to pick another card?\n"
                               "Enter 1 to stand\n"
                               "Enter 2 to pick another card\n"))
            if choice != 1 and choice != 2:
                print("Enter 1 or 2!")
            else:
                if choice == 1:
                    print("player decides to stand...")
                elif choice == 2:
                    card = pick_card(deck)
                    p_cards.append(card)
                    print("picking another card for player...", card)
                break
        except Exception as ex:
            print("Input Exception! Enter 1 or 2: ", ex)
    return choice


def dealer_decision(d_cards, deck):
    # check ace and try 11 first
    cutoff = 17
    index = 0
    for d_card in d_cards:
        d_card = str(d_card)
        if "Ace" in d_card:
            suit = d_card.replace("Ace", "")
            d_cards[index] = "11" + suit
            total = get_total(d_cards)
            if total > 21:
                # bust try 1
                d_cards[index] = "1" + suit
        index += 1
    total = get_total(d_cards)
    if total > 21:
        print("Dealer is busted!")
        return 0, d_cards
    if total >= cutoff:
        choice = 1
        print("dealer decides to stand...")
    else:
        choice = 2
        card = pick_card(deck)
        d_cards.append(card)
        print("dealer is picking another card...", card)
    return choice


def get_total(cs):
    total = 0
    for card in cs:
        card = str(card)
        if "King" in card:
            total += 10
        elif "Queen" in card:
            total += 10
        elif "Jack" in card:
            total += 10
        else:
            card_arr = card.split()
            number = card_arr[0]
            total += int(number)
    return total


def display_results(p_total, d_total):
    if p_total > 21 and d_total > 21:
        print("Both player and dealer are busted!")
        print("Player total: ", p_total)
        print("Dealer total: ", d_total)
        print(Fore.RED + "Game ends in a tie!")
        print(Style.RESET_ALL)
    elif p_total > 21 >= d_total:
        print("Player is busted!")
        print("Player total: ", p_total)
        print("Dealer total: ", d_total)
        print(Fore.RED + "Dealer wins the game!")
        print(Style.RESET_ALL)
    elif p_total <= 21 < d_total:
        print("Dealer is busted!")
        print("Player total: ", p_total)
        print("Dealer total: ", d_total)
        print(Fore.RED + "Player wins the game!")
        print(Style.RESET_ALL)
    elif p_total == d_total:
        print("Player total: ", p_total)
        print("Dealer total: ", d_total)
        print(Fore.RED + "Game ends in a tie!")
        print(Style.RESET_ALL)
    elif p_total > d_total:
        print("Player total: ", p_total)
        print("Dealer total: ", d_total)
        print(Fore.RED + "Player wins the game!")
        print(Style.RESET_ALL)
    elif d_total > p_total:
        print("Player total: ", p_total)
        print("Dealer total: ", d_total)
        print(Fore.RED + "Dealer wins the game!")
        print(Style.RESET_ALL)


if __name__ == '__main__':
    print("***************************WELCOME TO BLACKJACK WORLD*******************************")
    while True:
        print("*" * 50)
        print("Black Jack game is starting...")
        cards = ["Ace of clubs", "2 of clubs", "3 of clubs", "4 of clubs", "5 of clubs",
                 "6 of clubs", "7 of clubs", "8 of clubs", "9 of clubs", "10 of clubs",
                 "King of clubs", "Queen of clubs", "Jack of clubs",
                 "Ace of diamonds", "2 of diamonds", "3 of diamonds", "4 of diamonds", "5 of diamonds",
                 "6 of diamonds", "7 of diamonds", "8 of diamonds", "9 of diamonds", "10 of diamonds",
                 "King of diamonds", "Queen of diamonds", "Jack of diamonds",
                 "Ace of hearts", "2 of hearts", "3 of hearts", "4 of hearts", "5 of hearts",
                 "6 of hearts", "7 of hearts", "8 of hearts", "9 of hearts", "10 of hearts",
                 "King of hearts", "Queen of hearts", "Jack of hearts",
                 "Ace of spades", "2 of spades", "3 of spades", "4 of spades", "5 of spades",
                 "6 of spades", "7 of spades", "8 of spades", "9 of spades", "10 of spades",
                 "King of spades", "Queen of spades", "Jack of spades",
                 ]
        print("shuffling cards...")
        random.shuffle(cards)
        # print(cards)
        print("2 rounds of cards are being dealt to player and dealer...")
        # cards are pulled from the top after shuffling -> player, dealer, player, dealer
        player_cards = []
        dealer_cards = []
        deal_cards(player_cards, dealer_cards, cards)
        view_player_cards(player_cards)
        view_dealer_cards(dealer_cards, True)
        # process for player
        while True:
            decision = player_decision(player_cards, cards)
            view_player_cards(player_cards)
            if decision != 2:
                break
        player_total = get_total(player_cards)
        print("******************************************************")
        # process for dealer
        while True:
            decision = dealer_decision(dealer_cards, cards)
            if decision != 2:
                break
        view_dealer_cards(dealer_cards)
        dealer_total = get_total(dealer_cards)
        display_results(player_total, dealer_total)
        # print("cards: ", cards)
        # print("count of cards left in deck: ", len(cards))
        print("End of game...")
        play_again = 0
        while True:
            try:
                play_again = int(input("Would you like to play another game?\n"
                                       "Enter 0 to quit\n"
                                       "Enter 1 to play another game\n"))
                if play_again != 0 and play_again != 1:
                    print("Please enter 0 to quit or 1 to play again!")
                else:
                    break
            except Exception as e:
                print("Input Exception! Enter 0 or 1: ", e)
        if play_again == 0:
            break

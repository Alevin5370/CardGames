import random, sys
from scoreCheck import get_high_score, update_high_score
from cards import createCards

GAME = "rideTheBus"
states = {}
states.update({
    "playermoney": 200.00,
    "bet": 0.0,
    "payout": 0.0,
    "cardsInDeck": 0
    })

def shuffleCards():
    deck = createCards()
    for i in range(1,3):
        random.shuffle(deck)
    states['cardsInDeck'] = len(deck)
    return deck

def findBetween(card1, card2, card3):
    value_order = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
    index1 = value_order.index(card1[0])
    index2 = value_order.index(card2[0])
    index3 = value_order.index(card3[0])
    list = [index1, index2, index3]
    list.sort()
    if(list[0] == index3 or list[2] == index3):
        if(index1 == index2 or index1 == index3 or index2 == index3):
            return True
        return False
    else:
        return True

def continueGame():
    continue_game = ""
    while(continue_game != "y" and continue_game != "n"):
        continue_game=input("Continue to next phase? (y/n): ").lower()
        if(continue_game not in ['n','y']):
            print("Invalid input, please enter y or n.")
        else:
            break
    if(continue_game == "n"):
        print(f"You cash out with ${states['payout']:.2f}")
        states['playermoney'] += states['payout']
        return False
    else:
        return True

def highScoreCheck():
    score, date, time = get_high_score(GAME)
    if score == 0:
        print("No high score yet")
    else:
        print(f"Current high score: ${score:.2f} set on {date} at {time}")

def highScoreUpdate():
    if update_high_score(GAME, states['playermoney']):
        print("Congratulations! You set a new high score!")
    else: None

def main():  
    while(True):
        gameBeingPlayed = True
        while(gameBeingPlayed):
            money=states['playermoney']
            print("\nWelcome to Ride the Bus!\n")
            highScoreCheck()
            print(f'You have ${money:.2f}')
            while(True):
                try:
                    states['bet']=float(input("How much would you like to bet? $"))
                except KeyboardInterrupt:
                    print("\nExiting game.")
                    sys.exit()
                except:
                    print("please enter a valid bet amount")
                    continue
                if(states['playermoney']<(states['bet'])):
                    print("you do not have that much money")
                elif(states['bet']<=0):
                    print("nice try")
                else:
                    break
            states['payout'] = 0.0
            print("=== RIDE THE BUS ===\n")
            print("PHASE 1: Red or Black")
            invalid_input = False
            deck = shuffleCards()
            card1 = deck.pop()
            while(invalid_input == False):
                print(f"Predict Red (R) or Black (B)")
                guess = input("Your guess: ").upper()
                if(guess not in ['R','B']):
                    print("Invalid input, please enter R or B.")
                else:
                    invalid_input = True
            print(f"The card is: {card1}")
            if((guess == 'R' and card1[1] == 'Diamonds') or (guess == 'R' and card1[1] == 'Hearts') or (guess == 'B' and card1[1] == 'Spades') or (guess == 'B' and card1[1] == 'Clubs')):
                print("Correct! You win this round.")
                states['payout'] += states['bet']
            else:
                print("Wrong! You lose this round.")
                states['playermoney'] -= states['bet']
                break
            print(f"Your current payout is: ${states['payout']:.2f}")
            if (continueGame()==False):
                break
            print("\nPHASE 2: Higher or Lower")
            invalid_input = False
            card2 = deck.pop()
            while(invalid_input == False):
                print(f"Predict Higher (H) or Lower (L) than {card1}")
                guess = input("Your guess: ").upper()
                if(guess not in ['H','L']):
                    print("Invalid input, please enter H or L.")
                else:
                    invalid_input = True
            print(f"The card is: {card2}")
            value_order = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
            if((guess == 'H' and value_order.index(card2[0]) > value_order.index(card1[0])) or (guess == 'L' and value_order.index(card2[0]) < value_order.index(card1[0]))):
                print("Correct! You win this round.")
                states['payout'] += states['bet']
            else:
                print("Wrong! You lose this round.")
                states['playermoney'] -= states['bet']
                break
            print(f"Your current payout is: ${states['payout']:.2f}")
            if (continueGame()==False):
                break
            print("\nPHASE 3: Inside or Outside")
            invalid_input = False
            card3 = deck.pop()
            while(invalid_input == False):
                print(f"Predict Inside (I) or Outside (O) of {card1} and {card2}")
                guess = input("Your guess: ").upper()
                if(guess not in ['I','O']):
                    print("Invalid input, please enter I or O.")
                else:
                    invalid_input = True
            print(f"The card is: {card3}")
            if(findBetween(card1, card2, card3) and guess == 'I' or (not findBetween(card1, card2, card3) and guess == 'O')):
                print("Correct! You win this round.")
                states['payout'] += states['bet']
            else:
                print("Wrong! You lose this round.")
                states['playermoney'] -= states['bet']
                break
            print(f"Your current payout is: ${states['payout']:.2f}")
            if (continueGame()==False):
                break
            print("\nPHASE 4: Suit")
            invalid_input = False
            card4 = deck.pop()
            while(invalid_input == False):
                print(f"Predict the suit of the card: Hearts (H), Diamonds (D), Clubs (C), Spades (S)")
                guess = input("Your guess: ").upper()
                if(guess not in ['H','D','C','S']):
                    print("Invalid input, please enter H, D, C, or S.")
                else:
                    invalid_input = True
            print(f"The card is: {card4}")
            if((guess == 'H' and card4[1] == 'Hearts') or (guess == 'D' and card4[1] == 'Diamonds') or (guess == 'C' and card4[1] == 'Clubs') or (guess == 'S' and card4[1] == 'Spades')):
                print("Correct! You win this round.")
                states['payout'] = (states['bet']*20)
            else:
                print("Wrong! You lose this round.")
                states['playermoney'] -= states['bet']
                break
            print(f"Your current payout is: ${states['payout']:.2f}")
            states['playermoney'] += states['payout']
            print(f"You cash out with ${states['playermoney']:.2f}")
            playAgain = input("Congratulations! You completed all phases. Would you like to play again? (y/n): ")
            if(playAgain.lower() == 'n'):
                gameBeingPlayed = False
                break
            else:
                print("\nStarting new game...\n")
        print("Thanks for playing Ride the Bus!")
        repeat = ""
        while(repeat != 'y' and repeat != 'n'):
            repeat=input("Would you like to play again? (y/n): ").lower()
        if(repeat == 'n'):
            print(f"You cash out with ${states['playermoney']:.2f}")
            highScoreUpdate()
            print("Goodbye!")
            break
        elif(repeat == 'y'):
            print("\nStarting new game...\n")

if __name__ == "__main__":
    main()

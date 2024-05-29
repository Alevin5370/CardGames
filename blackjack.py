import random
from cards import createCards
# from termcolor import colored

def shuffleCards():
    deck = createCards()
    # shuffledDeck = []
    # print("Shuffling deck")
    for i in range(1,3):
        random.shuffle(deck)
    return deck


def handCalculator(hand):
    playerValue=0
    for card in hand:
        if card[0] in ["J", "Q", "K"]:
            playerValue+=10
        elif isinstance(card[0],int):
            playerValue+= card[0]
        else:
            if (playerValue+11)>21:
                playerValue+=1
            else:
                playerValue+=11
    return playerValue

def main():
    playerWins=0
    dealerWins=0
    print("Welcome to Blackjack: \n")
    while(True):
        decision = ''
        again=''
        playerHand = []
        playerValue=0
        dealerHand=[]
        dealerValue=0
        print("Shuffling and Dealing cards...")
        deck=shuffleCards()
        playerHand.append(deck.pop(0))
        dealerHand.append(deck.pop(0))
        playerHand.append(deck.pop(0))
        dealerHand.append(deck.pop(0))
        playerValue=handCalculator(playerHand)
        dealerValue=handCalculator(dealerHand)
        # print("The dealer has a ",dealerHand[0])
        print("You have ", *playerHand)
        print("Your hand has a value of ", playerValue)
        if playerValue == 21:
            print("21! You win! :)")
            playerWins+=1
        else:
            while(decision != 'STAY'):
                print("The dealer has a ", dealerHand[0])
                decision=input("would you like to hit or stay? ")
                decision=decision.upper()
                decision.strip()
                if decision == 'HIT':
                    playerHand.append(deck.pop(0))
                    for card in playerHand:
                        if card[0] == 'A':
                            playerHand.remove(card)
                            playerHand.append(card)
                    print("New hand: ", *playerHand)
                    playerValue=handCalculator(playerHand)
                    print("You now have: ", playerValue)
                if playerValue>=21:
                    break
            if playerValue>21:
                print("Bust :(")
                dealerWins+=1
            elif playerValue == 21:
                print("21! You win! :)")
                playerWins+=1
            else:
                print("The dealer has ", *dealerHand, " which is a value of ", dealerValue)
                while ((dealerValue<17) and (dealerValue<playerValue)):
                    print("The dealer hits...")
                    dealerHand.append(deck.pop(0))
                    for card in dealerHand:
                        if card[0] == 'A':
                            dealerHand.remove(card)
                            dealerHand.append(card)
                    dealerValue=handCalculator(dealerHand)
                    print("The dealer now has ", *dealerHand, " which is a value of ", dealerValue)
                    if dealerValue>21: 
                        print("Dealer busts. You Win! :)")
                        playerWins+=1
                if dealerValue>21:
                    continue
                elif (dealerValue<playerValue):
                    print("You have ", playerValue, " and the dealer has ", dealerValue, "\nYou win! :)")
                    playerWins+=1
                elif(dealerValue>playerValue):
                    print("You have ", playerValue, " and the dealer has ", dealerValue, ".\nThe dealer wins :(")
                    dealerWins+=1
                elif(dealerValue==playerValue):
                    print("You have ", playerValue, " and the dealer has ", dealerValue, ".\nTie... :|")
        print("You have won ", playerWins, " times and the dealer has won ", dealerWins, " times")
        if again == '': 
            again=input("Would you like to play again?(default is yes) ")
            if again.upper() == "NO":
                break
            else:
                continue

if __name__ == "__main__":
    main()
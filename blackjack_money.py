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
    playermoney=200
    # dealerWins=0
    buyin=20
    print("Welcome to Blackjack: \n")
    while(True):
        print("You have $", playermoney)
        print("The buy in is $", buyin)
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
        bet=0
        while(True):
            bet=int(input("How much would you like to bet? "))
            if(playermoney<(bet+buyin)):
                print("you do not have that much money")
            elif(bet<0):
                print("nice try")
            else:
                break
        if playerValue == 21:
            print("21! You win! :)")
            playermoney+=(bet+buyin)
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
                playermoney-=(bet+buyin)
            elif playerValue == 21:
                print("21! You win! :)")
                playermoney+=(bet+buyin)
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
                        playermoney+=(bet+buyin)
                if dealerValue>21:
                    continue
                elif (dealerValue<playerValue):
                    print("You have ", playerValue, " and the dealer has ", dealerValue, "\nYou win! :)")
                    playermoney+=(bet+buyin)
                elif(dealerValue>playerValue):
                    print("You have ", playerValue, " and the dealer has ", dealerValue, ".\nThe dealer wins :(")
                    playermoney-=(bet+buyin)
                elif(dealerValue==playerValue):
                    print("You have ", playerValue, " and the dealer has ", dealerValue, ".\nTie... :|")
        if again == '': 
            if (playermoney==0):
                print("you are out of money. :( Ending game.")
                break
            again=input("Would you like to play again?(default is yes) ")
            if again.upper() == "NO":
                break
            else:
                continue

if __name__ == "__main__":
    main()
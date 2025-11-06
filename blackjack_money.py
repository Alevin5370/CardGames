import random
from time import sleep
from cards import createCards

states = {}
states.update({
    "playerBusts1": False,
    "playerBusts2": False,
    "hasDealerPlayed" : False,
    "playermoney": 200
    })

def shuffleCards():
    deck = createCards()
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

def playHand(dealerHand, playerHand, deck, playerBusts):
    decision = ''
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
            if playerValue>21:
                states[playerBusts] = True
                break

def evaluteHand(playerValue, dealerValue, bet, playermoney):
    if playerValue == 21:
        print("21! You win! :)")
        states[playermoney]+=(bet)
    else:
        if dealerValue>21: 
            print("Dealer busts. You Win! :)")
            states[playermoney]+=(bet)
        elif (dealerValue<playerValue):
            print("You have ", playerValue, " and the dealer has ", dealerValue, "\nYou win! :)")
            states[playermoney]+=(bet)
        elif(dealerValue>playerValue):
            print("You have ", playerValue, " and the dealer has ", dealerValue, ".\nThe dealer wins :(")
            states[playermoney]-=(bet)
        elif(dealerValue==playerValue):
            print("You have ", playerValue, " and the dealer has ", dealerValue, ".\nTie... :|")

def dealerPlay(dealerHand, deck, playerValue, hasDealerPlayed):
    dealerValue=handCalculator(dealerHand)
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
        sleep(1)
    states[hasDealerPlayed] = True   
    
def main():
    print("Welcome to Blackjack: \n")
    while(True):
        buyin=20
        print("You have $", states['playermoney'])
        bet=0
        while(True):
            try:
                bet=int(input("How much would you like to bet? "))
            except:
                print("please enter a valid bet amount")
                continue
            if(states['playermoney']<(bet+buyin)):
                print("you do not have that much money")
            elif(bet<0):
                print("nice try")
            else:
                break
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
        print("You have ", *playerHand)
        print("Your hand has a value of ", playerValue)
        if playerHand[0][0] == playerHand[1][0]:
            print("You have a pair of ", playerHand[0][0], "s!")
            splitDecision = input("Would you like to split? (yes/no) ")
            splitDecision = splitDecision.upper()
            splitDecision.strip()
            if splitDecision == 'YES':
                print("Splitting hand...")
                hand1 = [playerHand[0], deck.pop(0)]
                hand2 = [playerHand[1], deck.pop(0)]
                print("Hand 1: ", *hand1)
                hand1Value = handCalculator(hand1)
                print("Hand 1 value: ", hand1Value)
                print("Hand 2: ", *hand2)
                hand2Value = handCalculator(hand2)
                print("Hand 2 value: ", hand2Value)
                print("Playing Hand 1:")
                playHand(dealerHand, hand1, deck, 'playerBusts1')
                hand1Value = handCalculator(hand1)
                print("Final Hand 1: ", *hand1, " Value: ", hand1Value)
                sleep(1)
                print("Playing Hand 2:")
                playHand(dealerHand, hand2, deck, 'playerBusts2')
                hand2Value = handCalculator(hand2)
                print("Final Hand 2: ", *hand2, " Value: ", hand2Value)
                sleep(1)
                if states['playerBusts1'] != True:
                    dealerPlay(dealerHand, deck, hand1Value, 'hasDealerPlayed')
                    dealerValue = handCalculator(dealerHand)
                    evaluteHand(hand1Value, dealerValue, bet, 'playermoney')
                if states['playerBusts2'] != True:
                    if states['hasDealerPlayed'] == True:
                        dealerValue = handCalculator(dealerHand)
                        evaluteHand(hand2Value, dealerValue, bet, 'playermoney')
                    else:
                        dealerPlay(dealerHand, deck, hand2Value, 'hasDealerPlayed')
                        dealerValue = handCalculator(dealerHand)
                        evaluteHand(hand2Value, dealerValue, bet, 'playermoney')
        else:
            playHand(dealerHand, playerHand, deck, 'playerBusts1')
            playerValue=handCalculator(playerHand)
            print("Final hand: ", *playerHand, " Value: ", playerValue)
            sleep(1)
            if states['playerBusts1'] != True:
                dealerPlay(dealerHand, deck, playerValue, 'hasDealerPlayed')
                dealerValue = handCalculator(dealerHand)
                evaluteHand(playerValue, dealerValue, bet, 'playermoney')
            else:
                print("Bust :(")
                states['playermoney']-=(bet)
        if again == '': 
            if (states['playermoney']==0):
                print("you are out of money. :( Ending game.")
                break
            again=input("Would you like to play again?(default is yes) ")
            if again.upper() == "NO":
                break
            else:
                states['playerBusts1']=False
                states['playerBusts2']=False
                states['hasDealerPlayed']=False
                continue

if __name__ == "__main__":
    main()


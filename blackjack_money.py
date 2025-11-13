import random, sys
from time import sleep
from cards import createCards

states = {}
states.update({
    "playerBusts1": False,
    "playerBusts2": False,
    "hasDealerPlayed" : False,
    "playermoney": 200,
    "bet": 0,
    "split": 0 
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
            sleep(1) 
            if playerValue>21:
                states[playerBusts] = True
                break

def evaluteHand(playerValue, dealerValue, bet, playermoney, handname=None):
    if handname:
        print("Evaluating ", handname, "...")
    if playerValue == 21:
        if(dealerValue==playerValue):
            print("You have ", playerValue, " and the dealer has ", dealerValue, "\nTie...   :/")
        else:
            print("21! You win! :)")
            states[playermoney]+=(states[bet]*1.5)
    else:
        if dealerValue>21: 
            print("Dealer busts. You Win! :)")
            states[playermoney]+=(states[bet]*1.5)
        elif (dealerValue<playerValue):
            print("You have ", playerValue, " and the dealer has ", dealerValue, "\nYou win! :)")
            states[playermoney]+=(states[bet]*1.5)
        elif(dealerValue>playerValue):
            print("You have ", playerValue, " and the dealer has ", dealerValue, "\nThe dealer wins :(")
            states[playermoney]-=(states[bet])
        elif(dealerValue==playerValue):
            print("You have ", playerValue, " and the dealer has ", dealerValue, "\nTie...   :/")

def dealerPlay(dealerHand, deck, playerValue, hasDealerPlayed):
    dealerValue=handCalculator(dealerHand)
    print("The dealer has ", *dealerHand, " which is a value of ", dealerValue)
    while ((dealerValue<17) and (dealerValue<playerValue)):
        print("The dealer hits...")
        sleep(1.5)
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
        print("You have $", states['playermoney'])
        while(True):
            try:
                states['bet']=float(input("How much would you like to bet? "))
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
        again=''
        splitDecision = ''
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
        print("The dealer has a ", dealerHand[0])   
        if playerHand[0][0] == playerHand[1][0]:
            while True:
                print("You have a pair of ", str(playerHand[0][0]) + "s!")
                splitDecision = input("Would you like to split? (yes/no) ")
                splitDecision = splitDecision.upper()
                splitDecision.strip()
                if splitDecision == 'YES':
                    break
                elif splitDecision == 'NO':
                    break
                else:
                    print("Please enter a valid response.")
                    continue
        if splitDecision == 'YES':
            if states['playermoney']<(states['bet']*2):
                print("You do not have enough money to split.")
            else:
                print("Splitting hand...")
                hand1 = [playerHand[0], deck.pop(0)]
                hand2 = [playerHand[1], deck.pop(0)]
                states['split']=states['bet']
                print("Playing Hand 1:")
                print("Hand 1: ", *hand1)
                hand1Value = handCalculator(hand1)
                print("Hand 1 value: ", hand1Value)
                playHand(dealerHand, hand1, deck, 'playerBusts1')
                hand1Value = handCalculator(hand1)
                print("Final Hand 1: ", *hand1, " Value: ", hand1Value)
                sleep(1)
                print("Playing Hand 2:")
                print("Hand 2: ", *hand2)
                hand2Value = handCalculator(hand2)
                print("Hand 2 value: ", hand2Value)
                playHand(dealerHand, hand2, deck, 'playerBusts2')
                hand2Value = handCalculator(hand2)
                print("Final Hand 2: ", *hand2, " Value: ", hand2Value)
                sleep(1)
                if states['playerBusts1'] != True:
                    dealerPlay(dealerHand, deck, hand1Value, 'hasDealerPlayed')
                    dealerValue = handCalculator(dealerHand)
                    evaluteHand(hand1Value, dealerValue, 'bet', 'playermoney', 'Hand 1')
                else:
                    print("Hand 1 Bust :(")
                    states['playermoney']-=(states['bet'])
                if states['playerBusts2'] != True:
                    if states['hasDealerPlayed'] == True:
                        dealerValue = handCalculator(dealerHand)
                        evaluteHand(hand2Value, dealerValue, 'split', 'playermoney', 'Hand 2')
                    else:
                        dealerPlay(dealerHand, deck, hand2Value, 'hasDealerPlayed')
                        dealerValue = handCalculator(dealerHand)
                        evaluteHand(hand2Value, dealerValue, 'split', 'playermoney', 'Hand 2')
                else:
                    print("Hand 2 Bust :(")
                    states['playermoney']-=(states['split'])
        else:
            while True:
                doubleDecision = input("Would you like to double down? (yes/no) ")
                doubleDecision = doubleDecision.upper()
                doubleDecision.strip()
                if doubleDecision == 'YES':
                    if states['playermoney']<(states['bet']*2):
                        print("You do not have enough money to double down.")
                    else:
                        print("Doubling down...")
                        states['bet']*=2
                    break
                elif doubleDecision == 'NO':
                    break
                else:
                    print("Please enter a valid response.")
                    continue
            playHand(dealerHand, playerHand, deck, 'playerBusts1')
            playerValue=handCalculator(playerHand)
            print("Final hand: ", *playerHand, " Value: ", playerValue)
            sleep(1)
            if states['playerBusts1'] != True:
                dealerPlay(dealerHand, deck, playerValue, 'hasDealerPlayed')
                dealerValue = handCalculator(dealerHand)
                evaluteHand(playerValue, dealerValue, 'bet', 'playermoney')
            else:
                print("Bust :(")
                states['playermoney']-=(states['bet'])
        if again == '': 
            if (states['playermoney']==0):
                print("you are out of money. :( Ending game.")
                break
            again=input("Would you like to play again?(default is yes) ")
            if again.upper() == "NO":
                print("Thanks for playing! You are leaving with $", states['playermoney'])
                break
            else:
                states['playerBusts1']=False
                states['playerBusts2']=False
                states['hasDealerPlayed']=False
                continue

if __name__ == "__main__":
    main()

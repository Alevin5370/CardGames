import random, sys
from scoreCheck import get_high_score, update_high_score
from time import sleep
from cards import createCards

GAME = "blackjack"
states = {}
states.update({
    "playerBusts1": False,
    "playerBusts2": False,
    "hasDealerPlayed" : False,
    "playermoney": 200.00,
    "bet": 0.0,
    "split": 0.0,
    "cardsInDeck": 0
    })

def shuffleCards():
    deck = createCards()
    for i in range(1,3):
        random.shuffle(deck)
    states['cardsInDeck'] = len(deck)
    return deck

def handCalculator(hand):
    aceCount = 0
    playerValue=0
    for card in hand:
        if card[0] in ["J", "Q", "K"]:
            playerValue+=10
        elif isinstance(card[0],int):
            playerValue+= card[0]
        elif card[0] == 'A':
            playerValue+=11
            aceCount += 1
    while playerValue > 21 and aceCount > 0:
        playerValue -= 10
        aceCount -= 1
    return playerValue

def playHand(dealerHand, playerHand, deck, playerBusts):
    decision = ''
    while not (decision == 'S' or decision == 'STAY'):    
        playerValue=handCalculator(playerHand)
        if playerValue==21:
            break
        print("The dealer has a ", dealerHand[0])   
        decision=input("would you like to hit(h) or stay(s)? Your hand: " + " ".join(str(card) for card in playerHand) + " | Dealer's hand: " + str(dealerHand[0])+ ' ')
        decision=decision.strip()
        decision=decision.upper()
        if decision == 'H' or decision == 'HIT':
            playerHand.append(deck.pop(0))
            states['cardsInDeck'] -= 1
            print("New hand: ", *playerHand)
            playerValue=handCalculator(playerHand)
            print("You now have: ", playerValue)
            sleep(1) 
            if playerValue>21:
                states[playerBusts] = True
                break

def evaluateHand(playerValue, dealerValue, bet, playermoney, handname=None):
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
            states[playermoney]+=(states[bet])
        elif (dealerValue<playerValue):
            print("You have ", playerValue, " and the dealer has ", dealerValue, "\nYou win! :)")
            states[playermoney]+=(states[bet])
        elif(dealerValue>playerValue):
            print("You have ", playerValue, " and the dealer has ", dealerValue, "\nThe dealer wins :(")
            states[playermoney]-=(states[bet])
        elif(dealerValue==playerValue):
            print("You have ", playerValue, " and the dealer has ", dealerValue, "\nTie...   :/")

def dealerPlay(dealerHand, deck, hasDealerPlayed):
    dealerValue=handCalculator(dealerHand)
    print("The dealer has ", *dealerHand, " which is a value of ", dealerValue)
    while (dealerValue<17):
        print("The dealer hits...")
        sleep(1.5)
        dealerHand.append(deck.pop(0))
        states['cardsInDeck'] -= 1
        dealerValue=handCalculator(dealerHand)
        print("The dealer now has ", *dealerHand, " which is a value of ", dealerValue)
        sleep(1)
    states[hasDealerPlayed] = True   

def highScoreCheck():
    score, date, time = get_high_score(GAME)
    if score == 0:
        print("No high score yet")
    else:
        print(f"Current high score: ${score:.2f} set on {date} at {time}")

def highScoreUpdate():
    if update_high_score(GAME, states['playermoney']):
        print("Congratulations! You set a new high score!")

def main():
    print("Welcome to Blackjack: \n")
    highScoreCheck()
    while(True):
        money=states['playermoney']
        print(f'You have ${money:.2f}')
        while(True):
            try:
                states['bet']=float(input("How much would you like to bet? $"))
            except KeyboardInterrupt:
                print("\nExiting game.")
                sys.exit()
            except ValueError:
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
        doubleDecision = ''
        playerHand = []
        playerValue=0
        dealerHand=[]
        dealerValue=0
        if states['cardsInDeck']<15:
            print("Shuffling and Dealing cards...")
            deck=shuffleCards()
            sleep(1)
        playerHand.append(deck.pop(0))
        states['cardsInDeck'] -= 1
        dealerHand.append(deck.pop(0))
        states['cardsInDeck'] -= 1
        playerHand.append(deck.pop(0))
        states['cardsInDeck'] -= 1
        dealerHand.append(deck.pop(0))
        states['cardsInDeck'] -= 1
        playerValue=handCalculator(playerHand)
        dealerValue=handCalculator(dealerHand)
        print("You have ", *playerHand)
        print("Your hand has a value of ", playerValue)
        sleep(1)
        print("The dealer has a ", dealerHand[0])
        if dealerHand[0][0] in ['A', 10, 'J', 'Q', 'K']:
            print("Checking for blackjack...")
            sleep(.8)
            if dealerValue == 21:
                print("The dealer has a blackjack")
                evaluateHand(playerValue, dealerValue, 'bet', 'playermoney')   
            else:
                print("The dealer does not have a blackjack.")
        if dealerValue != 21:
            if playerHand[0][0] == playerHand[1][0]:
                while True:
                    print("You have a pair of ", str(playerHand[0][0]) + "s!")
                    splitDecision = input("Would you like to split? yes(y) or no(n) ")
                    splitDecision = splitDecision.strip()
                    splitDecision = splitDecision.upper()
                    if splitDecision == 'YES' or splitDecision == 'Y':
                        break
                    elif splitDecision == 'NO' or splitDecision == 'N':
                        break
                    else:
                        print("Please enter a valid response.")
                        continue
            if splitDecision == 'YES' or splitDecision == 'Y':
                if states['playermoney']<(states['bet']*2):
                    print("You do not have enough money to split.")
                else:
                    print("Splitting hand...")
                    hand1 = [playerHand[0], deck.pop(0)]
                    states['cardsInDeck'] -= 1
                    hand2 = [playerHand[1], deck.pop(0)]
                    states['cardsInDeck'] -= 1
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
                        dealerPlay(dealerHand, deck, 'hasDealerPlayed')
                        dealerValue = handCalculator(dealerHand)
                        evaluateHand(hand1Value, dealerValue, 'bet', 'playermoney', 'Hand 1')
                    else:
                        print("Hand 1 Bust :(")
                        states['playermoney']-=(states['bet'])
                    if states['playerBusts2'] != True:
                        if states['hasDealerPlayed'] == True:
                            dealerValue = handCalculator(dealerHand)
                            evaluateHand(hand2Value, dealerValue, 'split', 'playermoney', 'Hand 2')
                        else:
                            dealerPlay(dealerHand, deck, 'hasDealerPlayed')
                            dealerValue = handCalculator(dealerHand)
                            evaluateHand(hand2Value, dealerValue, 'split', 'playermoney', 'Hand 2')
                    else:
                        print("Hand 2 Bust :(")
                        states['playermoney']-=(states['split'])
            else:
                while True:
                    if playerValue==21:
                        break
                    doubleDecision = input("Would you like to double down? yes(y) or no(n) ")
                    doubleDecision = doubleDecision.strip()
                    doubleDecision = doubleDecision.upper()
                    if doubleDecision == 'YES' or doubleDecision == 'Y':
                        if states['playermoney']<(states['bet']*2):
                            print("You do not have enough money to double down.")
                            playHand(dealerHand, playerHand, deck, 'playerBusts1')
                            break
                        else:
                            print("Doubling down...")
                            states['bet']*=2
                            playerHand.append(deck.pop(0))
                            states['cardsInDeck'] -= 1
                            playerValue=handCalculator(playerHand)
                            if playerValue>21:
                                states['playerBusts1'] = True
                            break
                    elif doubleDecision == 'NO' or doubleDecision == 'N':
                        playHand(dealerHand, playerHand, deck, 'playerBusts1')
                        break
                    else:
                        print("Please enter a valid response.")
                        continue
                playerValue=handCalculator(playerHand)
                print("Final hand: ", *playerHand, " Value: ", playerValue)
                sleep(1)
                if states['playerBusts1'] != True:
                    dealerPlay(dealerHand, deck, 'hasDealerPlayed')
                    dealerValue = handCalculator(dealerHand)
                    evaluateHand(playerValue, dealerValue, 'bet', 'playermoney')
                else:
                    print("Bust :(")
                    states['playermoney']-=(states['bet'])
        if again == '': 
            if (states['playermoney']<=0):
                print("you are out of money. :( Ending game.")
                break
            again=input("Would you like to play again?(default is yes) ")
            if again.upper() == "NO" or again.upper() == "N":
                money=states['playermoney']
                print(f'Thanks for playing! You are leaving with ${money:.2f}')
                highScoreUpdate()
                break
            else:
                states['playerBusts1']=False
                states['playerBusts2']=False
                states['hasDealerPlayed']=False
                states['bet'] = 0.0
                states['split'] = 0.0
                continue

if __name__ == "__main__":
    main()

import random
from cards import createCards

def shuffleCards():
    deck = createCards()
    for i in range(1,3):
        random.shuffle(deck)
    return deck


def bookIsIn(hand):
    check=None
    for card in hand:
        if 'check' in locals():
            if check == True:
                break
        for card2 in hand:
            if (card[0]==card2[0] and card[1]!=card2[1]):
                print("Thats a book of ", card[0])
                hand.remove(card)
                hand.remove(card2)
                check=True
                break
            else:
                check=False
    return check

def cardIsIn(value, hand):
    test=None
    for card in hand:
        temp=str(card[0])
        if temp==value:
            test=True
            break
        else: 
            test=False
    return test
        
def giveCard(value, taker, giver):
    for card in giver:
        temp=str(card[0])
        if temp==value:
            taker.append(giver.pop(giver.index(card)))

def main():
    playerBooks=0
    dealerBooks=0
    print("Welcome to Go Fish: \n")
    print("Shuffling and Dealing cards...")
    deck=shuffleCards()
    playerHand = []
    dealerHand=[]
    for d in range(0,5):
        playerHand.append(deck.pop(0))
        dealerHand.append(deck.pop(0)) 
    print("You have ", *playerHand)
    search=True
    while (search):
            if bookIsIn(playerHand):
                playerBooks+=1
            else: 
                search=False    
    print("You have ", playerBooks, " books.")
    search=True
    while (search):
            if bookIsIn(dealerHand):
                dealerBooks+=1
            elif not bookIsIn(dealerHand): 
                search=False    
    print("The dealer has ", dealerBooks, " books.")
    while(len(playerHand)!=0 or len(dealerHand)!=0):       
        while (True):
            print("You have ", *playerHand)
            decision=input("What would you like to ask for? ")
            if cardIsIn(decision,playerHand):
                break
            else:
                print("That card is not in your hand")
                
        if cardIsIn(decision, dealerHand):
            giveCard(decision, playerHand, dealerHand)
            if(bookIsIn(playerHand)):
                playerBooks+=1
                print("You have ", playerBooks, " books. You now have ", *playerHand)
                if len(playerHand)==0:
                    break
        else:
            print("Go Fish!")
            fishcard=deck.pop(0)
            playerHand.append(fishcard)
            print ("You now have ", *playerHand)
            if(bookIsIn(playerHand)):
                playerBooks+=1
                print("You have ", playerBooks, " books. You now have ", *playerHand)
                if len(playerHand)==0:
                    break
            if(str(fishcard[0])==decision):
                continue
            else:
                dealersTurn=True
                while(dealersTurn):
                    dealerCard=random.choice(dealerHand)
                    dealerChoice=str(dealerCard[0])
                    print("The dealer chose ", dealerChoice)
                    if cardIsIn(dealerChoice, playerHand):
                        giveCard(dealerChoice, dealerHand, playerHand)
                        if(bookIsIn(dealerHand)):
                            dealerBooks+=1
                            print("The dealer has ", dealerBooks, " books.")
                            if len(dealerHand)==0:
                                break                      
                    else:
                        print("Dealer must fish!")
                        fishcard=deck.pop(0)
                        dealerHand.append(fishcard)
                        if(bookIsIn(dealerHand)):
                            dealerBooks+=1
                            print("The dealer got a ",fishcard ," and now has ", dealerBooks, " books.")
                            if len(dealerHand)==0:
                                break
                        if(str(fishcard[0])==dealerChoice):
                            dealersTurn=True
                        else:
                            dealersTurn=False
    if len(dealerHand)==0:
        print("Dealer is out of cards")
    elif len(playerHand)==0:
        print("You are out of cards")
    print("You end the game with ", playerBooks, "books and the dealer had ", dealerBooks)
    if playerBooks>dealerBooks:
        print("You win!!")
    elif playerBooks<dealerBooks:
        print("You lose")
    elif playerBooks==dealerBooks:
        print("Tie")
if __name__ == "__main__":
    main()
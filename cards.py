def createCards():
    cards = []
    values = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    for suit in suits: 
        for value in values:
            cardtuple = (value, suit)
            cards.append(cardtuple)
    return cards

def main():
    print(createCards())
    # None

if __name__ == "__main__":
    main()
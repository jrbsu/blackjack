import sys
import re
from termcolor import colored, cprint
import numpy as np
import plotext as plt
import locale

#iterations = int(input("Number of iterations — "))
iterations = 100

moneyPlot = []
moneyPlotTemp = []
bankruptLine = []
moneyLine = []
endText = []
cards = []

initialMoney = 100

gameOver = False
bust = False
bustCard = 0
BBWin = 0
standValue = 20
doubleDown = False

for x in range(iterations):
    bankruptLine.append(0)
    moneyLine.append(initialMoney)

initialMoney = []
initialWager = []
initialBBWager = []

for x in range(2):
    print("Setup for Simulation " + str(x+1))
    #nitialMoney.append(int(input("Amount of money to begin with – ")))
    #initialWager.append(int(input("Amount of money to wager – ")))
    #initialBBWager.append(int(input("Amount of money to wager on Buster Blackjack – ")))
    initialMoney.append(100)
    initialWager.append(15)
    initialBBWager.append(5)

def generate_cards():
    numbers = [2,3,4,5,6,7,8,9,10,10,10,10,11] #special case for the 11 (ace)

    for i in range(24):
        for x in numbers:
            cards.append(x)

    np.random.shuffle(cards)

def player_turn(playerCards):
    global gameOver
    global dealerWins
    playerPoints = sum(playerCards)

    # Hitting
    while (playerPoints < 12 or (playerPoints == 12 and dealerCards[0] <= 3) or dealerCards[0] >= 7) and playerPoints < 17 and gameOver == False and doubleDown == False:
        if playerPoints <= 21:
            print("Player has " + str(playerPoints) + " and sees the dealer's " + str(dealerCards[0]) + ", so hits")
            if cards[0] == 11 and playerPoints > 10:
                playerCards.append(1)
                playerPoints += 1
                print("Player draws an ace")
            else:
                playerCards.append(cards[0])
                playerPoints += cards[0]
                print("Player draws", cards[0])
            del cards[0]
            print("Player cards: ", playerCards, playerPoints)
        if playerPoints > 21:
            if 11 in playerCards:
                for i in range(len(playerCards)):
                    if playerCards[i] == 11:
                        playerCards[i] = 1
                playerPoints = sum(playerCards)
                continue
            else:
                print(colored("Player busts. Dealer wins.","white","on_red")) # I think this can probably be handled later with a return statement
                dealerWins += 1
                gameOver = True
                winner = "d"

    # Standing
    if gameOver == False and doubleDown == False:
        print("Player has " + str(playerPoints) + " and sees the dealer's " + str(dealerCards[0]) + ", so stands at", playerPoints)

#sys.stdout = open('output.txt','wt')

for a in range(2):
    cprint("\n\nSimulation " + str(a+1), attrs=["bold"])

    # Some resets
    moneyPlotTemp = []
    winner = ""
    runOutHand = []
    hands = 0
    playerWins = 0
    dealerWins = 0
    ties = 0
    dealerBlackjack = 0
    playerBlackjack = 0
    money = initialMoney[a]
    wager = initialWager[a]
    BBWager = initialBBWager[a]
    mostMoney = money
    leastMoney = money
    bustCount = 0
    biggestBBWin = 0
    biggestBBWinHand = 0
    doubleDowns = 0
    splits = 0
    # Resets end

    while hands < iterations:
        # LOOP BEGINS
        hands += 1
        gameOver = False
        bust = False
        bustCard = 0
        BBWin = 0
        standValue = 20
        doubleDown = False
        split = False
        wager = initialWager[a]
        splitHands = [[],[]]
        splitActive = [True, True]
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        moneyDisplay = locale.currency(money, grouping=True)
        cprint("\nHand " + str(hands), attrs=["bold"])
        print("Player has", str(moneyDisplay))
        print("Wagering", "$" + str(wager))
        print("---")
        moneyPlotTemp.append(money)
        if money > mostMoney:
            mostMoney = money
        if money < leastMoney:
            leastMoney = money

        # Generate cards
        generate_cards()

        # Initial deal
        dealerCards = []
        playerCards = []

        dealerCards.append(cards[0])
        dealerCards.append(cards[1])
        playerCards.append(cards[2])
        playerCards.append(cards[3])
        if dealerCards[0] == 11 and dealerCards[1] == 11:
            dealerCards[1] = 1
        dealerPoints = dealerCards[0] + dealerCards[1];
        playerPoints = playerCards[0] + playerCards[1];
        del cards[0]; del cards[0]; del cards[0]; del cards[0]

        print("Dealer face card: ", dealerCards[0])
        print("Player cards: ", playerCards, playerPoints)
        print("---")

        # BLACKJACK CHECK...
        if dealerPoints == 21 and playerPoints != 21:
            print(colored("Dealer wins (blackjack).","white","on_red"))
            dealerBlackjack += 1
            dealerWins += 1
            gameOver = True
            winner = "d"
        if playerPoints == 21 and gameOver == False and dealerPoints != 21:
            print(colored("Player wins (blackjack).","black","on_green"))
            playerBlackjack += 1
            playerWins += 1
            gameOver = True
            winner = "b"

        # PLAYER TURN
        # Logic from https://blackjacktips.com.au/basic-strategy/hit-or-stand/

        # Doubling down
        if (playerPoints == 11 and dealerCards[0] != 11) or (playerPoints == 10 and dealerCards[0] <= 10) or (playerPoints == 9 and dealerCards[0] != 2 and dealerCards[0] <= 7) and gameOver == False:
            cprint("Player has " + str(playerPoints) + " and sees the dealer's " + str(dealerCards[0]) + ", so DOUBLES DOWN","black","on_yellow")
            wager = wager * 2
            doubleDown = True
            playerCards.append(cards[0])
            playerPoints += cards[0]
            if cards[0] == 11 and playerPoints > 10:
                print("Player draws an ace")
            else:
                print("Player draws", cards[0])
            print("Player must stand at", playerPoints)

        # Regular player turn
        # First, check for split
        if playerCards[0] == playerCards[1] and playerCards[0] != 10 and doubleDown == False:
            cprint("Player has a pair and and SPLITS","white","on_blue")
            splits += 1
            split = True
            splitHands[0].append(playerCards[0])
            splitHands[1].append(playerCards[1])
            print("---\nSplit hand 1")
            player_turn(splitHands[0]) #FIXME. Needs to utilise splitActive somehow
            gameOver = False
            print("---\nSplit hand 2")
            player_turn(splitHands[1])
        else:
            player_turn(playerCards)

        # DEALER TURN
        print("---")
        print("Dealer reveals both cards:", dealerCards, dealerPoints)
        if dealerPoints > 17 and dealerPoints <= 21 and gameOver == False:
            print("Dealer stands at", dealerPoints)

        while dealerPoints < 17 and gameOver == False:
            print("Dealer isn't at their stand amount of 17. Hitting!")
            if cards[0] == 11 and dealerPoints > 10:
                dealerCards.append(1)
                dealerPoints += 1
            else:
                dealerCards.append(cards[0])
                dealerPoints += cards[0]
            if cards[0] == 11:
                print("Dealer draws", "an ace")
            else:
                print("Dealer draws", cards[0])
            del cards[0]
            print("Dealer cards: ", dealerCards, dealerPoints)
            if dealerPoints > 17 and dealerPoints <= 21:
                print("Dealer stands at", dealerPoints)

        if dealerPoints > 21 and gameOver == False:
            print(colored("Dealer busts. Player wins.","black","on_green"))
            playerWins += 1
            gameOver = True
            if split == True:
                winner = "pp"
            else:
                winner = "p"
            bust = True
            bustCard = len(dealerCards)
        if split == True: # FIXME: `gameOver == False` or something needed
            winner = ""
            for x in range(2):
                print("In hand " + str(x+1) + "...")
                playerPoints = sum(splitHands[x])
                if dealerPoints > playerPoints:
                    print(colored("Dealer wins.","white","on_red"))
                    dealerWins += 1
                    gameOver = True
                    winner += "d"
                if dealerPoints == playerPoints:
                    print(colored("It's a tie.","black","on_light_blue"))
                    ties += 1
                    gameOver = True
                    winner += "t"
                if dealerPoints < playerPoints:
                    print(colored("Player wins.","black","on_green"))
                    playerWins += 1
                    gameOver = True
                    winner += "p"
        else:
            if dealerPoints > playerPoints and gameOver == False:
                print(colored("Dealer wins.","white","on_red"))
                dealerWins += 1
                gameOver = True
                winner = "d"
            if dealerPoints == playerPoints and gameOver == False:
                print(colored("It's a tie.","black","on_light_blue"))
                ties += 1
                gameOver = True
                winner = "t"
            if dealerPoints < playerPoints and gameOver == False:
                print(colored("Player wins.","black","on_green"))
                playerWins += 1
                gameOver = True
                winner = "p"

        # Buster Blackjack
        if bust == True and gameOver == True and BBWager != 0:
            bustCount += 1
            if bustCard == 3 or bustCard == 4:
                BBWin = BBWager * 2
            elif bustCard == 5:
                BBWin = BBWager * 4
            elif bustCard == 6:
                BBWin = BBWager * 15
            elif bustCard == 7:
                BBWin = BBWager * 50
            else:
                BBWin = BBWager * 250
            print("---\nBecause the dealer bust, the player also wins " + str(locale.currency(BBWin, grouping=True)))
            money += BBWin
            if BBWin > biggestBBWin:
                biggestBBWin = BBWin
                biggestBBWinHand = hands
        if bust == False and gameOver == True and BBWager != 0:
            print("---\nBecause the dealer did not bust, the player loses their " + str(locale.currency(BBWager, grouping=True)))
            money -= BBWager

        # Distribute winnings / losses
        if winner == "d" or winner == "td" or winner == "dt":
            print("Player loses " + str(locale.currency(wager, grouping=True)))
            money -= wager
        elif winner == "dd":
            print("Player loses " + str(locale.currency(wager * 2, grouping=True)))
            money -= wager * 2
        elif winner == "p" or winner == "pt" or winner == "tp":
            print("Player wins " + str(locale.currency(wager, grouping=True)))
            money += wager
        elif winner == "pp":
            print("Player wins " + str(locale.currency(wager * 2, grouping=True)))
            money += wager * 2
        elif winner == "b":
            print("Player wins " + str(locale.currency(wager * 1.5, grouping=True)))
            money += wager * 1.5
        elif winner == "t" or winner == "dp" or winner == "pd" or winner == "tt":
            print("Player has no change")

        if money <= wager:
            runOutHand.append(hands)

        print("\n")

        # WHILE ends

    moneyPlot.append(moneyPlotTemp)
    totalGames = playerWins + dealerWins + ties
    endText.append("(Started with " + str(locale.currency(initialMoney[a], grouping=True)) + ", wagering " + str(locale.currency(wager, grouping=True)))
    if BBWager != 0:
        endText[a] += ", Buster wager " + str(locale.currency(BBWager, grouping=True)) + ")"
    else:
        endText[a] += ", no Buster wager)"
    endText[a] += "\nDealer wins: " + str(dealerWins) + " (" + str(round(dealerWins / totalGames * 100,2)) + "%)\nPlayer wins: " + str(playerWins) + " (" + str(round(playerWins / totalGames * 100,2)) + "%)\nTies: " + str(ties) + " (" + str(round(ties / totalGames * 100,2)) + "%)\n---\nDealer blackjacks: " + str(dealerBlackjack) + "\nPlayer blackjacks: " + str(playerBlackjack) + "\nDouble-downs: " + str(doubleDowns) + "\nSplits: " + str(splits) + "\n---"
    try:
        endText[a] += "\nPlayer went bankrupt at hand " + str(runOutHand[0])
    except:
        endText[a] += "\nPlayer did not go bankrupt!"
    endText[a] += "\nMost money: " + str(locale.currency(mostMoney, grouping=True)) + "\nLeast money: " + str(locale.currency(leastMoney, grouping=True)) + "\nPlayer's final total: " + str(moneyDisplay) + "\n"
    if BBWager != 0:
        endText[a] += "---\nBuster Blackjacks won: " + str(bustCount) + " (" + str(round(bustCount / totalGames * 100,2)) + "%)\n"
        endText[a] += "Biggest Buster Blackjack win: " + str(locale.currency(biggestBBWin, grouping=True)) + " (Hand " + str(biggestBBWinHand) + ")\n"

plt.plot(moneyPlot[0], color=13, label="Simulation 1")
plt.plot(moneyPlot[1], color=34, label="Simulation 2")
#plt.plot(moneyPlot[2], color=38, label="Simulation 3")
plt.plot(bankruptLine, color=1, label="Bankrupt line")
plt.canvas_color(0)
plt.axes_color(0)
plt.ticks_color("white")
plt.show()

cprint("Final stats:", attrs=["bold"])
print(colored("Simulation 1","black","on_magenta"))
print(endText[0])
print(colored("Simulation 2","black","on_green"))
print(endText[1])
#print(colored("Simulation 3","black","on_cyan"))
#print(endText[2])

import sys
import requests
import json
import random

# Command Line error handling
if len(sys.argv) < 3:
    raise Exception("You have not provided enough arguments\nThis script should be run like: 'python3 deck.ydk 100'")
elif len(sys.argv) > 3:
    raise Exception("You have provided too many arguments\nThis script should be run like: 'python3 deck.ydk 100'")
elif sys.argv[1][-4:] != '.ydk':
    raise Exception("Provided decklist is not a .ydk file!")
elif not (isinstance(int(sys.argv[2]), int)):
    raise Exception("Loop amount is not a positive integer!")

class Calculator:
    def __init__(self):
        self.mechaba_and_dpe = 0
        self.mechaba_and_dpe_fleur_used = 0
        self.mechaba_and_dpe_maximus_used = 0
        self.mechaba_and_dpe_schism = 0
        self.loopAmount = int(sys.argv[2])

        with open(sys.argv[1]) as f:
            deck_ids = f.read().splitlines()
        deck_ids.pop(0)
        deck_ids.pop(0)
        self.decksize = deck_ids.index("#extra")
        deck_ids = deck_ids[:self.decksize]
        deck = []
        # Convert card ids to names
        for card in deck_ids:
            response = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={card}")
            info = json.loads(response.text)
            name = info["data"][0]["name"]
            deck.append(name)
        self.deck  = deck

    # Function to check the other combo pieces apart from getting to Aleister
    def checkNonAleisterPieces(self, hand):
        if "Dogmatika Ecclesia, the Virtuous" in hand:
            hand.remove("Dogmatika Ecclesia, the Virtuous")
            self.mechaba_and_dpe += 1
            self.checkForSchism(hand)
        elif ("Small World" in hand and "Ash Blossom & Joyous Spring" in hand):
            hand.remove("Small World")
            hand.remove("Ash Blossom & Joyous Spring")
            self.mechaba_and_dpe += 1
            self.checkForSchism(hand)
        elif "Fusion Destiny" in hand:
            hand.remove("Fusion Destiny")
            self.mechaba_and_dpe += 1
            self.checkForSchism(hand)
        elif "Dogmatika Fleurdelis, the Knighted" in hand:
            hand.remove("Dogmatika Fleurdelis, the Knighted")
            self.mechaba_and_dpe += 1
            self.mechaba_and_dpe_fleur_used += 1
            self.checkForSchism(hand)
        elif "Dogmatika Maximus" in hand:
            hand.remove("Dogmatika Maximus")
            self.mechaba_and_dpe += 1
            self.mechaba_and_dpe_maximus_used += 1
            self.checkForSchism(hand)

    # Function to check if Nadir Servant exists in hand after combo for Schism
    def checkForSchism(self, hand):
        if "Nadir Servant" in hand:
            hand.remove("Nadir Servant")
            self.mechaba_and_dpe_schism += 1

    def run(self):
        # Combo Logic
        for i in range(self.loopAmount):
            random.shuffle(self.deck)
            hand = self.deck[-5:]

            # Mechaba + DPE
            # Cases for getting to Aleister
            if ("Terraforming" in hand):
                hand.remove("Terraforming")
                self.checkNonAleisterPieces(hand)
            elif ("Magical Meltdown" in hand):
                hand.remove("Magical Meltdown")
                self.checkNonAleisterPieces(hand)
            elif ("Aleister the Invoker" in hand):
                hand.remove("Aleister the Invoker")
                self.checkNonAleisterPieces(hand)
            elif ("Small World" in hand):
                hand.remove("Small World")
                if ("Droll & Lock Bird" in hand):
                    hand.remove("Droll & Lock Bird")
                    self.checkNonAleisterPieces(hand)
                elif ("Ash Blossom & Joyous Spring" in hand):
                    hand.remove("Ash Blossom & Joyous Spring")
                    self.checkNonAleisterPieces(hand)
        print("Total percent Boards finishing on Mechaba + DPE:")
        print((self.mechaba_and_dpe / self.loopAmount) * 100)
        print("Percent of boards finishing on Mechaba + DPE with Fleur used:")
        print((self.mechaba_and_dpe_fleur_used / self.loopAmount) * 100)
        print("Percent of boards finishing on Mechaba + DPE with Maximus used:")
        print((self.mechaba_and_dpe_maximus_used / self.loopAmount) * 100)
        print("Percent of boards finishing on Mechaba + DPE with Schism set:")
        print((self.mechaba_and_dpe_schism / self.loopAmount) * 100)

test = Calculator()
test.run()
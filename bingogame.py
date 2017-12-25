# %%% Project Name - Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%% Project Name - Section - Subsection

class Bingo():
    numbers = np.array(range(1, 91))
    np.random.shuffle(numbers)
    current_index = -1
    current_number = numbers[current_index]
    cards = []

    def __init__(self):
        self.numbers = np.array(range(1, 91))
        np.random.shuffle(self.numbers)
        self.current_index = -1
        self.cards = []

    def get_next_number(self):
        self.current_index += 1
        return self.numbers[self.current_index]

    def generate_cards(self, n=1):
        for _ in range(n):
            self.cards.append(np.random.choice(self.numbers, 15, replace=False))
    
    def show_cards(self):
        for i, card in enumerate(self.cards):
            print(f"{i} {card}")
        
    def next_round(self):
        for i, card in enumerate(self.cards):
            index = np.argwhere(card == self.current_number)
#            print(f"Card: {i} has number: {current_number} at index: {index}")
            self.cards[i] = np.delete(card, index)
            if self.cards[i].size == 0:
                print(f"BINGO for card: {i} @ round: {self.current_index}")
                return 1
        self.current_number = self.get_next_number()

#%%%
mybingo = Bingo()
mybingo.generate_cards(n=9)
mybingo.show_cards()

#%%
for _ in range(10):
    if mybingo.next_round() == 1:
        break
mybingo.show_cards()



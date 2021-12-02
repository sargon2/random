#!/usr/bin/env python3

# What bankroll size do we need to make money using modified reverse martingale?
# Modified: during a win streak, don't wager your initial stake.

import random

target = 100 # 100x our initial bet

def get_flip():
    return bool(random.getrandbits(1))

def modified_reverse_martingale(bank, win_streak, target):
    print("modified_reverse_martingale(" + str(bank) + ", " + str(win_streak) + ", " + str(target) + ")")
    num_bets = 0
    min_bank = bank
    while True:
        if bank < 1 and win_streak + bank > 0:
            bank += win_streak
            win_streak = 0
        if bank > 1:
            win_streak += (bank - 1)
            bank = 1

        # If we're in the red, our target is to be solvent
        tmp_target = target
        if bank < 1:
            tmp_target = 1

        print("after adust: bank=" + str(bank) + ", win_streak=" + str(win_streak) + ", tmp_target=" + str(tmp_target))
        if bank + win_streak >= target:
            print("Made it! bank=" + str(bank) + ", win_streak=" + str(win_streak) + ", target=" + str(target))
            print("num_bets=" + str(num_bets) + ", min_bank=" + str(min_bank))
            return

        # Calculate bet amount
        bet_amt = win_streak
        if bank + (bet_amt * 2) > tmp_target:
            bet_amt = tmp_target - (bank + win_streak)
        if bet_amt <= 0:
            bet_amt = 1

        # Do the bet
        flip = get_flip()
        if flip:
            # Won
            print("Bet " + str(bet_amt) + "; Win")
            win_streak += bet_amt
        else:
            # Lost
            print("Bet " + str(bet_amt) + "; Loss")
            win_streak -= bet_amt
            if win_streak < 0:
                bank += win_streak
            win_streak = 0

        num_bets += 1
        if bank < min_bank:
            min_bank = bank

def just_target(bank, target):
    # Bet the amount that, if won, would cancel all our debt and reach our target in one go.
    print("just_target(" + str(bank) + ", " + str(target) + ")")
    num_bets = 0
    min_bank = bank
    while True:
        if bank >= target:
            print("Made it! bank=" + str(bank) + ", target=" + str(target))
            print("num_bets=" + str(num_bets) + ", min_bank=" + str(min_bank))
            return

        print("bank=" + str(bank) + ", target=" + str(target))

        # Calculate bet amount
        bet_amt = target - bank

        # Do the bet
        flip = get_flip()
        if flip:
            # Won
            print("Bet " + str(bet_amt) + "; Win")
            bank += bet_amt
        else:
            # Lost
            print("Bet " + str(bet_amt) + "; Loss")
            bank -= bet_amt

        num_bets += 1
        if bank < min_bank:
            min_bank = bank

modified_reverse_martingale(1, 0, target)
# just_target(1, target)

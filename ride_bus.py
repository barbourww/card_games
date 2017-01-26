from deck import deck
from random import random
from copy import copy


def ride_the_bus(draw, order_hand, risky=0.0, intox=0.0):
    """

    :param draw:
    :param order_hand:
    :param risky:
    :param intox:
    :return:
    """
    assert 0.0 <= risky <= 1.0, "Risk taking factor out of bounds."
    assert 0.0 <= intox <= 1.0, "Intoxication factor out of bounds."
    d = deck()
    hand = []
    for n in range(draw):
        h = d.deal_card()
        hand.append((h, d.space(h)))
    if order_hand:
        hand = sorted(sorted(hand, key=lambda y: d.nums.index(y[0].split('-')[0])), key=lambda x: (x[1]), reverse=True)
    difficulty = sum([h[1] for h in hand])
    hand = [h[0] for h in hand]
    dealt = 0
    deals = 0
    longest_miss = 0
    misses = []

    while True:
        deals += 1
        print "Hand:", hand
        try:
            for i in range(len(hand)):
                c = hand[i]
                delta = float(d.over(c) - d.under(c))
                if delta > 0:
                    if random() > (risky / delta**2) + intox:
                        guess = 'higher'
                    else:
                        guess = 'lower'
                elif delta < 0:
                    if random() > (risky / delta**2) + intox:
                        guess = 'lower'
                    else:
                        guess = 'higher'
                else:
                    if random() > 0.500:
                        guess = 'higher'
                    else:
                        guess = 'lower'
                print c, '...', guess,

                deal = d.deal_card()
                dealt += 1
                hand[i] = copy(deal)

                if guess == d.compare(c, deal):
                    print '...', deal
                    continue
                else:
                    print "\nwrong ...", deal, '\n'
                    longest_miss = max(longest_miss, i + 1)
                    misses.append(i+1)
                    break
            else:
                print "Winner!"
                outcome = 'w'
                break
        except IndexError:
            print "Couldn't finish."
            outcome = 'l'
            break

    print "dealt", dealt, "cards"
    print "longest miss was card", longest_miss

    return outcome, dealt, longest_miss, difficulty, deals, misses


if __name__ == '__main__':
    ride_the_bus(7, True)
else:
    pass

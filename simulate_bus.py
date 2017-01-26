from ride_bus import *
from contextlib import contextmanager
import os
import sys
import matplotlib.pyplot as plt


@contextmanager
def suppress_console(suppress_active=False):
    if suppress_active:
        with open(os.devnull, "w") as devnull:
            old_console = sys.stdout
            sys.stdout = devnull
            try:
                yield
            finally:
                sys.stdout = old_console
    else:
        yield


n = 10000
lmin = 5
lmax = 12

plt.figure(1)
fig1, ax11 = plt.subplots()
ax11.set_xlabel("Length of card bus")
ax11.set_ylabel("Proportion of hands won in simulation")

ax12 = ax11.twinx()
ax12.set_ylabel("Proportion of total cards in deck that were dealt")

plt.figure(2)
fig2, ax21 = plt.subplots()
ax21.set_xlabel("Length of miss")
ax21.set_ylabel("Probability of missing")

ax22 = ax21.twinx()
ax22.set_ylabel("Number of misses")

cg1 = iter(['b', 'g', 'r', 'c', 'm', 'k', 'y'])
cg2 = iter(['b', 'g', 'r', 'c', 'm', 'k', 'y'])

for strategy in [True, False]:
    print "\nOrder cards =", strategy
    x = []
    w = []
    d = []
    ms = []
    lm = {m: [] for m in range(0, lmax+1)}
    for l in range(lmin, lmax + 1):
        results = []
        keys = ['outcome', 'cards_dealt', 'longest_miss', 'difficulty', 'deals', 'misses']
        with suppress_console(suppress_active=True):
            for simulation in range(n):
                r = ride_the_bus(l, order_hand=strategy)
                results.append({k: v for k, v in zip(keys, r)})
        # print "Length of deal =", l
        x.append(l)
        # print "Number of wins =", [r['outcome'] for r in results].count('w')
        w.append([r['outcome'] for r in results].count('w') / float(n))
        # print "Average dealt =", sum([r['cards_dealt'] for r in results]) / len(results)
        d.append((sum([r['cards_dealt'] for r in results]) / len(results)) / (52. - l))
        ms += r['misses']
        lm[r['longest_miss']].append(r['cards_dealt'])
    ax11.plot(x, w, label='wins, order=' + str(strategy), color=cg1.next())
    ax12.plot(x, d, label='mean cards dealt, order=' + str(strategy), color=cg1.next())

    for ml in sorted(lm.keys()):
        if lm[ml]:
            avg = float(sum(lm[ml])) / len(lm[ml])
        else:
            avg = 0.
        print "Miss length =", ml, "...mean cards dealt when longest miss =", round(avg, 1), \
            "...probability of miss =", round(sum(m == ml for m in ms) * 100. / len(ms), 1), "%"
    ax21.plot(sorted(lm.keys()), [round(sum(m == j for m in ms) * 100. / len(ms), 1) for j in sorted(lm.keys())],
              label='order='+str(strategy), color=cg2.next())
    ax22.plot(sorted(lm.keys()), [sum(m == j for m in ms) for j in sorted(lm.keys())],
              label='order='+str(strategy), color=cg2.next())


ax11.legend(loc='upper left', bbox_to_anchor=(0.7, 1.35))
ax12.legend(loc='upper right', bbox_to_anchor=(0.5, 1.35))
fig1.subplots_adjust(top=0.75)

ax21.legend(loc='upper left', bbox_to_anchor=(0.7, 1.35))
ax22.legend(loc='upper right', bbox_to_anchor=(0.5, 1.35))
fig1.subplots_adjust(top=0.75)
8
plt.show()

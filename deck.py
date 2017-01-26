from random import shuffle


class deck():
    """

    """
    def __init__(self):
        suits = ['H', 'C', 'S', 'D']
        self.nums = map(str, range(2, 10 + 1)) + ['J', 'Q', 'K', 'A']
        self.cards = [n + s for n in self.nums for s in ['-' + su for su in suits]]
        shuffle(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def space(self, card):
        i = self.nums.index(card.split('-')[0])
        return min(len(self.nums) - 1 - i, i) + 1

    def over(self, card):
        return len(self.nums) - 1 - self.nums.index(card.split('-')[0])

    def under(self, card):
        return self.nums.index(card.split('-')[0])

    def compare(self, c1, c2):
        if self.nums.index(c1.split('-')[0]) > self.nums.index(c2.split('-')[0]):
            return 'lower'
        elif self.nums.index(c1.split('-')[0]) < self.nums.index(c2.split('-')[0]):
            return 'higher'
        else:
            return 'same'

    def remaining(self):
        return len(self.cards)


if __name__ == '__main__':
    d = deck()
    for n in range(5):
        c = d.deal_card()
        print "\nCARD: ", c
        print "space", d.space(c)
        print "over", d.over(c)
        print "under", d.under(c)

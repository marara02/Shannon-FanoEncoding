class Characters:
    def __init__(self, char, freq) -> None:
        self._char = char
        self._freq = freq
        self._code = ""

    def __lt__(self, other):
        return True if self._freq < other.get_freq() else False

    def __eq__(self, other):
        return True if self._char == other.get_char() and self._freq == other.get_freq() else False

    def __str__(self):
        return "{0}\t {1}\t {2}".format(self._char, str(self._freq), self._code)

    def __iter__(self):
        return self

    def get_char(self):
        return self._char

    def get_freq(self):
        return self._freq

    def get_code(self):
        return self._code

    def append_code(self, code):
        self._code += str(code)


# Dividing to left and right, first getting half, then compare difference between left and right for subdivision
def DivideList(lst):
    if len(lst) == 1:
        return None
    s = k = b = 0
    for p in lst:
        s += p.get_freq()
    s /= 2
    for p in range(len(lst)):
        k += lst[p].get_freq()
        if k == s:
            return p
        elif k > s:
            j = len(lst) - 1
            while b < s:
                b += lst[j].get_freq()
                j -= 1
            return p if abs(s - k) < abs(s - b) else j
    return


# Assigning 0 and 1 to divided groups
def Shannon_fano_code(lst):
    middle = DivideList(lst)
    if middle is None:
        return
    for i in lst[: middle + 1]:
        i.append_code(0)
    Shannon_fano_code(lst[: middle + 1])
    for i in lst[middle + 1:]:
        i.append_code(1)
    Shannon_fano_code(lst[middle + 1:])


# sorting probability in descending order
def sorted_probability(sorting_list):
    desc = sorted(sorting_list, key=lambda x: x[1], reverse=True)
    return desc


# Adding all char with probability to new list by addressing from var Character
def get_all(probabilities):
    lst = []
    for key, value in probabilities:
        lst.append(Characters(key, value))
    return lst


if __name__ == "__main__":
    """Open file read text, count frequency, calculate probability"""
    f = open('hah.txt', 'r')
    test_str = f.read()
    total = len(test_str)

    all_freq = {}
    lists = []
    for i in test_str:
        all_freq[i] = test_str.count(i)
    for key, value in all_freq.items():
        prob = round(value / total, 4)
        lists.append((key, prob))
    print("Probabilities of each char: \n", lists)

    result = sorted_probability(lists)
    print("Sorted probabilities: \n", result)

    all = get_all(result)

    all.sort(reverse=True)
    Shannon_fano_code(all)
    for c in all:
        print(c)

    r = ""
    for u in test_str:
        for n in all:
            if u == n.get_char():
                r += str(n.get_code())

    print("Encoded message: \n", r)

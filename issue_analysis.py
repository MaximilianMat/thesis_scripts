import json
from collections import Counter

class BoolList(object):

    def __init__(self, val):
        self.val = val

    def __hash__(self):
        return hash(str(self.val))

    def __repr__(self):
        # Bonus: define this method to get clean output
        return str(self.val)

    def __eq__(self, other):
        return str(self.val) == str(other.val)


with open('results.json') as f:
    # get test gap information
    d = json.load(f)

    for issue in d:
        if not d[issue]['java_gap'] and d[issue]['js_gap']:
            print(issue)

        # transform list elements into hashable objects
        d[issue] = BoolList(d[issue])

    print("\nSummary (Testgaps in [Java, JS]):  ")

    count = Counter(d.values())
    print(count)

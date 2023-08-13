import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# use previously mapped method lengths
with open('method_length.json') as f:
    # get test gap information
    d = json.load(f)

    dicts = dict(sorted(d.items(), key=lambda item: item[1])).values()
    dicts = [x + 1 for x in dicts]

def check_gt(number, lower_bound):
    if number > lower_bound:
          return True

    return False

print(f"Number of methods: {len(dicts)}")
print(f"Number of methods with len > 2: {len(list(filter(lambda x: check_gt(x, 2), dicts)))}")
print(f"Number of methods with len > 10: {len(list(filter(lambda x: check_gt(x, 10), dicts)))}")

# X axis parameter:
xaxis = np.array(range(0, len(dicts)))
# Y axis parameter:
yaxis = np.array(dicts)

fig = plt.gcf()
fig.set_size_inches(9, 3)
plt.rcParams["font.family"] = "serif"
plt.rc('text', usetex=True)
sns.set_theme(style="whitegrid")
sns.set_palette(sns.color_palette("tab10"))
sns.lineplot(x = xaxis, y = yaxis)

# get indicator line for len > 10
index10 = np.where(yaxis > 10)[0][0]
plt.axvline(index10, color='red')

# get indicator line for len > 2
index2 = np.where(yaxis > 2)[0][0]
plt.axvline(index2, color='orange')

plt.annotate(f'len = {10}', (index10, plt.ylim()[1]), xytext=(10, -10),
             textcoords='offset points', color='gray')

plt.annotate(f'len = {2}', (index2, plt.ylim()[1]), xytext=(10, -10),
             textcoords='offset points', color='gray')
# Get the current axes
ax = plt.gca()

# Turn off right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.xaxis.grid(False)  # Hide vertical grid lines

plt.yscale('log')

plt.title("Method length")
plt.xlabel("Method")
plt.ylabel("Length")

#plt.xticks(rotation = 30)
plt.tight_layout()
plt.savefig('method_length.eps',dpi=400, bbox_inches='tight')
plt.show()
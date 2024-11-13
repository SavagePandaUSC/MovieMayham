import numpy as np
import matplotlib.pyplot as plt
def ipCountries():
    count = {}
    countires = {}
    with open('outputFlow1.txt', 'r', encoding='utf-8') as f:
        hold = f.read().split("\n")
    for aline in hold:
            aline = aline.split("_")
            if aline[0] in count.keys():
                count[aline[0]] += 1
            else:
                count[aline[0]] = 1
            if(len(aline) > 3):
                if (aline[3] in countires.keys()):
                    countires[aline[3]] += 1
                else:
                    countires[aline[3]] = 1
    x = list (countires.keys())
    y = list (countires.values())
    plt.figure(figsize=(12, 8))
    plt.bar(x, y, color='maroon')
    plt.xlabel("Country")
    plt.ylabel("Count")
    plt.title("Countries")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

ipCountries()
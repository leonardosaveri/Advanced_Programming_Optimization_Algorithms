# importing all the necessary packages
from pulp import *
from itertools import combinations
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import datetime  # useful to compute time given seconds are from midnight


# creating a class to store all the information the pastries
class Pastries:
    allPastries = []

    def __init__(self, ID, PRE, DLN, BAK, start=None):
        self.id = str(ID)
        self.pre = int(PRE)
        self.dln = int(DLN)
        self.bak = int(BAK)
        self.start = int(start) if start is not None else None
        self.end = [None if start is None else start + int(BAK)]
        Pastries.allPastries.append(self)

    def __str__(self):
        return f"ID: {self.id}, PRE: {self.pre}, BAK: {self.bak}, DLN: {self.dln}, START: {self.start}, END: {self.end}"


class Colors:
    grid = 'green'
    bakeCritical = '#C33C23'
    bakeAlmostCritical = '#FFB447'
    bakeNonCritical = '#77DF79'
    preparationTime = '#efe3b3'
    deliveryTime = '#08447b'
    endOven = '#9DBDD4'
    extremelyCriticalPreparation = '#A98093'
    criticalPreparation = '#E2C2B9'
    almostCriticalPreparation = '#E7EAB5'
    nonCriticalPreparation = '#BFD8B8'


# reading the txt file to gel all the pastries and their information
with open("bakery.txt", "r") as f:
    howManyPastries = 0
    for line in f:
        howManyPastries += 1
        line = line.split()
        Pastries(int(line[0])+1, line[1], line[2], line[3])

# # to print a list of all the pastries' information
# for i in Pastries.allPastries:
#     print(i)

# this list stores all the LpVariables of starting time
startingTime = [LpVariable("s{0}".format(i.id), lowBound=i.pre, upBound=(i.dln-i.bak), cat=LpInteger)
                for i in Pastries.allPastries]

# here I create the LpProblem, since we want to get the minimum overall time I want to minimize the solution
prob = LpProblem("Bakery", LpMinimize)

# adding the objective (the sum of the starting times)
prob += sum(startingTime)

# adding the constraints
M = 27000
c = 1
for i, j in combinations(list(range(howManyPastries)), 2):
    z = LpVariable("z{}".format(c), lowBound=0, upBound=1, cat="Binary")
    prob += startingTime[i] + Pastries.allPastries[i].bak <= startingTime[j] + M * z
    prob += startingTime[j] + Pastries.allPastries[j].bak <= startingTime[i] + M * (1-z)
    c += 1

# # to check everything
# print(prob)

# solving the problem
status = prob.solve(PULP_CBC_CMD(msg=False))

# # these variables can be used to check what is the ending time and the last start
# ending = 0
# lastStart = 0

# to print the output
# and to update the starting (and ending) value in the pastries list
for i, j in zip(startingTime, Pastries.allPastries):
    print(f"{i}: {value(i)}")
    j.id = str(i)
    j.start = value(i)
    '''
    # this has to be used if we want to check the last start and the ending
    if j.start > lastStart:
        lastStart = j.start
    if j.start + j.bak > ending:
        ending = j.start + j.bak
    '''

# # to check the last start and the ending
# print(lastStart, ending)


'''
THE OUTPUT

s1: 5400.0
s2: 6000.0
s3: 0.0
s4: 4800.0
s5: 1800.0
s6: 9000.0
s7: 10200.0
s8: 11400.0
s9: 15600.0
s10: 600.0
s11: 14400.0
s12: 20400.0
s13: 16800.0
s14: 18600.0
s15: 12600.0
s16: 6600.0
s17: 2400.0
'''


# THE PLOT

# sorting based on which pastry ends last to have the plot show on the first line the first pastry
allPastriesSorted = sorted(Pastries.allPastries, key=lambda x: -x.start)


# getting the pre, dln, bake_time, start_time and names sorted
pre = [int(i.pre) for i in allPastriesSorted]
dln = [int(i.dln) for i in allPastriesSorted]
bakeTime = [int(i.bak) for i in allPastriesSorted]
startTime = [int(i.start) for i in allPastriesSorted]
name = [i.id for i in allPastriesSorted]

# computing the end time of each pastry
endTime = [i + j for i, j in zip(startTime, bakeTime)]

# creating the plot
fig, ax = plt.subplots(1, figsize=(100, 30))

# setting some parameters
plt.tick_params('both', length=10, width=1, labelsize=40, pad=15)

font = {'family': 'DejaVu Sans',
        'weight': 'normal',
        'size': 40}

plt.rc('font', **font)


# Use this if you want to start the preparation just in time for the baking
'''
times = [str(datetime.timedelta(seconds=i))
         for i in list({*end_time, *start_time, *dln, *[a_i - b_i for a_i, b_i in zip(start_time, pre)]})]
'''

# use this for starting all the preparation at time 0
times = [str(datetime.timedelta(seconds=i))
         for i in list({*endTime, *startTime, *dln, *pre})]

# WE CAN USE THIS TO PLOT ONLY THE USEFUL TIMES WITH A DATE:MINUTES:SECONDS FORMAT

plt.xticks(list({*endTime, *startTime, *dln, *pre}),
           labels=times, fontsize=40, rotation=45, va='center', rotation_mode="anchor", ha="right")

# use this if you want to start the preparations just in time for the baking
'''
plt.xticks(list({*end_time, *start_time, *dln, *[a_i - b_i for a_i, b_i in zip(start_time, pre)]}),
           labels=times, fontsize=40, rotation=45, va='center', rotation_mode="anchor", ha="right")
'''

# use this to plot only the useful times in seconds
'''
plt.xticks(list({*end_time, *start_time, *dln, *[a_i - b_i for a_i, b_i in zip(start_time, pre)]}),
           fontsize=40, rotation=45, va='center', rotation_mode="anchor", ha="right")
'''

# I create this dict to store all the values of the pastries, so that I can create a label saying what needs to be taken
# out of the oven, and what needs to be put in, the delivery times and the preparation
scheduleTimes = {"pre": {}, "dln": {}, "endOven": max(endTime), "ending": {}, "start": {}}

for i in Pastries.allPastries:
    scheduleTimes["pre"][i.pre] = []    # scheduleTimes["pre"][i.start - i.pre] = []    # for starting the preparations just in time for baking
    scheduleTimes["dln"][i.dln] = []
    scheduleTimes["ending"][i.start + i.bak] = []
    scheduleTimes["start"][i.start] = []

for i in Pastries.allPastries:
    scheduleTimes["pre"][i.pre].append(i.id)  # scheduleTimes["pre"][i.start - i.pre].append(i.id)  # for starting the preparations just in time for baking
    scheduleTimes["dln"][i.dln].append(i.id)
    scheduleTimes["ending"][i.start + i.bak].append(i.id)
    scheduleTimes["start"][i.start].append(i.id)

# list to store all the information
# use the one below to start th preparation just in time for baking
# scheduleSeconds = list({*end_time, *start_time, *dln, *[a_i - b_i for a_i, b_i in zip(start_time, pre)]})

# use the one below to start preparations at time 0
scheduleSeconds = list({*endTime, *startTime, *dln, *pre})

scheduleMoments = [""] * len(scheduleSeconds)


# If we want the preparations to start just in time for the baking we need to change here some things
for i in range(len(scheduleSeconds)):
    scheduleMoments[i] += "At " + str(datetime.timedelta(seconds=scheduleSeconds[i])) + ": "
    if i == 0:
        scheduleMoments[i] += "Start all preparations; "
    if scheduleSeconds[i] in scheduleTimes["pre"] and scheduleSeconds[i] != 0:
        scheduleMoments[i] += "End Preparation of " + ', '.join(scheduleTimes["pre"][scheduleSeconds[i]]) + "; "
    if scheduleSeconds[i] in scheduleTimes["ending"]:
        scheduleMoments[i] += "Take out of oven " + ', '.join(scheduleTimes["ending"][scheduleSeconds[i]]) + "; "
    if scheduleSeconds[i] in scheduleTimes["start"]:
        scheduleMoments[i] += "Insert in oven " + ', '.join(scheduleTimes["start"][scheduleSeconds[i]]) + "; "
    if scheduleSeconds[i] in scheduleTimes["dln"]:
        scheduleMoments[i] += "Delivery of " + ', '.join(scheduleTimes["dln"][scheduleSeconds[i]]) + "; "
    if scheduleSeconds[i] == scheduleTimes["endOven"]:
        scheduleMoments[i] += "Shut down oven" + "; "

# # to check everything
# print(scheduleMoments)

# creating an axis on the top of the graph to put schedule labels
secx = ax.secondary_xaxis('top')
secx.set_xticks(scheduleSeconds)
secx.set_xticklabels(scheduleMoments, rotation=45, va='center', rotation_mode='anchor', ha="left")
secx.tick_params('both', length=10, width=1, pad=15)

# plotting a grid and setting it under the plots
plt.grid(color=Colors.grid, linestyle='dotted', linewidth=0.5)
ax.set_axisbelow(True)
secx.set_axisbelow(True)

# creating a legend with the colors and the info
c_dict = {'=0min to delivery | Critical baking time' : Colors.bakeCritical,
          '<30min to delivery | Almost critical baking time': Colors.bakeAlmostCritical,
          '>=30min to delivery | Non critical baking time': Colors.bakeNonCritical,
          # 'Preparation time': Colors.preparationTime,
          'Time of Delivery': Colors.deliveryTime,
          'End of use of Oven': Colors.endOven,
          'Extremely critical preparation | =0min to baking': Colors.extremelyCriticalPreparation,
          'Critical Preparation | <=15min to Baking': Colors.criticalPreparation,
          "Almost critical preparation | <=30min to baking": Colors.almostCriticalPreparation,
          "No critical preparation | >30min to baking": Colors.nonCriticalPreparation
          }

legend_elements = [Patch(facecolor=c_dict[i], label=i) for i in c_dict]
legend = plt.legend(handles=legend_elements, ncol=2, title="Legend", edgecolor="black")
legend.get_frame().set_alpha(1)
legend.get_frame().set_facecolor("#faf6e8")
legend.get_frame().set_linewidth(2)

# to say if baking is critical or not
colors = []
for e, d in zip(endTime, dln):
    if d - e == 0:
        colors.append(Colors.bakeCritical)
    elif d - e < 1800:    # less than 30 minutes
        colors.append(Colors.bakeAlmostCritical)
    else:
        colors.append(Colors.bakeNonCritical)


# plotting the time in the oven, with color based on critical
ax.barh(name, bakeTime, left=startTime, color=colors)

# colors preparation
colorsPre = []
for p, s in zip(pre, startTime):
    if s - p >= 1800:
        colorsPre.append(Colors.nonCriticalPreparation)
    elif s - p >= 900:
        colorsPre.append(Colors.almostCriticalPreparation)
    elif s - p == 0:
        colorsPre.append(Colors.extremelyCriticalPreparation)
    else:
        colorsPre.append(Colors.criticalPreparation)

# plotting preparation time with color based on if critical
ax.barh(name, pre, left=0, color=colorsPre, alpha=1)
# use the one below if you want the preparation to start just in time for baking
# ax.barh(name, pre, left=[a_i - b_i for a_i, b_i in zip(start_time, pre)], color="#efe3b3", alpha=0.5)

# plotting the delivery time
ax.barh(name, 30, left=[i-15 for i in dln], color="#08447B", align="center")

# plotting the end of the use of the oven
plt.axvline(x=max(endTime), color="#9DBDD4", linewidth=5)

# if we choose to plot using the hour:minute:second plot time
ax.set_xlabel('Time (Hour:Minutes:Seconds) | 24h format', labelpad=30, fontsize=50)

# to set the labels
# use the one below if you want to show seconds as lable
# ax.set_xlabel('Seconds', labelpad=20, fontsize=50)
ax.set_ylabel('Pastries', labelpad=30, fontsize=50)
ax.set_title('Oven Schedule', pad=50, fontsize=100)


# to save the graph
plt.savefig("graph_Saveri.png", bbox_inches="tight", pad_inches=0.5)

# # to show the graph
# plt.show()


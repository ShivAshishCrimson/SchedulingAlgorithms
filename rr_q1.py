class ProcessNode:
    def __init__(self,ID,arrivalTime,burstTime,priority):
        self.ID = ID
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.priority = priority
        self.startTime = 0
        self.endTime = 0
        self.completionTime = 0
        self.finishTime = 0
        self.turnAroundTime = 0
        self.waitingTime = 0
        self.progress = 0
    def getDetails(self):
        print(f"Process ID : {self.ID}")
        print(f"Arrival Time : {self.arrivalTime}")
        print(f"Burst Time : {self.burstTime}")
        print(f"Start Time : {self.startTime}")
        print(f"Completion Time:{self.completionTime}")
        print(f"End Time : {self.endTime}")

import pandas as pd        
class RR:
    def __init__(self,processNodes,timeQuantum):
        self.MainProcessNodes = processNodes.copy()
        self.processNodes = processNodes.copy()
        self.finalProcessNodes = []
        self.currentTime = 0
        self.timeQuantum = 2
        self.arrivalTimes = []
        self.n = 4
        self.burstTimes = []
        self.wait = [0]*self.n
        self.turn = [0]*self.n
        self.queue = [0]*self.n
        self.complete = [False]*self.n
        self.tb = []
        self.maxProccessIndex = 0
        self.tatAverage=0
        self.wtAverage = 0
    def convertToLists(self):
        for process in self.processNodes:
            self.arrivalTimes.append(process.arrivalTime)
            self.burstTimes.append(process.burstTime)
            self.tb.append(process.burstTime)
    def feedUpdate(self):
        zi = -1
        for i in range(self.n):
            if(self.queue[i] == 0):
                zi = i
                break
        if(zi == -1):
            return
        self.queue[zi] = self.maxProccessIndex + 1
    def newProcess(self):
        if(self.currentTime <= self.arrivalTimes[self.n-1]):
            na = False
            for j in range(self.maxProccessIndex+1, self.n):
                if(self.arrivalTimes[j] <= self.currentTime):
                    if(self.maxProccessIndex < j):
                        self.maxProccessIndex = j
                        na = True
            if(na):
                self.feedUpdate()
    def feed(self):
        for i in range(self.n-1):
            if(self.queue[i+1] != 0):
                self.queue[i], self.queue[i+1] = self.queue[i+1], self.queue[i]
    def start(self):
        print("Start Round Robin")
        for i in range(self.n):
            self.complete[i] = False
            self.queue[i] = 0
        while(self.currentTime < self.arrivalTimes[0]):
            self.currentTime += 1
        self.queue[0] = 1
        while(True):
            flag = True
            for i in range(self.n):
                if(self.tb[i] != 0):
                    flag = False
                    break
            if(flag):
                break
            for i in range(self.n and self.queue[i] != 0):
                ctr = 0
                while((ctr < self.timeQuantum) and (self.tb[self.queue[0]-1] > 0)):
                    self.tb[self.queue[0]-1] -= 1
                    self.currentTime += 1
                    ctr += 1
                    self.newProcess()
                if((self.tb[self.queue[0]-1] == 0) and (self.complete[self.queue[0]-1] == False)):
                    self.turn[self.queue[0]-1] = self.currentTime
                    self.complete[self.queue[0]-1] = True
                idle = True
                if(self.queue[self.n-1] == 0):
                    for k in range(self.n):
                        if(self.queue[k] != 0):
                            if(self.complete[self.queue[k]-1] == False):
                                idle = False
                else:
                    idle = False
                if(idle):
                    self.currentTime += 1
                    self.newProcess()
                self.feed()

    def showResult(self):
        l1 = [];l2 = [];l3 = [];l4 = [];l5 =[];l6 =[]
        for i in range(self.n):
            self.turn[i] = self.turn[i] - self.arrivalTimes[i]
            self.wait[i] = self.turn[i] - self.burstTimes[i]
        for process in self.MainProcessNodes:
            l1.append(process.ID)
            l2.append(process.arrivalTime)
            l3.append(process.burstTime)
            
        RRTable = pd.DataFrame({"Process ID":l1,
                                  "Arrival Time":l2,
                                 "Burst Time": l3,
                                 "Turn Around Time":self.turn,
                                 "Waiting Time":self.wait})

        self.tatAverage = RRTable.loc[:, 'Turn Around Time'].mean()
        print(f"Average Turn Around Time : {self.tatAverage}")
        self.wtAverage = RRTable.loc[:, 'Waiting Time'].mean()
        print(f"Average Waiting Time : {self.wtAverage}")
        print(f"Round Robin Scheduling Table")
        return RRTable.head(len(RRTable))  
    
# INITIALIZING PROCESS DATA
allProcessNodes = []
allProcessData = [["P1",0,24,3],["P2",4,3,1],["P3",5,3,4],["P4",6,12,2]]
for process in allProcessData:
    selectedProcess = ProcessNode(process[0],process[1],process[2],process[3])
    allProcessNodes.append(selectedProcess)

#RR    
RR_Scheduling = RR(allProcessNodes,
                  timeQuantum=2)
RR_Scheduling.convertToLists()
RR_Scheduling.start()
RR_Scheduling.showResult()
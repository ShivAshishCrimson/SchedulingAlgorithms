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
class FCFS:
    def __init__(self,processNodes):
        self.MainProcessNodes = processNodes.copy()
        self.processNodes = processNodes.copy()
        self.finalProcessNodes = []
        #Assuming time units 
        self.currentTime = 0
        self.startTime = 0
        self.tatAverage= 0
        self.wtAverage = 0
    def start(self):
        print("FCFS START")
        while len(self.processNodes) != 0:
            process = self.getProcess(self.processNodes)
            if self.currentTime < process.arrivalTime:
                self.currentTime+=1
                continue
            self.completeProcess(process)
        return self.MainProcessNodes
    def getProcess(self,nodes):
        tempArrivalList = [process.arrivalTime for process in nodes]
        minArrivalTime = min(tempArrivalList)
        tempProcessList = [process for process in nodes if process.arrivalTime == minArrivalTime]
        tempIDList = [int(process.ID[-1]) for process in tempProcessList]
        tempProcessList = [process for process in tempProcessList if int(process.ID[-1]) == min(tempIDList)]
        return tempProcessList[0]
    
    def completeProcess(self,fcfsp):
        st = self.currentTime
        self.currentTime += fcfsp.burstTime
        et = self.currentTime
        for pdx,process in enumerate(self.processNodes):
            if process.ID == fcfsp.ID:
                self.processNodes.pop(pdx)
        for pdx,process in enumerate(self.MainProcessNodes):
            if process.ID == fcfsp.ID:
                process.startTime = st
                process.waitingTime = st - process.arrivalTime
                process.endTime = et
                process.completionTime = et - process.arrivalTime
                process.finishTime = self.currentTime
                process.turnArroundTime = process.finishTime - process.arrivalTime
                print(f"Process : {process.ID} Handled")
                self.finalProcessNodes.append(process)
    def showResult(self):
        l1 = [];l2 = [];l3 = [];l4 = [];l5 =[];l6 =[]
        for process in self.finalProcessNodes:
            l1.append(process.ID)
            l2.append(process.arrivalTime)
            l3.append(process.burstTime)
            l4.append(process.finishTime)
            l5.append(process.turnArroundTime)
            l6.append(process.waitingTime)
        fcfsTable = pd.DataFrame({"Process ID":l1,
                                  "Arrival Time":l2,
                                 "Burst Time": l3,
                                 "Finish Time":l4,
                                 "Turn Around Time":l5,
                                 "Waiting Time":l6})
        self.tatAverage = fcfsTable.loc[:, 'Turn Around Time'].mean()
        print(f"Average Turn Around Time : {self.tatAverage}")
        self.wtAverage = fcfsTable.loc[:, 'Waiting Time'].mean()
        print(f"Average Waiting Time : {self.wtAverage}")
        print(f"FCFS Scheduling Table")
        return fcfsTable.head(len(fcfsTable)) 

# Q2
# INITIALIZING PROCESS DATA
allProcessNodes = []
allProcessData = [["P1",0,30,3],["P2",10,20,5],["P3",15,40,2],["P4",20,15,4]]
for process in allProcessData:
    selectedProcess = ProcessNode(process[0],process[1],process[2],process[3])
    allProcessNodes.append(selectedProcess)
    
FCFS_Sceduling = FCFS(allProcessNodes)
FCFS_Sceduling.start()
FCFS_Sceduling.showResult()
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
class PS:
    def __init__(self,processNodes):
        self.MainProcessNodes = processNodes.copy()
        self.processNodes = processNodes.copy()
        self.finalProcessNodes = []
        self.currentTime = 0
        self.startTime = 0
        self.tatAverage= 0
        self.wtAverage = 0
    def start(self):
        print(f"Start Priority Scheduling")
        while len(self.processNodes) != 0:
            psProcess = self.getProcess()
            self.completeProcess(psProcess)
    def getProcess(self):
        processList = []
        for process in self.processNodes:
            if process.arrivalTime <= self.currentTime:
                processList.append(process)
        tempPriorityList = []
        for process in processList:
            tempPriorityList.append(process.priority)
        psp = [process for process in processList if process.priority == max(tempPriorityList)]
        return psp[0]
    def completeProcess(self,psp):
        st = self.currentTime
        self.currentTime += psp.burstTime
        et = self.currentTime
        for pdx, process in enumerate(self.processNodes):
            if process.ID == psp.ID:
                self.processNodes.pop(pdx)
        for pdx, process in enumerate(self.MainProcessNodes):
            if process.ID == psp.ID:
                process.startTime = st
                process.waitingTime = st - process.arrivalTime
                process.endTime = et
                process.completionTime = et - process.arrivalTime
                process.finishTime = self.currentTime
                process.turnArroundTime = process.finishTime - process.arrivalTime
                self.finalProcessNodes.append(process)
        print(f"Process : {psp.ID} Handled")
                
    def showResult(self):
        l1 = [];l2 = [];l3 = [];l4 = [];l5 =[];l6 =[]
        for process in self.finalProcessNodes:
            l1.append(process.ID)
            l2.append(process.arrivalTime)
            l3.append(process.burstTime)
            l4.append(process.finishTime)
            l5.append(process.turnArroundTime)
            l6.append(process.waitingTime)
        PSTable = pd.DataFrame({"Process ID":l1,
                                  "Arrival Time":l2,
                                 "Burst Time": l3,
                                 "Finish Time":l4,
                                 "Turn Around Time":l5,
                                 "Waiting Time":l6})
        self.tatAverage = PSTable.loc[:, 'Turn Around Time'].mean()
        print(f"Average Turn Around Time : {self.tatAverage}")
        self.wtAverage = PSTable.loc[:, 'Waiting Time'].mean()
        print(f"Average Waiting Time : {self.wtAverage}")
        print(f"Priority Scheduling Table")
        return PSTable.head(len(PSTable))           
    
# INITIALIZING PROCESS DATA
allProcessNodes = []
allProcessData = [["P1",0,24,3],["P2",4,3,1],["P3",5,3,4],["P4",6,12,2]]
for process in allProcessData:
    selectedProcess = ProcessNode(process[0],process[1],process[2],process[3])
    allProcessNodes.append(selectedProcess)
#PS
PS_Sceduling = PS(allProcessNodes)
PSresults = PS_Sceduling.start()
PS_Sceduling.showResult()
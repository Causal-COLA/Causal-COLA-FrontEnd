
class Hospital:    
    def __init__(self) -> None:
        self.prev = None
        self.next = None
        self.dataReady = False
        self.dataUploaded = False
    
    def setNextHospital(self,nextHospital):
        self.next = nextHospital
    
    def setPrevHospital(self,prevHospital):
        self.prev = prevHospital

    def setDataReady(self, dataReady):
        self.dataReady = dataReady
    
    def setDataUploaded(self, dataUploaded):
        self.dataUploaded = dataUploaded
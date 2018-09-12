import datetime
import hashlib
from cryptography.fernet import Fernet

# key = Fernet.generate_key()
class node:
  def __init__(self, nodeNumber, refNodeID, genRefNodeID, oID, value, oName, key):
    self.time = datetime.datetime.now()
    self.nodeID = hashlib.md5(str(self.time).encode('utf-8')).hexdigest()[:31]
    self.nodeNumber = nodeNumber
    self.genRefNodeID = genRefNodeID
    self.refNodeID = refNodeID
    self.childRefNodeID = []
    self.addData(oID, value, oName, key)
    self.valueSet = {self.time, str(self.data), self.nodeNumber, self.nodeID, self.refNodeID, str(self.childRefNodeID), self.genRefNodeID}
  
  def addData(self, oID, value, oName, key):
    cipher_suite = Fernet(key)
    self.data = {'oID': oID, 'value': value, 'oName': oName}
    self.hashedData = hashlib.sha256(str(self.data).encode()).hexdigest()
    self.cipher_text = cipher_suite.encrypt(str([self.data, self.hashedData]).encode())

  def getdata(self, key):
    cipher_suite = Fernet(key)
    decrypted_text = cipher_suite.decrypt(self.cipher_text)
    data = eval(decrypted_text)
    print(data[0])
  
class tree:
  def incrementNodeNum(self):
    self.nodeNumber = self.nodeNumber + 1

  def __init__(self, oID, value, oName, key):
    self.nodeNumber = 1
    self.genesisNode = node(self.nodeNumber, None, None, oID, value, oName, key)
    print(self.genesisNode.getdata(key))

  def addChildtoParent(self, parentID, oID, value, oName, key):
    self.incrementNodeNum()
    sum = 0
    if value>self.genesisNode.data['value']:
      print("The new value is greater than the sum of children values")
      return
    for i in self.genesisNode.childRefNodeID:
      sum = sum + i.data['value']
      if (sum+value>self.genesisNode.data['value']):
        print("The new value is greater than the sum of children values")
        return
    self.genesisNode.childRefNodeID.append(node(self.nodeNumber, parentID, self.genesisNode.nodeID, oID, value, oName, key))
  
  def printData(self, nodeID, key):
    for i in self.genesisNode.childRefNodeID:
      if(i.nodeID == nodeID):
        i.getdata(key)
  
  def printChildren(self, rootNode=None):
    if rootNode is None:
      rootNode = self.genesisNode.childRefNodeID
    for i in rootNode:
      if(len(i.childRefNodeID) != 0):
        self.printChildren(i)
      else:
        print(i.time)
  



# Create Child
# 
# Print tree

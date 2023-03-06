from random import *
import sys
import argparse

parser = argparse.ArgumentParser(description="HexNode Test", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-r", help="red value (0-255)", type=int)
parser.add_argument("-g", help="green value (0-255)", type=int)
parser.add_argument("-b", help="blue value (0-255)", type=int)
parser.add_argument("--range", help="variance range for color change", type=int)
parser.add_argument("--side", help="hexes per outer edge, minimum 2. Lower values ignored.", type=int)

args = parser.parse_args()

config = vars(args)
print(config)


colorCode = {0: "red", 1: "green", 2: "blue"}

class HexNode(object):
  sides = [None]*6
  row = 0
  col = 0
  red = 0
  green = 0
  blue = 0
  opacity: float = 0
  colorChecked = False

  def __init__(self, row, col, red=0, green=0, blue=0):
    super().__init__()
    self.row = row
    self.col = col
    self.red = red
    self.green = green
    self.blue = blue
    self.sides = [None]*6
    if (row == 0 and col == 0):
      self.colorChecked = True
    else:
      self.colorChecked = False
  
  def Id(self):
    return "{}-{}".format(self.row, self.col)

  def GetSides(self):
    return self.sides

  def AdjustSideColors(self):
    for s in (t for t in self.GetSides() if t != None):
      #R = 0, G = 1, B = 2
      nodeId = s.Id()
      colorToChange = randint(0, 2)
      if (nodes["{}".format(nodeId)].colorChecked != True):
        initVal = getattr(nodes["{}".format(nodeId)], colorCode[colorToChange])
        rangeBound = int(config["range"]) if (config["range"] != None and int(config["range"] > 0) and int(config["range"] < 256)) else randint(15, 31)
        changeInc = randint(-rangeBound, rangeBound) # [-15, 15][randint(0, 1)]
        if (initVal + changeInc < 0 or initVal + changeInc > 255):
          changeInc = changeInc * (-1)
        changedVal = initVal + changeInc
        #print(getattr(nodes["{}".format(nodeId)], colorCode[colorToChange]))
        setattr(nodes["{}".format(nodeId)], colorCode[colorToChange], changedVal)
        nodes["{}".format(nodeId)].colorChecked = True
        print("{}'s {} changed by : {}".format(s.Id(), colorCode[colorToChange], changeInc))

sideSize = int(config["side"]) if (config["side"] != None and int(config["side"] >= 2)) else 2

#Column with the highest number of nodes.
nodeRadius = sideSize + (sideSize - 1)

currentColumn = sideSize

nodes = {}

# nodes["0-0"] = HexNode(0, 0)
# nodes["0-1"] = HexNode(0, 1)
# nodes["0-2"] = HexNode(0, 2)

# nodes["0-0"].sides[2] = nodes["0-1"]
# nodes["0-1"].sides[2] = nodes["0-2"]
# nodes["0-1"].sides[5] = nodes["0-0"]

baseRed = int(config["r"]) if config["r"] != None else randint(0, 255)
baseGreen = int(config["g"]) if config["g"] != None else randint(0, 255)
baseBlue = int(config["b"]) if config["b"] != None else randint(0, 255)

for i in range (0, nodeRadius):
  currentHex: HexNode = None
  if (i < (sideSize - 1)):
    for j in range (0, sideSize + i):
      currentHex = HexNode(i, j, baseRed, baseGreen, baseBlue)
      nodes["{}-{}".format(currentHex.row, currentHex.col)] = currentHex
  else:
    for j in range (0, sideSize + i - (2 * (i - (sideSize - 1)))):
      currentHex = HexNode(i, j, baseRed, baseGreen, baseBlue)
      nodes["{}-{}".format(currentHex.row, currentHex.col)] = currentHex  

#n: HexNode
for k, n in nodes.items():
  print ("{}-{} - #{:02x}{:02x}{:02x}".format(n.row, n.col, n.red, n.green, n.blue))
  #print ("{}-{} - #{:02x}{:02x}{:02x}".format(v.row, v.col, v.red, v.green, v.blue))
  try:
    nodes["{}-{}".format(n.row, n.col)].sides[0] = nodes["{}-{}".format(n.row + 1, n.col)]    
  except:
    nodes["{}-{}".format(n.row, n.col)].sides[0] = None
  try:
    nodes["{}-{}".format(n.row, n.col)].sides[1] = nodes["{}-{}".format(n.row + 1, n.col + 1)]
  except:
    nodes["{}-{}".format(n.row, n.col)].sides[1] = None
  try:
    nodes["{}-{}".format(n.row, n.col)].sides[2] = nodes["{}-{}".format(n.row, n.col + 1)]
  except:
    nodes["{}-{}".format(n.row, n.col)].sides[2] = None
  try:
    nodes["{}-{}".format(n.row, n.col)].sides[3] = nodes["{}-{}".format(n.row - 1, n.col)]
  except:
    nodes["{}-{}".format(n.row, n.col)].sides[3] = None
  try:
    nodes["{}-{}".format(n.row, n.col)].sides[4] = nodes["{}-{}".format(n.row - 1, n.col - 1)]
  except:
    nodes["{}-{}".format(n.row, n.col)].sides[4] = None
  try:
    nodes["{}-{}".format(n.row, n.col)].sides[5] = nodes["{}-{}".format(n.row, n.col - 1)]
  except:
    nodes["{}-{}".format(n.row, n.col)].sides[5] = None

s: HexNode
for s in nodes["0-0"].GetSides():
  if (s != None):
    print("0-0's {}-{}".format(s.row, s.col))    

for k, n in nodes.items():
  nodes["{}".format(n.Id())].AdjustSideColors()

with open("hexatestout.svg", "w") as w:
  w.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg version="1.1" xmlns="http://www.w3.org/2000/svg" height="2000" width="2000">')

  polygonPoints = ""
  n: HexNode
  for n in nodes.values():
    #print (randint(0, 255))
    if (n.row < (sideSize)):
      w.write('<polygon points="25,8 75,8 100,50, 75,92, 25,92, 0,50" fill="#{:02x}{:02x}{:02x}" transform="translate({} {})" stroke="black" stroke-width="0"/>'.format(n.red, n.green, n.blue, 
      n.row * 75, (n.col * 84 + n.row * 50 + ((sideSize - 1) - n.row - (sideSize - 1) / 2) * 84) - (n.row * 8)))
    else:
      w.write('<polygon points="25,8 75,8 100,50, 75,92, 25,92, 0,50" fill="#{:02x}{:02x}{:02x}" transform="translate({} {})" stroke="black" stroke-width="0"/>'.format(n.red, n.green, n.blue, 
      n.row * 75, (n.col * 84 + n.row * 50 - (n.row - (sideSize - 1) / 2) * 84) + (sideSize - 1) * 84 + (n.row - (nodeRadius - 1)) * 84 - (n.row * 8)))
  w.write('</svg>')
#print (nodes["0-1"].sides[2].Id())
try:
  print (nodes["5-1"])
except:
  print ("no node at 5-1")


print(config)
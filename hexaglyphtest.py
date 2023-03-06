from random import *
import argparse
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser(description="HexNode Test", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-r", help="red value (0-255)", type=int)
parser.add_argument("-g", help="green value (0-255)", type=int)
parser.add_argument("-b", help="blue value (0-255)", type=int)
parser.add_argument("--range", help="variance range for color change", type=int)
parser.add_argument("--side", help="hexes per outer edge, minimum 2. Lower values ignored.", type=int)
parser.add_argument("--size", help="radius of the hex, minimum 25. Lower values ignored. default 100", type=int)

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
  glyphNode = False
  outerEdgeNode = False

  def __init__(self, row, col, red=0, green=0, blue=0):
    super().__init__()
    self.row = row
    self.col = col
    self.red = red
    self.green = green
    self.blue = blue
    self.glyphNode = False
    self.outerEdgeNode = False
    self.sides = [None]*6
    if (row == 0 and col == 0):
      self.colorChecked = True
    else:
      self.colorChecked = False
  
  def Id(self):
    return "{}-{}".format(self.row, self.col)

  def GetSides(self):
    return self.sides

  def SetAsGlyphNode(self):
    self.glyphNode = True

  def UnsetAsGlyphNode(self):
    self.glyphNode = False

  def SetAsOuterEdgeNode(self):
    self.outerEdgeNode = True

  def UnsetAsOuterEdgeNode(self):
    self.outerEdgeNode = False


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

baseRed = int(config["r"]) if config["r"] != None else randint(0, 255)
baseGreen = int(config["g"]) if config["g"] != None else randint(0, 255)
baseBlue = int(config["b"]) if config["b"] != None else randint(0, 255)

for i in range (0, nodeRadius):
  currentHex: HexNode = None
  if (i < (sideSize - 1)):
    for j in range (0, sideSize + i):
      currentHex = HexNode(i, j, baseRed, baseGreen, baseBlue)
      if (i == 0 or j == 0 or j == (sideSize + i - 1)):
        currentHex.SetAsOuterEdgeNode()
      else:
        if (randint(1, 20) >= 15):
          currentHex.SetAsGlyphNode()
      nodes["{}-{}".format(currentHex.row, currentHex.col)] = currentHex
  else:
    for j in range (0, sideSize + i - (2 * (i - (sideSize - 1)))):
      currentHex = HexNode(i, j, baseRed, baseGreen, baseBlue)
      if (i == (nodeRadius - 1) or j == 0 or j == (sideSize + i - (2 * (i - (sideSize - 1))) - 1)):
        currentHex.SetAsOuterEdgeNode()
      else:
        if (randint(1, 20) >= 15):
          currentHex.SetAsGlyphNode()
      nodes["{}-{}".format(currentHex.row, currentHex.col)] = currentHex  

#n: HexNode
for k, n in nodes.items():
  print ("{}-{} - #{:02x}{:02x}{:02x}".format(n.row, n.col, n.red, n.green, n.blue))
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


ut = datetime.now(timezone.utc)
utstring = "{:04d}-{:02d}-{:02d} {:02d}{:02d}{:02d}".format(ut.year, ut.month, ut.day, ut.hour, ut.minute, ut.second)

Path("hexdat").mkdir(parents=True, exist_ok=True)

with open("hexdat\hexaglyphtestout-{}.svg".format(utstring), "w") as w:
  w.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg version="1.1" xmlns="http://www.w3.org/2000/svg" height="2000" width="2000">')

  hexwidth = int(config["size"]) if (config["size"] != None and int(config["size"] >= 25)) else 100
  print (hexwidth)
  polygonPoints = "{},{} {},{} {},{}, {},{}, {},{}, {},{}".format(
    float(hexwidth * .25),
    float(hexwidth * .08),
    float(hexwidth * .75),
    float(hexwidth * .08),
    float(hexwidth * 1),
    float(hexwidth * .5),
    float(hexwidth * .75),
    float(hexwidth * .92),
    float(hexwidth * .25),
    float(hexwidth * .92),
    float(hexwidth * 0),
    float(hexwidth * .5)
  )

  print (polygonPoints)
  n: HexNode
  for n in nodes.values():
    #print (randint(0, 255))
    if (n.row < (sideSize)):
      rowPos = n.row * float(hexwidth * 0.75)
      colPos = (n.col * float(hexwidth * 0.84) + n.row * float(hexwidth * 0.50) + ((sideSize - 1) - n.row - (sideSize - 1) / 2) * float(hexwidth * 0.84)) - (n.row * float(hexwidth * 0.08))
      #w.write('<polygon points="25,8 75,8 100,50, 75,92, 25,92, 0,50" fill="#{:02x}{:02x}{:02x}" transform="translate({} {})" stroke="black" stroke-width="0"/>'.format(n.red, n.green, n.blue, 
      w.write('<polygon points="{}" fill="#{:02x}{:02x}{:02x}" transform="translate({} {})" stroke="black" stroke-width="0"/>'.format(polygonPoints, n.red, n.green, n.blue, 
      rowPos, colPos))
      # if (n.outerEdgeNode == True):
      #   w.write('<circle cx="{}" cy="{}" r="{}" fill="transparent" transform="translate({} {})" stroke="#ffffff" stroke-width="4"/>'.format(
      #     float(hexwidth * .5), float(hexwidth * .5), float(hexwidth * .2), rowPos, colPos))
      if (n.glyphNode == True):
        w.write('<circle cx="{}" cy="{}" r="{}" fill="transparent" transform="translate({} {})" stroke="#ffffff" stroke-width="{}"/>'.format(
          float(hexwidth * .5), float(hexwidth * .5), float(hexwidth * .1), rowPos, colPos, float(hexwidth * .05)))
    else:
      rowPos = n.row * float(hexwidth * 0.75)
      colPos = (n.col * float(hexwidth * 0.84) + n.row * float(hexwidth * 0.50) - (n.row - (sideSize - 1) / 2) * float(hexwidth * 0.84)) + (sideSize - 1) * float(hexwidth * 0.84) + (n.row - (nodeRadius - 1)) * float(hexwidth * 0.84) - (n.row * float(hexwidth * 0.08))
      #w.write('<polygon points="25,8 75,8 100,50, 75,92, 25,92, 0,50" fill="#{:02x}{:02x}{:02x}" transform="translate({} {})" stroke="black" stroke-width="0"/>'.format(n.red, n.green, n.blue, 
      w.write('<polygon points="{}" fill="#{:02x}{:02x}{:02x}" transform="translate({} {})" stroke="black" stroke-width="0"/>'.format(polygonPoints, n.red, n.green, n.blue, 
      rowPos, colPos))
      # if (n.outerEdgeNode == True):
      #   w.write('<circle cx="{}" cy="{}" r="{}" fill="transparent" transform="translate({} {})" stroke="#ffffff" stroke-width="4"/>'.format(
      #     float(hexwidth * .5), float(hexwidth * .5), float(hexwidth * .2), rowPos, colPos))
      if (n.glyphNode == True):
        w.write('<circle cx="{}" cy="{}" r="{}" fill="transparent" transform="translate({} {})" stroke="#ffffff" stroke-width="{}"/>'.format(
          float(hexwidth * .5), float(hexwidth * .5), float(hexwidth * .1), rowPos, colPos, float(hexwidth * .05)))
  edgeNodes = [nodes["{}-{}".format(0, 0)], 
  nodes["{}-{}".format(sideSize - 1, 0)], 
  nodes["{}-{}".format(nodeRadius - 1, 0)],
  nodes["{}-{}".format(nodeRadius - 1, sideSize - 1)],
  nodes["{}-{}".format(sideSize - 1, nodeRadius - 1)],
  nodes["{}-{}".format(0, sideSize - 1)]]

  def GetEdgeLinePolygon(n):
    rowPos = 0
    colPos = 0
    if (n.row < (sideSize)):
      rowPos = n.row * float(hexwidth * 0.75)
      colPos = (n.col * float(hexwidth * 0.84) + n.row * float(hexwidth * 0.50) + ((sideSize - 1) - n.row - (sideSize - 1) / 2) * float(hexwidth * 0.84)) - (n.row * float(hexwidth * 0.08))
    else:
      rowPos = n.row * float(hexwidth * 0.75)
      colPos = (n.col * float(hexwidth * 0.84) + n.row * float(hexwidth * 0.50) - (n.row - (sideSize - 1) / 2) * float(hexwidth * 0.84)) + (sideSize - 1) * float(hexwidth * 0.84) + (n.row - (nodeRadius - 1)) * float(hexwidth * 0.84) - (n.row * float(hexwidth * 0.08))
    return "{},{}".format(rowPos, colPos)

  outerPolygonPoints = "{} {} {} {} {} {}".format(
    GetEdgeLinePolygon(edgeNodes[0]),
    GetEdgeLinePolygon(edgeNodes[1]),
    GetEdgeLinePolygon(edgeNodes[2]),
    GetEdgeLinePolygon(edgeNodes[3]),
    GetEdgeLinePolygon(edgeNodes[4]),
    GetEdgeLinePolygon(edgeNodes[5]),
  )

  w.write('<polygon points="{}" transform="translate({} {})" fill="transparent" stroke="black" stroke-width="{}"/>'.format(outerPolygonPoints, float(hexwidth * .5), float(hexwidth * .5), float(hexwidth * .25)))
  w.write('</svg>')
#print (nodes["0-1"].sides[2].Id())
try:
  print (nodes["5-1"])
except:
  print ("no node at 5-1")


print(config)
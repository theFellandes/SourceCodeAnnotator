import math
from stdlib import StdDraw, Color

class StudentDemo:

  def main(self):
    POINTS = 10
    xValues = []
    yValues = []
    dot = 0
    while dot < POINTS:
      if isMousePressed():
        x = StdDraw.mouseX()
        y = StdDraw.mouseY()

        StdDraw.drawSquare(x, y, 0.01)

        xValues[dot] = x
        yValues[dot] = y
        dot += 1
        StdDraw.pause(200)

    index1 = 0
    index2 = 1
    longestDist = self.distance(xValues[index1], yValues[index1], xValues[index2], yValues[index2])

    for i in range(0, POINTS):
      for j in range(i + 1, POINTS):
        dist = self.distance(xValues[i], yValues[i], xValues[j], yValues[j])
        if dist > longestDist:
          longestDist = dist
          index1 = i
          index2 = j

    midX = (xValues[index1] + xValues[index2]) / 2
    midY = (yValues[index1] + yValues[index2]) / 2
    StdDraw.circle(midX, midY, longestDist / 2)
    StdDraw.setPenColor(Color.BLUE)
    StdDraw.drawCircle(
        xValues[index1],
        yValues[index1],
        0.015)
    StdDraw.drawSquare(
      xValues[index1],
      yValues[index1],
      0.015)
    StdDraw.drawTriangle(
      xValues[index1],
      yValues[index1],
      0.015)

  @staticmethod
  def distance(xValues: float, yValues: float, index1: float, index2: float):
    return math.sqrt(math.pow(xValues - index1, 2) + math.pow(yValues - index2, 2))



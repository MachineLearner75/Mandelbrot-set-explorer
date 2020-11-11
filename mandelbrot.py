from multiprocessing import Pool
import sys
import os


class Mandelbrot():
    def __init__(self, canvasW, canvasH, x=-0.75, y=0, m=1.5, iterations=None, w=None, h=None, zoomFactor=0.1, multi=True):
        # our class has 10 parameters related to the tkinter canvas used in the framework, parameters for the mandelbrot, multiprocessing and the zoom

        if None in {w, h}:
            self.width = round(canvasW*0.9)
            self.height = round(canvasH*0.9)
        else:
            w, h

        # if we don't precise the iterations, it will automatically be set at 256. Otherwise, it will take the value set
        if iterations is None:
            self.iterations = 256
        else:
            iterations

        self.xCenter = x #adding the attribute xCenter. The drawing is centered on this x
        self.yCenter = y #adding the attribute yCenter. The drawing is centered on this y

        #Canvas height and width. We scale the size to match the size of the largest dimension
        if canvasW > canvasH:
            self.xDelta = m/(canvasH/canvasW)
            self.yDelta = m
        else:
            self.yDelta = m/(canvasW/canvasH)
            self.xDelta = m

        self.delta = m
        self.multi = multi

        #convert to a bounded box, same logic as Part 1 but translated in OOP
        self.min_x = x - self.xDelta /2
        self.max_x = x + self.xDelta /2 # add /2, to see if it works well
        self.min_y = y - self.yDelta /2
        self.max_y = y + self.yDelta /2

        self.zoomFactor = zoomFactor #adding the attribute zoomFactor = 0.1
        self.yScaleFactor = self.height/canvasH
        self.xScaleFactor = self.width/canvasW

        self.c = 0
        self.z = 0

    def shiftView(self, event):
        self.xCenter = translate(event.x*self.xScaleFactor, 0, self.width, self.min_x, self.max_x)
        self.yCenter = translate(event.y*self.yScaleFactor, self.height, 0, self.min_y, self.max_y)
        self.max_x = self.xCenter + self.xDelta
        self.max_y = self.yCenter + self.yDelta
        self.min_x = self.xCenter - self.xDelta
        self.min_y = self.yCenter - self.yDelta

    def zoomOut(self, event):
        self.xCenter = translate(event.x*self.xScaleFactor, 0, self.width, self.min_x, self.max_x)
        self.yCenter = translate(event.y*self.yScaleFactor, self.height, 0, self.min_y, self.max_y)
        self.xDelta /= self.zoomFactor
        self.yDelta /= self.zoomFactor
        self.delta /= self.zoomFactor
        self.max_x = self.xCenter + self.xDelta
        self.max_y = self.yCenter + self.yDelta
        self.min_x = self.xCenter - self.xDelta
        self.min_y = self.yCenter - self.yDelta

    def zoomIn(self, event):
        self.xCenter = translate(event.x*self.xScaleFactor, 0, self.width, self.min_x, self.max_x)
        self.yCenter = translate(event.y*self.yScaleFactor, self.height, 0, self.min_y, self.max_y)
        self.xDelta *= self.zoomFactor # self.xDelta * self.zoomFactor
        self.yDelta *= self.zoomFactor
        self.delta *= self.zoomFactor
        self.max_x = self.xCenter + self.xDelta
        self.max_y = self.yCenter + self.yDelta
        self.min_x = self.xCenter - self.xDelta
        self.min_y = self.yCenter - self.yDelta

    def getPixels(self):
        coordinates = []
        for x in range(self.width):
            for y in range(self.height):
                coordinates.append((x, y))
        if self.multi:
            pool = Pool()
            self.pixels = pool.starmap(self.getEscapeTime, coordinates)
            pool.close()
            pool.join()
        else:
            print("Using 1 core...")
            pixels = []
            for coord in coordinates:
                pixels.append(self.getEscapeTime(coord[0], coord[1]))
            self.pixels = pixels

    def getEscapeTime(self, x, y):
        re = translate(x, 0, self.width, self.min_x, self.max_x)
        im = translate(y, 0, self.height, self.max_y, self.min_y)
        z, c = complex(re, im), complex(re, im)
        for i in range(1, self.iterations):
            if abs(z) > 2:
                return (x, y, i)
            z = z*z + c
        return (x, y, 0)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

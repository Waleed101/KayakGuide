import PIL.Image
import numpy as geek

def avgImage(w, l, q):
    avgColor = [0,0,0]

    if q==1 or q==2:
        yQuad = 1
    else:
        yQuad = 2

    if q==1 or q==3:
        xQuad = 1
    else:
        xQuad = 2
        
    for x in range(0,w):
        for y in range(0,l):
            avgColor = geek.add(avgColor,pix[x*xQuad,y*yQuad])
    
    avgColor = geek.divide(avgColor,[(w*l)/2,(w*l)/2,(w*l)/2])
    return avgColor

def similar(compare,base):
    return ([abs(base[0]-compare[0]), abs(base[1]-compare[1]), abs(base[2]-compare[2])])

def mostSimilar(quadOne, quadTwo, quadThree, quadFour): # to find which of the four provided quadrant arrays is the most similar to the target value
    tot = [0,0,0,0]
    tot[0] = quadOne[0] + quadOne[1] + quadOne[2]
    tot[1] = quadTwo[0] + quadTwo[1] + quadTwo[2]
    tot[2] = quadThree[0] + quadThree[1] + quadThree[2]
    tot[3] = quadFour[0] + quadFour[1] + quadFour[2]
    if(tot[0] < tot[1] and tot[0] < tot[2] and tot[0] < tot[3]):
        return 0
    elif(tot[1] < tot[0] and tot[1] < tot[2] and tot[1] < tot[3]):
        return 1
    elif(tot[2] < tot[1] and tot[2] < tot[0] and tot[2] < tot[3]):
        return 2
    else:
        return 3

def getNewBounds(quad,width,height): # to convert 
    bounds[0] = quad%2 * width/2
    bounds[1] = int(quad/2) * height/2
    bounds[2] = width/2 + bounds[0]
    bounds[3] = height/2 + bounds[1]

def findBoxBounds(): # to find the bounds of the box
    for x in range(int(bounds[0]), int(bounds[2])):
        for y in range(int(bounds[1]), int(bounds[3])):
            if similarRatio(x,y):
                boxBounds[0] = x
                boxBounds[1] = y
                for w in range(x, int(bounds[2])):                                                                                                                                                   
                    if not similarRatio(w,y):
                        boxBounds[2] = w
                        break
                for z in range(y, int(bounds[3])):                                                                                                                                                   
                    if not similarRatio(x,z):
                        boxBounds[3] = z
                        break
                break
        if not (boxBounds[0]==0 or  boxBounds[1]==0 or boxBounds[2]==0 or boxBounds[3]==0):
            break

    print(boxBounds)
    


def similarRatio(x,y): # function to check if a specific pixel is close to the target value
    sim = similar(pix[x,y], targColor)
    totalSIM = sim[0] + sim[1] + sim[2]                                                                                                                                                   
    if totalSIM < 70:
        return True
    else:
        return False

#------------MAIN CODE------------#
# start_time = time.time()
loc = r"C:\Users\walee\Desktop\Eng Comps\Western Engineering Competition 2020\programming\python\pic.jpg"
im = PIL.Image.open(loc)
#im = image.resize((20,20))
pix = im.load()
quadSize = [int(im.size[0]/2), int(im.size[1]/2)]
bounds = [0,0,im.size[0],im.size[1]] # left, top, right, bottom

targColor = [20,244,240]
boxBounds = [0,0,0,0]

# Finding region
color = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
color[0] = avgImage(quadSize[0],quadSize[1],1)
color[1] = avgImage(quadSize[0],quadSize[1],2)
color[2] = avgImage(quadSize[0],quadSize[1],3)
color[3] = avgImage(quadSize[0],quadSize[1],4)
msSimilar = mostSimilar(similar(color[0], targColor), similar(color[1], targColor), similar(color[2], targColor), similar(color[3], targColor))
# print(msSimilar)

getNewBounds(msSimilar, im.size[0], im.size[1])

# print ("Portion 1: ", time.time() - start_time)
# second_time = time.time()
findBoxBounds()
# print ("Portion 2: ", time.time() - second_time)
shapeIM = im.crop((boxBounds[0], boxBounds[1], boxBounds[2], boxBounds[3]))
shapeIM.show()




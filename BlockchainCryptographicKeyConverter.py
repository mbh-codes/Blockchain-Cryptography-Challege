# BlockchainCryptographicKeyConverter.py
# Created by Miguel Barba

import pygame


#Constants
windowConstant  = 800

validKeys       = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits          = "1234567890"
letters         = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
upper           = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lower           = 'abcdefghijklmnopqrstuvwxyz'
mod             = 127
WHITE           = (255,255,255)
BLACK           = (000,000,000)
lineWidth       = 6
displacement    = 10
topRadians      = 1.57079632679
rightRadians    = 0
leftRadians     = 3.14159265359
bottomRadians   = 4.71238898038
textLocations   = [(330,360),(402,360),(330,397),(402,397)]



#ColorDisplacement
firstSquare  = [125,000,000]
secondSquare = [125,125,000]
thirdSquare  = [000,125,125]
fourthSquare = [125,000,125]
displacementDirectory = [firstSquare,secondSquare,thirdSquare,fourthSquare]


#Setting up rectangles
#pygame.Rect(x_coordinate,y_coordinate,width,height)

def getPublicKey():
    #returns a PublicKey
    print('A public key is 40 keys long and only contains numbers and upper/lower case letters')
    while True:
        publicKey = input('Please enter a public key:\n')
        if len(publicKey) == 40 and (x for x in publicKey if x in validKeys):
            break
    return publicKey

def getSortedPublicKey(rawPublicKey:str):
    #returns a list of 4 string with lengths of 10
    return [rawPublicKey[0:10],rawPublicKey[10:20],rawPublicKey[20:30],rawPublicKey[30:40]]

def getBackgroundColor(aFourth:str):
    template = [[0,0,0],[0,0,0],[0,0,0]]
    for index in range(9):
        if aFourth[index] in digits:
            template[index//3][index%3] = int(aFourth[index])
    return template

def rawColorToRGB(rawColor:[list]):
    RGB = list()
    for set in rawColor:
        triple = ''
        for digit in set:
            triple += str(digit)
        RGB.append(int(triple))
    return RGB

def constrainDirectory(listOfRGB:list):
    copy = listOfRGB[:]
    for square_index in range(len(copy)):
        for triple_index in range(len(copy[square_index])):
            copy[square_index][triple_index] = copy[square_index][triple_index] % mod
    return copy

def refineDirectory(listOfRGB:list):
    copy = listOfRGB[:]
    for index in range(4):
        for triple in range(3):
            copy[index][triple] += displacementDirectory[index][triple]
    return copy

def getPins(listOfRaw:[list],sortedPublicKey:list):
    listOfRGB = [rawColorToRGB(color) for color in listOfRaw]
    retlist = []
    count = 0
    for square in listOfRGB: #indexing through squares/10digits
        pin = ''
        for value in square: #indexing through colors sections
            pin += str(value // mod)

        if sortedPublicKey[count][9] in digits:
            pin += str(sortedPublicKey[count][9])
        count +=1
        retlist.append(pin)
    return retlist

def getLetters(publicKey:list):
    #Takes in a list of 4 10length strings and returns a dictionary for constructing
    retDict = dict()
    for square in range(len(publicKey)):
        retDict[square] = dict()
        for index in range(len(publicKey[0])):
            if publicKey[square][index] in letters:
                if publicKey[square][index] not in retDict[square]:
                    retDict[square][publicKey[square][index]] = [index]
                else:
                    retDict[square][publicKey[square][index]].append(index)
    return retDict

def displayFirstLetters(windowSurface:'surface',letters:dict):
    for letter in letters[0]:
        if letter in lower:
            for length in letters[0][letter]:
                y_placement =  (windowConstant/2) * ((1+lower.find(letter))/(2+len(lower)))
                x_placement =  (windowConstant/2) * ((length+1)/14)

                #pygame.draw.line(windowSurface,WHITE,(0,y_placement),(x_placement,y_placement),lineWidth)
                #pygame.draw.rect(windowSurface,BLACK,(-1 * x_placement,y_placement, x_placement*2, 2*((windowConstant/2)-y_placement)), 5)
                pygame.draw.arc(windowSurface, WHITE,(-1 * x_placement, y_placement, x_placement*2, 2*((windowConstant/2)-y_placement)), rightRadians, topRadians, lineWidth)
        elif letter in upper:
            for length in letters[0][letter]:
                x_placement =  (windowConstant/2) * ((1+upper.find(letter))/(2+len(upper)))
                y_placement =  (windowConstant/2) * ((1+length)/14)
                #pygame.draw.line(windowSurface,WHITE,(x_placement,0),(x_placement,y_placement),lineWidth)
                #pygame.draw.rect(windowSurface,BLACK,(x_placement,-1*y_placement,2*((windowConstant/2)-x_placement),y_placement*2),5)
                pygame.draw.arc(windowSurface,WHITE,(x_placement,-1*y_placement,2*((windowConstant/2)-x_placement),y_placement*2),leftRadians,bottomRadians,lineWidth)

def displaySecondLetters(windowSurface:'surface',letters:dict):
    for letter in letters[1]:
        if letter in lower:
            for length in letters[1][letter]:
                y_placement = (windowConstant/2) * ((1+lower.find(letter))/(2+len(lower)))
                x_placement = ((windowConstant/2) * ((length+1)/14))
                rectangleConstraints = (400-x_placement,-1*y_placement,2*x_placement,2*y_placement)
                #pygame.draw.line(windowSurface,WHITE,(400+x_placement,0),(400+x_placement,y_placement),lineWidth)
                #pygame.draw.rect(windowSurface,BLACK,rectangleConstraints,5)
                pygame.draw.arc(windowSurface,WHITE,rectangleConstraints,bottomRadians,rightRadians,5)

        elif letter in upper:
            for length in letters[1][letter]:
                x_placement = (windowConstant/2) * ((1+upper.find(letter))/(2+len(upper)))
                y_placement = (windowConstant/2) *  ((length+1)/14)
                rectangleConstraints = (x_placement+400,y_placement,2*(windowConstant-(x_placement+400)),2*((windowConstant/2)-y_placement))
                #print(rectangleConstraints)
                #pygame.draw.line(windowSurface,WHITE,(800,y_placement),(x_placement+400,y_placement),lineWidth)
                #pygame.draw.rect(windowSurface,BLACK,rectangleConstraints,lineWidth)
                pygame.draw.arc(windowSurface,WHITE,rectangleConstraints,topRadians,leftRadians,lineWidth)



def displayThirdLetters(windowSurface:'surface',letters:dict):
    for letter in letters[2]:
        if letter in lower:
            for length in letters[2][letter]:
                y_placement = 400 + ((windowConstant/2) * ((1+lower.find(letter))/(len(lower)+2)))
                x_placement =  (windowConstant/2) * ((length+1)/14)
                rectangleConstraints = (x_placement,y_placement,2*((windowConstant/2)-x_placement),2*(windowConstant-y_placement))
                print(rectangleConstraints)
                #pygame.draw.line(windowSurface,WHITE,(x_placement,800),(x_placement,y_placement),lineWidth)
                #pygame.draw.rect(windowSurface,BLACK,rectangConstraints,lineWidth)
                pygame.draw.arc(windowSurface,WHITE,rectangleConstraints,topRadians,leftRadians,lineWidth)

        elif letter in upper:
            for length in letters[2][letter]:
                x_placement = (windowConstant/2) * ((1+upper.find(letter))/(len(upper)+2))
                y_placement = 400 + ((windowConstant/2) *((length+1)/14))
                rectangleConstraints = (-1*x_placement,  (windowConstant/2)-(y_placement-(windowConstant/2)),2*x_placement,(y_placement-400)*2)
                #pygame.draw.line(windowSurface,WHITE,(0,y_placement),(x_placement,y_placement),lineWidth)
                #pygame.draw.rect(windowSurface,BLACK,rectangleConstraints,lineWidth)
                pygame.draw.arc(windowSurface,WHITE,rectangleConstraints,bottomRadians,leftRadians*2,lineWidth)

def displayFourthLetters(windowSurface:'surface',letters:dict):
    for letter in letters[3]:
        if letter in lower:
            if len(letters[3][letter]) != 1:
                #add circles
                pass
            for length in letters[3][letter]:
                y_placement = 400 + (windowConstant/2) * ((lower.find(letter)+1)    /   (2 + len(lower)))
                x_placement = 400 + (windowConstant/2) * ((length+1)/14)
                rectangleConstraints = (x_placement,(windowConstant/2)-(y_placement-(windowConstant/2)),2*(windowConstant-x_placement),                                                                                                             2*(y_placement-(windowConstant/2))  )
                #print(rectangleConstraints)
                #pygame.draw.line(windowSurface,WHITE,(800,y_placement),(x_placement,y_placement),lineWidth)
                #pygame.draw.rect(windowSurface,BLACK,rectangleConstraints,lineWidth)
                pygame.draw.arc(windowSurface,WHITE,rectangleConstraints,leftRadians,bottomRadians,lineWidth)

        elif letter in upper:
            if len(letters[3][letter]) != 1:
                #add circles
                pass
            for length in letters[3][letter]:
                x_placement = 400 + ((windowConstant/2) * ((upper.find(letter)+1)/(len(upper)+2)))
                y_placement = 400 + ((windowConstant/2) * ((length+1)/14))
                rectangleConstraints = ((windowConstant/2)-(x_placement-(windowConstant/2)),y_placement,2*(x_placement-(windowConstant/2)),2*(windowConstant-y_placement))

                #print(rectangleConstraints)
                #pygame.draw.line(windowSurface,WHITE,(x_placement,800),(x_placement,y_placement),lineWidth)
                #pygame.draw.rect(windowSurface,BLACK,rectangleConstraints,lineWidth)
                pygame.draw.arc(windowSurface,WHITE,rectangleConstraints,rightRadians,topRadians,lineWidth)


def displayLetter(windowSurface:'surface',letters:dict):
    displayFirstLetters(windowSurface,letters)
    displaySecondLetters(windowSurface,letters)
    displayThirdLetters(windowSurface,letters)
    displayFourthLetters(windowSurface,letters)


def renderPins(windowSurface:'surface',Pins:dict,font:'font'):
    texts = []
    for pin in Pins:
        texts.append(font.render(pin,False,BLACK))
    for index in range(len(texts)):
        windowSurface.blit(texts[index],textLocations[index])

def run():
    pygame.init()
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS',30)
    clock = pygame.time.Clock()

    try:
        while True:
            windowSurface = pygame.display.set_mode((windowConstant,windowConstant))

            sortedPublicKey = getSortedPublicKey(getPublicKey())
            firstColor  = getBackgroundColor(sortedPublicKey[0])
            secondColor = getBackgroundColor(sortedPublicKey[1])
            thirdColor  = getBackgroundColor(sortedPublicKey[2])
            fourthColor = getBackgroundColor(sortedPublicKey[3])
            rawColor = [firstColor,secondColor,thirdColor,fourthColor]

            #Required Information
            colors  = refineDirectory(constrainDirectory([rawColorToRGB(color) for color in rawColor])) #Color
            pins    = getPins(rawColor,sortedPublicKey)
            letters = getLetters(sortedPublicKey)


            #Displaying the Background
            windowSurface.fill((0,0,0))

            #Displaying the squares
            squares = [pygame.Rect(0,0,400,400),pygame.Rect(400,0,800,400),pygame.Rect(0,400,400,800),pygame.Rect(400,400,800,800)]
            for index in range(4):
                pygame.draw.rect(windowSurface,tuple(colors[index]),squares[index])
            #print(letters)


            #Displaying the curves
            #print(letters)
            displayLetter(windowSurface,letters)

            #Displaying the pins
            renderPins(windowSurface,pins,myfont)



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            pygame.display.update()
            pygame.display.flip()
            clock.tick(60)
    finally:
        pygame.quit()



if __name__ == '__main__':
    run()

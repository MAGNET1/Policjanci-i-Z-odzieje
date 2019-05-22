import pygame
import silnik_main
import silnik_board
import copy

N = silnik_board.N + 2

mul = 1000 # do zmiany wielkości okna. Dostępna jeszcze wartosc to 1000 - pozostałe się rozjeżdżają
boardXratio = 1.2
boardYratio = 0.7

boardX = int(boardXratio * mul)
boardY = int(boardYratio * mul)

thiefImage = pygame.image.load('Thief.png')
thiefImage = pygame.transform.scale(thiefImage, (int(boardY / N), int(boardY / N)))

policemanImage = pygame.image.load('Policeman.png')
policemanImage = pygame.transform.scale(policemanImage, (int(boardY / N), int(boardY / N)))

def writeText(window, text, fontSize, coords, color):
    font = pygame.font.SysFont("Times New Roman, Arial", fontSize)
    text = font.render(text, True, color)
    window.blit(text, coords)

def drawElement(window, elementType, coords, idx=-1):
    color = (0,0,0)
    if elementType is 'wall':
        color = (122, 82, 119)
    elif elementType is 'obstacle':
        color = (83,193,92)
    elif elementType is 'gate':
        color = (234,186,53)
    elif elementType is 'thief':
        color = (234,62,53)
    elif elementType is 'policeman':
        color = (53,93,234)

    size = int(boardY / N)

    finalCoordsX = coords[1] * size+int(coords[1]/2)
    finalCoordsY = coords[0] * size+int(coords[0]/2)
    if mul == 1000:
        finalCoordsX = coords[1] * size+int(coords[1]*0.9)
        finalCoordsY = coords[0] * size+int(coords[0]*0.9)
    
    pygame.draw.rect(window, color, (finalCoordsX, finalCoordsY, size, size))
    # pygame.draw.rect(window, color, (coords[1] * size+int(coords[1]/2), coords[0] * size+int(coords[0]/2)), size, size)
    if elementType is 'policeman':
        window.blit(policemanImage, (finalCoordsX, finalCoordsY))
        writeText(window, str(idx), 15, (finalCoordsX, finalCoordsY - 3), (255,255,255))
    if elementType is 'thief':
        window.blit(thiefImage, (finalCoordsX, finalCoordsY))

def gameLoop(printStatee, lock):

    pygame.init()

    win = pygame.display.set_mode((boardX,boardY))
    pygame.display.set_caption("Policjanci i Złodzieje")

    run = True
    while run:
        pygame.time.delay(200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        win.fill((0,0,0))
        

        # writeText(window=win, text="Hello World!", fontSize = 20, coords=(20, 30), color=(128,155,23))

        for i in range(N):
            drawElement(win,'wall',[i,0])
            drawElement(win,'wall',[i,N-1])
            drawElement(win,'wall',[0,i])
            drawElement(win,'wall',[N-1,i])

        # getting board state
        for key,value in printStatee['board'].items():
            if key is 'gatesCoords':
                for i in range(len(value)):
                    for j in range(len(value[i])):
                        drawElement(win, 'gate', value[i][j])
            elif key is 'obstaclesCoords':
                for i in range(len(value)):
                    for j in range(len(value[i])):
                        drawElement(win, 'obstacle', value[i][j])
            elif key is 'thiefCoords':
                drawElement(win, 'thief', value)
            elif 'policeman' in key:
                drawElement(win, 'policeman', value['coords'], value['ID'])

        # text
        textCoordX = int(boardX/8) * 5
        textCoordY = int(boardY/20)
        writeText(win, 'Runda: ' + str(printStatee['t']) + '/' + str(printStatee['TMax']), 30, (textCoordX, textCoordY), (255,255,255))
        writeText(win, 'Zlodziej: ' + str(printStatee['ttSequence']), 30, (textCoordX + 37, textCoordY + 60), (255,255,255))
        ctSequence = copy.deepcopy(printStatee['ctSequence'])
        i = 0
        for key,value in ctSequence.items():
            polStr = str(value)
            if 'playerMove' in polStr:
                continue
            # xDDDDDDDDDDDDDDDDDDDDDDD (usprawiedliwiam się: nie dało się wyłuskać zagnieżdżonego słownika, więc na patencie)
            writeText(win, 'Policjant ' + polStr[7] + ' : ' + polStr[-16:-1], 30, (textCoordX, textCoordY + 90 + (30 * i)), (255,255,255))
            i += 1

        if printStatee['winner'] == 0:
            writeText(win, 'Zwyciezca: Zlodziej!', 30, (textCoordX, 300), (234,62,53))
            writeText(win, 'Punkty: ' + str(printStatee['points']), 30, (textCoordX, 330), (234,62,53))
        elif printStatee['winner'] == 1:
            writeText(win, 'Zwyciezca: Policjant!', 30, (textCoordX, 300), (53,93,234))
            writeText(win, 'Punkty: ' + str(printStatee['points']), 30, (textCoordX, 330), (53,93,234))

        writeText(win, 'O', 30, (textCoordX + 155 + (((printStatee['t']+3)%5)*30), 60), (255,255,255))


        # drawing board
        gridColor = (150,150,150)
        for i in range(N):
            offset = int((boardY / N)*i)
            pygame.draw.line(win, gridColor,(0, offset),(boardY, offset), 1)
            pygame.draw.line(win, gridColor,(offset,0),(offset, boardY), 1)
        pygame.draw.line(win, gridColor,(boardY,0),(boardY, boardY), 1)

        pygame.display.update()

    pygame.quit()
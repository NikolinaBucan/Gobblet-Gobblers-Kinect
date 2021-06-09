import pygame
from pykinect import nui
from pykinect.nui import JointId, SkeletonTrackingState


# GLOBAL VARIABLES
KINECTEVENT = pygame.USEREVENT

pygame.init()
screen = pygame.display.set_mode((1300, 1000))
pygame.display.set_caption("TIC - TAC - TOE")
pozadina = pygame.image.load('Pozadina.png')
cPobeda = pygame.image.load('cPobeda.png')
pPobeda = pygame.image.load('pPobeda.png')
nereseno = pygame.image.load('Nereseno.png')
crveni3 = pygame.image.load('Crveni3.png')
crveni2 = pygame.image.load('Crveni2.png')
crveni1 = pygame.image.load('Crveni1.png')
crveni3_2 = pygame.image.load('Crveni3.png')
crveni2_2 = pygame.image.load('Crveni2.png')
crveni1_2 = pygame.image.load('Crveni1.png')
plavi3 = pygame.image.load('Plavi3.png')
plavi2 = pygame.image.load('Plavi2.png')
plavi1 = pygame.image.load('Plavi1.png')
plavi3_2 = pygame.image.load('Plavi3.png')
plavi2_2 = pygame.image.load('Plavi2.png')
plavi1_2 = pygame.image.load('Plavi1.png')
selekcija1 = pygame.image.load('Selekcija1.png')
selekcija2 = pygame.image.load('Selekcija2.png')
potvrda = pygame.image.load('Selekcija2Potvrda.png')

running = True

player1 = True
player2 = False

c1_1x = 10
c1_1y = 315
c1_2x = 10
c1_2y = 485
c1_3x = 10
c1_3y = 655

c2_1x = 150
c2_1y = 315
c2_2x = 150
c2_2y = 485
c2_3x = 150
c2_3y = 655

p3_1x = 1008
p3_1y = 315
p3_2x = 1008
p3_2y = 485
p3_3x = 1008
p3_3y = 655

p4_1x = 1158
p4_1y = 315
p4_2x = 1158
p4_2y = 485
p4_3x = 1158
p4_3y = 655

mestoSvihPijuna = [[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3], [4, 1], [4, 2], [4, 3]]

polje11 = [0,0] #prva koordinata odredjuje sta poslednje stoji na njemu, 0 za prazno, 1 za malog pijuna, 2 za srednjeg, 3 za velikog, kao sto je druga koordinata za mesto
polje21 = [0,0] #druga odredjuje koja boja stoji na njemu, 0 - niko, 1 - crveni, 2 - plavi
polje31 = [0,0]
polje12 = [0,0]
polje22 = [0,0]
polje32 = [0,0]
polje13 = [0,0]
polje23 = [0,0]
polje33 = [0,0]

svaPolja = [polje11, polje12, polje13, polje21, polje22, polje23, polje31, polje32, polje33]

pijunSelekcija = True
poljeSelekcija = True
polje = [0, 0]
poljeTMP = [0, 0]

mesto = [0, 0]

polozajLeveRuke = 0
br1 = 0
br2 = 0
br3 = 0
br = 0



# Functions
def post_frame(frame):
    try:
        pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons=frame.SkeletonData))
    except:
        pass


def CrtajPozadinu():
    global player1, player2
    if ProveriKrajIgre() == 1:
        screen.blit(cPobeda, (0, 0))
        player1 = False
        player2 = False
    elif ProveriKrajIgre() == 2:
        screen.blit(pPobeda, (0, 0))
        player1 = False
        player2 = False
    elif ProveriKrajIgre() == 3:
        screen.blit(nereseno, (0, 0))
        player1 = False
        player2 = False
    else:
        screen.blit(pozadina, (0, 0))

        screen.blit(crveni1, (c1_1x, c1_1y))
        screen.blit(crveni1_2, (c2_1x, c2_1y))
        screen.blit(plavi1, (p4_1x, p4_1y))
        screen.blit(plavi1_2, (p3_1x, p3_1y))

        screen.blit(crveni2, (c1_2x, c1_2y))
        screen.blit(crveni2_2, (c2_2x, c2_2y))
        screen.blit(plavi2, (p4_2x, p4_2y))
        screen.blit(plavi2_2, (p3_2x, p3_2y))

        screen.blit(crveni3, (c1_3x, c1_3y))
        screen.blit(crveni3_2, (c2_3x, c2_3y))
        screen.blit(plavi3, (p4_3x, p4_3y))
        screen.blit(plavi3_2, (p3_3x, p3_3y))

def ProveriKrajIgre():
    sveKombinacijeZaPolja = [[polje11, polje21, polje31], [polje12, polje22, polje32], [polje13, polje23, polje33],[polje11, polje12, polje13], [polje21, polje22, polje23], [polje31, polje32, polje33],[polje11, polje22, polje33], [polje31, polje22, polje13]]


    for kombinacijaPolja in sveKombinacijeZaPolja:
        crveni = 0
        plavi = 0
        for p in kombinacijaPolja:
            if p[1] == 1:
                crveni += 1
            elif p[1] == 2:
                plavi += 1
        if crveni == 3:
            return 1
        elif plavi == 3:
            return 2

    mmax = 0
    nmin = 4
    if mestoSvihPijuna is []:
        return 3
    elif [0,0] not in svaPolja:
        for m in mestoSvihPijuna:
            if m[1] > mmax:
                mmax = m[1]
        for n in svaPolja:
            if n[0] < nmin:
                nmin = n[0]
        if mmax <= nmin:
            return 3

#Game
with nui.Runtime() as kinect:
    kinect.skeleton_engine.enabled = True
    kinect.skeleton_frame_ready += post_frame


    while running:
        CrtajPozadinu()

        if player1:
            if pijunSelekcija:
                if polozajLeveRuke == 1:
                    if [1, 1] in mestoSvihPijuna:
                        screen.blit(selekcija2, (10, 315))
                    elif [2, 1] in mestoSvihPijuna:
                        screen.blit(selekcija2, (150, 315))
                elif polozajLeveRuke == 2:
                    if [1, 3] in mestoSvihPijuna:
                        screen.blit(selekcija2, (10, 655))
                    elif [2, 3] in mestoSvihPijuna:
                        screen.blit(selekcija2, (150, 655))
                elif polozajLeveRuke == 3:
                    if [1, 2] in mestoSvihPijuna:
                        screen.blit(selekcija2, (10, 485))
                    elif [2, 2] in mestoSvihPijuna:
                        screen.blit(selekcija2, (150, 485))

            else:
                if polozajLeveRuke == 1:
                    if [1, 1] in mestoSvihPijuna:
                        screen.blit(potvrda, (10, 315))
                    elif [2, 1] in mestoSvihPijuna:
                        screen.blit(potvrda, (150, 315))
                elif polozajLeveRuke == 2:
                    if [1, 3] in mestoSvihPijuna:
                        screen.blit(potvrda, (10, 655))
                    elif [2, 3] in mestoSvihPijuna:
                        screen.blit(potvrda, (150, 655))
                elif polozajLeveRuke == 3:
                    if [1, 2] in mestoSvihPijuna:
                        screen.blit(potvrda, (10, 485))
                    elif [2, 2] in mestoSvihPijuna:
                        screen.blit(potvrda, (150, 485))

                # selekcija Polja
                if poljeSelekcija:
                    if polje == [1, 1] and mesto[1] > polje11[0]:
                        screen.blit(selekcija1, (305, 155))
                    elif polje == [1, 2] and mesto[1] > polje12[0]:
                        screen.blit(selekcija1, (305, 385))
                    elif polje == [1, 3] and mesto[1] > polje13[0]:
                        screen.blit(selekcija1, (305, 615))
                    elif polje == [2, 1] and mesto[1] > polje21[0]:
                        screen.blit(selekcija1, (535, 155))
                    elif polje == [2, 2] and mesto[1] > polje22[0]:
                        screen.blit(selekcija1, (535, 385))
                    elif polje == [2, 3] and mesto[1] > polje23[0]:
                        screen.blit(selekcija1, (535, 615))
                    elif polje == [3, 1] and mesto[1] > polje31[0]:
                        screen.blit(selekcija1, (765, 155))
                    elif polje == [3, 2] and mesto[1] > polje32[0]:
                        screen.blit(selekcija1, (765, 385))
                    elif polje == [3, 3] and mesto[1] > polje33[0]:
                        screen.blit(selekcija1, (765, 615))
                else:
                    if polje == [1, 1]:
                        x = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 305 + 49
                        y = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 155 + 49
                        player1 = False
                        player2 = True
                        polje11[0] = mesto[1]
                        polje11[1] = 1

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0,0]
                        polje = [0,0]

                    elif polje == [1, 2]:
                        x = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 305 + 49
                        y = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 385 + 49
                        player1 = False
                        player2 = True
                        polje12[0] = mesto[1]
                        polje12[1] = 1

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]

                    elif polje == [1, 3]:
                        x = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 305 + 49
                        y = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 615 + 49
                        player1 = False
                        player2 = True
                        polje13[0] = mesto[1]
                        polje13[1] = 1

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]

                    elif polje == [2, 1]:
                        x = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 535 + 49
                        y = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 155 + 49
                        player1 = False
                        player2 = True
                        polje21[0] = mesto[1]
                        polje21[1] = 1

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]

                    elif polje == [2, 2]:
                        x = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 535 + 49
                        y = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 385 + 49
                        player1 = False
                        player2 = True
                        polje22[0] = mesto[1]
                        polje22[1] = 1

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]

                    elif polje == [2, 3]:
                        x = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 535 + 49
                        y = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 615 + 49
                        player1 = False
                        player2 = True
                        polje23[0] = mesto[1]
                        polje23[1] = 1

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]

                    elif polje == [3, 1]:
                        x = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 765 + 49
                        y = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 155 + 49
                        player1 = False
                        player2 = True
                        polje31[0] = mesto[1]
                        polje31[1] = 1

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]

                    elif polje == [3, 2]:
                        x = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 765 + 49
                        y = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 385 + 49
                        player1 = False
                        player2 = True
                        polje32[0] = mesto[1]
                        polje32[1] = 1

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]

                    elif polje == [3, 3]:
                        x = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 765 + 49
                        y = "c" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 615 + 49
                        player1 = False
                        player2 = True
                        polje33[0] = mesto[1]
                        polje33[1] = 1

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]

        if player2:
            if pijunSelekcija == True:
                if polozajLeveRuke == 1:
                    if [3, 1] in mestoSvihPijuna:
                        screen.blit(selekcija2, (1008, 315))
                    elif [4, 1] in mestoSvihPijuna:
                        screen.blit(selekcija2, (1158, 315))
                elif polozajLeveRuke == 2:
                    if [3, 3] in mestoSvihPijuna:
                        screen.blit(selekcija2, (1008, 655))
                    elif [4, 3] in mestoSvihPijuna:
                        screen.blit(selekcija2, (1158, 655))
                elif polozajLeveRuke == 3:
                    if [3,2] in mestoSvihPijuna:
                        screen.blit(selekcija2, (1008, 485))
                    elif [4, 2] in mestoSvihPijuna:
                        screen.blit(selekcija2, (1158, 485))


            if pijunSelekcija == False:
                if polozajLeveRuke == 1:
                    if [3, 1] in mestoSvihPijuna:
                        screen.blit(potvrda, (1008, 315))
                    elif [4, 1] in mestoSvihPijuna:
                        screen.blit(potvrda, (1158, 315))
                elif polozajLeveRuke == 2:
                    if [3, 3] in mestoSvihPijuna:
                        screen.blit(potvrda, (1008, 655))
                    elif [4, 3] in mestoSvihPijuna:
                        screen.blit(potvrda, (1158, 655))
                elif polozajLeveRuke == 3:
                    if [3,2] in mestoSvihPijuna:
                        screen.blit(potvrda, (1008, 485))
                    elif [4, 2] in mestoSvihPijuna:
                        screen.blit(potvrda, (1158, 485))
                # selekcija Polja
                if poljeSelekcija:
                    if polje == [1, 1] and mesto[1] > polje11[0]:
                        screen.blit(selekcija1, (305, 155))
                    elif polje == [1, 2] and mesto[1] > polje12[0]:
                        screen.blit(selekcija1, (305, 385))
                    elif polje == [1, 3] and mesto[1] > polje13[0]:
                        screen.blit(selekcija1, (305, 615))
                    elif polje == [2, 1] and mesto[1] > polje21[0]:
                        screen.blit(selekcija1, (535, 155))
                    elif polje == [2, 2] and mesto[1] > polje22[0]:
                        screen.blit(selekcija1, (535, 385))
                    elif polje == [2, 3] and mesto[1] > polje23[0]:
                        screen.blit(selekcija1, (535, 615))
                    elif polje == [3, 1] and mesto[1] > polje31[0]:
                        screen.blit(selekcija1, (765, 155))
                    elif polje == [3, 2] and mesto[1] > polje32[0]:
                        screen.blit(selekcija1, (765, 385))
                    elif polje == [3, 3] and mesto[1] > polje33[0]:
                        screen.blit(selekcija1, (765, 615))
                else:
                    if polje == [1, 1]:
                        x = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 305 + 49
                        y = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 155 + 49
                        player2 = False
                        player1 = True
                        polje11[0] = mesto[1]
                        polje11[1] = 2

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]


                    elif polje == [1, 2]:
                        x2 = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x2] = 305 + 49
                        y2 = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y2] = 385 + 49
                        player2 = False
                        player1 = True
                        polje12[0] = mesto[1]
                        polje12[1] = 2

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]

                    elif polje == [1, 3]:
                        x = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 305 + 49
                        y = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 615 + 49
                        player2 = False
                        player1 = True
                        polje13[0] = mesto[1]
                        polje13[1] = 2

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]

                    elif polje == [2, 1]:
                        x = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 535 + 49
                        y = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 155 + 49
                        player2 = False
                        player1 = True
                        polje21[0] = mesto[1]
                        polje21[1] = 2

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]

                    elif polje == [2, 2]:
                        x = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 535 + 49
                        y = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 385 + 49
                        player2 = False
                        player1 = True
                        polje22[0] = mesto[1]
                        polje22[1] = 2

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]

                    elif polje == [2, 3]:
                        x = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 535 + 49
                        y = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 615 + 49
                        player2 = False
                        player1 = True
                        polje23[0] = mesto[1]
                        polje23[1] = 2

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]

                    elif polje == [3, 1]:
                        x = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 765 + 49
                        y = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 155 + 49
                        player2 = False
                        player1 = True
                        polje31[0] = mesto[1]
                        polje31[1] = 2

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]

                    elif polje == [3, 2]:
                        x = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 765 + 49
                        y = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 385 + 49
                        player2 = False
                        player1 = True
                        polje32[0] = mesto[1]
                        polje32[1] = 2

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]

                    elif polje == [3, 3]:
                        x = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "x"
                        vars()[x] = 765 + 49
                        y = "p" + str(mesto[0]) + "_" + str(mesto[1]) + "y"
                        vars()[y] = 615 + 49
                        player2 = False
                        player1 = True
                        polje33[0] = mesto[1]
                        polje33[1] = 2

                        pijunSelekcija = True
                        poljeSelekcija = True
                        mesto = [0, 0]
                        polje = [0, 0]

        pygame.display.flip()

        e = pygame.event.wait()

        if e.type == pygame.QUIT:
            break
        elif e.type == KINECTEVENT:
            skeletons = e.skeletons
            if player1:
                for i, data in enumerate(skeletons):
                    if i == 0:
                        if data.tracking_state == SkeletonTrackingState.TRACKED:

                            if pijunSelekcija:
                                left_hand = data.SkeletonPositions[JointId.hand_left]
                                left_shoulder = data.SkeletonPositions[JointId.shoulder_left]

                                LHand_y = left_hand.y
                                LShoulder_y = left_shoulder.y

                                if (LHand_y - LShoulder_y) > 0.2:
                                    polozajLeveRuke = 1
                                    if [1, 1] in mestoSvihPijuna:
                                        mesto = [1, 1]
                                    elif [2, 1] in mestoSvihPijuna:
                                        mesto = [2, 1]
                                    else:
                                        mesto = [0, 0]

                                    if mesto != [0, 0]:
                                        br1 += 1
                                        br2 = 0
                                        br3 = 0
                                        if br1 == 80:
                                            pijunSelekcija = False
                                            br1 = 0


                                elif (LShoulder_y - LHand_y) > 0.2:
                                    polozajLeveRuke = 2
                                    if [1, 3] in mestoSvihPijuna:
                                        mesto = [1, 3]
                                    elif [2, 3] in mestoSvihPijuna:
                                        mesto = [2, 3]
                                    else:
                                        mesto = [0, 0]

                                    if mesto != [0, 0]:
                                        br1 = 0
                                        br2 += 1
                                        br3 = 0
                                        if br2 == 80:
                                            pijunSelekcija = False
                                            br2 = 0

                                else:
                                    polozajLeveRuke = 3
                                    if [1, 2] in mestoSvihPijuna:
                                        mesto = [1, 2]
                                    elif [2, 2] in mestoSvihPijuna:
                                        mesto = [2, 2]
                                    else:
                                        mesto = [0, 0]

                                    if mesto != [0, 0]:
                                        br1 = 0
                                        br2 = 0
                                        br3 += 1
                                        if br3 == 80:
                                            pijunSelekcija = False
                                            br3 = 0

                            else:
                                right_hand = data.SkeletonPositions[JointId.hand_right]
                                right_shoulder = data.SkeletonPositions[JointId.shoulder_right]

                                RHand_x = right_hand.x
                                RShoulder_x = right_shoulder.x

                                RHand_y = right_hand.y
                                RShoulder_y = right_shoulder.y

                                if (RHand_y - RShoulder_y) > 0.1:
                                    polje[1] = 1
                                    if (RHand_x - RShoulder_x) > 0.1:
                                        polje[0] = 3
                                    elif (RShoulder_x - RHand_x) > 0.1:
                                        polje[0] = 1
                                    else:
                                        polje[0] = 2

                                elif (RShoulder_y - RHand_y) > 0.1:
                                    polje[1] = 3
                                    if (RHand_x - RShoulder_x) > 0.1:
                                        polje[0] = 3
                                    elif (RShoulder_x - RHand_x) > 0.1:
                                        polje[0] = 1
                                    else:
                                        polje[0] = 2

                                else:
                                    polje[1] = 2
                                    if (RHand_x - RShoulder_x) > 0.1:
                                        polje[0] = 3
                                    elif (RShoulder_x - RHand_x) > 0.1:
                                        polje[0] = 1
                                    else:
                                        polje[0] = 2


                                if (polje != [0, 0]) and (mesto in mestoSvihPijuna) and (mesto[1] > vars()["polje"+str(polje[0])+str(polje[1])][0]):
                                    if polje == poljeTMP:
                                        br += 1
                                    else:
                                        poljeTMP = list(polje)
                                        br = 0
                                    if br == 80:
                                        poljeSelekcija = False
                                        mestoSvihPijuna.remove(mesto)
                                        br = 0

            if player2:
                for i, data in enumerate(skeletons):
                    if i == 1:
                        if data.tracking_state == SkeletonTrackingState.TRACKED:

                            if pijunSelekcija:
                                left_hand = data.SkeletonPositions[JointId.hand_left]
                                left_shoulder = data.SkeletonPositions[JointId.shoulder_left]

                                LHand_y = left_hand.y
                                LShoulder_y = left_shoulder.y

                                if (LHand_y - LShoulder_y) > 0.2:
                                    polozajLeveRuke = 1
                                    if [3, 1] in mestoSvihPijuna:
                                        mesto = [3, 1]
                                    elif [4, 1] in mestoSvihPijuna:
                                        mesto = [4, 1]
                                    else:
                                        mesto = [0, 0]

                                    if mesto != [0, 0]:
                                        br1 += 1
                                        br2 = 0
                                        br3 = 0
                                        if br1 == 80:
                                            pijunSelekcija = False
                                            br1 = 0


                                elif (LShoulder_y - LHand_y) > 0.2:
                                    polozajLeveRuke = 2
                                    if [3, 3] in mestoSvihPijuna:
                                        mesto = [3, 3]
                                    elif [4, 3] in mestoSvihPijuna:
                                        mesto = [4, 3]
                                    else:
                                        mesto = [0, 0]

                                    if mesto != [0, 0]:
                                        br1 = 0
                                        br2 += 1
                                        br3 = 0
                                        if br2 == 80:
                                            pijunSelekcija = False
                                            br2 = 0

                                else:
                                    polozajLeveRuke = 3
                                    if [3, 2] in mestoSvihPijuna:
                                        mesto = [3, 2]
                                    elif [4, 2] in mestoSvihPijuna:
                                        mesto = [4, 2]
                                    else:
                                        mesto = [0, 0]

                                    if mesto != [0, 0]:
                                        br1 = 0
                                        br2 = 0
                                        br3 += 1
                                        if br3 == 80:
                                            pijunSelekcija = False
                                            br3 = 0

                            else:
                                right_hand = data.SkeletonPositions[JointId.hand_right]
                                right_shoulder = data.SkeletonPositions[JointId.shoulder_right]

                                RHand_x = right_hand.x
                                RShoulder_x = right_shoulder.x

                                RHand_y = right_hand.y
                                RShoulder_y = right_shoulder.y

                                if (RHand_y - RShoulder_y) > 0.1:
                                    polje[1] = 1
                                    if (RHand_x - RShoulder_x) > 0.2:
                                        polje[0] = 3
                                    elif (RShoulder_x - RHand_x) > 0.2:
                                        polje[0] = 1
                                    else:
                                        polje[0] = 2


                                elif (RShoulder_y - RHand_y) > 0.1:
                                    polje[1] = 3
                                    if (RHand_x - RShoulder_x) > 0.2:
                                        polje[0] = 3
                                    elif (RShoulder_x - RHand_x) > 0.2:
                                        polje[0] = 1
                                    else:
                                        polje[0] = 2


                                else:
                                    polje[1] = 2
                                    if (RHand_x - RShoulder_x) > 0.2:
                                        polje[0] = 3
                                    elif (RShoulder_x - RHand_x) > 0.2:
                                        polje[0] = 1
                                    else:
                                        polje[0] = 2

                                if polje != [0, 0] and (mesto in mestoSvihPijuna) and (mesto[1] > vars()["polje"+str(polje[0])+str(polje[1])][0]):
                                    if polje == poljeTMP:
                                        br += 1
                                    else:
                                        poljeTMP = list(polje)
                                        br = 0
                                    if br == 80:
                                        poljeSelekcija = False
                                        mestoSvihPijuna.remove(mesto)
                                        br = 0

pygame.quit()
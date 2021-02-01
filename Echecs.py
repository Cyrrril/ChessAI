# Classe important toutes les autres classes permettant le lancement du jeu
from PlateauEchecs import *
from GraphEchecs import GraphEchecs
from IA import *
import time, threading

def real_coord(x):
    if x <= 100:
        return 0
    else:
        return (x-100)/100 + 1

def Plateau_coord(x):
    return 100 * x + 50

class Echecs:

    Distribution_Info = ["Lancement classique", "Single Tour Kill", "Pion mange Pion "]     #afficher le mode de lancement sur le terminal
    Game_Mode_Info = ["Humain vs Humain", "Humain vs IA", "IA vs IA"]

    def __init__(self, mode = 1, dis = 0, showMove = True, showRecherche = False, showGUI = True, saveInfo = False):
                self.Plateau = PlateauEchecs()
                self.Player_Side = False
                self.GameMode = mode
                self.distribution = dis

                self.ai_0 = IA()
                self.ai_1 = IA()

                self.ShowMoveInfo = showMove
                self.ShowRechercheInfo = showRecherche
                self.ShowGraphUI = showGUI
                self.SaveInfo = saveInfo

                self.view = GraphEchecs(self)

    def Set(self, mode = 1, dis = 0, showMove = True, showRecherche = False, showGUI = True,
                saveInfo = False, saveChemin = r".\Records",
                ai_name_0 = "MinMaxRecherche", use_pos_0 = False, profondeur_0 = 3,
                ai_name_1 = "MinMaxRecherche", profondeur_1 = 3, use_pos_1 = False):
        self.GameMode = mode
        self.distribution = dis
        self.ShowMoveInfo = showMove
        self.ShowRechercheInfo = showRecherche
        self.ShowGraphUI = showGUI
        self.SaveInfo = saveInfo
        self.SaveChemin = saveChemin
        self.SaveFileName = ""
        if ai_name_0 == "MinMaxRecherche":
            ai_0 = MinMaxRechercheIA(profondeur_0, True, use_pos_0)
        else:
            ai_0 = RandomMoveIA()
        if ai_name_1 == "MinMaxRecherche":
            ai_1 = MinMaxRechercheIA(profondeur_1, True, use_pos_1)
        else:
            ai_1 = RandomMoveIA()
        self.SetIA(ai_0, ai_1)

    def SetGame(self, mode = 1, dis = 0):
        self.GameMode = mode
        self.distribution = dis

    def SetInfo(self, showMove = True, showRecherche = False, showGUI = True, saveInfo = False):
            self.ShowMoveInfo = showMove
            self.ShowRechercheInfo = showRecherche
            self.ShowGraphUI = showGUI
            self.SaveInfo = saveInfo

    def SetIA(self, ai_0, ai_1):
        self.ai_0 = ai_0
        self.ai_1 = ai_1

    def start(self):

        timeInfo = time.strftime('%Y-%m-%d %H:%M:%S')   #Temps passe
        timeLabel = time.strftime('%Y-%m-%d-%H-%M-%S')

        self.SaveFileName = timeLabel + ".txt"  #Sauvegarder une partie avec la date et l'heure a laquelle la personne a joue

        Msg = timeInfo + " " \
              + Echecs.Game_Mode_Info[self.GameMode] + " " \
              + Echecs.Distribution_Info[self.distribution] + "\n"
        Msg_IA = ""
        if self.GameMode == 1:
            Msg_IA += str(self.ai_0) + "\n"
        elif self.GameMode == 2:
            Msg_IA += str(self.ai_0) + "\n"
            Msg_IA += str(self.ai_1) + "\n"

        print Msg + Msg_IA,
        if self.SaveInfo:
            self.SaveData(Msg + Msg_IA)

        self.Plateau.Plateau_Init(self.distribution)

        if self.GameMode == 2:
            if not self.ShowGraphUI:
                self.Game_IAvIA_Auto(self.ai_0, self.ai_1)

        self.view.showMsg("Jeu D'Echecs")
        self.view.draw_Plateau(self.Plateau)
        self.view.start()

    def callback(self, event):
        rx, ry = real_coord(event.x), real_coord(800 - event.y)
        self.Game(rx, ry, self.GameMode)

    def Move_Info(self, move_info):
        game_info = {0:"", 1:" #", 2:" #", 3:" Impasse", 4:" Egalite", 5:" Perpetual check"}
        return "(" + str(self.Plateau.Round) + "):" + move_info \
        + game_info[self.Plateau.Statut] \
        + ("; " if self.Player_Side else ";\n")

    def SaveData(self, info):
        fileName = self.SaveChemin + r'\chess-' + self.SaveFileName
        with open(fileName, 'a') as data:
            data.write(info)

    def Game(self, x, y, mode = 0):
        if mode == 0:
            self.Game_PvP(x, y)
        elif mode == 1:
            self.Game_PvIA(x, y)
        elif mode == 2:
            self.Game_IAvIA(self.ai_0, self.ai_1)
        else:
            raise Exception("Mode de jeu invalide: " + str(mode))

    
    def Game_PvIA(self, rx, ry):  #Fonction qui fait le jeu entre un joueur et l'IA
        if self.Plateau.Statut != 0:
            return
        move_info = self.Plateau.select(rx, ry, self.Player_Side)
        self.view.draw_Plateau(self.Plateau)
        if move_info != "":
            self.view.showMsg("Tour Blanc" if self.Player_Side else "Tour Noir")    #On affiche en titre de fenetre si c'est aux blancs ou aux noirs de jouer
            self.Player_Side = not self.Player_Side
            self.Plateau.Round += 1
            self.Plateau.UpdateStatu()
            if self.ShowMoveInfo:
                print self.Move_Info(move_info),
                if self.SaveInfo:
                    self.SaveData(self.Move_Info(move_info))
            self.view.draw_Plateau(self.Plateau)

            if self.Plateau.Statut != 0:
                return

            move, msg = self.ai_0.Play(self.Plateau, self.Player_Side)
            self.Plateau.select(move[0][0], move[0][1], self.Player_Side)
            move_info = self.Plateau.select(move[1][0], move[1][1], self.Player_Side)
            self.view.showMsg("Tour Blanc" if self.Player_Side else "Tour Noir")
            self.Player_Side = not self.Player_Side
            self.Plateau.Round += 1
            self.Plateau.UpdateStatu()
            if self.ShowRechercheInfo:
                print msg,
                if self.SaveInfo:
                    self.SaveData(msg + " ")
            if self.ShowMoveInfo:
                print self.Move_Info(move_info),
                if self.SaveInfo:
                    self.SaveData(self.Move_Info(move_info))
            self.view.draw_Plateau(self.Plateau)

    def Game_IAvIA_Auto(self, ai_0, ai_1):
        while self.Plateau.Statut == 0:
            ai_0.Clear()
            move, msg = ai_0.Play(self.Plateau, self.Player_Side)
            self.Plateau.select(move[0][0], move[0][1], self.Player_Side)
            move_info = self.Plateau.select(move[1][0], move[1][1], self.Player_Side)
            self.view.showMsg("Tour Blanc" if self.Player_Side else "Tour Noir")
            self.Player_Side = not self.Player_Side
            self.Plateau.Round += 1
            self.Plateau.UpdateStatu()
            if self.ShowRechercheInfo:
                print msg,
                if self.SaveInfo:
                    self.SaveData(msg + " "),
            if self.ShowMoveInfo:
                print self.Move_Info(move_info),
                if self.SaveInfo:
                    self.SaveData(self.Move_Info(move_info))

            if self.Plateau.Statut != 0:
                self.SaveData("\n")
                print ""
                break

            ai_1.Clear()
            move, msg = ai_1.Play(self.Plateau, self.Player_Side)
            self.Plateau.select(move[0][0], move[0][1], self.Player_Side)
            move_info = self.Plateau.select(move[1][0], move[1][1], self.Player_Side)
            self.view.showMsg("Tour Blanc" if self.Player_Side else "Tour Noir")
            self.Player_Side = not self.Player_Side
            self.Plateau.Round += 1
            self.Plateau.UpdateStatu()
            if self.ShowRechercheInfo:
                print msg,
                if self.SaveInfo:
                    self.SaveData(msg + " ")
            if self.ShowMoveInfo:
                print self.Move_Info(move_info),
                if self.SaveInfo:
                    self.SaveData(self.Move_Info(move_info))

        print self.Plateau
        print self.Plateau.Statut
        if self.SaveInfo:
            self.SaveData(str(self.Plateau)+"\n")
            self.SaveData(str(self.Plateau.Statut) + "\n")

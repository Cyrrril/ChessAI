#Classe permettant la gestion de tous les mouvements sur le plateau de jeu, en fonction des differentes pieces
import copy
from PiecesEchecs import *

class PlateauEchecs:

    MaxRound = 300
    MidRound = 50

    def __init__(self):
            self.Pieces = dict()
            self.PieceChoisi = None
            self.Statut = 0
            self.Round = 0
            self.DernierMouvmnt = [(-1,-1), (-1,-1)]

    def __str__(self):
        info = ""
        for piece in self.Pieces.values():
                info += str(piece)
                info += " "
        return info

#On sauvegarde l'etat du plateau a l'instant t, lorsqu'une piece bouge il suffit d'utiliser le tableau copie en modifiant la position de la piece en question
    def __deepcopy__(self, memodict={}):
        newPlateau = PlateauEchecs()
        if self.PieceChoisi:
            newPlateau.PieceChoisi = self.PieceChoisi.__deepcopy__()
        newPlateau.Statut = self.Statut
        newPlateau.Round = self.Round
        newPlateau.DernierMouvmnt = self.DernierMouvmnt
        for key in self.Pieces.keys():
            newPlateau.Pieces[key] = self.Pieces[key].__deepcopy__()
            
        return newPlateau

    @staticmethod
    def Move_Info(x, y):
        table = ["a", "b", "c", "d", "e", "f", "g", "h"]
        x = int(x) % 8
        return table[x] + str(int(y) + 1)

    def MouvmntLegal(self, x, y, dx, dy):
        return self.Pieces[x, y].MouvmntLegal(self, dx, dy)

    def Move(self, x, y, dx, dy):
        self.DernierMouvmnt = [(x, y), (x + dx, y + dy)]
        return self.Pieces[x, y].Move(self, dx, dy)

    def Move_(self, position, move):
        self.DernierMouvmnt = [position, move]
        return self.Pieces[position].Move(self, move[0] - position[0], move[1] - position[1])

    def remove(self, x, y):
        del self.Pieces[x, y]

    def select(self, x, y, camp):
        if not self.PieceChoisi:
            if (x, y) in self.Pieces and self.Pieces[x, y].NoirOuBlanc == camp:
                self.Pieces[x, y].EstChoisi = True
                self.PieceChoisi = self.Pieces[x, y]
            return ""

        moves = self.PieceChoisi.Get_Move_Locs(self)

        if (x, y) in moves:
            self.MangePion_By(x, y) # avant d'appeler la fonction MangePion

        if not (x, y) in self.Pieces.keys():
            if self.PieceChoisi:
                ox, oy = self.PieceChoisi.x, self.PieceChoisi.y
                #moves = self.PieceChoisi.Get_Move_Locs(self)
                if (x, y) in moves: # self.MouvmntLegal(ox, oy, x-ox, y-oy):
                    move_info = ""
                    if self.PieceChoisi.EstRoi \
                            and self.PieceChoisi.Moved == False \
                            and self.Peut_Roque(x, y):
                        move_info = self.Roque(x, y)
                    else:
                        self.Move(ox, oy, x-ox, y-oy)
                        if self.PieceChoisi.PieceType == 5:
                            Piece_Type_Promotion = 1
                            if self.Pion_Promotion(x, y, Piece_Type_Promotion):
                                self.PieceChoisi.Name = PiecesEchecs.Get_Name(Piece_Type_Promotion)
                        if self.RoiEnEchec(not self.PieceChoisi.NoirOuBlanc):
                            move_info = self.PieceChoisi.Name + " " + PlateauEchecs.Move_Info(ox, oy) \
                                        + " + " + PlateauEchecs.Move_Info(x, y)
                        else:
                            move_info = self.PieceChoisi.Name + " " + PlateauEchecs.Move_Info(ox, oy) \
                                        + " - " + PlateauEchecs.Move_Info(x, y)
                    self.PieceChoisi.Moved = True
                    self.PieceChoisi.EstChoisi = False
                    self.PieceChoisi = None
                    return move_info
                else:
                    self.PieceChoisi = None
            return ""

        if self.Pieces[x, y].NoirOuBlanc != camp:
            ox, oy = self.PieceChoisi.x, self.PieceChoisi.y
            if (x, y) in moves:
                self.Move(ox, oy, x-ox, y-oy)
                if self.PieceChoisi.PieceType == 5:
                    Piece_Type_Promotion = 1
                    if self.Pion_Promotion(x, y, Piece_Type_Promotion):
                        self.PieceChoisi.Name = PiecesEchecs.Get_Name(Piece_Type_Promotion)
                if self.RoiEnEchec(not self.PieceChoisi.NoirOuBlanc):
                    move_info = self.PieceChoisi.Name + " " + PlateauEchecs.Move_Info(ox, oy) \
                                + " X+" + PlateauEchecs.Move_Info(x, y)
                else:
                    move_info = self.PieceChoisi.Name + " " + PlateauEchecs.Move_Info(ox, oy) \
                                + " X " + PlateauEchecs.Move_Info(x, y)
                self.PieceChoisi.Moved = True
                self.PieceChoisi.EstChoisi = False
                self.PieceChoisi = None
                return move_info
            return ""

        for key in self.Pieces.keys():
            self.Pieces[key].EstChoisi = False
        self.Pieces[x, y].EstChoisi = True
        self.PieceChoisi = self.Pieces[x,y]
        return ""

    def Select_For_IA(self, position, move):
        x, y = move[0], move[1]
        self.PieceChoisi = self.Pieces[position]
        if self.Pieces[position].EstRoi and self.PieceChoisi.Moved == False and self.Peut_Roque(x, y):
            self.Roque(x, y)
        else:
            self.MangePion_By(x, y)
            self.Move_(position, move)
            if self.PieceChoisi.PieceType == 5:
                Piece_Type_Promotion = 1
                self.Pion_Promotion(x, y, Piece_Type_Promotion)

    def Est_Impasse(self):
        if len(self.Pieces) == 2:
            return True
        elif len(self.Pieces) == 3:
            for piece in self.Pieces.values():
                if piece.PieceType == 3 or piece.PieceType == 4:
                    return True
        elif len(self.Pieces) == 4:
            i = 0
            pieces_restant = []
            for piece in self.Pieces.values():
                if piece.PieceType != 0:
                    pieces_restant.append(piece)
                    i += 1
            if pieces_restant[0].PieceType == 3 and pieces_restant[1].PieceType == 3:
                if pieces_restant[0].NoirOuBlanc != pieces_restant[1].NoirOuBlanc:
                    x0 = pieces_restant[0].x
                    y0 = pieces_restant[0].y
                    x1 = pieces_restant[1].x
                    y1 = pieces_restant[1].y
                    if (x0 + y0) % 2 == (x1 + y1) % 2:
                        return True
            return False

    def UpdateStatu(self):
        """0:Jeu; 1:blanc gagne; 2:noir gagne; 3: impasse; 4:egalite; 5:Perpetual check; """
        Succ_Compte_Blanc = Succ_Compte_Noir = 0

        if self.Est_Impasse():
            self.Statut = 4
            return

        for piece in self.Pieces.values():
            if piece.NoirOuBlanc == False:
                Succ_Compte_Blanc += len(piece.Get_Move_Locs(self))
            else:
                Succ_Compte_Noir += len(piece.Get_Move_Locs(self))

        if Succ_Compte_Blanc != 0 and Succ_Compte_Noir == 0:
            if self.RoiEnEchec(True):
                self.Statut = 1
            else:
                self.Statut = 3
        elif Succ_Compte_Noir != 0 and Succ_Compte_Blanc == 0:
            if self.RoiEnEchec(False):
                self.Statut = 2
            else:
                self.Statut = 3
        elif Succ_Compte_Noir == 0 and Succ_Compte_Blanc == 0:
            self.Statut = 3
        elif self.Round >= PlateauEchecs.MaxRound:
            self.Statut = 5

    def Attaque(self, x, y, camp):
        for piece in self.Pieces.values():
            if piece.NoirOuBlanc != camp:
                if piece.MouvmntLegal(self, x-piece.x, y-piece.y):
                    return True
        return False

    def RoiEnEchec(self, camp):
        x, y = -1, -1
        for piece in self.Pieces.values():
            if piece.EstRoi and piece.NoirOuBlanc == camp:
                x, y = piece.x, piece.y
                break
        return self.Attaque(x, y, camp)

#Verifie si les positions du Roi et de la Tour sont corrects pour effectuer un roque
    def Peut_Roque(self, x, y):
        if x == 2 and y == 0:
            if (4, 0) in self.Pieces.keys() and (0, 0) in self.Pieces.keys():
                if self.Pieces[(4, 0)].PieceType == 0 and self.Pieces[(4, 0)].Moved == False:
                    if self.Pieces[(0, 0)].PieceType == 2 and self.Pieces[(0, 0)].Moved == False:
                        for i in range(1, 5):
                            if self.Attaque(i, 0, False):
                                return False
                        return True
        elif x == 6 and y == 0:
            if (4, 0) in self.Pieces.keys() and (7, 0) in self.Pieces.keys():
                if self.Pieces[(4, 0)].PieceType == 0 and self.Pieces[(4, 0)].Moved == False:
                    if self.Pieces[(7, 0)].PieceType == 2 and self.Pieces[(7, 0)].Moved == False:
                        for i in range(4, 8):
                            if self.Attaque(i, 0, False):
                                return False
                        return True
        elif x == 2 and y == 7:
            if (4, 7) in self.Pieces.keys() and (0, 7) in self.Pieces.keys():
                if self.Pieces[(4, 7)].PieceType == 0 and self.Pieces[(4, 7)].Moved == False:
                    if self.Pieces[(0, 7)].PieceType == 2 and self.Pieces[(0, 7)].Moved == False:
                        for i in range(1, 5):
                            if self.Attaque(i, 7, True):
                                return False
                        return True
        elif x == 6 and y == 7:
            if (4, 7) in self.Pieces.keys() and (7, 7) in self.Pieces.keys():
                if self.Pieces[(4, 7)].PieceType == 0 and self.Pieces[(4, 7)].Moved == False:
                    if self.Pieces[(7, 7)].PieceType == 2 and self.Pieces[(7, 7)].Moved == False:
                        for i in range(4, 8):
                            if self.Attaque(i, 7, True):
                                return False
                        return True


#Modifie les positions du Roi et de la Tour pour effectuer un roque
    def Roque(self, x, y):
        if x == 2 and y == 0:
            self.Pieces[(4, 0)].Move(self, -2, 0)
            self.Pieces[(0, 0)].Move(self, 3, 0)
            return "0-0-0"
        elif x == 6 and y == 0:
            self.Pieces[(4, 0)].Move(self, 2, 0)
            self.Pieces[(7, 0)].Move(self, -2, 0)
            return "0-0"
        elif x == 2 and y == 7:
            self.Pieces[(4, 7)].Move(self, -2, 0)
            self.Pieces[(0, 7)].Move(self, 3, 0)
            return "0-0-0"
        elif x == 6 and y == 7:
            self.Pieces[(4, 7)].Move(self, 2, 0)
            self.Pieces[(7, 7)].Move(self, -2, 0)
            return "0-0"
        return ""


#Si un pion arrive au bout du plateau, il est "promu", on l'echange alors avec une reine, une tour, un fou ou un cavalier 
    def Pion_Promotion(self, x, y, pieceType = 1):
        if self.Pieces[(x,y)].PieceType == 5 and y == 0 or y == 7:
            camp = self.Pieces[(x,y)].NoirOuBlanc
            switch = {
                1: Reine(x, y, camp),
                2: Tour(x, y, camp),
                3: Fou(x, y, camp),
                4: Cavalier(x, y, camp),
            }
            self.Pieces[(x,y)] = switch.get(pieceType, Reine(x, y, camp))
            return True
        return False

    def MangePion_By(self, x, y):
        if self.PieceChoisi.NoirOuBlanc == False and self.PieceChoisi.PieceType == 5:
            if self.PieceChoisi.y == 4:
                if self.Pieces[self.DernierMouvmnt[1]].PieceType == 5:
                    if self.DernierMouvmnt[1][1] == 4 and self.DernierMouvmnt[0][1] == 6:
                        if x == self.DernierMouvmnt[1][0] and y == 5:
                            if abs(self.PieceChoisi.x - x) == 1:
                                self.Move_(self.DernierMouvmnt[1], (x, y))
                                return True
        elif self.PieceChoisi.NoirOuBlanc == True and self.PieceChoisi.PieceType == 5:
            if self.PieceChoisi.y == 3:
                if self.Pieces[self.DernierMouvmnt[1]].PieceType == 5:
                    if self.DernierMouvmnt[1][1] == 3 and self.DernierMouvmnt[0][1] == 1:
                        if x == self.DernierMouvmnt[1][0] and y == 2:
                            if abs(self.PieceChoisi.x - x) == 1:
                                self.Move_(self.DernierMouvmnt[1], (x, y))
                                return True
        return False

#Efface le plateau, toutes les pieces sont effaces
    def Plateau_Clear(self):
        self.Pieces.clear()

#Initialise le plateau
    def Plateau_Init(self, dis = 0):
        self.Pieces = dict()
        self.PieceChoisi = None
        self.Statut = 0
        self.Round = 0

        if dis == 0:
            self.Game_Standard()
        elif dis == 1:
            self.Game_Test_SingleTour()
        elif dis == 2:
            self.Game_Test_Eat_Pion_Pass_By()
        else:
            raise Exception("PlateauEchecs::Plateau_Init(): pas de lancement !")

    def Game_Void(self):
        pass

    #Mode de jeu standard, on place les differentes pieces de maniere classique
    def Game_Standard(self):
        self.Plateau_Clear()

        self.Pieces[(4, 0)] = Roi(4, 0, False)
        self.Pieces[(3, 0)] = Reine(3, 0, False)
        self.Pieces[(0, 0)] = Tour(0, 0, False)
        self.Pieces[(7, 0)] = Tour(7, 0, False)
        self.Pieces[(2, 0)] = Fou(2, 0, False)
        self.Pieces[(5, 0)] = Fou(5, 0, False)
        self.Pieces[(1, 0)] = Cavalier(1, 0, False)
        self.Pieces[(6, 0)] = Cavalier(6, 0, False)
        for i in range(8):      #Ligne de pions
            self.Pieces[(i, 1)] = Pion(i, 1, False)

        self.Pieces[(4, 7)] = Roi(4, 7, True)
        self.Pieces[(3, 7)] = Reine(3, 7, True)
        self.Pieces[(0, 7)] = Tour(0, 7, True)
        self.Pieces[(7, 7)] = Tour(7, 7, True)
        self.Pieces[(2, 7)] = Fou(2, 7, True)
        self.Pieces[(5, 7)] = Fou(5, 7, True)
        self.Pieces[(1, 7)] = Cavalier(1, 7, True)
        self.Pieces[(6, 7)] = Cavalier(6, 7, True)
        for i in range(8):
            self.Pieces[(i, 6)] = Pion(i, 6, True)

    def Game_Test_SingleTour(self):
        self.Plateau_Clear()

        self.Pieces[(4, 1)] = Roi(4, 1, False)
        self.Pieces[(4, 6)] = Roi(4, 6, True)
        self.Pieces[(0, 5)] = Tour(0, 5, True)
        self.Pieces[(4, 1)].Moved = True
        self.Pieces[(4, 6)].Moved = True
        self.Pieces[(0, 5)].Moved = True

    def Game_Test_Eat_Pion_Pass_By(self):
        self.Plateau_Clear()

        self.Pieces[(1, 1)] = Roi(1, 1, False)
        self.Pieces[(7, 3)] = Roi(7, 3, True)
        self.Pieces[(0, 3)] = Tour(0, 3, False)
        self.Pieces[(4, 3)] = Pion(4, 3, True)
        self.Pieces[(5, 1)] = Pion(5, 1, False)
        self.Pieces[(4, 3)].Moved = True

    def Evaluation_Materiel(self, camp):
        eva = 0
        for piece in self.Pieces.values():
            if piece.NoirOuBlanc == camp:
                eva += piece.Materiel()
            else:
                eva -= piece.Materiel()
        return eva

    def Evaluation_Position(self, camp):
        eva = 0
        for piece in self.Pieces.values():
            if piece.NoirOuBlanc == camp: # Cote du joueur humain
                if piece.NoirOuBlanc == False:
                    eva += piece.Position_Evaluation(piece.y, piece.x, self.Round, self.MidRound)
                else:
                    eva += piece.Position_Evaluation(7 - piece.y, piece.x, self.Round, self.MidRound)
            else: # Cote de l'IA
                if piece.NoirOuBlanc == False:
                    eva -= piece.Position_Evaluation(piece.y, piece.x, self.Round, self.MidRound)
                else:
                    eva -= piece.Position_Evaluation(7 - piece.y, piece.x, self.Round, self.MidRound)
        return eva

#Classe permettant de donner des valeurs aux differentes pieces pour permettre des calculs
import copy

class PiecesEchecs:

    def __init__(self, x, y, Type, camp):
            self.x = x
            self.y = y
            self.NoirOuBlanc = camp
            self.PieceType = Type
            self.EstRoi = False
            self.EstChoisi = False
            self.EstRoi = False
            self.Moved = False
            self.Name = ""

    def __str__(self):
        return ("Noir:" if self.NoirOuBlanc else "Blanc:") + PiecesEchecs.Get_Name(self.PieceType) \
               + "(" + str(self.x) + "," + str(self.y) + ")"

    def __deepcopy__(self, memodict={}):
        newPiece = PiecesEchecs(self.x, self.y, self.PieceType, self.NoirOuBlanc)
        newPiece.EstChoisi = self.EstChoisi
        newPiece.EstRoi = self.EstRoi
        newPiece.Moved = self.Moved
        return newPiece

    @staticmethod
    def Get_Name(i):
        names = ["K", "Q", "T", "F", "C", " "]      # "King" "Queen" "Tour" "Fou" "Cavalier" " " <- pion 
        return names[i]

    def MouvmntLegal(self, Plateau, dx, dy):        #Verifie si l'on peut deplacer un pion ou pas
        raise Exception("PiecesEchecs::MouvmntLegal(..) : Commande errone.")

    def Get_Move_Locs(self, Plateau):  
        moves = []
        for x in xrange(8):         #on parcourt tout le plateau
            for y in xrange(8):
                if (x,y) in Plateau.Pieces and Plateau.Pieces[x,y].NoirOuBlanc == self.NoirOuBlanc:
                    continue
                if self.MouvmntLegal(Plateau, x-self.x, y-self.y):
                    piece_copy = self.__deepcopy__()
                    Plateau_copy = Plateau.__deepcopy__()           #on realise une copie du plateau avant d'effectuer toutes modifications sur ce dernier
                    Plateau_copy.PieceChoisi = piece_copy
                    Plateau_copy.MangePion_By(x, y)
                    piece_copy.Move(Plateau_copy, x-self.x, y-self.y)
                    if Plateau_copy.RoiEnEchec(piece_copy.NoirOuBlanc) == False:
                        EstRoquePosition = (x == 2 and y == 0) \
                                             or (x == 6 and y == 0) \
                                             or (x == 2 and y == 7) \
                                             or (x == 6 and y == 7)
                        if self.EstRoi \
                                and self.Moved == False \
                                and EstRoquePosition \
                                and Plateau.Peut_Roque(x, y) == False:
                            continue
                        else:
                            moves.append((x, y))
        return moves

    def Move(self, Plateau, dx, dy):         #Fonction pour deplacer un pion et le retirer de sa position precedente
        nx, ny = self.x + dx, self.y + dy
        if (nx, ny) in Plateau.Pieces:
            Plateau.remove(nx, ny)
        Plateau.remove(self.x, self.y)
        
        self.x += dx
        self.y += dy
        Plateau.Pieces[self.x, self.y] = self
        return True

    def Compte_Pieces_Entre(self, Plateau, x, y, dx, dy):       #compte le nombre de pieces qu'il y a autour d'une piece situe en (x,y)
        sx = dx/abs(dx) if dx!=0 else 0
        sy = dy/abs(dy) if dy!=0 else 0
        nx, ny = x + dx, y + dy
        x, y = x + sx, y + sy
        cnt = 0
        while x != nx or y != ny:
            if (x, y) in Plateau.Pieces:
                cnt += 1
            x += sx
            y += sy
        return cnt

    def Materiel(self):
            raise Exception("PiecesEchecs::Materiel() : Commande errone.")

    def Position_Evaluation(self, x, y, Round, mid = 100):
            raise Exception("PiecesEchecs::Position_Evaluation(..) : Commande errone.")

class Roi(PiecesEchecs):

    Value_Materiel = 20000

    Piece_Position_Eva_0 = [                #On donne des valeurs pour les differentes positions sur le plateau pour le roi
            [20, 50, 10,  0,  0, 10, 50, 20],
            [20, 20,  0,  0,  0,  0, 20, 20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30]
    ]

    Piece_Position_Eva_1 = [
            [-50,-40,-30,-20,-20,-30,-40,-50],
            [-30,-30,  0,  0,  0,  0,-30,-30],
            [-30,-10, 20, 30, 30, 20,-10,-30],
            [-30,-10, 30, 40, 40, 30,-10,-30],
            [-30,-10, 30, 40, 40, 30,-10,-30],
            [-30,-10, 20, 30, 30, 20,-10,-30],
            [-30,-20,-10,  0,  0,-10,-20,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30]
    ]

    def __init__(self, x, y, camp):
        PiecesEchecs.__init__(self, x, y, 0, camp)
        self.EstRoi = True
        self.Name = "K"     #King (Roi)

    def __deepcopy__(self, memodict={}):
        newPiece = Roi(self.x, self.y, self.NoirOuBlanc)
        newPiece.EstChoisi = self.EstChoisi
        newPiece.EstRoi = self.EstRoi
        newPiece.Moved = self.Moved
        newPiece.Name = self.Name
        return newPiece

    def get_image_file_name(self):
        if self.EstChoisi:
            if self.NoirOuBlanc:
                return "images/NoirRoi.gif"
            else:
                return "images/BlancRoi.gif"
        else:
            if self.NoirOuBlanc:
                return "images/NoirRoi.gif"
            else:
                return "images/BlancRoi.gif"

    def MouvmntLegal(self, Plateau, dx, dy):        #verifie si le roi peut bien effectuer le mouvement voulu par l'utilisateur
        if self.Moved == False:
            if self.NoirOuBlanc == False and self.x == 4 and self.y == 0:
                if dx == 2 and dy == 0:
                    if self.Compte_Pieces_Entre(Plateau, 4, 0, 3, 0) == 0:
                        return True
                elif dx == -2 and dy == 0:
                    if self.Compte_Pieces_Entre(Plateau, 4, 0, -4, 0) == 0:
                        return True
            elif self.NoirOuBlanc == True and self.x == 4 and self.y == 7:
                if dx == 2 and dy == 0:
                    if self.Compte_Pieces_Entre(Plateau, 4, 7, 3, 0) == 0:
                        return True
                elif dx == -2 and dy == 0:
                    if self.Compte_Pieces_Entre(Plateau, 4, 7, -4, 0) == 0:
                        return True
        if dx>1 or dy>1 or dx<-1 or dy<-1:
            return False
        return True

    def Materiel(self):
        return Roi.Value_Materiel

    

class Reine(PiecesEchecs):

    Value_Materiel = 925

    Piece_Position_Eva_0 = [                #On donne des valeurs pour les differentes positions sur le plateau pour la reine
            [-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [0,  0,  5,  5,  5,  5,  0, -5],
            [-5,  0,  5,  5,  5,  5,  0, -5],
            [-10,  0,  5,  5,  5,  5,  0,-10],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20]
    ]

    Piece_Position_Eva_1 = [
            [-20, -10, -10, -5, -5, -10, -10, -20],
            [-10, 0, 5, 0, 0, 0, 0, -10],
            [-10, 5, 5, 5, 5, 5, 0, -10],
            [0, 0, 5, 5, 5, 5, 0, -5],
            [-5, 0, 5, 5, 5, 5, 0, -5],
            [-10, 0, 5, 5, 5, 5, 0, -10],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-20, -10, -10, -5, -5, -10, -10, -20]
    ]

    def __init__(self, x, y, camp):
        PiecesEchecs.__init__(self, x, y, 1, camp)
        self.Name = "Q"     #Queen (Reine)

    def __deepcopy__(self, memodict={}):
        newPiece = Reine(self.x, self.y, self.NoirOuBlanc)
        newPiece.EstChoisi = self.EstChoisi
        newPiece.EstRoi = self.EstRoi
        newPiece.Moved = self.Moved
        newPiece.Name = self.Name
        return newPiece

    def get_image_file_name(self):
        if self.EstChoisi:
            if self.NoirOuBlanc:
                return "images/NoirReine.gif"
            else:
                return "images/BlancReine.gif"
        else:
            if self.NoirOuBlanc:
                return "images/NoirReine.gif"
            else:
                return "images/BlancReine.gif"

    def MouvmntLegal(self, Plateau, dx, dy):        #verifie si la reine peut bien effectuer le mouvement voulu par l'utilisateur
        if dx!=dy and dx!=-dy and dx!=0 and dy!=0:
            return False
        cnt = self.Compte_Pieces_Entre(Plateau, self.x, self.y, dx, dy)
        if cnt != 0:
            return False
        return True

    def Materiel(self):
        return Reine.Value_Materiel

    
class Tour(PiecesEchecs):

    Value_Materiel = 500

    Piece_Position_Eva_0 = [            #On donne des valeurs pour les differentes positions sur le plateau pour la tour
            [0,  0,  0,  5,  5,  0,  0,  0],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [5, 10, 10, 10, 10, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]
    ]

    Piece_Position_Eva_1 = [
            [0, 0, 0, 5, 5, 0, 0, 0],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [5, 10, 10, 10, 10, 10, 10, 5],
            [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    def __init__(self, x, y, camp):
        PiecesEchecs.__init__(self, x, y, 2, camp)
        self.Name = "T"     #Tour

    def __deepcopy__(self, memodict={}):
        newPiece = Tour(self.x, self.y, self.NoirOuBlanc)
        newPiece.EstChoisi = self.EstChoisi
        newPiece.EstRoi = self.EstRoi
        newPiece.Moved = self.Moved
        newPiece.Name = self.Name
        return newPiece

    def get_image_file_name(self):
        if self.EstChoisi:
            if self.NoirOuBlanc:
                return "images/NoirTour.gif"
            else:
                return "images/BlancTour.gif"
        else:
            if self.NoirOuBlanc:
                return "images/NoirTour.gif"
            else:
                return "images/BlancTour.gif"

    def MouvmntLegal(self, Plateau, dx, dy):        #verifie si la tour peut bien effectuer le mouvement voulu par l'utilisateur
        if (dx != 0) and (dy != 0):
            return False
        cnt = self.Compte_Pieces_Entre(Plateau, self.x, self.y, dx, dy)
        if cnt != 0:
            return False
        return True

    def Materiel(self):
        return Tour.Value_Materiel

  

class Fou(PiecesEchecs):

    Value_Materiel = 325

    Piece_Position_Eva_0 = [            #On donne des valeurs pour les differentes positions sur le plateau pour le fou
            [-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  5,  0,  0,  0,  0,  5,-10],
            [-10, 10, 10, 10, 10, 10, 10,-10],
            [-10,  0, 10, 10, 10, 10,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]
    ]

    Piece_Position_Eva_1 = [
            [-20, -10, -10, -10, -10, -10, -10, -20],
            [-10, 5, 0, 0, 0, 0, 5, -10],
            [-10, 10, 10, 10, 10, 10, 10, -10],
            [-10, 0, 10, 10, 10, 10, 0, -10],
            [-10, 5, 5, 10, 10, 5, 5, -10],
            [-10, 0, 5, 10, 10, 5, 0, -10],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20]
    ]

    def __init__(self, x, y, camp):
        PiecesEchecs.__init__(self, x, y, 3, camp)
        self.Name = "F"     #Fou

    def __deepcopy__(self, memodict={}):
        newPiece = Fou(self.x, self.y, self.NoirOuBlanc)
        newPiece.EstChoisi = self.EstChoisi
        newPiece.EstRoi = self.EstRoi
        newPiece.Moved = self.Moved
        newPiece.Name = self.Name
        return newPiece

    def get_image_file_name(self):
        if self.EstChoisi:
            if self.NoirOuBlanc:
                return "images/NoirFou.gif"
            else:
                return "images/BlancFou.gif"
        else:
            if self.NoirOuBlanc:
                return "images/NoirFou.gif"
            else:
                return "images/BlancFou.gif"

    def MouvmntLegal(self, Plateau, dx, dy):        #verifie si le fou peut bien effectuer le mouvement voulu par l'utilisateur
        if dx!=dy and dx!=-dy:
            return False
        cnt = self.Compte_Pieces_Entre(Plateau, self.x, self.y, dx, dy)
        if cnt != 0:
            return False
        return True

    def Materiel(self):
        return Fou.Value_Materiel

    

class Cavalier(PiecesEchecs):

    Value_Materiel = 300

    Piece_Position_Eva_0 = [            #On donne des valeurs pour les differentes positions sur le plateau pour le cavalier
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
    ]

    Piece_Position_Eva_1 = [
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20, 0, 5, 5, 0, -20, -40],
            [-30, 5, 10, 15, 15, 10, 5, -30],
            [-30, 0, 15, 20, 20, 15, 0, -30],
            [-30, 5, 15, 20, 20, 15, 5, -30],
            [-30, 0, 10, 15, 15, 10, 0, -30],
            [-40, -20, 0, 0, 0, 0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50]
    ]

    def __init__(self, x, y, camp):
        PiecesEchecs.__init__(self, x, y, 4, camp)
        self.Name = "C"     #Cavalier

    def __deepcopy__(self, memodict={}):
        newPiece = Cavalier(self.x, self.y, self.NoirOuBlanc)
        newPiece.EstChoisi = self.EstChoisi
        newPiece.EstRoi = self.EstRoi
        newPiece.Moved = self.Moved
        newPiece.Name = self.Name
        return newPiece

    def get_image_file_name(self):
        if self.EstChoisi:
            if self.NoirOuBlanc:
                return "images/NoirCavalier.gif"
            else:
                return "images/BlancCavalier.gif"
        else:
            if self.NoirOuBlanc:
                return "images/NoirCavalier.gif"
            else:
                return "images/BlancCavalier.gif"

    def MouvmntLegal(self, Plateau, dx, dy):        #verifie si le cavalier peut bien effectuer le mouvement voulu par l'utilisateur
        if abs(dx) == 1 and abs(dy) == 2:
            return True
        elif abs(dx) == 2 and abs(dy) == 1:
            return True
        return False

    def Materiel(self):
        return Cavalier.Value_Materiel

    
class Pion(PiecesEchecs):

    Value_Materiel = 100

    Piece_Position_Eva_0 = [        #On donne des valeurs pour les differentes positions sur le plateau pour le pion
            [0, 0, 0, 0, 0, 0, 0, 0],
            [5, 10, 10, -20, -20, 10, 10, 5],
            [5, -5, -10, 0, 0, -10, -5, 5],
            [0, 0, 0, 20, 20, 0, 0, 0],
            [5, 5, 10, 25, 25, 10, 5, 5],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [900, 900, 900, 900, 900, 900, 900, 900]
    ]

    Piece_Position_Eva_1 = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [5, 10, 10, -20, -20, 10, 10, 5],
            [5, -5, -10, 0, 0, -10, -5, 5],
            [0, 0, 0, 20, 20, 0, 0, 0],
            [5, 5, 10, 25, 25, 10, 5, 5],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [900, 900, 900, 900, 900, 900, 900, 900]
    ]

    def __init__(self, x, y, camp):
        PiecesEchecs.__init__(self, x, y, 5, camp)
        self.Name = " " #On a defini un tableau nom, " " correspond aux pions

    def __deepcopy__(self, memodict={}):
        newPiece = Pion(self.x, self.y, self.NoirOuBlanc)
        newPiece.EstChoisi = self.EstChoisi
        newPiece.EstRoi = self.EstRoi
        newPiece.Moved = self.Moved
        newPiece.Name = self.Name
        return newPiece

    def get_image_file_name(self):
        if self.EstChoisi:
            if self.NoirOuBlanc:
                return "images/NoirPion.gif"
            else:
                return "images/BlancPion.gif"
        else:
            if self.NoirOuBlanc:
                return "images/NoirPion.gif"
            else:
                return "images/BlancPion.gif"

    def MouvmntLegal(self, Plateau, dx, dy):        #verifie si le pion peut bien effectuer le mouvement voulu par l'utilisateur
        if self.NoirOuBlanc == False:
            if dy == 1 and dx == 0:
                if not (self.x + dx, self.y + dy) in Plateau.Pieces.keys():
                    return True
            if dy == 1 and abs(dx) == 1:
                if (self.x + dx, self.y + dy) in Plateau.Pieces.keys():
                    return True
                elif self.y == 4:
                    if Plateau.Pieces[Plateau.DernierMouvmnt[1]].PieceType == 5:
                        if Plateau.DernierMouvmnt[1][1] == 4 and Plateau.DernierMouvmnt[0][1] == 6:
                            if Plateau.DernierMouvmnt[1][0] == self.x + dx:
                                return True
            if self.Moved == False and dy == 2 and dx == 0:
                if not (self.x + dx, self.y + dy) in Plateau.Pieces.keys():
                    cnt = self.Compte_Pieces_Entre(Plateau, self.x, self.y, dx, dy)
                    if cnt == 0:
                        return True
        else:
            if dy == -1 and dx == 0:
                if not (self.x + dx, self.y + dy) in Plateau.Pieces.keys():
                    return True
            if dy == -1 and abs(dx) == 1:
                if (self.x + dx, self.y + dy) in Plateau.Pieces.keys():
                    return True
                elif self.y == 3:
                    if Plateau.Pieces[Plateau.DernierMouvmnt[1]].PieceType == 5:
                        if Plateau.DernierMouvmnt[1][1] == 3 and Plateau.DernierMouvmnt[0][1] == 1:
                            if Plateau.DernierMouvmnt[1][0] == self.x + dx:
                                return True
            if self.Moved == False and dy == -2 and dx == 0:
                if not (self.x + dx, self.y + dy) in Plateau.Pieces.keys():
                    cnt = self.Compte_Pieces_Entre(Plateau, self.x, self.y, dx, dy)
                    if cnt == 0:
                        return True
        return False

    def Materiel(self):
        return Pion.Value_Materiel


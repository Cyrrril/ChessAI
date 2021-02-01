#Classe permettant la gestion de l'IA
import random, Queue, threading

class noeud:

    def __init__(self, v = 0, pere = None):
        self.value = v
        self.profondeur = 0
        self.pere = pere
        self.enfants = []

    def EstFeuille(self):       #Feuille correspond aux noeuds qui n'ont pas d'enfants
        if self is not None and len(self.enfants) == 0:
            return True
        else:
            return False

    def Getprofondeur(self):
        if self is not None:
            return self.profondeur
        else:
            return -1

    def Add_enfant(self, noeud):    #ajouter un enfant a un noeud 
        if self is not None:
            if noeud is not None:
                noeud.Update_profondeur()
                self.enfants.append(noeud)
                return True
            else:
                return False
        else:
            raise Exception("noeud: Add_enfant(..): reference null ")

    def Del_enfants(self):      #supprimer des enfants d'un noeud
        if self is not None:
            if self.EstFeuille() == False:
                for noeud in self.enfants:
                    noeud.Del_enfants()
                self.enfants = []
                return True
            else:
                return False
        else:
            raise Exception("noeud: Add_enfant(..): reference null ")

    def Compte_noeuds(self):
        if self is not None:
            if self.EstFeuille() == True:
                return 0
            else:
                Compte = len(self.enfants)
                for noeud in self.enfants:
                    Compte += noeud.Compte_noeuds()
                return Compte
        else:
            return -1

    def Set_pere(self, noeud):
        if self is not None:
            self.pere = noeud
            self.Update_profondeur()
            return True
        else:
            raise Exception("noeud: Add_enfant(..): reference null ")

    def Update_profondeur(self):
        self.profondeur = self.pere.Getprofondeur() + 1
        if self.EstFeuille() is False:
            for noeud in self.enfants:
                noeud.Update_profondeur()

class MinMaxnoeud(noeud):

    def __init__(self, v = 0, type = True, info = None, pere = None):
        noeud.__init__(self, v, pere)
        self.type = type
        self.info = info

    def GetValue(self, a, b):
        if self.EstFeuille() == True:
            return self.value
        elif self.type == True:
            return self.GetMax(a, b)
        else:
            return self.GetMin(a, b)

    def GetMax(self, a, b):     #avoir la valeur minimale
        v = -999999
        for noeud in self.enfants:
            v = max(v, noeud.GetValue(a, b))
            if v >= b:
                self.value = v
                return v
            a = max(a, v)
        self.value = v
        return v

    def GetMin(self, a, b):     #avoir la valeur maximale
        v = 999999
        for noeud in self.enfants:
            v = min(v, noeud.GetValue(a, b))
            if v <= a:
                self.value = v
                return v
            b = min(b, v)
        self.value = v
        return v

class IA:

    def __str__(self):
        raise Exception("IA::__str__() : Commande errone.")

    def Clear(self):
        raise Exception("IA::Clear() : Commande errone.")

    def Play(self, Plateau, camp):
        raise Exception("IA::Play(..) : Commande errone.")

class RandomMoveIA(IA):

    def __str__(self):
        return "RandomMove"

    def Clear(self):
        pass

    def Play(self, Plateau, camp):
        move = []
        pieces = [piece for piece in Plateau.Pieces.values()]
        random.shuffle(pieces)
        for piece in pieces:
            if piece.NoirOuBlanc == camp:
                succ = piece.Get_Move_Locs(Plateau)
                if len(succ) != 0:
                    move.append((piece.x, piece.y))
                    move.append(random.choice(succ))
                    break
        return move

class MinMaxRechercheIA(IA):

    Infinity = 999999

    def __init__(self, limit, use_Materiel = True, use_position = True):
        self.racine = MinMaxnoeud()
        self.profondeurLimit = limit
        self.Camp = True
        self.Use_Materiel_Balance = use_Materiel
        self.Use_Position_Evaluation = use_position
        self.Thread_Result = Queue.Queue()

    def __str__(self):
        msg = "MinMaxRecherche"
        msg += " - " + "Max Recherche profondeur: " + str(self.profondeurLimit)
        msg += " - " + "Use Position Evaluation: " + str(self.Use_Position_Evaluation)
        return msg

    def Clear(self):
        self.racine.Del_enfants()

    def Play_Thread(self, Plateau, camp):
        eva = self.Expand(self.racine, Plateau, camp, 0, -self.Infinity, self.Infinity)
        self.Thread_Result.put(eva)

    def Play(self, Plateau, camp):
        self.Camp = camp
        self.racine.type = True
        self.racine.Del_enfants()
        choice = ((-1, -1), (-1, -1))
        choices = []

        thr = threading.Thread(target=self.Play_Thread, name='thread_ai', args=(Plateau, camp))
        thr.setDaemon(True)
        thr.start()
        thr.join()

        eva = self.Thread_Result.get()
        Compte = self.racine.Compte_noeuds()
        Msg = "noeuds: " + str(Compte) + " Eva: " + str(eva)

        for enfant in self.racine.enfants:
            if enfant.value == eva:
                choices.append(enfant.info)
        random.shuffle(choices)
        if len(choices) != 0:
            choice = choices[0]

        return choice, Msg

    def Expand(self, noeud, Plateau, camp, profondeur, a, b):
        if profondeur >= self.profondeurLimit:
            return noeud.value
        elif noeud.type: # MAX
            return self.Expand_Max(noeud, Plateau, camp, profondeur, a, b)
        else:
            return self.Expand_Min(noeud, Plateau, camp, profondeur, a, b)

    def Expand_Max(self, noeud, Plateau, camp, profondeur, a, b):
        v = -self.Infinity
        position_move = []
        for position in Plateau.Pieces.keys():
            if Plateau.Pieces[position].NoirOuBlanc == camp:
                moves = Plateau.Pieces[position].Get_Move_Locs(Plateau)
                for move in moves:
                    position_move.append((position, move))
        random.shuffle(position_move)
        for move in position_move:
            Plateau_futur = Plateau.__deepcopy__()
            Plateau_futur.Select_For_IA(move[0], move[1])
            eva = 0
            if profondeur + 1 >= self.profondeurLimit:
                if self.Use_Materiel_Balance:
                    eva += Plateau_futur.Evaluation_Materiel(self.Camp)
                if self.Use_Position_Evaluation:
                    eva += Plateau_futur.Evaluation_Position(self.Camp)
            newnoeud = MinMaxnoeud(eva, not noeud.type, move, noeud)
            v = max(v, self.Expand(newnoeud, Plateau_futur, not camp, profondeur + 1, a, b))

            # La valeur doit etre plus grande que le bord superieur sinon il y a un risque d'erreurs 
            if v > b:
                noeud.value = v
                noeud.Add_enfant(newnoeud)
                return v
            a = max(a, v)
            
            noeud.Add_enfant(newnoeud)
        if noeud.EstFeuille():
            if not Plateau.RoiEnEchec(camp):
                v = 0
        noeud.value = v
        return v

    def Expand_Min(self, noeud, Plateau, camp, profondeur, a, b):
        v = self.Infinity
        position_move = []
        for position in Plateau.Pieces.keys():
            if Plateau.Pieces[position].NoirOuBlanc == camp:
                moves = Plateau.Pieces[position].Get_Move_Locs(Plateau)
                for move in moves:
                    position_move.append((position, move))
        random.shuffle(position_move)
        for move in position_move:
            Plateau_futur = Plateau.__deepcopy__()
            Plateau_futur.Select_For_IA(move[0], move[1])
            eva = 0
            if profondeur + 1 >= self.profondeurLimit:
                if self.Use_Materiel_Balance:
                    eva += Plateau_futur.Evaluation_Materiel(self.Camp)
                if self.Use_Position_Evaluation:
                    eva += Plateau_futur.Evaluation_Position(self.Camp)
            newnoeud = MinMaxnoeud(eva, not noeud.type, move, noeud)
            v = min(v, self.Expand(newnoeud, Plateau_futur, not camp, profondeur + 1, a, b))

             # La valeur doit etre plus grande que le bord superieur sinon il y a un risque d'erreurs 
            if v < a:
                noeud.value = v
                noeud.Add_enfant(newnoeud)
                return v
            b = min(b, v)
            # ----------
            noeud.Add_enfant(newnoeud)
        if noeud.EstFeuille():
            if not Plateau.RoiEnEchec(camp):
                v = 0
        noeud.value = v
        return v

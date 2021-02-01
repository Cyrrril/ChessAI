#Classe permettant de gerer l'interface graphique

import Tkinter          #bibliotheque pour l'interface graphique

def Plateau_coord(x):
    return 100 * x + 50

class GraphEchecs:
    racine = Tkinter.Tk()
    racine.title("Chess")
    racine.resizable(0, 0)
    can = Tkinter.Canvas(racine, width=800, height=800)
    can.pack(expand=Tkinter.YES, fill=Tkinter.BOTH)
    img = Tkinter.PhotoImage(file="images/PlateauEchecs.gif")
    can.create_image(0, 0, image=img, anchor=Tkinter.NW)
    piece_images = dict()
    move_images = []

    def draw_Plateau(self, Plateau):  #Fonction permettant de modifier la position des pions dans l'interface graphique
        self.piece_images.clear()
        self.move_images = []
        pieces = Plateau.Pieces
        for (x, y) in pieces.keys():
            self.piece_images[x, y] = Tkinter.PhotoImage(file=pieces[x, y].get_image_file_name())
            self.can.create_image(Plateau_coord(x), Plateau_coord(7-y), image=self.piece_images[x, y])
        if Plateau.PieceChoisi:
            self.move_images.append(Tkinter.PhotoImage(file="images/select.gif"))
            self.can.create_image(Plateau_coord(Plateau.PieceChoisi.x), Plateau_coord(7 - Plateau.PieceChoisi.y), image=self.move_images[-1])
            for (x, y) in Plateau.PieceChoisi.Get_Move_Locs(Plateau):
                self.move_images.append(Tkinter.PhotoImage(file="images/select.gif"))
                self.can.create_image(Plateau_coord(x), Plateau_coord(7-y), image=self.move_images[-1])

    def showMsg(self, msg):
        self.racine.title(msg)   

    def __init__(self, control):
        self.control = control
        self.can.bind('<Button-1>', self.control.callback)

    def start(self):         #Lance la fenetre de jeu et la garde ouverte tant qu'elle n'a pas ete ferme
        Tkinter.mainloop()

from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import * 
import cv2
import sys
import numpy as np
import math
import json


class Window2(QMainWindow):
    def __init__(self, parent=None, average_waiting=0 ):
        super().__init__(parent)
        self.setWindowTitle("FCFS")
        #self.setWindowIcon(QtGui.QIcon("download.jpg"))
        self.setGeometry(200,50,1150,900)
        self.setFixedSize(1150,900)
        self.home()
        self.show()
    def refresh(self):
        
        d = int(self.dimension.text())
        nbf =int(self.nb_canaux.text())
        t =float( self.tauxinter.text())
        tch = float(self.chevauch.text())
        dab = int(self.densite.text())
        c = 9
        ps = int(self.recevable.text())
        p=100-int(ps)
        nbcanauxparcellule = (nbf/c )* 8
        

        d1 = p* 200
        d2 = 1800000/(400-(6*tch)-(100*t))
        d3 = 2*math.sqrt((nbcanauxparcellule*1000000)/(math.pi*dab))
        r = 0
        if(d3<d2):
            r = d3
        else:
            if(d3>d1):
                r = d1
            else:
                r = d3
        self.rayon.setText(str(r))
        self.distance1.setText(str(d1))
        self.distance2.setText(str(d2))
        self.distance3.setText(str(d3))
        self.distancefinal.setText(str(r))
        self.station.setText(str(self.nombre(d,r,tch)))
        #debut de la phase de dessin
        #on creer une image blanche avec la taille de la dimension
        img3 = np.zeros([int(d/50),int(d/50),3],dtype=np.uint8)
        img3.fill(255)
        #c'est la position ou commence le premier cercle
        vertical=int(r/50)
        diametre=int((r*2)/50)
        while ((vertical+(r/50))<=int(d/50)):
            center = int(r/50)
            while((center+(r/50))<=int(d/50)):
                #c'est le coordonnee du centre
                center_coordinates = (center, vertical)
                #c'est le rayon
                radius = int(r/50)
                #couleur du cercle
                color = (255,255,0)
                #pour afficher le contour
                thickness = 2
                #dessin du cercle
                img3 = cv2.circle(img3, center_coordinates, radius, color, thickness)
                #on va ecrire un chiffre au milieu du cercle
                font=cv2.FONT_HERSHEY_SIMPLEX
                fontScale=0.5
                #la couleur du chiffre
                color1=(2555,0,0)
                #coordonnee du chiffre
                text_coordinates=(center-6,vertical+2)
                #on ecrit le chiffre
                img3=cv2.putText(img3,'X',text_coordinates,font,fontScale,color1,thickness,cv2.LINE_AA)
                center=center+int(diametre-((diametre*tch)))
            vertical=vertical+int(diametre-((diametre*tch)))
    
     
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
       
        self.image1 = img3
        self.image1 = QImage(self.image1.data, self.image1.shape[1], self.image1.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.image_frame.setPixmap(QPixmap.fromImage(self.image1))
        self.scroll.setWidget(self.image_frame)
        
        #sauvegarde des parametres
        f = open('settings.json',)
        i = json.load(f)
        # Closing file
        f.close()
        i["ri"]=r
        i["d"]=d
        i["nbf"]=nbf
        i["t"]=t
        i["tch"]=tch
        i["dab"]=dab
        i["ps"]=ps
        a_file=open("settings.json","w")
        json.dump(i,a_file)
        a_file.close
        
        
    
    def nombre(self,dimension,rayon,chevau):
        diametre=rayon*2
        longueur=0
        nb=0
        while((longueur+diametre)<=dimension) :
            longueur=longueur+(diametre-((diametre*chevau)))
            nb=nb+1
        return nb*nb
    def home(self):
        f = open('settings.json',)
        i = json.load(f)
       
        # Closing file
        f.close()
        #ri est le rayon initial
        ri= i["ri"] 
        #d est la dimension de la zone
        d = i["d"]
        #nbf est le nombre de frequence
        nbf= i["nbf"]
        #t est le taux d'interference
        t = i["t"]
        #tch est le taux de chevauchement
        tch = i["tch"]
        #dab est la densite d'habitant
        dab = i["dab"]
        #C est le nombre de cellule par motif
        C = 9
        #ps est la puissance du signal pour qu'elle soit recevable
        ps= i["ps"]
        p=100-ps
        
        self.label1=QLabel(self)
        self.label1.setText("Rayon_Init")
        self.label1.move(10,0) #col ,row
        self.rayon=QLineEdit(self)
        self.rayon.move(100,0)
        self.rayon.setFixedWidth(150)
        #on bloque le rayon initial car elle est calculer a chaque fois
        self.rayon.setEnabled(False)
        self.rayon.setText(str(ri))
        self.label3=QLabel(self)
        self.label3.setText("Dimension")
        self.label3.move(10,50)
        self.label4=QLabel(self)
        self.label4.setText("NB_Canaux")
        self.label4.move(10,100)
        self.label5=QLabel(self)
        self.label5.setText("Taux_Interf")
        self.label5.move(10,150)
        self.dimension=QLineEdit(self)
        self.dimension.setFixedWidth(150)
        self.dimension.move(100,50)
        self.dimension.resize(1400,30)
        #vue que je sais faire le zoom, j'ai ficher la taille de la dimension par defaut
        self.dimension.setEnabled(False)
        self.dimension.setText(str(d))
        self.nb_canaux=QLineEdit(self)
        self.nb_canaux.setFixedWidth(150)
        self.nb_canaux.move(100,100)
        self.nb_canaux.resize(1400,30)
        self.nb_canaux.setText(str(nbf))
        self.tauxinter=QLineEdit(self)
        self.tauxinter.setFixedWidth(150)
        self.tauxinter.move(100 ,150)
        self.tauxinter.resize(1400,30)
        self.tauxinter.setText(str(t))
        #self.textEdit=QTextEdit(self)
        #self.textEdit.move(20,250)
        self.label6 = QLabel(self)
        self.distance1 = QLabel(self)
        self.label8 = QLabel(self)
        self.label9 = QLabel(self)
        self.label10 = QLabel(self)
        self.label8.setText("Taux_Chevau")
        self.label8.move(10,200)
        self.chevauch=QLineEdit(self)
        self.chevauch.setFixedWidth(150)
        self.chevauch.move(100,200)
        self.chevauch.resize(1400,30)
        self.chevauch.setText(str(tch))
        self.label9.setText("Densité")
        self.label9.move(10,250)
        self.densite=QLineEdit(self)
        self.densite.setFixedWidth(150)
        self.densite.move(100,250)
        self.densite.resize(1400,30)
        self.densite.setText(str(dab))
        self.label10 = QLabel(self)
        self.label10.setText("Puiss_Receva")
        self.label10.move(10,300)
        self.recevable=QLineEdit(self)
        self.recevable.setFixedWidth(150)
        self.recevable.move(100,300)
        self.recevable.resize(1400,30)
        self.recevable.setText(str(ps))
        self.button=QPushButton("Actualiser Parametre",self)
        self.button.move(50,350)
        self.button.setFixedWidth(200)
        self.button.clicked.connect(self.refresh)
#        self.label6.setText("Waiting Time=", self.average_waiting)
        
        self.label10 = QLabel(self)
        self.label10.setFont(QFont('Arial',18))
        self.label10.setFixedWidth(150)
        self.label10.setText("Resultats")
        self.label10.move(60,450)
      
        self.label6.setText("Rayon D1 : " )  # +++
        self.label6.move(10,500)
        self.distance1.move(100,500)
        self.label11 = QLabel(self)
        self.label11.move(10,550)
        self.label11.setText("Rayon D2 : " )
        self.distance2 = QLabel(self)
        self.distance2.move(100,550)
        self.label12 = QLabel(self)
        self.label12.move(10,600)
        self.label12.setText("Rayon D3 : " )
        self.distance3= QLabel(self)
        self.distance3.move(100,600)
        self.label13 = QLabel(self)
        self.label13.move(10,650)
        self.label13.setText("Rayon Final : " )
        self.distancefinal = QLabel(self)
        self.distancefinal.move(100,650)
        #ici on affiche le rayon initial
        self.distancefinal.setText(str(ri))
        self.label14 = QLabel(self)
        self.label14.move(10,700)
        self.label14.setText("Nb _Station :" )
        self.station = QLabel(self)
        self.station.move(100,700)
        #ici on affiche le nombre de station en divisant la dimension par le rayon initial
        self.station.setText(str(self.nombre(d,ri,tch)))
        #debut de la phase de dessin
        #on creer une image blanche avec la taille de la dimension
        img2 = np.zeros([int(d/50),int(d/50),3],dtype=np.uint8)
        img2.fill(255)
        #c'est la position ou commence le premier cercle
        vertical=int(ri/50)
        diametre=int(ri/25)
        while ((vertical+(ri/50))<=(d/50)):
            center = int(ri/50)
            while((center+(ri/50))<=(d/50)):
                #c'est le coordonnee du centre
                center_coordinates = (center, vertical)
                #c'est le rayon
                radius = int(ri/50)
                #couleur du cercle
                color = (255,255,0)
                #pour afficher le contour
                thickness = 2
                #dessin du cercle
                img2 = cv2.circle(img2, center_coordinates, radius, color, thickness)
                #on va ecrire un chiffre au milieu du cercle
                font=cv2.FONT_HERSHEY_SIMPLEX
                fontScale=0.5
                #la couleur du chiffre
                color1=(2555,0,0)
                #coordonnee du chiffre
                text_coordinates=(center-6,vertical+2)
                #on ecrit le chiffre
                img2=cv2.putText(img2,'X',text_coordinates,font,fontScale,color1,thickness,cv2.LINE_AA)
                center=center+int(diametre-((diametre*tch)))
            vertical=vertical+int(diametre-((diametre*tch)))
        self.label15 = QLabel(self)
        self.label15.move(600,25)
        self.label15.setText("Echelle 50 % et motif de 9" )
        self.label15.setFixedWidth(250)
        self.image_frame = QLabel(self)
        self.scroll = QScrollArea(self)  
        self.scroll.move(300,50)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedSize(800,800)
       
        self.image = img2
        self.image = QImage(self.image.data, self.image.shape[1], self.image.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.image_frame.setPixmap(QPixmap.fromImage(self.image))
        self.scroll.setWidget( self.image_frame)
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)        
    form = Window2()
    form.show()
    sys.exit(app.exec_())
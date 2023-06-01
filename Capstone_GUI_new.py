from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import QRegularExpression, Qt
import sys
from SingleImageDetector_V4 import Detectron_Detector
import numpy as np
class Ui_MainWindow(QMainWindow):
    
    def setupUi(self, MainWindow):
        #Define the screen size
        screen = QApplication.primaryScreen() #Get the screen size
        size = screen.size() #define a size variable

        #Define the main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(size.width(), size.height())
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #Define the scroll area for the list of knots
        self.knots_list = QtWidgets.QScrollArea(self.centralwidget)
        self.knots_list.setGeometry(QtCore.QRect(20, 80, 161, size.height()-250)) #sets the size and location of the scroll area
        self.knots_list.setObjectName("knots_list")
        #self.knots_list.setStyleSheet("border: 1px solid black; padding: 5px;")
        self.knots_list.setAlignment(Qt.AlignmentFlag.AlignTop) #aligns the text to the top of the scroll area
        self.knots_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) #sets the scroll bar to always be on
        self.knots_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) #sets the horizontal scroll bar to always be off

        #Define the label for the list of knots
        self.knots_list_label = QTextEdit(self.centralwidget) #define the label
        self.knots_list_label.setGeometry(QtCore.QRect(20, 80, 161, size.height()-250)) #sets the size and location of the label
        self.knots_list_label.setAlignment(Qt.AlignmentFlag.AlignTop) #aligns the text to the top of the label
        self.knots_list_label.setReadOnly(True) #makes the label read only

        #Define the label for the image
        self.Image = QtWidgets.QLabel(self.centralwidget) #define the label
        self.Image.setGeometry(QtCore.QRect(200, 80, 400, 280)) #sets the size and location of the label

        #Define the Open Folder button
        self.open_folder = QtWidgets.QPushButton(self.centralwidget) #define the button
        self.open_folder.setGeometry(QtCore.QRect(40, 30, 121, 41)) #sets the size and location of the button
        self.open_folder.setObjectName("open_folder") #sets the name of the button
        self.open_folder.clicked.connect(lambda: self.openImage()) #connect the button to the openImage function

        #Define the Predict button
        self.train_button = QtWidgets.QPushButton(self.centralwidget) #define the button
        self.train_button.setGeometry(QtCore.QRect(size.width()-400,size.height()-250, 121, 41)) #sets the size and location of the button
        self.train_button.setObjectName("trian_button") #sets the name of the button
        self.train_button.setText("Predict") #sets the text of the button
        self.train_button.clicked.connect(lambda: self.trainAndShow()) #connect the button to the trainAndShow function

        #Define the clear Button
        self.clear_button = QtWidgets.QPushButton(self.centralwidget) #define the button
        self.clear_button.setGeometry(QtCore.QRect(size.width()-400,size.height()-200, 121, 41)) #sets the size and location of the button
        self.clear_button.setObjectName("clear_button") #sets the name of the button
        self.clear_button.setText("Clear") #sets the text of the button
        self.clear_button.clicked.connect(lambda: self.clearAll()) #connect the button to the clear function

        #Define the Previous Image button (getting removed)
        # self.Image.setObjectName("Image")
        # self.previous_image = QtWidgets.QPushButton(self.centralwidget)
        # self.previous_image.setGeometry(QtCore.QRect(200, 370, 121, 41))
        # self.previous_image.setObjectName("previous_image")
        # self.next_image = QtWidgets.QPushButton(self.centralwidget)
        # self.next_image.setGeometry(QtCore.QRect(650, 370, 121, 41))
        # self.next_image.setObjectName("next_image")

        #Define the label for the number of knots
        self.conf_label = QtWidgets.QLabel(self.centralwidget) #define the label
        self.conf_label.setGeometry(QtCore.QRect(210, size.height()-260, 150, 20)) #sets the size and location of the label
        self.conf_label.setObjectName("confidence box") #sets the name of the label

        #Define the split selector label
        # self.split_selector = QtWidgets.QLabel(self.centralwidget) #define the label
        # self.split_selector.setGeometry(QtCore.QRect(210, size.height()-230, 87, 20)) #sets the size and location of the label
        # self.split_selector.setObjectName("split_selector") #sets the name of the label

        #define the partial selector label
        # self.partial_selector = QtWidgets.QLabel(self.centralwidget) #define the label
        # self.partial_selector.setGeometry(QtCore.QRect(210, size.height()-200, 87, 20)) #sets the size and location of the label
        # self.partial_selector.setObjectName("partial_selector") #sets the name of the label

        #Define the knot selector box
        self.conf_box = QtWidgets.QLineEdit(self.centralwidget) #define the box
        self.conf_box.setGeometry(QtCore.QRect(345, size.height()-260, 160, 24)) #sets the size and location of the box
       # self.knot_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.conf_box.setObjectName("conf_box") #sets the name of the box
        # set validator to only allow ints and doubles
        # Create a validator using the regular expression
        # Create a regular expression that matches integers and doubles
        regex = QRegularExpression("^[+-]?[0-9]*[.]?[0-9]+$")

        # Create a validator using the regular expression
        validator = QRegularExpressionValidator(regex, self.conf_box)
        self.conf_box.setValidator(validator)
    
        #Define the progress bar (getting removed)
        # self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        # self.progressBar.setGeometry(QtCore.QRect(420, 380, 118, 23))
        # self.progressBar.setProperty("value", 24)
        # self.progressBar.setObjectName("progressBar")

        #Define the split selector box
        # self.split_box = QtWidgets.QLineEdit(self.centralwidget) #define the box
        # self.split_box.setGeometry(QtCore.QRect(280, size.height()-230, 160, 24)) #sets the size and location of the box
        # #self.split_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        # self.split_box.setObjectName("split_box") #sets the name of the box

        #Define the partial selector box
    #     self.partial_box = QtWidgets.QLineEdit(self.centralwidget) #define the box
    #     self.partial_box.setGeometry(QtCore.QRect(280, size.height()-200, 160, 24)) #sets the size and location of the box
    #    # self.partial_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
    #     self.partial_box.setObjectName("partial_box") #sets the name of the box


        MainWindow.setCentralWidget(self.centralwidget) #sets the central widget
        self.menubar = QtWidgets.QMenuBar(MainWindow) #define the menubar
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 37)) #sets the size and location of the menubar
        self.menubar.setObjectName("menubar") #sets the name of the menubar
        MainWindow.setMenuBar(self.menubar) 
        self.statusbar = QtWidgets.QStatusBar(MainWindow) #define the statusbar
        self.statusbar.setObjectName("statusbar") #sets the name of the statusbar
        MainWindow.setStatusBar(self.statusbar) 

        #Define the graphics view label
        self.graphicsView = QtWidgets.QLabel(self.centralwidget) #define the label
        self.graphicsView.setGeometry(QtCore.QRect(200,30,size.width()-400,size.height()-300)) #sets the size and location of the label
        self.graphicsView.setScaledContents(True) #sets the label to scale the image
        self.graphicsView.setObjectName("graphicsView") #sets the name of the label
        self.graphicsView.setStyleSheet("border: 1px solid grey;") #sets the border of the label
        
        #Retranslate the UI
        self.retranslateUi(MainWindow) 
        QtCore.QMetaObject.connectSlotsByName(MainWindow) 


    def retranslateUi(self, MainWindow):

        #Retranslate the UI and set the text
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Plywood Defect Predictor")) #Title of the window
        self.open_folder.setText(_translate("MainWindow", "Open Folder"))  #Text for the open folder button
        self.conf_label.setText(_translate("MainWindow", "Confidence Threshold")) #Text for the knot selector label
        self.knots_list.setWidget(self.knots_list_label) #Set the knots list widget to the knots list label
        
    def clearAll(MainWindow):
        
        MainWindow.graphicsView.clear() #clear the image
        MainWindow.knots_list_label.clear() #clear the knots list
        MainWindow.conf_box.clear() #clear the confidence box
        fileName = None #set the filename to none
        

    def trainAndShow(MainWindow):

        try:
            #get the value from the confidence box
            conf = MainWindow.conf_box.text()
            if not conf:
                conf = 0.5
            else:
                conf = float(conf)

            #create the predictor
            predictor = Detectron_Detector()
            predictor.make_predictor(weights = '/Users/spencermarchand/Documents/VS_code/Python/Capstone/Training_1_BAD/model_final.pth', score_thresh=conf)

            #make the prediciton on the image using the filename from the file dialog
            b_boxes_dict = predictor.predict_classes(fileName)
            print(b_boxes_dict)
            knot_centers = predictor.compute_centers(b_boxes_dict['knots'])
            partial_centers = predictor.compute_centers(b_boxes_dict['partials'])
            centers = np.concatenate((knot_centers, partial_centers), axis=0)
            #save the image into a variable
            label_img_path = predictor.save_image('/Users/spencermarchand/Documents/VS_code/Python/Capstone/training/output_predictions')

            print("knott centers: ", knot_centers)
            print("partial centers: ", partial_centers)
            print("centers: ", centers)
            
            #put the predicited image into the graphics view
            MainWindow.graphicsView.setPixmap(QtGui.QPixmap(label_img_path))

            #Take the datapoints and create a string to display into the scrollable area.
            centerPointsKnots = " Knot Center Points: " +"\n"
            centerPointsPartials = " Partials Center Points: " +"\n"
            allpoints = ''
            for i,row in enumerate(knot_centers):
                centerPointsKnots += " {:d}: {:.2f}, {:.2f}".format(i+1 ,row[0], row[1]) + "\n"
            for i,row in enumerate(partial_centers):
                centerPointsPartials += " {:d}: {:.2f}, {:.2f}".format(i+1 ,row[0], row[1]) + "\n"
            allpoints = centerPointsKnots + '\n' + centerPointsPartials
            MainWindow.knots_list_label.setText(allpoints)
            #send the data to the database
            #predictor.send_to_plc(centers)
        except NameError:
            MainWindow.graphicsView.setText("Please pick an image") #Throw error if the user never selected the image
        except Exception:
            MainWindow.graphicsView.setText("Error")


    def openImage(MainWindow):

        #open the file dialog and get the file path
        fileDialog = QFileDialog(MainWindow)
        fileDialog.setWindowTitle("Open Image")
        fileDialog.setNameFilter("Images (*.png *.jpg)") #filter out the types of files you can choose from
        global fileName
        fileName = fileDialog.getOpenFileName(MainWindow)
        fileName = fileName[0] #get the file path from the tuple
        if not fileName: return #if the user cancels the file dialog, return
        MainWindow.graphicsView.setPixmap(QtGui.QPixmap(fileName))
    

if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv) #create the application
    MainWindow = QtWidgets.QMainWindow() #create the main window
    ui = Ui_MainWindow() #create the UI
    ui.setupUi(MainWindow) #setup the UI
    MainWindow.show() #show the main window
    sys.exit(app.exec()) #exit the application when the user closes the window

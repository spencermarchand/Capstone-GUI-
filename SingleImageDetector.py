import os
import cv2
import numpy as np
import time 
import mysql.connector
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer

class Detectron_Detector(): 
    def __init__(self):
        #initialize variables
        self.config ='COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml'
        self.num_classes = 4
        self.device ='cpu'
        self.im_num = 1


    #create predictor object 
    def make_predictor(self, weights, score_thresh):
        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file(self.config))
        cfg.MODEL.WEIGHTS = os.path.join(weights)
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = self.num_classes
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = score_thresh
        cfg.MODEL.DEVICE = self.device
        self.predictor = DefaultPredictor(cfg)

    #checks input image for correct dimensions 
    # def check_image_dimensions(self, image_np):
    #     height, width = image_np.shape[:2]  
    #     #return same image if correct 
    #     if width == 2048 and height == 1536:
    #         return image_np 
    #     #resize if incorrect
    #     else:
    #         print('image size incorrect, resizing it for you...')
    #         image = cv2.resize(image, (2048, 1536)) 
      



    #run prediction and return numpy array of bounding boxes 
    def predict(self, image_path): 
        self.image_path = image_path
        self.img = cv2.imread(image_path)
        # self.img = self.check_image_dimensions(self.img)
        start_time = time.time()
        self.outputs = self.predictor(self.img)
        print(f"Inference time: {round(time.time() - start_time, 3)} seconds")
        out = self.outputs
        pred_boxes = out["instances"].pred_boxes.tensor.numpy()
        return pred_boxes
    

    def extract_data(self, box):
        """
        calculates x, y, and area data from bounding boxes and returns a numpy array of the data.
        """
        metrics = np.zeros((len(box), 3))

        for i in range(len(box)): 
            area = (box[i][2] - box[i][0]) * (box[i][3] - box[i][1])
            x = (box[i][0] + box[i][2])/2
            y = (box[i][1] + box[i][3])/2
            metrics[i] = [x, y, area]
        return metrics


    def convert_to_mm(self, centers, height, field_of_view):
        """ 
        Converts all values to mm from pixels 
        """
        pxFactor = 2*height*(np.tan(field_of_view/2)/2048)
        centers = centers * pxFactor


    def show(self): 
        """ 
        Displays image with bounding boxes  
        """
        image = self.img
        vis = Visualizer(image[:, :, ::-1], MetadataCatalog.get(self.config), scale=2)
        im_output = vis.draw_instance_predictions(self.outputs['instances'].to("cpu"))
        im_output = im_output.get_image()[:, :, ::-1]
        cv2.imshow("predictions", im_output)
        cv2.waitKey(0)


    def save_image(self, output_path):
        """
        Saves image with bounding boxes drawn to specified location
        """
        image = self.img
        vis = Visualizer(image[:, :, ::-1], MetadataCatalog.get(self.config), scale=1)
        im_output = vis.draw_instance_predictions(self.outputs['instances'].to("cpu"))
        im_output = im_output.get_image()[:, :, ::-1]
        cv2.imwrite(os.path.join(output_path, str(self.im_num) + '.jpg'), im_output)
        return os.path.join(output_path, str(self.im_num) + '.jpg')


    def send_to_db(self, data):
        """
        Sends data to database
        """
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hcvk9J79F5",
        )
        print(mydb)
        mycursor = mydb.cursor()

        #delete database if it already exists
        mycursor.execute("DROP DATABASE IF EXISTS capstone")
        mycursor.execute("CREATE DATABASE capstone")

        #create a login for a new user called plc connected over ethernet to the capstone database with a password of plc
        # mycursor.execute("CREATE USER 'plc'@'%' IDENTIFIED BY PASSWORD 'plc'")
        # mycursor.execute("GRANT ALL PRIVILEGES ON capstone.* TO 'plc'@'%'")
        # mycursor.execute("FLUSH PRIVILEGES")

        mycursor.execute("USE capstone")

        #create database to store centers
        mycursor.execute("CREATE TABLE IF NOT EXISTS knots (id INT AUTO_INCREMENT PRIMARY KEY, x DOUBLE, y DOUBLE, area DOUBLE)")

        #insert data into database
        for i in range(len(data)):
            mycursor.execute("INSERT INTO centers (x, y, area) VALUES (%s, %s, %s)", (int(data[i][0]), int(data[i][1]), int(data[i][2])))
            mydb.commit()
        
        #show data in database
        mycursor.execute("SELECT * FROM centers")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
        

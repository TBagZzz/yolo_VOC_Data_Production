import os
import cv2
import math
import numpy as np
import shutil
from copy import deepcopy
from lxml import etree
import xml.etree.ElementTree as ET
import glob


class multiAnnotation:



    def __init__(self):
        self.Path = os.getcwd()
        self.location1 = os.path.join(self.Path, "img/")
        self.result_loc = os.path.join(self.Path, "Results/")
        self.result_locenter_xML = os.path.join(self.Path, "ResultsXML/")
        self.inFolder = os.path.join(self.Path, "input/")
        self.iteration = 0
        self.size = 0
        self.iterationXML = 0
        self.org_Height = 0
        self.org_Width = 0

    def imgProduce(self, angle, size):
        count_1 = 0
        count_2 = 0
        self.angle = angle
        for i in range(len(self.angle)):
            self.angle[i] = int(self.angle[i])
        for filename in sorted(glob.glob(self.inFolder + "*.png")):
            imgPath = os.path.join(self.inFolder, ("%s.png" % count_1))
            img = cv2.imread(imgPath, cv2.IMREAD_UNCHANGED)
            Height = img.shape[0]
            Width = img.shape[1]
            center_x= Width // 2
            center_y = Height // 2
            count_1 += 1

            for i in range(len(angle)):
     
                ref = cv2.getRotationMatrix2D((center_x, center_y), self.angle[i], 1)
                cos = np.abs(ref[0, 0])
                sin = np.abs(ref[0, 1])

                # New dimensions for bounding image.
                new_Width = int((Height*sin) + (Width*cos))
                new_Height = int((Height*cos) + (Width*sin))

                # Rotation matrix adjustion.
                ref[0, 2] += (new_Width / 2) - center_x
                ref[1, 2] += (new_Height / 2) - center_y

                # Actual rotation.
                for l in range(size):
                    image = cv2.warpAffine(img, ref, (new_Width, new_Height))
                #Writing Image.
                    cv2.imwrite((self.result_loc + '%s.png' % count_2), image)
                    count_2 += 1
        self.size = size

    def rotate_box(self, corners, angle, center_x, center_y, Height, Width):
        corners = corners.reshape(-1,2)
        corners = np.hstack((corners, np.ones((corners.shape[0],1), dtype = type(corners[0][0]))))
        ref = cv2.getRotationMatrix2D((center_x, center_y), angle, 1)
        cos = np.abs(ref[0, 0])
        sin = np.abs(ref[0, 1])
        new_Width = int((Height * sin) + (Width * cos))
        new_Height = int((Height * cos) + (Width * sin))
        # adjust the rotation matrix to take into account translation
        ref[0, 2] += (new_Width / 2) - center_x
        ref[1, 2] += (new_Height / 2) - center_y
        # Prepare the vector to be transformed
        result = np.dot(ref,corners.T).T
        result = result.reshape(-1,8)
        return result


    def final_enclosing(self, corners):
        x_coordinates = corners[:,[0,2,4,6]]
        y_coordinates = corners[:,[1,3,5,7]]
        
        xmin = np.min(x_coordinates,1).reshape(-1,1)
        ymin = np.min(y_coordinates,1).reshape(-1,1)
        xmax = np.max(x_coordinates,1).reshape(-1,1)
        ymax = np.max(y_coordinates,1).reshape(-1,1)
        
        result = np.hstack((xmin, ymin, xmax, ymax,corners[:,8:]))
        
        return result

    def produceCoordinates(self, angle, coordinate_Arr):

        min_x = coordinate_Arr[0]
        min_y = coordinate_Arr[1]
        max_x = coordinate_Arr[2]
        max_y = coordinate_Arr[3]

        corners = np.hstack((min_x, min_y, min_x, max_y, max_x, min_y, max_x, max_y))
        center_y = self.org_Height // 2
        center_x = self.org_Width // 2
        
        new_corners = self.rotate_box(corners,angle,center_x,center_y,self.org_Height,self.org_Width)
        result_coordinates = self.final_enclosing(new_corners)
        final_result = []
        for i in range(len(result_coordinates[0])):
            result_coordinates[0][i] = math.ceil(result_coordinates[0][i])
            final_result.append(int(result_coordinates[0][i]))
        final_result[0] = final_result[0]
        final_result[1] = final_result[1]
        final_result[2] = final_result[2]
        final_result[3] = final_result[3]
        return (final_result)
    

    def combine_Annotation(self):
        count = 0
        xmlPath = self.Path + "/XMLs/"
        final_imgPath = self.Path + "/Results/"
        Set1 = []
        setName = []
        Set2 = []

        for filename in sorted(glob.glob(xmlPath + "*.xml")):

            tree = ET.parse(filename)
            root = tree.getroot()
            for elem1 in root.findall("size"):
                org_Width = int((elem1.find('width').text))
                org_Height = int((elem1.find('height').text))
                setDepth = (elem1.find('depth').text)
                self.org_Height = org_Height
                self.org_Width = org_Width
            for elem1 in root.findall("object"):
                setName.append(elem1.find('name').text)

                for elem2 in elem1.findall("bndbox"):
                    coordinates = []
                    for i in list(elem2):
                        coordinates.append(int(i.text))
                    Set1.append(coordinates)
            angle = self.angle
            
            for I in angle:

                for n in range(self.size):
                    for i in range(len(Set1)):
                        Set2.append(self.produceCoordinates(I, Set1[i]))
                        Set2tmp = deepcopy(Set2)

                    Set2.clear()
                    annotation = ET.Element('annotation')
                    ET.SubElement(annotation, 'folder').text = ("input")
                    ET.SubElement(annotation, 'filename').text = ("%s.png" % count)
                    ET.SubElement(annotation, 'path').text = (final_imgPath + "%s.png" % count)
                    ET.SubElement(annotation, 'segmented').text = '0'
                    size = ET.SubElement(annotation, 'size')

                    img = cv2.imread((final_imgPath + "%s.png" % count), cv2.IMREAD_UNCHANGED)
                    (current_Height, current_Width) = img.shape[:2]
                    ET.SubElement(size, 'width').text = str(current_Width)
                    ET.SubElement(size, 'height').text = str(current_Height)
                    ET.SubElement(size, 'depth').text = setDepth
                    setNumber = 0

                    for l in Set2tmp:
                        obj = ET.SubElement(annotation, 'object')
                        ET.SubElement(obj, 'name').text = setName[setNumber]
                        ET.SubElement(obj, 'pose').text = 'Unspecified'
                        ET.SubElement(obj, 'truncated').text = '0'
                        ET.SubElement(obj, 'difficult').text = '0'
                        bbox = ET.SubElement(obj, 'bndbox')
                        
                        if l[0] >= 0:
                            ET.SubElement(bbox, 'xmin').text = str(l[0])
                        else:
                            ET.SubElement(bbox, 'xmin').text = str(0)
                        if l[1] >= 0:
                            ET.SubElement(bbox, 'ymin').text = str(l[1])
                        else:
                            ET.SubElement(bbox, 'ymin').text = str(0)
                        if l[2] <= current_Width:
                            ET.SubElement(bbox, 'xmax').text = str(l[2])
                        else:
                            ET.SubElement(bbox, 'xmax').text = str(current_Width)
                        if l[3] <= current_Height:
                            ET.SubElement(bbox, 'ymax').text = str(l[3])
                        else:
                            ET.SubElement(bbox, 'ymax').text = str(current_Height)

                        setNumber += 1
                    xml_str = ET.tostring(annotation)
                    rootX = etree.fromstring(xml_str)
                    xml_str = etree.tostring(rootX, pretty_print=True)

                    save_path = os.path.join(self.result_locenter_xML, ("%s.xml" % count))
                    with open(save_path, 'wb') as temp_xml:
                        temp_xml.write(xml_str)
                    temp_xml.close()
                    count += 1
            Set1.clear()
        print("Done.")


obj1 = multiAnnotation()

print("NOTE : Total images = size input x number of angles.")
size = int(input("Enter number of images for angle : "))
angle = input("Input angle with spaces : ")
angle = angle.split(" ")
obj1.imgProduce(angle, size)
obj1.combine_Annotation()















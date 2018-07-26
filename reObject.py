#coding=utf-8
import xml.etree.ElementTree as ET

clses = ['fire','fire_tiny','fire_medium','fire_large']
cls = 'fire'

image_ids = open('/home/tency/caffe/data/fire_data/ImageSets/Main/trainval.txt').read().strip().split()
def convert_imgsize(xmin,ymin,xmax,ymax,norm_w,norm_h):
    width = (ymax-ymin)/norm_w
    height = (xmax-xmin)/norm_h
    area = width*height
    return area 

def write_file(out_file,area):
    f = open(out_file,"a")
    f.write(area+'\n')
    f.close()  

def read_xml(image_id):
    in_file = open('/home/tency/caffe/data/fire_data/Annotations/%s.xml'%(image_id))
    out_file = open('/home/tency/caffe/data/fire_data/1/%s.xml'%(image_id),'w')
    #out_file_txt = '/home/tency/caffe/data/fire_data/1/1.txt'

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = float(size.find('width').text)
    h = float(size.find('height').text)
    norm_w = w/300
    norm_h = h/300
    
    for obj in root.iter('object'):
        for name in root.iter('name'):
            while name.text == cls:
                xmlbox = obj.find('bndbox')
                xmin = float(xmlbox.find('xmin').text)
                ymin = float(xmlbox.find('ymin').text)
                xmax = float(xmlbox.find('xmax').text)
                ymax = float(xmlbox.find('ymax').text)
                # area = str(convert_imgsize(xmin,ymin,xmax,ymax,norm_w,norm_h)) #if need
                area = int(convert_imgsize(xmin, ymin, xmax, ymax, norm_w, norm_h))
                # write_file(out_file_txt,area)   #write area of objects to .txt file
                if area <= 1024:
                    name.text = 'fire_tiny'
                elif 1024 < area <= 9216:
                    name.text = 'fire_medium'
                else:
                    name.text = 'fire_large'
                    
    tree.write(out_file)


for image_id in image_ids:
    read_xml(image_id)



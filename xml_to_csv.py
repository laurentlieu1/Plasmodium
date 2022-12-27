import os
import glob
import pandas as pd
import argparse
import xml.etree.ElementTree as ET


def xml_to_csv(path):


    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                    int(root.find('size')[0].text),
                    int(root.find('size')[1].text),
                    member[0].text,
                    float(member[4][0].text),
                    float(member[4][1].text),
                    float(member[4][2].text),
                    float(member[4][3].text)
                    )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height',
                'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


df = xml_to_csv(r"C:\Users\molan\Downloads\Datasets\Algo\job_13-2022_12_06_20_30_22-pascal voc 1.1\Annotations\images_5000-5453")

df.to_csv("labels.csv", index=False)
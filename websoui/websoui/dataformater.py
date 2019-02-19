import os
import base64
import io
import json
#import matplotlib.pyplot as plt

"""
def graph_to_base64_image(losses):
        fig = plt.plot(losses)
        in_memory_image = io.BytesIO()
        plt.savefig(in_memory_image
                    , bbox_inches='tight'
                    , pad_inches = 0)
        plt.close()
        base64_image = base64.b64encode(in_memory_image.getvalue())
        return base64_image.decode('utf-8')

def numpy_to_base64_image(numpy_matrix):
        fig = plt.imshow(numpy_matrix)
        plt.axis('off')
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        in_memory_image = io.BytesIO()
        plt.savefig(in_memory_image
                    , bbox_inches='tight'
                    , pad_inches = 0)
        plt.close()
        base64_image = base64.b64encode(in_memory_image.getvalue())
        return base64_image.decode('utf-8')
"""

def text_to_base64(text):
    return base64.encodestring(text)

def image_file_to_base64(path):
    with open(path, 'rb') as f:
        img = f.read()
        base64_image = base64.b64encode(img)
    return base64_image.decode('utf-8')

def create_image_graph_data_obj(xs_list, list_of_texts):
    #TODO: this method and create_image_data_obj should be refactored
    dic = {}
    if not isinstance(list_of_texts, list):
        raise TypeError("Passed a " + str(type(list_of_texts)) + " and was expecting a list.")
    dic["image"] = graph_to_base64_image(xs_list)
    dic["image_texts_list"] = list_of_texts
    return dic

def create_image_data_obj(numpy_matrix, list_of_texts):
    dic = {}
    if not isinstance(list_of_texts, list):
        raise TypeError("Passed a " + str(type(list_of_texts)) + " and was expecting a list.")
    dic["image"] = numpy_to_base64_image(numpy_matrix)
    dic["image_texts_list"] = list_of_texts
    return dic


class Data_package():
    def __init__(self):
        self.dict = {}
        self.dict["data_type"]="data"
        self.dict["images"]=[]
        self.dict["special_images"]=[]
    
    def get_json(self):
        return json.dumps(self.dict)

    def add_image_and_texts_list(self, numpy_matrix, list_of_texts, is_special_image=False):
        obj = create_image_data_obj(numpy_matrix, list_of_texts)
        if is_special_image:
            #add the index of the last image to a different list.
            self.dict["special_images"].append(obj)
        else:
            self.dict["images"].append( obj )

    def add_graph_and_texts_list(self, xs_list, list_of_texts, is_special_image=False):
        #This method and add_image_and_texts_list should be refactored
        obj = create_image_graph_data_obj(xs_list, list_of_texts)
        if is_special_image:
            #add the index of the last image to a different list.
            self.dict["special_images"].append(obj)
        else:
            self.dict["images"].append( obj )


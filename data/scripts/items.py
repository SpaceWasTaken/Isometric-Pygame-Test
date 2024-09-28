import os, json
from data.scripts.funcs import load_image, set_img_colorkey

class Items:
    def __init__(self, attr_path):
        self.attr_path = attr_path
        self.item_names = []
        self.manage_items = []
        self.hand_manage_items = []
        self.item_data = []
        self.load_item_image() 

    def get_attribs(self):
        files = []
        for i in os.listdir(self.attr_path):
            files.append(self.attr_path + '/' + i)
        for file in files:
            with open(file) as readf:
                content = json.load(readf)
                self.item_data.append(content)
    
    def load_item_image(self): # Setting the items image here
        self.get_attribs()
        for item in self.item_data:
            item['image'] = load_image('data/entities/items/' + item['name'].lower() + 'Item' + '.png')
            set_img_colorkey(item['image'])

    def create_manage_list(self): 
        self.manage_items = []
        for name in self.item_names:
            for item in self.item_data:
                if name == item['name']:
                    self.manage_items.append([name, item['image'], item['maxStack']])

    def get_item_data(self, name):
        for item in self.item_data:
            if name == item['name']:
                return {
                        'type':name, 
                        'item_img':item['image'], 
                        'max_stack':item['maxStack'],
                        'is_full':False,
                        'count':1, 
                        'set':0
                        }
                







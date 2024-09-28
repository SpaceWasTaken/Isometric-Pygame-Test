import json, os
from data.scripts.funcs import load_image, set_img_colorkey

class Resources:
    def __init__(self, attr_path, get_iso_pos, draw_order, ground_collisions):
        self.attr_path = attr_path
        self.draw_order = draw_order
        self.ground_collisions = ground_collisions
        self.get_iso_pos = get_iso_pos
        self.entity_data = []
        self.resource_data = []
        self.rendered_resources = []
        self.load_resource_image()

    def get_attribs(self):
        files = []
        for i in os.listdir(self.attr_path):
            files.append(self.attr_path + '/' + i)
        for file in files:
            with open(file) as readf:
                content = json.load(readf)
                self.resource_data.append(content)
    
    def load_resource_image(self):
        self.get_attribs()
        for resource in self.resource_data:
            resource['image'] = load_image('data/entities/resources/' + resource['name'].lower() + '.png')
            set_img_colorkey(resource['image'])

    def resource_gen(self, noise, rand_val):
        resource_type = ()
        for resource in self.resource_data:
            if noise < resource['generation'] and rand_val[0] == 3:
                resource_type = (resource['name'], resource['image'])
        if resource_type != () or resource_type != None:
            return resource_type

    def render_resources(self):
        ...
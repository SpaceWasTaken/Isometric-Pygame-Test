from pprint import pprint
import pygame, copy

class Inventory():
    def __init__(self, x, y, draw_order, hand_inv_img, inventory_img, slot_img, slot_select_img):
        self.x = x
        self.y = y
        self.draw_order = draw_order
        self.hand_inv_img = hand_inv_img 
        self.inventory_img = inventory_img
        self.slot_img = slot_img
        self.slot_select_img = slot_select_img
        self.hand_slot_count = 2
        self.visible = False
        self.avatar_width = 72 
        self.avatar_height = 190 
        self.items_width = 200
        self.items_height = 200
        self.row_count = 6
        self.col_count = 4
        self.count = 0
        self.slot_width = 20
        self.slot_spacing = 2
        self.inv_items_ = {}
        for x in range(self.row_count+1):
            for y in range(self.col_count+1):
                slot = f"{x}:{y}"
                self.inv_items_[slot] = {}
        self.hand_inv_items_ = {}
        for x in range(1):
            for y in range(2):
                slot = f"{x}:{y}"
                self.hand_inv_items_[slot] = {}
        self.currentSelectSlot = {} 
        self.selectSlot = {}
        self.final_items = {}
        self.cursorSlotPopul = False
        self.click_count = 0 
        self.a = []
        self.item_pos = []
        self.click_log = []
        self.flip = {}

    def draw_inventory(self, mouse_data, surface):
        from main import mfont
        
        # inv base
        inventory_rect = pygame.Rect(self.x, self.y, 300, 200)
        self.draw_order.append([self.inventory_img, [inventory_rect.x, inventory_rect.y, inventory_rect.y*inventory_rect.y*1000]])
        self.item_pos = []
        self.flip = []
        # items in slots

        for item in self.inv_items_:
            if self.inv_items_[item] != {}:
                if self.inv_items_[item]['count'] >= self.inv_items_[item]['max_stack']:
                    self.inv_items_[item]['count'] = self.inv_items_[item]['max_stack']

                if int(item[0]) > 3:
                    x_pos = int(item[0])*(self.slot_width+self.slot_spacing)+self.x+78
                    y_pos = int(item[2])*(self.slot_width+self.slot_spacing)+self.y+8
                else:
                    x_pos = int(item[0])*(self.slot_width+self.slot_spacing)+self.x+6
                    y_pos = int(item[2])*(self.slot_width+self.slot_spacing)+self.y+8

                try:
                    if self.inv_items_[item] == self.selectSlot[item][0]:
                        x_pos = mouse_data[0].x
                        y_pos = mouse_data[0].y
                except:pass

                if item != '0:0' and item != '1:0':
                    item_rect = pygame.Rect(x_pos, y_pos, 18, 18)
                    if mouse_data[1] and mouse_data[0].colliderect(item_rect) and self.selectSlot == {}:
                        self.selectSlot[item] = [self.inv_items_[item], item]

                    count_font = mfont.render(str(self.inv_items_[item]['count']), False, ((255, 255, 255)))
                    self.draw_order.append([self.inv_items_[item]['item_img'], [x_pos, y_pos, y_pos*999999]])
                    surface.blit(count_font, (x_pos+5, y_pos+5))

        # slots
        for y in range(self.col_count):
            for x in range(self.row_count):
                target_item = pygame.Rect(x*(self.slot_width+self.slot_spacing) + self.x + 2,  y*(self.slot_width + self.slot_spacing) + self.y + 8, 20, 20)
                if mouse_data[0].colliderect(target_item):
                    self.draw_order.append([self.slot_select_img, [x*(self.slot_width+self.slot_spacing) + self.x + 3, y*(self.slot_width + self.slot_spacing) + self.y + 4, y*(self.slot_width + self.slot_spacing) + self.y + 10*999999 + 1]]) 

    def draw_hand_inventory(self, mouse_data):
        from main import item, mfont, surface
        # inv base
        hand_inventory_rect = pygame.Rect(2, 2, 32, 61)
        self.draw_order.append([self.hand_inv_img, [hand_inventory_rect.x, hand_inventory_rect.y, hand_inventory_rect.y*hand_inventory_rect.y*1000]])

        for y in range(2):
            for x in range(1):
                self.draw_order.append([self.slot_img, [x*(self.slot_width+self.slot_spacing) + 8, y*(self.slot_width + self.slot_spacing) + 2 + 8, y*(self.slot_width + self.slot_spacing) + 2 + 10*999999]])
                target_item = pygame.Rect(x*(self.slot_width+self.slot_spacing) + 8,  y*(self.slot_width + self.slot_spacing) + 2 + 8, 20, 20)
                if mouse_data[0].colliderect(target_item):
                    self.draw_order.append([self.slot_select_img, [x*(self.slot_width+self.slot_spacing) + 8, y*(self.slot_width + self.slot_spacing) + 2 + 8, y*(self.slot_width + self.slot_spacing) + 2 + 10*999999]]) 
        # item
        for item in self.inv_items_:
            if item == '0:0' or item == '1:0':
                if self.inv_items_[item] != {}:
                    if self.inv_items_[item]['count'] >= self.inv_items_[item]['max_stack']:
                        self.inv_items_[item]['count'] = self.inv_items_[item]['max_stack']

                    x_pos = int(item[2])*(self.slot_width+self.slot_spacing)+11 
                    y_pos = int(item[0])*(self.slot_width+self.slot_spacing)+14
                    
                    item_rect = pygame.Rect(x_pos, y_pos, 18, 18)
                    if mouse_data[1] and mouse_data[0].colliderect(item_rect) and self.selectSlot == {}:
                        self.selectSlot[item] = [self.inv_items_[item], item]
                    try:
                        if self.inv_items_[item] == self.selectSlot[item][0]:
                            x_pos = mouse_data[0].x
                            y_pos = mouse_data[0].y
                    except:pass

                    count_font = mfont.render(str(self.inv_items_[item]['count']), False, ((255, 255, 255)))
                    self.draw_order.append([self.inv_items_[item]['item_img'], [x_pos, y_pos, y_pos*999999]])
                    surface.blit(count_font, (x_pos+5, y_pos+5))

    def drag_drop(self):
        from main import cursor_data

        for y in range(self.col_count+1):
            for x in range(self.row_count+1):
                if str(x)+':'+str(y) == '0:0' or str(x)+':'+str(y) == '1:0':
                    target_item = pygame.Rect(y*(self.slot_width + self.slot_spacing) + 14, x*(self.slot_width+self.slot_spacing) +11, 20, 20)
                else:
                    target_item = pygame.Rect(x*(self.slot_width+self.slot_spacing) + self.x + 3,  y*(self.slot_width + self.slot_spacing) + self.y + 8, 20, 20)
                
                if cursor_data[0].colliderect(target_item):
                    if cursor_data[1]:
                        self.click_count += 1

                    new_slot = '0:0'
                    if str(x)+':'+str(y) == '0:0' or str(x)+':'+str(y) == '1:0':
                        x = int(target_item.y) // (self.slot_width+self.slot_spacing) 
                        y = int(target_item.x) // (self.slot_width+self.slot_spacing) 
                    else:
                        x = int(target_item.x) // (self.slot_width + self.slot_spacing) + self.x + 13 - 90
                        y = int(target_item.y) // (self.slot_width + self.slot_spacing) + self.y + 10 - 109

                    new_slot = f'{x}:{y}'

                    # item swap
                    if self.inv_items_[new_slot] != {}:
                        if self.selectSlot != {}:
                            for i in self.selectSlot:
                                if new_slot != self.selectSlot[i][1]:
                                    if cursor_data[1]:
                                        copy_new_item = copy.copy(self.inv_items_[new_slot])
                                        self.inv_items_[new_slot] = self.inv_items_[self.selectSlot[i][1]]
                                        self.inv_items_[self.selectSlot[i][1]] = copy_new_item
                                        self.selectSlot = {}

                    # item drop
                    if self.selectSlot != {}:
                        if cursor_data[1] and self.click_count % 3 == 0 and self.inv_items_[new_slot] == {}:
                            currentSlotCopy = copy.copy(self.selectSlot)
                            for i in currentSlotCopy:
                                self.inv_items_[new_slot] = self.selectSlot[i][0]

                                if new_slot != self.selectSlot[i][1]:
                                    self.inv_items_[self.selectSlot[i][1]] = {}
                                self.selectSlot.clear()



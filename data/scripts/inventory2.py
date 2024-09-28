import pygame, noise, random

class Map:
    def __init__(self, grass_tile, water_tile, select_tile_img, tree_img, get_iso_pos, draw_order, ground_collisions, maps_surface):
        self.grass_tile = grass_tile
        self.water_tile = water_tile
        self.get_iso_pos = get_iso_pos
        self.select_tile_img = select_tile_img
        self.tree_img = tree_img
        self.draw_order = draw_order
        self.ground_collisions = ground_collisions
        self.maps_surface = maps_surface
        self.map = {}
        self.tile_type = {
            'grass':[self.grass_tile, ['variation'], 0, 0], # [image, tile_data, animation_timer, animation_frame]
            'water':[self.water_tile, ['animation'], 0, 0],
        }
        self.row = 0
        self.col = 0
        self.grass_type = 0
        self.tiles = []
        self.map_width = 48
        self.width = 32
        self.height = 32
        self.chunk_size = 8
        self.frame_count = 0
        self.tick = 0
        self.tile_scroll = [0,0]
        
    # loop through all the elements on the dictionary, if there is the same type of item then check if the stack is full.
    # if stack is *not* full - increment one to the item found (slot to which item was added to)
    # if stack is full -  start a new slot

    def get_chunks(self, x, y):
        from main import resource
        chunk_data = []
        for y_pos in range(self.chunk_size):
            for x_pos in range(self.chunk_size):
                target_x = x * self.chunk_size + x_pos
                target_y = y * self.chunk_size + y_pos

                rand = random.choices((3,4,5), weights=(1, 24, 75))
                n = noise.pnoise2(target_x*0.02, target_y*0.02)

                resource_type = []
                resource_type = resource.resource_gen(n, rand)

                tile_type = 'grass'
                if (n > 0.1):
                    tile_type = 'water'
                    self.ground_collisions.append(pygame.Rect(target_x, target_y, 1, 1))
                    
                #__________________________________________________# Checking noise value to render different grass tiles
                if round(n, 2) == 0.09 or round(n, 2) == 0.10:
                    self.grass_type = 0
                elif round(n, 2) == 0.08:
                    self.grass_type = 1
                elif round(n, 2) == 0.07:
                    self.grass_type = 1
                elif round(n, 2) == 0.05 or round(n, 2) == 0.06:
                    self.grass_type = 2
                else:
                    self.grass_type = rand[0]
                #__________________________________________________#
                chunk_data.append([[target_x, target_y], tile_type, self.grass_type, resource_type])
        
        return chunk_data

    def get_tiles(self, player, mx, my, get_cart_pos, restr_tiles, scroll):
        from main import item, inventory
        c_mx, c_my = get_cart_pos(mx + scroll[0], my + scroll[1])
        cart_mouse_rect = pygame.Rect(c_mx, c_my, 1, 1)
        self.tile_scroll[0] += round(player.x - self.tile_scroll[0] - 1)
        self.tile_scroll[1] += round(player.y - self.tile_scroll[1] - 1)

        for y in range(5):
            for x in range(5):
                target_x = x - 2.4 + round(self.tile_scroll[0]/(self.chunk_size))
                target_y = y - 2.2 + round(self.tile_scroll[1]/(self.chunk_size))
                chunk = str(target_x) + ":" + str(target_y)
                if chunk not in self.map:
                    self.map[chunk] = self.get_chunks(target_x, target_y)
                    
                for tile in self.map[chunk]: 
                    cart_tile_rect = pygame.Rect(tile[0][0], tile[0][1], 1, 1)

                    is_x, is_y = self.get_iso_pos(tile[0][0], tile[0][1])
                    if self.tile_type[tile[1]][1][0] == 'animation': 
                        self.draw_order.append([self.tile_type[tile[1]][0][self.tile_type[tile[1]][3]], [is_x - scroll[0], is_y - scroll[1], is_y]])

                    if self.tile_type[tile[1]][1][0] == 'variation': 
                        self.draw_order.append([self.tile_type[tile[1]][0][tile[2]], [is_x - scroll[0], is_y - scroll[1], is_y]])

                    # rendering resources
                    if tile[3] != (): 
                        cart_tile_rect = pygame.Rect(tile[0][0]-1, tile[0][1], 1, 1)
                        if cart_mouse_rect.colliderect(cart_tile_rect):
                            ''' adding the resource removed to the 
                                items to add to inventory slot '''
                            item.item_names.append(tile[3][0])

                            slot = f'{self.row}:{self.col}'

                            self.row += 1
                            if self.row > 5:
                                self.col += 1
                                self.row = 1

                            for i in inventory.inv_items_:
                                if i['type'] == inventory.inv_items_[i]['type'] and inventory.inv_items_[i]['count'] != inventory.inv_items_[i]['max_stack']:
                                    inventory.inv_items_[i]['count'] += 1
                                else:
                                    # if no type or maxed stack start a new slot

                                    # inventory.inv_items_[slot] = {
                                    # 'type':'Tree', 
                                    # 'item_img':pygame.image.load('data/entities/items/treeItem.png'), 
                                    # 'max_stack':5,
                                    # 'is_full':False,
                                    # 'count':0, 
                                    # 'set':0
                                    # }
                                    ...

                            inventory.inv_items_[slot] = {
                            'type':'Tree', 
                            'item_img':pygame.image.load('data/entities/items/treeItem.png'), 
                            'max_stack':5,
                            'is_full':False,
                            'count':0, 
                            'set':0
                            }
                                
                            tile[3] = ()
                        else:
                            res_rect = tile[3][1].get_rect(topleft=(is_x, is_y))
                            res_rect.midbottom = res_rect.x, res_rect.y 
                            self.draw_order.append([tile[3][1], [res_rect.x - scroll[0], res_rect.y - scroll[1], res_rect.y+tile[3][1].get_height()]])

                    if (cart_mouse_rect.x, cart_mouse_rect.y) == (cart_tile_rect.x, cart_tile_rect.y):
                        self.draw_order.append([self.select_tile_img, [is_x - scroll[0], is_y - scroll[1], is_y+32]])
        
        
                        




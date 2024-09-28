from tkinter import font
import pygame 
from data.scripts.funcs import load_animation, set_img_colorkey, load_image

pygame.init()
WIDTH, LENGTH = 500, 500
pygame.display.set_mode((WIDTH, LENGTH))

font_img = load_image('data/entities/other/font.png')
font7 = '7 Squared.ttf'

cursor_img = load_image('data/entities/other/cursor.png')

map_layout = load_image('data/entities/map/layout1.png')
grass_img = [load_image('data/entities/tiles/grass_tile1.png'), load_image('data/entities/tiles/grass_tile2.png'), load_image('data/entities/tiles/grass_tile3.png'),
            load_image('data/entities/tiles/grass_tile4.png'), load_image('data/entities/tiles/grass_tile5.png'), load_image('data/entities/tiles/grass_tile6.png')]
water_img = [load_image('data/entities/tiles/water_tile1.png'), load_image('data/entities/tiles/water_tile2.png'), load_image('data/entities/tiles/water_tile3.png')]
tree_img = load_image('data/entities/resources/tree.png')
rock_img = load_image('data/entities/resources/rock.png')

tile_select_img = load_image('data/entities/tiles/tile_select.png')

player_idle_r_img = load_animation('data/entities/player', 'player_idle_r', 5)
player_idle_l_img = load_animation('data/entities/player', 'player_idle_l', 5)
player_walk_r_img = load_animation('data/entities/player', 'player_walk_r', 6)
player_walk_l_img = load_animation('data/entities/player', 'player_walk_l', 6)

slot_img = load_image('data/entities/inventory/slot.png')
slot_select_img = load_image('data/entities/inventory/slot_select.png')
inventory_img = load_image('data/entities/inventory/inventory.png')
hand_inventory_img = load_image('data/entities/inventory/live_inventory.png')


set_img_colorkey(font_img)
set_img_colorkey(cursor_img)
set_img_colorkey(slot_img)
set_img_colorkey(slot_select_img)
set_img_colorkey(inventory_img)
set_img_colorkey(hand_inventory_img)
set_img_colorkey(tile_select_img)
set_img_colorkey(tree_img)
set_img_colorkey(rock_img)
set_img_colorkey(grass_img, list=True)
set_img_colorkey(water_img, list=True)
set_img_colorkey(player_idle_r_img, list=True)
set_img_colorkey(player_idle_l_img, list=True)
set_img_colorkey(player_walk_l_img, list=True)
set_img_colorkey(player_walk_r_img, list=True)









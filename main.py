import pygame, sys, time, glm
from OpenGL.GL import *
from OpenGL.GLU import *
from data.scripts.opengl.shader import *
from data.scripts.opengl.textures import *
from data.scripts.opengl.camera import *
from data.scripts.opengl.setup import *

from data.scripts.player import *
from data.scripts.resources import *
from data.scripts.inventory import *
from data.scripts.items import *
from data.scripts.map import *
from data.scripts.load import *
from data.scripts.funcs import *

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
mainsurf = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF|pygame.OPENGL)
surface = pygame.Surface((400, 300))

shader = Shader('data/scripts/opengl/shaderSettings/vertex.txt', 'data/scripts/opengl/shaderSettings/fragment.txt')
pixel_texture = Texture()

opengl = Opengl((WIDTH, HEIGHT))
camera = Camera(5, 2, 5)
#_______________________________________________#
# gl vars
aspectratio = WIDTH/HEIGHT 

img_pos = glm.vec3(0, 0, -12)

surfs = []
true_scroll = [0,0]
ground_collisions = []
restr_tiles = []
last_time = 0
mxr, myr = (0,0)
click = False
mouse_rect = None
click = False
cursor_data = []
#_______________________________________________#

FPS = 80
clock = pygame.time.Clock()
run = True

def draw_gl_rect():
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)  

def glRenderSetup():
    shader.use_shader()
    glBindVertexArray(opengl.VAO)

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)

def set_items(scroll):
    restr_tiles = []
    ground_collisions = []

    sorted_surfs = get_sortedList(surfs)
    surfs.clear()
    for surf in sorted_surfs:
        surface.blit(surf[0], (surf[1][0], surf[1][1]))

    player.draw(surfs, get_iso_pos, ground_collisions, scroll, surface)
    maps.get_tiles(player, mx, my, get_cart_pos, restr_tiles, scroll)
    resource.render_resources()

    item.create_manage_list()
    if inventory.visible:
        inventory.draw_inventory(cursor_data, surface)
    inventory.draw_hand_inventory(cursor_data)
    inventory.drag_drop()

    pygame.mouse.set_visible(False)

def __blit__(scroll):
    glRenderSetup()
    draw_gl_rect()
    set_items(scroll)
    
    surface.blit(cursor_img, (mx, my))
    mainsurf.blit(pygame.transform.scale(surface, mainsurf.get_rect().size), (0,0))

    pixel_texture.create_texture(mainsurf)

    pixel_texture.delete()
    pygame.display.flip()

player = Player(6, 19, player_idle_r_img, player_idle_l_img, player_walk_r_img, player_walk_l_img)
maps = Map(grass_img, water_img, tile_select_img, tree_img, get_iso_pos, surfs, restr_tiles, map_layout)
resource = Resources('data/scripts/resourceAttr', get_iso_pos, surfs, restr_tiles)
inventory = Inventory((WIDTH//4)-(inventory_img.get_rect().width//2), 95, surfs, hand_inventory_img, inventory_img, slot_img, slot_select_img)
item = Items('data/scripts/itemAttr')
mfont = pygame.font.Font(font7, 7)

def main():
    global last_time, dt, mx, my, scroll, click, mouse_rect, cursor_data, click

    shader.use_shader()
    shader.set_bool('sWaterTex', 0)

    running = True
    while running:
        
        shader.use_shader()
        glBindVertexArray(opengl.VAO)
        shader.clear_screen(0.1, 0.1, 0.1, 1.0)

        cam_view = camera.create_view()
        
        pygame.display.set_caption(str(f"FPS : {clock.get_fps()}"))
        clock.tick(FPS)
        surface.fill((0, 0, 0))
        
        dt = time.time() - last_time
        last_time = time.time()
        dt *= 80

        true_scroll[0] += (player.iso_rect.x - true_scroll[0] - 180)/5
        true_scroll[1] += (player.iso_rect.y - true_scroll[1] - 120)/5
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])+0.5

        mxr, myr = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.vel[0] = -0.12
                    player.directions["left"] = True
                    player.facing = "left"
                if event.key == pygame.K_d:
                    player.vel[0] = 0.12
                    player.directions["right"] = True
                    player.facing = "right"
                if event.key == pygame.K_w:
                    player.vel[1] = -0.12
                    player.directions["right"] = True
                    player.facing = "right"
                if event.key == pygame.K_s:
                    player.vel[1] = 0.12
                    player.directions["left"] = True
                    player.facing = "left"
                if event.key == pygame.K_e:
                    inventory.count += 1
                if event.key == pygame.K_q:
                    ...

                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
                    player.vel = [0,0]
                    player.directions["right"] = False
                    player.directions["left"] = False

        surfx_ratio = mainsurf.get_rect().width / surface.get_rect().width
        surfy_ratio = mainsurf.get_rect().height / surface.get_rect().height

        mx, my = (int(mxr/surfx_ratio)), int(myr/surfy_ratio)
        mouse_rect = pygame.Rect(mx, my, 1, 1)
        cursor_data = (mouse_rect, click)

        player.x += player.vel[0]*dt
        player.y += player.vel[1]*dt

        player._move(restr_tiles)

        if inventory.count % 2 == 0:
            inventory.visible = False
        else:
            inventory.visible = True

        # projection _________________________________________#
        colorVal = (math.cos(pygame.time.get_ticks()/500))+0.8
        if colorVal < 0.5:
            colorVal = 0.5

        # projection _________________________________________#
        img_pos = glm.vec3(0, 0, -5)
        model = glm.mat4(1)
        model = glm.rotate(model, glm.radians(0), glm.vec3(0, 0.5, .5))

        trans = glm.mat4(1)
        trans = glm.translate(trans, img_pos)
        trans = glm.scale(trans, glm.vec3(2,2,0))

        projection = glm.mat4(1)
        projection = glm.perspective(glm.radians(45), aspectratio, 0.1, 100)
        ortho_proj = glm.ortho(-1, 1, -(HEIGHT/WIDTH), (HEIGHT/WIDTH), 0.1, 10) * trans  # orthographic position to retain the scaling while rotating

        shader.set_vec1('vtime', pygame.time.get_ticks()/1000)
        shader.set_vec4('vertexColorRGB', colorVal, 0.8, 1.4, 1)
        shader.set_mat4('model', model)
        shader.set_mat4('view', trans)
        shader.set_mat4('projection', projection)
        shader.set_mat4('vertexRotation', ortho_proj)
        
        #____________________________________________________# 
        
        __blit__(scroll)

    shader.delete()
    pixel_texture.delete()
    delete_buffers(opengl.VAO, opengl.VBO, opengl.EBO)
    
    pygame.quit()
    
main()








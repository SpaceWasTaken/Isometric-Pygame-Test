import pygame

class Player:
    def __init__(self, x, y, player_idle_r_img, player_idle_l_img, player_walk_r_img, player_walk_l_img):
        self.x = x
        self.y = y
        self.player_idle_r_img = player_idle_r_img
        self.player_idle_l_img = player_idle_l_img
        self.player_walk_r_img = player_walk_r_img
        self.player_walk_l_img = player_walk_l_img
        self.rect_width = 1  # width of the rect in 2d
        self.rect_height = 1 # height of the rect in 2d
        self.iso_width = 26  # width of the rect in isometric
        self.iso_height = 36 # height of the rect in isometric
        self.vel = [0,0]
        self.rect = pygame.Rect(self.x, self.y, self.rect_width, self.rect_height)
        self.iso_rect = pygame.Rect(self.x, self.y, self.iso_width, self.iso_height)
        self.height = 0
        self.move = True
        self.grounded = True
        self.tick = 0
        self.frame_walk_count = 0
        self.frame_idle_count = 0
        self.facing = "left"
        self.directions = {
            "forward" : False, 
            "backward" : False,
            "left" : False, 
            "right" : False
        }
 
    def _move(self, restricted_tiles):
        new_rect = pygame.Rect(self.x - 1, self.y, 1, 1)
        for rect in restricted_tiles:
            if new_rect.colliderect(rect):
                if self.vel[0] >= 0:
                    self.directions["right"] = False
                    self.vel[0] = 0
                elif self.vel[0] <= 0:
                    self.directions["left"] = False
                    self.vel[0] = 0
                if self.vel[1] >= 0:
                    self.directions["left"] = False
                    self.vel[1] = 0
                elif self.vel[1] <= 0:
                    self.directions["right"] = False
                    self.vel[1] = 0

    def draw(self, draw_order, get_iso_pos, ground_collisions, scroll, surface):
        self.iso_rect.midbottom = get_iso_pos(self.x, self.y)

        self.tick += 4

        if self.tick % 10 == 0:
            self.frame_walk_count += 1
            self.frame_idle_count += 1

        if self.frame_walk_count >= len(self.player_walk_l_img):
            self.frame_walk_count = 0
        if self.frame_idle_count >= len(self.player_idle_l_img):
            self.frame_idle_count = 0

        if self.directions["right"]:
            draw_order.append([self.player_walk_r_img[self.frame_walk_count], [self.iso_rect.x - scroll[0], self.iso_rect.y + self.height - scroll[1], self.iso_rect.bottom]])
        elif self.directions["left"]:
            draw_order.append([self.player_walk_l_img[self.frame_walk_count], [self.iso_rect.x - scroll[0], self.iso_rect.y + self.height - scroll[1], self.iso_rect.bottom]])
        else:
            if self.facing == "right":
                draw_order.append([self.player_idle_r_img[self.frame_idle_count], [self.iso_rect.x - scroll[0], self.iso_rect.y + self.height - scroll[1], self.iso_rect.bottom]])
            elif self.facing == "left":
                draw_order.append([self.player_idle_l_img[self.frame_idle_count], [self.iso_rect.x - scroll[0], self.iso_rect.y + self.height - scroll[1], self.iso_rect.bottom]])
            



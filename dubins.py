#!/usr/bin/env python3

import math
import time
import pygame
from heapdict import heapdict

maxFPS = 60

def to_deg(radian):
    while radian < 0:
        radian += math.pi*2

    while radian > math.pi*2:
        radian -= math.pi*2

    return radian*180/math.pi


def dist(pos1, pos2):
    return math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)


def vector_rotate(v, theta):
    rv = [0, 0]
    rv[0] = v[0]*math.cos(theta)-v[1]*math.sin(theta)
    rv[1] = v[0]*math.sin(theta)+v[1]*math.cos(theta)
    return rv


class GameApp():
    def __init__(self):
        self.running = True
        self.screen = None
        self.boundary = (800, 600)
        self.arrow_pos = (130, 220)
        self.arrow_dir = 90.0*math.pi/180
        self.arrow_r = 50.0
        self.dest_pos = (300, 420)
        self.dump_pos = None

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.boundary)
        self.myfont = pygame.font.SysFont('Consolas', 12)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left
                self.arrow_pos = event.pos

    def on_update(self, dt):
        m1, m2, m3 = pygame.mouse.get_pressed()
        if m1:
            endpos = pygame.mouse.get_pos()
            length = dist(endpos,self.arrow_pos)
            if length > 0:
                v = ((endpos[0]-self.arrow_pos[0]), (endpos[1]-self.arrow_pos[1]))
                self.arrow_dir = math.atan2(v[1],v[0])


    def draw_text(self, text, color, pos):
        self.screen.blit(self.myfont.render(text, True, color), pos)

    def dump_info(self, text, color=(0, 255, 0)):
        if self.dump_pos is None:
            self.dump_pos = [10, 10]
        self.draw_text(text, color, self.dump_pos)
        self.dump_pos[1] += 16

    def draw_arrow(self, pos, angle, color):
        arrow_length = 30
        arrow_length2 = 7
        w = 3
        endpos = (pos[0]+int(arrow_length*math.cos(angle)),
                  pos[1]+int(arrow_length*math.sin(angle)))
        angle1 = angle+3*math.pi/4
        endpos1 = (endpos[0]+int(arrow_length2*math.cos(angle1)),
                   endpos[1]+int(arrow_length2*math.sin(angle1)))
        angle2 = angle+5*math.pi/4
        endpos2 = (endpos[0]+int(arrow_length2*math.cos(angle2)),
                   endpos[1]+int(arrow_length2*math.sin(angle2)))
        pygame.draw.line(self.screen, color, pos, endpos, w)
        pygame.draw.line(self.screen, color, endpos, endpos1, w)
        pygame.draw.line(self.screen, color, endpos, endpos2, w)

    def on_render(self):
        self.dump_pos = None
        self.screen.fill((50, 50, 50))

        def offset(pos):
            offset = 12
            return (pos[0]-offset, pos[1]-offset)

        tcolor = (255, 255, 255)
        color = (60, 100, 60)

        # circles
        left_dir = self.arrow_dir-math.pi/2
        left_cpos = (self.arrow_pos[0]+int(self.arrow_r*math.cos(left_dir)),
                   self.arrow_pos[1]+int(self.arrow_r*math.sin(left_dir)))
        if dist(left_cpos, self.dest_pos) < self.arrow_r+2:
            left_cpos = None
            lc_theta = 0.0

        right_dir = self.arrow_dir+math.pi/2
        right_cpos = (self.arrow_pos[0]+int(self.arrow_r*math.cos(right_dir)),
                   self.arrow_pos[1]+int(self.arrow_r*math.sin(right_dir)))
        if dist(right_cpos, self.dest_pos) < self.arrow_r+2:
            right_cpos = None
            rc_theta = 0.0

        if left_cpos:
            pygame.draw.circle(self.screen, color, left_cpos, int(self.arrow_r), 1)
        if right_cpos:
            pygame.draw.circle(self.screen, color, right_cpos, int(self.arrow_r), 1)

        # origin to dest
        if left_cpos:
            lc_o2d = dist(left_cpos, self.dest_pos)
            lc_theta = math.acos(self.arrow_r/lc_o2d)
            pygame.draw.line(self.screen, color, left_cpos, self.dest_pos)
        if right_cpos:
            rc_o2d = dist(right_cpos, self.dest_pos)
            rc_theta = math.acos(self.arrow_r/rc_o2d)
            pygame.draw.line(self.screen, color, right_cpos, self.dest_pos)

        # Q points
        hcolor = (255, 255, 0)
        if left_cpos:
            lcv = [self.dest_pos[0]-left_cpos[0],
                self.dest_pos[1]-left_cpos[1]]
            v2 = vector_rotate(lcv, lc_theta)
            qpos1 = [v2[0]*self.arrow_r/lc_o2d+left_cpos[0],
                    v2[1]*self.arrow_r/lc_o2d+left_cpos[1]]
            qpos1 = [int(i) for i in qpos1]
            pygame.draw.line(self.screen, color, left_cpos, qpos1)
            pygame.draw.line(self.screen, hcolor, self.dest_pos, qpos1)
            pygame.draw.circle(self.screen, color, qpos1, 2, 0)
            self.draw_text("LQ", tcolor, offset(qpos1))

            sdir = math.atan2(self.dest_pos[1]-qpos1[1],self.dest_pos[0]-qpos1[0])
            rect = ((left_cpos[0]-self.arrow_r,left_cpos[1]-self.arrow_r), 
                    (self.arrow_r*2, self.arrow_r*2))
            pygame.draw.arc(self.screen, hcolor, rect, -math.pi/2-self.arrow_dir, -math.pi/2-sdir, 1)

        if right_cpos:
            rcv = [self.dest_pos[0]-right_cpos[0],
                self.dest_pos[1]-right_cpos[1]]
            v2 = vector_rotate(rcv, -rc_theta)
            qpos1 = [v2[0]*self.arrow_r/rc_o2d+right_cpos[0],
                    v2[1]*self.arrow_r/rc_o2d+right_cpos[1]]
            qpos1 = [int(i) for i in qpos1]
            pygame.draw.line(self.screen, color, right_cpos, qpos1)
            pygame.draw.line(self.screen, hcolor, self.dest_pos, qpos1)
            pygame.draw.circle(self.screen, color, qpos1, 2, 0)
            self.draw_text("RQ", tcolor, offset(qpos1))

            sdir = math.atan2(self.dest_pos[1]-qpos1[1],self.dest_pos[0]-qpos1[0])
            rect = ((right_cpos[0]-self.arrow_r,right_cpos[1]-self.arrow_r), 
                    (self.arrow_r*2, self.arrow_r*2))
            pygame.draw.arc(self.screen, hcolor, rect, math.pi/2-sdir, math.pi/2-self.arrow_dir, 1)

        # arrow
        color = (0, 255, 0)
        arrow_length = 10
        self.draw_arrow(self.arrow_pos, self.arrow_dir, color)
        self.draw_text("O", tcolor, offset(self.arrow_pos))

        # dest
        color = (0, 255, 0)
        pygame.draw.circle(self.screen, color, self.dest_pos, 2, 0)
        self.draw_text("P", tcolor, offset(self.dest_pos))

        # display variables
        self.dump_info("Arrow: {}, {:.3f}, r={}".format(
            self.arrow_pos, to_deg(self.arrow_dir), self.arrow_r))
        self.dump_info("P: {}".format(self.dest_pos))

        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def run(self):
        self.on_init()

        st = et = time.time()
        while self.running:
            dt = et - st
            maxfpsCheck = (1.0/maxFPS) - dt
            if maxfpsCheck > 0:
                time.sleep(maxfpsCheck)
                dt += maxfpsCheck
            st = et
            for event in pygame.event.get():
                self.on_event(event)
            self.on_update(dt)
            self.on_render()
            et = time.time()
        self.on_cleanup()


if __name__ == "__main__":
    GameApp().run()

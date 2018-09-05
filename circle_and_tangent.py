#!/usr/bin/env python3

import math
import time
import pygame
from heapdict import heapdict

maxFPS = 60


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
        self.circle_pos = (130, 220)
        self.circle_r = 70.0
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
                if dist(event.pos, self.dest_pos) > self.circle_r+1:
                    self.circle_pos = event.pos
            elif event.button == 3:  # right
                if dist(event.pos, self.circle_pos) > self.circle_r+1:
                    self.dest_pos = event.pos

    def on_update(self, dt):
        pass

    def draw_text(self, text, color, pos):
        self.screen.blit(self.myfont.render(text, True, color), pos)

    def dump_info(self, text, color=(0, 255, 0)):
        if self.dump_pos is None:
            self.dump_pos = [10, 10]
        self.draw_text(text, color, self.dump_pos)
        self.dump_pos[1] += 16

    def on_render(self):
        self.dump_pos = None
        self.screen.fill((50, 50, 50))

        def offset(pos):
            offset = 12
            return (pos[0]-offset, pos[1]-offset)

        tcolor = (255, 255, 255)

        # circle
        color = (0, 255, 0)
        pygame.draw.circle(self.screen, color, self.circle_pos, 2, 0)
        pygame.draw.circle(self.screen, color,
                           self.circle_pos, int(self.circle_r), 1)
        self.draw_text("O", tcolor, offset(self.circle_pos))

        # dest
        color = (0, 255, 0)
        pygame.draw.circle(self.screen, color, self.dest_pos, 2, 0)
        self.draw_text("P", tcolor, offset(self.dest_pos))

        # origin to dest
        color = (0, 255, 0)
        o2d = dist(self.circle_pos, self.dest_pos)
        theta = math.acos(self.circle_r/o2d)
        pygame.draw.line(self.screen, color, self.circle_pos, self.dest_pos)

        # origin to tangent point, tangent line
        color = (0, 150, 0)
        v = [self.dest_pos[0]-self.circle_pos[0],
             self.dest_pos[1]-self.circle_pos[1]]
        pos = [v[0]+self.circle_pos[0], v[1]+self.circle_pos[1]]
        pygame.draw.line(self.screen, color, self.circle_pos, pos)
        v2 = vector_rotate(v, theta)
        color = (0, 255, 0)
        qpos1 = [v2[0]*self.circle_r/o2d+self.circle_pos[0],
                 v2[1]*self.circle_r/o2d+self.circle_pos[1]]
        qpos1 = [int(i) for i in qpos1]
        pygame.draw.line(self.screen, color, self.circle_pos, qpos1)
        pygame.draw.line(self.screen, color, self.dest_pos, qpos1)
        pygame.draw.circle(self.screen, color, qpos1, 2, 0)
        self.draw_text("Q1", tcolor, offset(qpos1))
        v2 = vector_rotate(v, -theta)
        qpos2 = [v2[0]*self.circle_r/o2d+self.circle_pos[0],
                 v2[1]*self.circle_r/o2d+self.circle_pos[1]]
        qpos2 = [int(i) for i in qpos2]
        pygame.draw.line(self.screen, color, self.circle_pos, qpos2)
        pygame.draw.line(self.screen, color, self.dest_pos, qpos2)
        pygame.draw.circle(self.screen, color, qpos2, 2, 0)
        self.draw_text("Q2", tcolor, offset(qpos2))

        # display variables
        self.dump_info(
            "O: {}, radius={}".format(self.circle_pos, self.circle_r))
        self.dump_info("P: {}".format(self.dest_pos))
        self.dump_info("Dist(O,P): {:.2f}, theta: {:.2f}".format(
            o2d, theta*180/math.pi))
        self.dump_info("Q1: {}, Q2: {}".format(qpos1, qpos2))

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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, math
from variables import GRAD

def text_to_screen(screen, text, x, y, size=14, color=(255, 255, 255), font='monospace'):
	myfont = pygame.font.SysFont(font, size)
	
	label = myfont.render(text, 1, color).convert_alpha()
	screen.blit(label, (x, y))

def get_angle(x1, y1, x2, y2):
	rise = y1 - y2
	run = x1 - x2
	angle = math.atan2(run, rise) # get the angle in radians
	angle = angle / GRAD # convert to degrees
	return angle

def get_vel(angle, offset):
	return (math.sin(angle * GRAD) * offset, math.cos(angle * GRAD) * offset)

class Spritesheet(object):
	def __init__(self, filename):
		   self.sheet = pygame.image.load(filename).convert()
	
	def image_at(self, rectangle, colorkey=None):
		"Loads image from x,y,x+offset,y+offset"
		rect = pygame.Rect(rectangle)
		image = pygame.Surface(rect.size).convert()
		image.blit(self.sheet, (0, 0), rect)
		if colorkey is not None:
			if colorkey == -1:
				colorkey = image.get_at((0,0))
			image.set_colorkey(colorkey, pygame.RLEACCEL)
		return image
	
	def images_at(self, rects, colorkey=None):
		"Loads multiple images, supply a list of coordinates" 
		return [self.image_at(rect, colorkey) for rect in rects]
	
	def load_strip(self, rect, image_count, lines, colorkey=None):
		"Loads a strip of images and returns them as a list"
		
		tups = []
		for i in range(1, lines+1):
			tups += [(rect[0]+rect[2]*x, rect[1]+rect[3]*i, rect[2], rect[3])
					for x in range(image_count)]
		return self.images_at(tups, colorkey)

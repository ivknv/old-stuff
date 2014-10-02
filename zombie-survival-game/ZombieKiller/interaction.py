#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, sys, math
from pygame.locals import *
from func import get_angle, get_vel, text_to_screen
from objects import *
from variables import *
import screens

def interaction(screen, total_frames, events):
	mx, my = pygame.mouse.get_pos()
	
	for event in events:
		if event.type == QUIT:
			pygame.quit()
			sys.exit(0)
		if event.type == KEYDOWN:
			if not screens.paused:
				if event.key == K_q:
					screens.survivor.switch_weapon(1)
				elif event.key == K_e:
					screens.survivor.switch_weapon(-1)
				elif event.key == K_SPACE:
					screens.survivor.throw_grenade(mx, my, total_frames)
			if event.key == K_ESCAPE:
				screens.paused = not screens.paused
	
	check_health(screens.survivor, screen, events)
	if not screens.paused:
		movement(screens.survivor)
		rotate_survivor(screens.survivor, mx-16, my-16)
		shoot(screens.survivor, mx, my, total_frames)
		Zombie.attack(screens.survivor, total_frames, None)
		Grenade.movement()
		Grenade.explode(total_frames)
	
def shoot(survivor, mx, my, total_frames):
	if pygame.mouse.get_pressed()[0]:
		if Bullet.last[survivor.current] is not None:
			diff = total_frames - Bullet.last[survivor.current]
			if float(diff) / FPS < Bullet.specs['delay'][survivor.current]:
				return
		Bullet.last[survivor.current] = total_frames
		Bullet(survivor.rect.centerx, survivor.rect.centery, mx, my,
			survivor.angle, survivor.current, total_frames)
		
		if survivor.current == SHOTGUN:
			for i in range(player_progress.weapons[SHOTGUN]['number_of_pellets']-1):
				Bullet(survivor.rect.centerx, survivor.rect.centery, mx, my,
					survivor.angle, survivor.current, total_frames)

def rotate_survivor(survivor, mx, my):
	survivor.rotate(get_angle(survivor.x, survivor.y, mx, my))

def check_health(survivor, screen, events):
	if survivor.health < 1:
		screens.paused = True
		for event in events:
			if 'click' in screens.button5.handleEvent(event):
				screens.reset_game()
				survivor.health = Survivor.health
				screens.paused = False
			elif 'click' in screens.upgradesButton.handleEvent(event):
				screens.reset_game()
				survivor.health = Survivor.health
				screens.paused = False
				screens.current_screen = screens.upgrade_screen
		
		font = pygame.font.SysFont('monospace', 40)
		text = font.render('OMG! You just died!', True, (255, 20, 20))
		x, y = WIDTH / 2 - text.get_width() / 2, 40 - text.get_height() / 2
		
		screen.blit(text, (x, y))
		
		for btn in screens.buttons3:
			btn.draw(screen)
		pygame.mouse.set_visible(True)

def movement(survivor):
	keys = pygame.key.get_pressed()
	
	if keys[K_w]:
		survivor.velx, survivor.vely = get_vel(directions['n'], PLAYER_SPEED)
		survivor.movement()
	elif keys[K_s]:
		survivor.velx, survivor.vely = get_vel(directions['s'], PLAYER_SPEED)
		survivor.movement()
	if keys[K_a]:
		survivor.velx, survivor.vely = get_vel(directions['w'], PLAYER_SPEED)
		survivor.movement()
	elif keys[K_d]:
		survivor.velx, survivor.vely = get_vel(directions['e'], PLAYER_SPEED)
		survivor.movement()

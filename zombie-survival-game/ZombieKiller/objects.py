#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, pyganim
import random, time, math
from variables import *
from func import *

explosion_sound = pygame.mixer.Sound('Audio/explosion.ogg')
explosions = []
explosion_weak_spritesheet = Spritesheet('images/explosion_weak.png')
explosion_normal_spritesheet = Spritesheet('images/explosion_normal.png')
explosion_weak_images = explosion_weak_spritesheet.load_strip((0, 0, 100, 100), 3, 3, -1)
explosion_normal_images = explosion_normal_spritesheet.load_strip((0, 0, 100, 100), 4, 4, -1)
ANIMATION_SPEED_WEAK = 1.0 / 15.0
ANIMATION_SPEED_NORMAL = 1.0 / 16.0
explosion_animation_weak = []
explosion_animation_normal = []
explosion_animations = []
for i in explosion_weak_images:
	explosion_animation_weak.append((i, ANIMATION_SPEED_WEAK))

for i in explosion_normal_images:
	explosion_animation_normal.append((i, ANIMATION_SPEED_NORMAL))

explosion_animation_weak = pyganim.PygAnimation(explosion_animation_weak, loop=False)
explosion_animation_weak.convert_alpha()
explosion_animation_normal = pyganim.PygAnimation(explosion_animation_normal, loop=False)
explosion_animation_normal.convert_alpha()

def add_explosion(x, y, total_frames, damage=150.0):
	if damage < 140:
		is_weak = True
	else:
		is_weak = False
	if is_weak:
		explosion_animations.append((explosion_animation_weak.getCopy(), (x-39, y-39), is_weak))
	else:
		explosion_animations.append((explosion_animation_normal.getCopy(), (x-50, y-50), is_weak))
	for zambie in Zombie.List:
		dx, dy = zambie.rect.x - x, + zambie.rect.y - y
		distance = math.hypot(dx, dy)
		if distance < 150:
			angle = get_angle(zambie.vx, zambie.vy, x, y)
			velx, vely = get_vel(angle, 30)
			nx, ny = zambie.vx + velx - zambie.velx, zambie.vy + vely - zambie.vely
			if nx < WIDTH - Zombie.width and ny > 0:
				zambie.vx = nx
			if ny < HEIGHT - Zombie.height and ny > 0:
				zambie.vy = ny
			if damage - distance > 0:
				zambie.health -= damage - distance
				min_blood = damage - distance
				if min_blood > 0:
					min_blood = int(round(min_blood / 5.0, 0))
				else:
					min_blood = 0
				zambie.check_health()
				Blood.create(zambie.x, zambie.y, total_frames,
					min_blood, min_blood + 10)
	explosion_animations[-1][0].play()
	explosion_sound.play()

def display_explosions(screen, paused=False):
	for explosion in explosion_animations:
		if paused:
			explosion[0].pause()
		else:
			if explosion[0].state not in [pyganim.STOPPED, pyganim.PLAYING]:
				explosion[0].togglePause()
		
		if explosion[2]:
			num = 8
		else:
			num = 15
		
		if explosion[0].currentFrameNum >= num:
			explosion[0].stop()
			explosion_animations.remove(explosion)
		
		if explosion in explosion_animations:
			explosion[0].blit(screen, explosion[1])

class Wave(object):
	types = [[0, 100], [1, -1], [2, -1], [3, -1]]
	multiplier = 1.0
	
	def __init__(self, number=1):
		self.num_zombies = number * 2
		self.multiplier += 0.05
		if self.num_zombies > 100:
			self.num_zombies = 100
		self.number = number
		self.alive = self.num_zombies
		if number == 50:
			Wave.types[0][1] = 0
			Wave.types[1][1] = 0
			Wave.types[2][1] = 50
			Wave.types[3][1] = 50
		elif number == 40:
			Wave.types[0][1] = 0
			Wave.types[1][1] = 5
			Wave.types[2][1] = 75
			Wave.types[3][1] = 20
		elif number == 35:
			Wave.types[0][1] = 0
			Wave.types[1][1] = 0
			Wave.types[2][1] = 45
			Wave.types[3][1] = 55
		elif number == 28:
			Wave.types[0][1] = 0
			Wave.types[1][1] = 15
			Wave.types[2][1] = 30
			Wave.types[3][1] = 55
		elif number == 23:
			Wave.types[0][1] = 0
			Wave.types[1][1] = 10
			Wave.types[2][1] = 55
			Wave.types[3][1] = 35
		elif number == 20:
			Wave.types[0][1] = 0
			Wave.types[1][1] = 30
			Wave.types[2][1] = 35
			Wave.types[3][1] = 35
		elif number == 15:
			Wave.types[0][1] = 0
			Wave.types[1][1] = 20
			Wave.types[2][1] = 55
			Wave.types[3][1] = 25
		elif number == 14:
			Wave.types[0][1] = 0
			Wave.types[1][1] = 80
			Wave.types[2][1] = 15
			Wave.types[3][1] = 5
		if number == 13:
			Wave.types[0][1] = 0
			Wave.types[1][1] = 0
			Wave.types[2][1] = 100
			Wave.types[3][1] = 0
		elif number == 12:
			Wave.types[0][1] = 0
			Wave.types[1][1] = 0
			Wave.types[2][1] = 0
			Wave.types[3][1] = 100
		elif number == 11:
			Wave.types[0][1] = 1
			Wave.types[1][1] = 9
			Wave.types[2][1] = 40
			Wave.types[3][1] = 50
		elif number == 10:
			Wave.types[0][1] = 1
			Wave.types[1][1] = 9
			Wave.types[2][1] = 30
			Wave.types[3][1] = 60
		elif number == 8:
			Wave.types[0][1] = 1
			Wave.types[1][1] = 4
			Wave.types[2][1] = 65
			Wave.types[3][1] = 30
		elif number == 6:
			Wave.types[0][1] = 3
			Wave.types[1][1] = 42
			Wave.types[2][1] = 55
		elif number == 3:
			Wave.types[0][1] = 10
			Wave.types[1][1] = 90
	
	def spawn_zombies(self, survivor, total_frames):
		if self.num_zombies > 0:
			if Zombie.spawn(survivor, Wave.types, Wave.multiplier, total_frames):
				self.num_zombies -= 1
	
	@staticmethod
	def reset():
		Wave.types = [[0, 100], [1, -1], [2, -1], [3, -1]]
		Wave.multiplier = 1.0

class BaseClass(pygame.sprite.DirtySprite):
	List = pygame.sprite.LayeredDirty()
	
	def __init__(self, x, y, img):
		super(BaseClass, self).__init__()
		
		self.x = x
		self.y = y
		self.vx, self.vy = self.x, self.y
		self.velx, self.vely = 0, 0
		self.angle = 90
		self.image = img
		self.orig_image = self.image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.rect.width
		self.height = self.rect.height
		
		self.colliderect = self.rect.colliderect
		
		BaseClass.List.add(self)
	
	def rotate(self, angle):
		if self.angle != angle:
			self.angle = angle
	
	def move_(self):
		self.vx -= self.velx
		self.vy -= self.vely
		self.rect.x, self.rect.y = int(round(self.vx, 0)), int(round(self.vy, 0))
		self.x, self.y = self.rect.x, self.rect.y
	
	def update(self, *args, **kwargs):
		self.rotate_image()
		self.x, self.y = int(round(self.vx, 0)), int(round(self.vy, 0))
		self.rect.x, self.rect.y = self.x, self.y
	
	@staticmethod
	def set_dirty():
		for i in BaseClass.List:
			i.dirty = 1

	def rotate_image(self):
		self.image = pygame.transform.rotate(self.orig_image, self.angle)
	
	def set_velocity(self, offset):
		self.velx, self.vely = get_vel(self.angle, offset)
	
class Character(BaseClass):
	List = pygame.sprite.LayeredDirty()
	
	def __init__(self, x, y, health, img):
		super(Character, self).__init__(x, y, img)
		self.tx, self.ty = None, None
		self.health = health
		self.velx = 0
		self.vely = 0
		
		Character.List.add(self)
	
	def move_(self):
		nx, ny = self.vx - self.velx, self.vy - self.vely
		
		if nx + self.width < WIDTH and nx > 0:
			self.vx -= self.velx
		if ny + self.height < HEIGHT and ny > 0:
			self.vy -= self.vely
		self.x, self.y = int(round(self.vx, 0)), int(round(self.vy, 0))
		self.rect.x, self.rect.y = self.x, self.y
	
class Zombie(Character):
	List = pygame.sprite.LayeredDirty()
	health = 100
	width = height = 32
	images = None
	wave_number = 1
	current_wave = Wave(1)
	types = [{'strength': [5.0, 7.0], 'speed': [1.7, 2.2], 'health': [150, 250]},
	{'strength': [5.5, 9.0], 'speed': [2.1, 2.3], 'health': [180, 280]},
	{'strength': [7.0, 11.0], 'speed': [2.1, 2.7], 'health': [500, 750]},
	{'strength': [6.0, 9.0], 'speed': [2.5, 3.0], 'health': [230, 350]}]
		
	def __init__(self, x, y, type_, multiplier, total_frames):
		self.type = type_
		if Zombie.images is None:
			Zombie.images = [pygame.image.load('images/zombie{}.png'.format(i)).convert_alpha()
				for i in range(0, 5)]
		super(Zombie, self).__init__(x, y, Zombie.health,
			Zombie.images[self.type])
		self.vel = random.uniform(Zombie.types[self.type]['speed'][0],
			Zombie.types[self.type]['speed'][1])
		self.last_attack = total_frames
		self.strength = random.uniform(Zombie.types[self.type]['strength'][0],
			Zombie.types[self.type]['strength'][1])
		self.health = random.uniform(Zombie.types[self.type]['health'][0],
			Zombie.types[self.type]['health'][1])
		self.orig_health = self.health * random.uniform(1.0, multiplier)
		self.orig_strength = self.strength * random.uniform(1.0, multiplier)
		self.orig_speed = self.vel * random.uniform(1.0, multiplier)
		Zombie.List.add(self)
	
	@staticmethod
	def draw_zombies(screen):
		for zombie in Zombie.List:
			zombie.draw(screen)
	
	@staticmethod
	def spawn(survivor, types, multiplier, total_frames):
		if total_frames % (FPS * 0.4) == 0 and len(Zombie.List) < 10:
			x = random.randint(0, WIDTH - Zombie.width)
			y = random.randint(0, HEIGHT - Zombie.height)
			while abs(x - survivor.x) < 100:
				x = random.randint(0, WIDTH - Zombie.width)
			while abs(y - survivor.y) < 100:
				y = random.randint(0, HEIGHT - Zombie.height)
			
			num = random.randint(0, 100)
			type_ = 0
			
			for i in types:
				if num <= i[1]:
					type_ = i[0]
					break
			
			Zombie(x, y, type_, multiplier, total_frames)
			return True
		return False
	
	def check_health(self):
		if self.health <= 0:
			self.kill()
			Zombie.current_wave.alive -= 1
			score = self.orig_health / 10.0 + self.orig_strength / 5.0
			Survivor.score += int(score)
			Survivor.money += int(score / 2)
			if Survivor.score > Survivor.max_score:
				Survivor.max_score = Survivor.score
			player_progress.update_data(money=Survivor.money,
				max_score=Survivor.max_score)
			player_progress.write()
	
	@staticmethod
	def movement(total_frames):
		for zombie in Zombie.List:
			xdiff = abs(zombie.x - zombie.tx) if zombie.tx is not None else 0
			ydiff = abs(zombie.y - zombie.ty) if zombie.ty is not None else 0
			
			if xdiff > 0 or ydiff > 0:
				if xdiff < 5:
					zombie.velx = 0
				elif ydiff < 5:
					zombie.vely = 0
				zombie.move_()
				
	@staticmethod
	def update(*args, **kwargs):
		for zombie in Zombie.List:
			super(Zombie, zombie).update()
			zombie.set_velocity(zombie.vel)
	
	@staticmethod
	def attack(survivor, total_frames, surface):
		for zombie in Zombie.List:
			if zombie.colliderect(survivor) and total_frames - zombie.last_attack >= FPS:
				survivor.health -= zombie.strength
				zombie.last_attack = total_frames

class Grenade(BaseClass):
	image = None
	List = pygame.sprite.LayeredDirty()
	last_throw = None
	damage = player_progress.weapons[4]['damage']
	delay = player_progress.weapons[4]['delay']
	
	def __init__(self, x, y, tx, ty, total_frames):
		if Grenade.image is None:
			Grenade.image = pygame.image.load('images/grenade.png').convert_alpha()
		
		if Grenade.last_throw is not None:
			if total_frames - Grenade.last_throw < FPS * Grenade.delay:
				return
		
		Grenade.last_throw = total_frames
		self.image = Grenade.image
		
		super(Grenade, self).__init__(x, y, self.image)
		
		self.tx, self.ty = tx, ty
		self.ox, self.oy = self.x, self.y
		
		self.angle = get_angle(self.x, self.y, self.tx, self.ty)
		self.set_velocity(8)
		
		self.image_angle = 0
		
		Grenade.List.add(self)
	
	@staticmethod
	def movement():
		for grenade in Grenade.List:
			if abs(grenade.ox - grenade.x) > 250 or abs(grenade.oy - grenade.y) > 250:
				grenade.tx = None
				grenade.ty = None
				continue
			dx = abs(grenade.vx - grenade.tx) if grenade.tx is not None else 0
			dy = abs(grenade.vy - grenade.ty) if grenade.ty is not None else 0
			
			if dx != 0:
				if dx < abs(grenade.velx):
					grenade.vx = grenade.tx
				else:
					grenade.vx -= grenade.velx
			
			if dy != 0:
				if dy < abs(grenade.vely):
					grenade.vy = grenade.ty
				else:
					grenade.vy -= grenade.vely
			
			if dy == 0:
				grenade.ty = None
			if dx == 0:
				grenade.tx = None
	
	@staticmethod
	def explode(total_frames):
		for grenade in Grenade.List:
			if grenade.tx is None and grenade.ty is None:
				add_explosion(grenade.x, grenade.y, total_frames, Grenade.damage)
				grenade.kill()
	
	def rotate_image(self):
		self.image_angle += 12
		self.image = pygame.transform.rotate(Grenade.image, self.image_angle)

class Survivor(Character):
	images = []
	width = height = 46
	health = player_progress.max_health
	money = player_progress.money
	max_score = player_progress.max_score
	score = 0
	available_weapons = [w['type'] for w in player_progress.available_weapons
		if w['type'] != GRENADE]
	weapons = [w['type'] for w in player_progress.available_weapons
		if w['type'] != GRENADE]
	
	def __init__(self, x, y):
		self.current = PISTOL
		self.weapon_num = 0
		if len(Survivor.images) == 0:
			Survivor.images = [
				pygame.image.load('images/survivor_{}.png'.format(i)).convert_alpha()
					for i in ('pistol', 'shotgun', 'automatic',
						'bazooka')]
		
		super(Survivor, self).__init__(x, y, Survivor.health,
			Survivor.images[self.current])
	
	def throw_grenade(self, tx, ty, total_frames):
		if player_progress.weapons[GRENADE]['available']:
			Grenade(self.rect.centerx, self.rect.centery,
				tx, ty, total_frames)
	
	def movement(self):
		self.move_()
		if self.x > WIDTH - self.width:
			self.x = WIDTH - self.width
		elif self.x < 0:
			self.x = 0
		if self.y + self.height > HEIGHT:
			self.y = HEIGHT - self.height
		elif self.y < 0:
			self.y = 0
		
	def switch_weapon(self, n=1):
		Survivor.available_weapons.sort()
		self.weapon_num += n
		
		if self.weapon_num > len(Survivor.available_weapons)-1:
			self.weapon_num = 0
		elif self.weapon_num < 0:
			self.weapon_num = len(Survivor.available_weapons)-1
		
		self.current = Survivor.available_weapons[self.weapon_num]
						
		self.orig_image = Survivor.images[self.current]
		self.image = self.orig_image
		self.rotate_image()

class Bullet(BaseClass):
	List = pygame.sprite.LayeredDirty()
	last = [None, None, None, None]
	specs = {'delay': [i['delay'] for i in player_progress.weapons[:-1]],
		'damage': [i['damage'] for i in player_progress.weapons[:-1]],
		'image': None,
		'rocket_image': None,
		'accuracy': [i['accuracy'] for i in player_progress.weapons[:-1]],
		'blood': [[14, 22], [10, 22], [8, 15], [0, 0]],
		'size': [5, 11],
		'sound': [pygame.mixer.Sound('Audio/{}.ogg'.format(i))
			for i in ('pistol', 'shotgun', 'automatic', 'bazooka')]}
	
	impact_sound = pygame.mixer.Sound('Audio/impact.ogg')
	
	def move_(self):
		cond1 = self.tx is None or abs(self.ox - self.x) >= abs(self.ox - self.tx)
		cond2 = self.ty is None or abs(self.oy - self.y) >= abs(self.oy - self.ty)
		if cond1 or cond2:
			self.tx = None
			self.ty = None
			return
		
		dx = abs(self.x - self.tx) if self.tx is not None else 0
		dy = abs(self.y - self.ty) if self.ty is not None else 0
		
		if dx != 0:
			if dx < abs(self.velx):
				self.vx = self.tx
				self.tx = None
			else:
				self.vx -= self.velx
		
		if dy != 0:
			if dy < abs(self.vely):
				self.vy = self.ty
				self.ty = None
			else:
				self.vy -= self.vely
		
		if dy == 0:
			self.ty = None
		if dx == 0:
			self.tx = None
		
		self.x = int(round(self.vx, 0))
		self.y = int(round(self.vy, 0))
		self.rect.x = self.x
		self.rect.y = self.y
	
	def set_specs(self):
		try:
			self.delay = Bullet.specs['delay'][self.type]
			self.blood = Bullet.specs['blood'][self.type]
			self.accuracy = Bullet.specs['accuracy'][self.type]
			self.image = Bullet.specs['image']
			self.damage = Bullet.specs['damage'][self.type]
		except IndexError:
			raise IndexError('Bullet type must be a number between 0 and 3')
	
	def __init__(self, x, y, tx, ty, angle, b_type, total_frames):
		self.type = b_type
		if Bullet.specs['image'] is None:
			Bullet.specs['image'] = pygame.image.load('images/bullet.png').convert_alpha()
		self.set_specs()
		if Bullet.specs['rocket_image'] is None:
			Bullet.specs['rocket_image'] = pygame.image.load('images/rocket.png').convert_alpha()
		
		if b_type == BAZOOKA:
			self.image = Bullet.specs['rocket_image']
		
		self.created_at = total_frames
		
		super(Bullet, self).__init__(x, y, self.image)
		
		self.width, self.height = self.rect.width, self.rect.height
		self.tx, self.ty = tx, ty
		self.otx, self.oty = tx, ty
		
		d = abs(self.x - self.tx) + abs(self.y - self.ty)
		if d == 0:
			num = 1
		else:
			num = d / 20.0
		
		if num:
			self.tx += random.randint(-int(num / self.accuracy), int(num / self.accuracy))
			self.ty += random.randint(-int(num / self.accuracy), int(num / self.accuracy))
		self.angle = get_angle(self.x, self.y, self.tx, self.ty)
				
		self.rotate_image()
		
		self.set_velocity(18)
		
		self.ox, self.oy = self.x, self.y
		
		self.vx -= self.velx
		self.vy -= self.vely
		
		self.x, self.y = int(round(self.x, 0)), int(round(self.y, 0))
		
		Bullet.List.add(self)
		BaseClass.List.remove(self)
		
		Bullet.specs['sound'][self.type].stop()
		Bullet.specs['sound'][self.type].set_volume(0.5)
		Bullet.specs['sound'][self.type].play()
	
	def offscreen(self):
		if self.x < 0 or self.y < 0 or self.x > WIDTH or self.y > HEIGHT:
			return True
		else:
			return False
	
	@staticmethod
	def set_dirty():
		for i in Bullet.List:
			i.dirty = 1
	
	@staticmethod
	def loop(screen, total_frames, survivor):
		for bullet in Bullet.List:
			bullet.move_()
			
			if bullet.offscreen():
				bullet.kill()
				continue
			
			for zombie in Zombie.List:
				if bullet.tx is None:
					dx = 0
				else:
					dx = abs(bullet.tx - zombie.x)
				if bullet.ty is None:
					dy = 0
				else:
					dy = abs(bullet.ty - zombie.y)
				if bullet.colliderect(zombie):
					try:
						bullet.kill()
					except ValueError:
						break
					
					dy = abs(bullet.oty - zombie.rect.centery)
					dx = abs(bullet.otx - zombie.rect.centerx)
					
					if dy < 8 or dx < 8:
						bullet.damage *= 2
						bullet.blood = bullet.blood[0] * 2, bullet.blood[1] * 2
						angle = get_angle(zombie.vx, zombie.vy, bullet.x, bullet.y)
						v = get_vel(angle, 5)
						zombie.vx += v[0]
						zombie.vy += v[1]
						Bullet.impact_sound.play()
					zombie.health -= bullet.damage
					Blood.create(zombie.x, zombie.y, total_frames,
						*bullet.blood)
					Bullet.impact_sound.play()
					
					zombie.check_health()
					
					if bullet.type == BAZOOKA:
						add_explosion(bullet.x, bullet.y, total_frames,
							player_progress.weapons[BAZOOKA]['explosion_damage'])
					break
			
			if bullet.tx is None and bullet.ty is None and bullet.alive():
				bullet.kill()
				if bullet.type == BAZOOKA:
					add_explosion(bullet.x, bullet.y, total_frames,
						player_progress.weapons[BAZOOKA]['explosion_damage'])

class Blood(pygame.Rect):
	List = []
	width = height = 2
	
	def __init__(self, x, y, total_frames):
		super(Blood, self).__init__((x, y), (Blood.width, Blood.height))
		self.created_at = total_frames
		self.x += random.randint(-15, 15) + Zombie.width / 2
		self.y += random.randint(-15, 15) + Zombie.height / 2
		self.vx, self.vy = self.x, self.y
		
		Blood.List.append(self)
	
	@staticmethod
	def update(total_frames):
		for particle in Blood.List:
			if abs(total_frames - particle.created_at) >= FPS*5:
				Blood.List.remove(particle)
			else:
				particle.x = int(round(particle.vx, 0))
				particle.y = int(round(particle.vy, 0))
	
	@staticmethod
	def draw(screen):
		for particle in Blood.List:
			pygame.draw.rect(screen, (220, 0, 0), particle)
	
	@staticmethod
	def create(x, y, total_frames, Min=1, Max=3):
		for i in range(random.randint(Min, Max)):
			Blood(x, y, total_frames)

Bullet.impact_sound.set_volume(0.75)

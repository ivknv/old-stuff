#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, sys
import func
from variables import *
from pygbutton import PygButton, DARKGRAY

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), FLAGS, 32)

from objects import *
from interaction import interaction
import re

bg = pygame.image.load('images/map.png').convert()

total_frames, total_frames_before = 0, 0
paused = False
clock = pygame.time.Clock()

button1 = PygButton((WIDTH / 2 - 60, 100, 120, 40), 'New game')
button2 = PygButton((WIDTH / 2 - 60, 150, 120, 40), 'Continue')
quitButton = PygButton((WIDTH / 2 - 60, 200, 120, 40), 'Quit')
button3 = PygButton((WIDTH / 2 - 60, 100, 120, 40), 'Continue')
button4 = PygButton((WIDTH / 2 - 60, 150, 120, 40), 'Quit')
button5 = PygButton((WIDTH / 2 - 60, 100, 120, 40), 'Try again')
upgradesButton = PygButton((WIDTH / 2 - 60, 150, 120, 40), 'Upgrades')
upgradePistol1 = PygButton((WIDTH / 2 - 125, 150, 250, 40), 'Upgrade Pistol accuracy $100')
upgradePistol2 = PygButton((WIDTH / 2 - 125, 200, 250, 40), 'Upgrade Pistol speed $100')
upgradePistol3 = PygButton((WIDTH / 2 - 125, 250, 250, 40), 'Upgrade Pistol damage $100')
upgradeShotgun1 = PygButton((WIDTH / 2 - 125, 150, 250, 40), 'Upgrade Shotgun speed $300')
upgradeShotgun2 = PygButton((WIDTH / 2 - 125, 200, 250, 40), 'Upgrade Shotgun damage $300')
upgradeShotgun3 = PygButton((WIDTH / 2 - 125, 250, 250, 40), 'Increase number of pellets $300')
upgradeMGun1 = PygButton((WIDTH / 2 - 140, 150, 280, 40), 'Upgrade Machine Gun speed $420')
upgradeMGun2 = PygButton((WIDTH / 2 - 140, 200, 280, 40), 'Upgrade Machine Gun damage $420')
upgradeMGun3 = PygButton((WIDTH / 2 - 140, 250, 280, 40), 'Upgrade Machine Gun accuracy $420')
upgradeBazooka1 = PygButton((WIDTH / 2 - 125, 150, 250, 40), 'Upgrade Bazooka speed $550')
upgradeBazooka2 = PygButton((WIDTH / 2 - 125, 200, 250, 40), 'Upgrade Bazooka damage $550')
upgradeBazooka3 = PygButton((WIDTH / 2 - 125, 250, 250, 40), 'Upgrade Bazooka accuracy $550')
upgradeGrenades1 = PygButton((WIDTH / 2 - 125, 150, 250, 40), 'Upgrade Grenade damage $750')
pistolButton = PygButton((WIDTH / 2 - 125, 150, 250, 40), 'Pistol')
shotgunButton = PygButton((WIDTH / 2 - 125, 200, 250, 40), 'Shotgun')
machineGunButton = PygButton((WIDTH / 2 - 125, 250, 250, 40), 'Machine Gun')
bazookaButton = PygButton((WIDTH / 2 - 125, 300, 250, 40), 'Bazooka')
grenadesButton = PygButton((WIDTH / 2 - 125, 350, 250, 40), 'Grenades')
buyShotgunButton = PygButton((WIDTH / 2 - 125, 150, 250, 40), 'Buy Shotgun $2000')
buyMGunButton = PygButton((WIDTH / 2 - 125, 150, 250, 40), 'Buy Machine Gun $5000')
buyBazookaButton = PygButton((WIDTH / 2 - 125, 150, 250, 40), 'Buy Bazooka $12000')
buyGrenadesButton = PygButton((WIDTH / 2 - 125, 150, 250, 40), 'Buy Grenades $8000')
backButton = PygButton((WIDTH / 2 - 125, 420, 250, 40), 'Back')
backToUpgradesButton = PygButton((WIDTH / 2 - 125, 320, 250, 40), 'Back')
upgrade_buttons = [pistolButton, shotgunButton, machineGunButton, bazookaButton, grenadesButton, backButton]
menu_buttons = [button1, button2, quitButton]
pause_menu_buttons = [button3, button4]
buttons3 = [button5, upgradesButton]
survivor = Survivor(WIDTH / 2, HEIGHT / 2)

def find_path(survivor):
	for zombie in Zombie.List:
		zombie.tx = survivor.rect.centerx 
		zombie.ty = survivor.rect.centery
		zombie.angle = func.get_angle(zombie.x, zombie.y,
			survivor.rect.centerx, survivor.rect.centery)
		zombie.update()

def get_upgrade_cost(weapon, feature):
	feature_level = '{}_level'.format(feature)
	weapon_specs = player_progress.weapons[weapon]
	return weapon_specs[feature_level]*weapon_specs['cost_multiplier']

def pause_menu(screen, survivor, events):
	global current_screen, paused
	
	for event in events:
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		if survivor.health > 0:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					paused = False
			elif 'click' in button3.handleEvent(event):
				paused = False
			elif 'click' in button4.handleEvent(event):
				current_screen = menu_screen
				paused = False
	
	if survivor.health > 0:
		for btn in pause_menu_buttons:
			btn.draw(screen)

def next_wave(screen):
	global total_frames_before
	
	if Zombie.current_wave.alive > 0 and not paused:
		Zombie.current_wave.spawn_zombies(total_frames)
		total_frames_before = total_frames
	else:
		if total_frames - total_frames_before > FPS * 2:
			Zombie.wave_number += 1
			Zombie.current_wave = Wave(Zombie.wave_number)
		else:
			func.text_to_screen(screen, 'Wave {}'.format(Zombie.wave_number+1),
				WIDTH / 2, HEIGHT / 2, size=40)

cursor = pygame.image.load('images/cursor.png')

def show_money():
	font = pygame.font.SysFont('monospace', 35)
	text = font.render('$' + str(Survivor.money), True, (173, 227, 141))
	screen.blit(text, (20, 20))

def update_cost(button, weapon, feature):
	regex = re.compile('\$\d+')
	new_cost = '$' + str(get_upgrade_cost(weapon, feature))
	button.caption = regex.sub(new_cost, button.caption)

def game_screen(*args, **kwargs):
	global total_frames, current_screen, total_frames_before, survivor
	
	screen.blit(bg, (0, 0))
	events = pygame.event.get()
	if not paused:
		pygame.mouse.set_visible(False)
		Zombie.movement(total_frames)
		Blood.update(total_frames)
		BaseClass.List.update(total_frames)
		Bullet.loop(screen, total_frames, survivor)
		if Zombie.current_wave.alive > 0:
			Zombie.current_wave.spawn_zombies(survivor, total_frames)
			total_frames_before = total_frames
		else:
			if total_frames - total_frames_before > FPS * 2:
				Zombie.wave_number += 1
				Zombie.current_wave = Wave(Zombie.wave_number)
			else:
				func.text_to_screen(screen, 'Wave {}'.format(Zombie.wave_number+1),
					WIDTH / 2, HEIGHT / 2, size=40)
		find_path(survivor)
		total_frames += 1
	else:
		pygame.mouse.set_visible(True)
		pause_menu(screen, survivor, events)
	interaction(screen, total_frames, events)
	BaseClass.set_dirty()
	Bullet.set_dirty()
	Blood.draw(screen)
	Bullet.List.draw(screen)
	BaseClass.List.draw(screen)
	display_explosions(screen, paused)
	func.text_to_screen(screen, str(int(survivor.health)), 20, 20,
		color=(30, 255, 20), size=40)
	func.text_to_screen(screen, 'Score: {}'.format(str(survivor.score)),
		20, 70, size=30)
	func.text_to_screen(screen, 'Highscore: {}'.format(str(survivor.max_score)),
		20, 110, size=30)
	if not paused:
		mx, my = pygame.mouse.get_pos()
		screen.blit(cursor, (mx-16, my-16))
	pygame.display.update()
	clock.tick(FPS)

def upgrade_screen(*args, **kwargs):
	global current_screen
	
	glevel_sum = player_progress.weapons[GRENADE]['damage_level']
	
	blevel_sum = player_progress.weapons[BAZOOKA]['explosion_damage_level']
	blevel_sum += player_progress.weapons[BAZOOKA]['accuracy_level']
	blevel_sum += player_progress.weapons[BAZOOKA]['delay_level']
	
	slevel_sum = player_progress.weapons[SHOTGUN]['damage_level']
	slevel_sum += player_progress.weapons[SHOTGUN]['number_of_pellets_level']
	slevel_sum += player_progress.weapons[SHOTGUN]['delay_level']
	
	mlevel_sum = player_progress.weapons[AUTOMATIC]['damage_level']
	mlevel_sum += player_progress.weapons[AUTOMATIC]['accuracy_level']
	mlevel_sum += player_progress.weapons[AUTOMATIC]['delay_level']
	
	plevel_sum = player_progress.weapons[PISTOL]['damage_level']
	plevel_sum += player_progress.weapons[PISTOL]['accuracy_level']
	plevel_sum += player_progress.weapons[PISTOL]['delay_level']
	
	if glevel_sum > 2:
		grenadesButton.bgcolor = DARKGRAY
	
	if blevel_sum > 12:
		bazookaButton.bgcolor = DARKGRAY
	
	if slevel_sum > 10:
		shotgunButton.bgcolor = DARKGRAY
	
	if mlevel_sum > 11:
		machineGunButton.bgcolor = DARKGRAY

	if plevel_sum > 11:
		pistolButton.bgcolor = DARKGRAY
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		if 'click' in backButton.handleEvent(event):
			current_screen = menu_screen
		if plevel_sum < 12:
			if 'click' in pistolButton.handleEvent(event):
				current_screen = upgrade_pistol_screen
		if slevel_sum < 11:
			if 'click' in shotgunButton.handleEvent(event):
				current_screen = upgrade_shotgun_screen
		if mlevel_sum < 12:
			if 'click' in machineGunButton.handleEvent(event):
				current_screen = upgrade_mgun_screen
		if blevel_sum < 13:
			if 'click' in bazookaButton.handleEvent(event):
				current_screen = upgrade_bazooka_screen
		if glevel_sum < 3:
			if 'click' in grenadesButton.handleEvent(event):
				current_screen = upgrade_grenades_screen
	
	screen.blit(bg, (0, 0))
	
	for btn in upgrade_buttons:
		btn.draw(screen)
	
	show_money()
	
	pygame.display.update()

def upgrade_pistol_screen(*args, **kwargs):
	global current_screen
	
	accuracy_cost = get_upgrade_cost(PISTOL, 'accuracy')
	delay_cost = get_upgrade_cost(PISTOL, 'delay')
	damage_cost = get_upgrade_cost(PISTOL, 'damage')
	
	if survivor.money < accuracy_cost:
		upgradePistol1.bgcolor = DARKGRAY
	if survivor.money < delay_cost:
		upgradePistol2.bgcolor = DARKGRAY
	if survivor.money < damage_cost:
		upgradePistol3.bgcolor = DARKGRAY
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		if 'click' in backToUpgradesButton.handleEvent(event):
			current_screen = upgrade_screen
		elif 'click' in upgradePistol1.handleEvent(event):
			if player_progress.weapons[PISTOL]['accuracy_level'] < 4:
				if survivor.money >= accuracy_cost:
					new_accuracy = Bullet.specs['accuracy'][PISTOL] + 0.1
					Bullet.specs['accuracy'][PISTOL] = new_accuracy
					player_progress.update_weapon(PISTOL, accuracy=new_accuracy)
					Survivor.money -= accuracy_cost
					player_progress.update_data(money=Survivor.money)
					player_progress.write()
					update_cost(upgradePistol1, PISTOL, 'accuracy')
		elif 'click' in upgradePistol2.handleEvent(event):
			if player_progress.weapons[PISTOL]['delay_level'] < 4:
				if survivor.money >= delay_cost:
					new_delay = Bullet.specs['delay'][PISTOL] - 0.05
					Bullet.specs['delay'][PISTOL] = new_delay
					player_progress.update_weapon(PISTOL, delay=new_delay)
					Survivor.money -= delay_cost
					player_progress.update_data(money=Survivor.money)
					player_progress.write()
					update_cost(upgradePistol2, PISTOL, 'delay')
		elif 'click' in upgradePistol3.handleEvent(event):
			if player_progress.weapons[PISTOL]['damage_level'] < 4:
				if survivor.money >= damage_cost:
					new_damage = Bullet.specs['damage'][PISTOL] + 10
					Bullet.specs['damage'][PISTOL] = new_damage
					player_progress.update_weapon(PISTOL, damage=new_damage)
					Survivor.money -= damage_cost
					player_progress.update_data(money=Survivor.money)
					player_progress.write()
					update_cost(upgradePistol3, PISTOL, 'damage')
	
	screen.blit(bg, (0, 0))
	
	if player_progress.weapons[PISTOL]['accuracy_level'] < 4:
		upgradePistol1.draw(screen)
	if player_progress.weapons[PISTOL]['delay_level'] < 4:
		upgradePistol2.draw(screen)
	if player_progress.weapons[PISTOL]['damage_level'] < 4:
		upgradePistol3.draw(screen)
	backToUpgradesButton.draw(screen)
	
	show_money()
	
	pygame.display.update()

def upgrade_shotgun_screen(*args, **kwargs):
	global current_screen
	
	pellets_cost = get_upgrade_cost(SHOTGUN, 'number_of_pellets')
	delay_cost = get_upgrade_cost(SHOTGUN, 'delay')
	damage_cost = get_upgrade_cost(SHOTGUN, 'damage')
	
	if survivor.money < delay_cost:
		upgradeShotgun1.bgcolor = DARKGRAY
	if survivor.money < damage_cost:
		upgradeShotgun2.bgcolor = DARKGRAY
	if survivor.money < pellets_cost:
		upgradeShotgun3.bgcolor = DARKGRAY
	if survivor.money < 2000:
		buyShotgunButton.bgcolor = DARKGRAY
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		if 'click' in backToUpgradesButton.handleEvent(event):
			current_screen = upgrade_screen
		if SHOTGUN in Survivor.available_weapons:
			if 'click' in upgradeShotgun1.handleEvent(event):
				if survivor.money >= delay_cost:
					if player_progress.weapons[SHOTGUN]['delay_level'] < 4:
						new_delay = Bullet.specs['delay'][SHOTGUN] - 0.05
						Bullet.specs['delay'][SHOTGUN] = new_delay
						player_progress.update_weapon(SHOTGUN, delay=new_delay)
						Survivor.money -= delay_cost
						player_progress.update_data(money=Survivor.money)
						player_progress.write()
						update_cost(upgradeShotgun1, SHOTGUN, 'delay')
			elif 'click' in upgradeShotgun2.handleEvent(event):
				if survivor.money >= damage_cost:
					if player_progress.weapons[SHOTGUN]['damage_level'] < 4:
						new_damage = Bullet.specs['damage'][SHOTGUN] + 5
						Bullet.specs['damage'][SHOTGUN] = new_damage
						player_progress.update_weapon(SHOTGUN, damage=new_damage)
						Survivor.money -= damage_cost
						player_progress.update_data(money=Survivor.money)
						player_progress.write()
						update_cost(upgradeShotgun2, SHOTGUN, 'damage')
			elif 'click' in upgradeShotgun3.handleEvent(event):
				if survivor.money >= pellets_cost:
					if player_progress.weapons[SHOTGUN]['number_of_pellets_level'] < 3:
						new_num = player_progress.weapons[SHOTGUN]['number_of_pellets'] + 1
						player_progress.update_weapon(SHOTGUN, number_of_pellets=new_num)
						Survivor.money -= pellets_cost
						player_progress.update_data(money=Survivor.money)
						player_progress.write()
						update_cost(upgradeShotgun3, SHOTGUN, 'number_of_pellets')
		else:
			if 'click' in buyShotgunButton.handleEvent(event):
				if Survivor.money >= 2000:
					Survivor.available_weapons.append(SHOTGUN)
					player_progress.update_weapon(SHOTGUN, available='true')
					Survivor.money -= 2000
					player_progress.update_data(money=Survivor.money)
					player_progress.write()
	
	screen.blit(bg, (0, 0))
	
	if SHOTGUN in Survivor.available_weapons:
		if player_progress.weapons[SHOTGUN]['delay_level'] < 4:
			upgradeShotgun1.draw(screen)
		if player_progress.weapons[SHOTGUN]['damage_level'] < 4:
			upgradeShotgun2.draw(screen)
		if player_progress.weapons[SHOTGUN]['number_of_pellets_level'] < 3:
			upgradeShotgun3.draw(screen)
		backToUpgradesButton.draw(screen)
	else:
		buyShotgunButton.draw(screen)
		backToUpgradesButton.draw(screen)
	
	show_money()
	
	pygame.display.update()

def upgrade_mgun_screen(*args, **kwargs):
	global current_screen
	
	accuracy_cost = get_upgrade_cost(AUTOMATIC, 'accuracy')
	delay_cost = get_upgrade_cost(AUTOMATIC, 'delay')
	damage_cost = get_upgrade_cost(AUTOMATIC, 'damage')
	
	if survivor.money < delay_cost:
		upgradeMGun1.bgcolor = DARKGRAY
	if survivor.money < damage_cost:
		upgradeMGun2.bgcolor = DARKGRAY
	if survivor.money < accuracy_cost:
		upgradeMGun3.bgcolor = DARKGRAY
	if survivor.money < 5000:
		buyMGunButton.bgcolor = DARKGRAY
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		if 'click' in backToUpgradesButton.handleEvent(event):
			current_screen = upgrade_screen
		if AUTOMATIC in Survivor.available_weapons:
			if 'click' in upgradeMGun1.handleEvent(event):
				if survivor.money >= delay_cost:
					if player_progress.weapons[AUTOMATIC]['delay_level'] < 4:
						new_delay = Bullet.specs['delay'][AUTOMATIC] - 0.04
						Bullet.specs['delay'][AUTOMATIC] = new_delay
						player_progress.update_weapon(AUTOMATIC, delay=new_delay)
						Survivor.money -= delay_cost
						player_progress.update_data(money=Survivor.money)
						player_progress.write()
			elif 'click' in upgradeMGun2.handleEvent(event):
				if survivor.money >= damage_cost:
					if player_progress.weapons[AUTOMATIC]['damage_level'] < 4:
						new_damage = Bullet.specs['damage'][AUTOMATIC] + 3
						Bullet.specs['damage'][AUTOMATIC] = new_damage
						player_progress.update_weapon(AUTOMATIC, damage=new_damage)
						Survivor.money -= damage_cost
						player_progress.update_data(money=Survivor.money)
						player_progress.write()
			elif 'click' in upgradeMGun3.handleEvent(event):
				if survivor.money >= accuracy_cost:
					if player_progress.weapons[AUTOMATIC]['accuracy_level'] < 4:
						new_accuracy = Bullet.specs['accuracy'][AUTOMATIC] + 0.025
						player_progress.update_weapon(AUTOMATIC, accuracy=new_accuracy)
						Survivor.money -= accuracy_cost
						player_progress.update_data(money=Survivor.money)
						player_progress.write()
		else:
			if 'click' in buyMGunButton.handleEvent(event):
				if survivor.money >= 5000:
					Survivor.money -= 5000
					Survivor.available_weapons.append(AUTOMATIC)
					player_progress.update_data(money=Survivor.money)
					player_progress.update_weapon(AUTOMATIC, available='true')
					player_progress.write()
	
	screen.blit(bg, (0, 0))
	
	if AUTOMATIC in Survivor.available_weapons:
		if player_progress.weapons[AUTOMATIC]['delay_level'] < 4:
			upgradeMGun1.draw(screen)
		if player_progress.weapons[AUTOMATIC]['damage_level'] < 4:
			upgradeMGun2.draw(screen)
		if player_progress.weapons[AUTOMATIC]['accuracy_level'] < 4:
			upgradeMGun3.draw(screen)
		backToUpgradesButton.draw(screen)
	else:
		buyMGunButton.draw(screen)
		backToUpgradesButton.draw(screen)
	
	show_money()
	
	pygame.display.update()

def upgrade_bazooka_screen(*args, **kwargs):
	global current_screen
	
	accuracy_cost = get_upgrade_cost(BAZOOKA, 'accuracy')
	delay_cost = get_upgrade_cost(BAZOOKA, 'delay')
	explosion_damage_cost = get_upgrade_cost(BAZOOKA, 'explosion_damage')
	
	if survivor.money < delay_cost:
		upgradeBazooka1.bgcolor = DARKGRAY
	if survivor.money < explosion_damage_cost:
		upgradeBazooka2.bgcolor = DARKGRAY
	if survivor.money < accuracy_cost:
		upgradeBazooka3.bgcolor = DARKGRAY
	if survivor.money < 12000:
		buyBazookaButton.bgcolor = DARKGRAY
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		if 'click' in backToUpgradesButton.handleEvent(event):
			current_screen = upgrade_screen
		if BAZOOKA in Survivor.available_weapons:
			if 'click' in upgradeBazooka1.handleEvent(event):
				if survivor.money >= delay_cost:
					if player_progress.weapons[BAZOOKA]['delay_level'] < 4:
						new_delay = Bullet.specs['delay'][BAZOOKA] - 0.5
						Bullet.specs['delay'][BAZOOKA] = new_delay
						player_progress.update_weapon(BAZOOKA, delay=new_delay)
						Survivor.money -= delay_cost
						player_progress.update_data(money=Survivor.money)
						player_progress.write()
			elif 'click' in upgradeBazooka2.handleEvent(event):
				if survivor.money >= explosion_damage_cost:
					if player_progress.weapons[BAZOOKA]['explosion_damage_level'] < 5:
						new_damage = player_progress.weapons[BAZOOKA]['explosion_damage'] + 50
						player_progress.weapons[BAZOOKA]['explosion_damage'] = new_damage
						player_progress.update_weapon(BAZOOKA, explosion_damage=new_damage)
						Survivor.money -= explosion_damage_cost
						player_progress.update_data(money=Survivor.money)
						player_progress.write()
			elif 'click' in upgradeBazooka3.handleEvent(event):
				if survivor.money >= accuracy_cost:
					if player_progress.weapons[BAZOOKA]['accuracy_level'] < 4:
						new_accuracy = Bullet.specs['accuracy'][BAZOOKA] + 0.1
						player_progress.update_weapon(BAZOOKA, accuracy=new_accuracy)
						Survivor.money -= accuracy_cost
						player_progress.update_data(money=Survivor.money)
						player_progress.write()
		else:
			if 'click' in buyBazookaButton.handleEvent(event):
				if survivor.money >= 12000:
					Survivor.money -= 12000
					Survivor.available_weapons.append(BAZOOKA)
					player_progress.update_data(money=Survivor.money)
					player_progress.update_weapon(BAZOOKA, available='true')
					player_progress.write()
	
	screen.blit(bg, (0, 0))
	
	if BAZOOKA in Survivor.available_weapons:
		if player_progress.weapons[BAZOOKA]['delay_level'] < 4:
			upgradeBazooka1.draw(screen)
		if player_progress.weapons[BAZOOKA]['explosion_damage_level'] < 5:
			upgradeBazooka2.draw(screen)
		if player_progress.weapons[BAZOOKA]['accuracy_level'] < 4:
			upgradeBazooka3.draw(screen)
		backToUpgradesButton.draw(screen)
	else:
		buyBazookaButton.draw(screen)
		backToUpgradesButton.draw(screen)

	show_money()
		
	pygame.display.update()

def upgrade_grenades_screen(*args, **kwargs):
	global current_screen
	
	damage_cost = get_upgrade_cost(GRENADE, 'damage')
	
	if survivor.money < damage_cost:
		upgradeGrenades1.bgcolor = DARKGRAY
	if survivor.money < 8000:
		buyGrenadesButton.bgcolor = DARKGRAY
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		if 'click' in backToUpgradesButton.handleEvent(event):
			current_screen = upgrade_screen
		if player_progress.weapons[GRENADE]['available']:
			if 'click' in upgradeGrenades1.handleEvent(event):
				if survivor.money >= damage_cost:
					if player_progress.weapons[GRENADE]['damage_level'] < 3:
						new_damage = player_progress.weapons[GRENADE]['damage'] + 20
						player_progress.weapons[GRENADE]['damage'] = new_damage
						player_progress.update_weapon(GRENADE, damage=new_damage)
						Survivor.money -= damage_cost
						player_progress.update_data(money=Survivor.money)
						player_progress.write()
						Grenade.damage = new_damage
		else:
			if 'click' in buyGrenadesButton.handleEvent(event):
				if survivor.money >= 8000:
					Survivor.money -= 8000
					player_progress.update_data(money=Survivor.money)
					player_progress.update_weapon(GRENADE, available='true')
					player_progress.write()
	
	screen.blit(bg, (0, 0))
	
	if player_progress.weapons[GRENADE]['available']:
		if player_progress.weapons[GRENADE]['damage_level'] < 3:
			upgradeGrenades1.draw(screen)
	else:
		buyGrenadesButton.draw(screen)
	backToUpgradesButton.draw(screen)
	
	show_money()
	
	pygame.display.update()

def reset_game():
	global survivor
	Blood.List = []
	Wave.reset()
	BaseClass.List.empty()
	Zombie.List.empty()
	Zombie.current_wave = Wave(1)
	Zombie.wave_number = 1
	Character.List.empty()
	Bullet.List.empty()
	survivor = Survivor(WIDTH / 2, HEIGHT / 2)
	Survivor.score = 0

def menu_screen(*args, **kwargs):
	global current_screen, survivor
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		if 'click' in button1.handleEvent(event):
			reset_game()
			current_screen = game_screen
		elif 'click' in quitButton.handleEvent(event):
			pygame.quit()
			sys.exit(0)
	screen.blit(bg, (0, 0))
	for btn in menu_buttons:
		btn.draw(screen)
	pygame.display.update()
	clock.tick(FPS)

current_screen = upgrade_screen

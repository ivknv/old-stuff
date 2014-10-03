#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom import minidom

PISTOL_TAG = 'Pistol'
SHOTGUN_TAG = 'Shotgun'
MACHINEGUN_TAG = 'MachineGun'
BAZOOKA_TAG = 'Bazooka'
AVAILABLE_ATTR = 'available'
COST_ATTR = 'cost'
GRENADE_TAG = 'Grenade'
MONEY_TAG = 'Money'
MAX_SCORE_TAG = 'MaxScore'
MAX_HEALTH_TAG = 'MaxHealth'
ROOT_TAG = 'GameProgress'
WEAPONS_TAG = 'Weapons'
DAMAGE_TAG = 'Damage'
ACCURACY_TAG = 'Accuracy'
NUMBER_OF_PELLETS_TAG = 'NumberOfPellets'
DELAY_TAG = 'Delay'
EXPLOSION_DAMAGE_TAG = 'ExplosionDamage'
COST_MULTIPLIER_TAG = 'CostMultiplier'
LEVEL_ATTR = 'level'
INT_VALUE, FLOAT_VALUE, BOOLEAN_VALUE = 0, 1, 2

class Node(dict):
	def __init__(self, tag, attrs, *value):
		self.content = value
		self.tag = tag
		self.attrs = attrs
		self.parent = None
		self.set_parents()
		super(Node, self).__init__({
			'content': self.content, 'tag': tag,
			'attrs': self.attrs, 'parent': self.parent})
		self.all_content = [self] + list(self.content)
	
	def set_parents(self):
		for node in self.content:
			if isinstance(node, Node):
				node.parent = self
				node.set_parents()
	
	def __repr__(self):
		return '<Node {}>'.format(self.tag)

def get_attibute_value(element, attr, default=None):
	node = element.attributes.get(attr, default)
	if node is not None:
		return node.nodeValue

class GameProgress(object):
	filename = 'progress.xml'
	map = Node(ROOT_TAG, {},
		Node(MAX_HEALTH_TAG, {}, INT_VALUE),
		Node(MAX_SCORE_TAG, {}, INT_VALUE),
		Node(MONEY_TAG, {}, INT_VALUE),
		Node(WEAPONS_TAG, {},
			Node(PISTOL_TAG,
				{AVAILABLE_ATTR: BOOLEAN_VALUE, COST_ATTR: INT_VALUE},
				Node(DAMAGE_TAG, {LEVEL_ATTR: INT_VALUE}, INT_VALUE),
				Node(DELAY_TAG, {LEVEL_ATTR: INT_VALUE}, FLOAT_VALUE),
				Node(ACCURACY_TAG, {LEVEL_ATTR: INT_VALUE}, FLOAT_VALUE),
				Node(COST_MULTIPLIER_TAG, {}, INT_VALUE)),
			Node(SHOTGUN_TAG,
				{AVAILABLE_ATTR: BOOLEAN_VALUE, COST_ATTR: INT_VALUE},
				Node(DAMAGE_TAG, {LEVEL_ATTR: INT_VALUE}, INT_VALUE),
				Node(DELAY_TAG, {LEVEL_ATTR: INT_VALUE}, FLOAT_VALUE),
				Node(ACCURACY_TAG, {}, FLOAT_VALUE),
				Node(NUMBER_OF_PELLETS_TAG, {LEVEL_ATTR: INT_VALUE}, INT_VALUE),
				Node(COST_MULTIPLIER_TAG, {}, FLOAT_VALUE)),
			Node(MACHINEGUN_TAG,
				{AVAILABLE_ATTR: BOOLEAN_VALUE, COST_ATTR: INT_VALUE},
				Node(DAMAGE_TAG, {LEVEL_ATTR: INT_VALUE}, INT_VALUE),
				Node(DELAY_TAG, {LEVEL_ATTR: INT_VALUE}, FLOAT_VALUE),
				Node(ACCURACY_TAG, {LEVEL_ATTR: INT_VALUE}, FLOAT_VALUE),
				Node(COST_MULTIPLIER_TAG, {}, FLOAT_VALUE)),
			Node(BAZOOKA_TAG,
				{AVAILABLE_ATTR: BOOLEAN_VALUE, COST_ATTR: INT_VALUE},
				Node(DAMAGE_TAG, {LEVEL_ATTR: INT_VALUE}, INT_VALUE),
				Node(DELAY_TAG, {LEVEL_ATTR: INT_VALUE}, FLOAT_VALUE),
				Node(ACCURACY_TAG, {LEVEL_ATTR: INT_VALUE}, FLOAT_VALUE),
				Node(EXPLOSION_DAMAGE_TAG, {LEVEL_ATTR: INT_VALUE}, INT_VALUE),
				Node(COST_MULTIPLIER_TAG, {}, FLOAT_VALUE)),
			Node(GRENADE_TAG,
				{AVAILABLE_ATTR: BOOLEAN_VALUE, COST_ATTR: INT_VALUE},
				Node(DAMAGE_TAG, {LEVEL_ATTR: INT_VALUE}, INT_VALUE),
				Node(DELAY_TAG, {}, FLOAT_VALUE),
				Node(COST_MULTIPLIER_TAG, {}, FLOAT_VALUE))))
	
	def __init__(self):
		self.xmldata = minidom.parse(GameProgress.filename)
		self.max_health = None
		self.max_score = None
		self.money = None
		self.weapons = []
		self.parse_xml()
		self.available_weapons = filter(lambda x: x['available'], self.weapons)
	
	def toxml(self):
		return self.xmldata.toxml()
	
	def write(self, output_file=None):
		if output_file is None:
			output_file = GameProgress.filename
		xml = self.xmldata.toxml()
		f = open(output_file, 'w')
		f.write(xml)
		f.close()
	
	def update_data(self, max_health=None, max_score=None, money=None):
		if max_health is None:
			max_health = self.max_health
		if max_score is None:
			max_score = self.max_score
		if money is None:
			money = self.money
		
		element = self.xmldata.getElementsByTagName(MAX_HEALTH_TAG)[0]
		element.firstChild.nodeValue = str(max_health)
		self.max_health = max_health

		element = self.xmldata.getElementsByTagName(MAX_SCORE_TAG)[0]
		element.firstChild.nodeValue = str(max_score)
		self.max_score = max_score

		element = self.xmldata.getElementsByTagName(MONEY_TAG)[0]
		element.firstChild.nodeValue = str(money)
		self.money = money
	
	def update_weapon(self, weapon, **specs):
		tag = None
		for w in self.weapons:
			if w['type'] == weapon:
				tag = w['tag']
				break
		
		if tag is None:
			raise Exception('Unknown weapon type')
		
		if 'accuracy' in specs:
			weapon_element = self.xmldata.getElementsByTagName(tag)[0]
			element = weapon_element.getElementsByTagName(ACCURACY_TAG)[0]
			element.firstChild.nodeValue = str(specs['accuracy'])
			w['accuracy'] = specs['accuracy']
			if w['accuracy_level'] is not None:
				w['accuracy_level'] += 1
				element.setAttribute('level', str(w['accuracy_level']))
		if 'available' in specs:
			element = self.xmldata.getElementsByTagName(tag)[0]
			element.setAttribute(AVAILABLE_ATTR, str(specs['available']).lower())
			w['available'] = specs['available'] == 'true'
			if w['available']:
				self.available_weapons.append(w)
		if 'damage' in specs:
			weapon_element = self.xmldata.getElementsByTagName(tag)[0]
			element = weapon_element.getElementsByTagName(DAMAGE_TAG)[0]
			element.firstChild.nodeValue = str(specs['damage'])
			w['damage'] = specs['damage']
			if w['damage_level'] is not None:
				w['damage_level'] += 1
				element.setAttribute('level', str(w['damage_level']))
		if 'delay' in specs:
			weapon_element = self.xmldata.getElementsByTagName(tag)[0]
			element = weapon_element.getElementsByTagName(DELAY_TAG)[0]
			element.firstChild.nodeValue = str(specs['delay'])
			w['delay'] = specs['delay']
			if w['delay_level'] is not None:
				w['delay_level'] += 1
				element.setAttribute('level', str(w['delay_level']))
		if 'number_of_pellets' in specs:
			weapon_element = self.xmldata.getElementsByTagName(tag)[0]
			element = weapon_element.getElementsByTagName(NUMBER_OF_PELLETS_TAG)[0]
			element.firstChild.nodeValue = str(specs['number_of_pellets'])
			w['number_of_pellets'] = specs['number_of_pellets']
			w['number_of_pellets_level'] += 1
			element.setAttribute('level', str(w['number_of_pellets_level']))
				
		if 'explosion_damage' in specs:
			weapon_element = self.xmldata.getElementsByTagName(tag)[0]
			element = weapon_element.getElementsByTagName(EXPLOSION_DAMAGE_TAG)[0]
			element.firstChild.nodeValue = str(specs['explosion_damage'])
			w['explosion_damage'] = specs['explosion_damage']
			w['explosion_damage_level'] += 1
			element.setAttribute('level', str(w['explosion_damage_level']))
	
	def parse_xml(self, nodes=None, dnodes=None):
		if dnodes is None:
			dnodes = self.xmldata.childNodes
		if nodes is None:
			nodes = [GameProgress.map]
		
		for node, dnode in zip(nodes, dnodes):
			if node.tag != dnode.tagName:
				message = '''Invalid document structure.
Expected {} but got <Node {}>'''.format(node, dnode.tagName)
				raise Exception(message)
			
			if dnode.tagName == MAX_HEALTH_TAG:
				self.max_health = int(dnode.firstChild.nodeValue)
			elif dnode.tagName == MAX_SCORE_TAG:
				self.max_score = int(dnode.firstChild.nodeValue)
			elif dnode.tagName == MONEY_TAG:
				self.money = int(dnode.firstChild.nodeValue)
			elif dnode.tagName in [PISTOL_TAG, SHOTGUN_TAG, MACHINEGUN_TAG,
				BAZOOKA_TAG, GRENADE_TAG]:
				if dnode.tagName == PISTOL_TAG:
					num = 0
				elif dnode.tagName == SHOTGUN_TAG:
					num = 1
				elif dnode.tagName == MACHINEGUN_TAG:
					num = 2
				elif dnode.tagName == BAZOOKA_TAG:
					num = 3
				elif dnode.tagName == GRENADE_TAG:
					num = 4
				
				is_available = get_attibute_value(dnode, 'available')
				if is_available is None:
					message = "Missing 'available' attribute at <Node {}>"
					raise Exception(message.format(dnode.tagName))
				
				if is_available == 'true':
					self.weapons.append({'type': num, 'available': True,
						'tag': dnode.tagName})
				elif is_available == 'false':
					self.weapons.append({'type': num, 'available': False,
						'tag': dnode.tagName})
				else:
					message = "Invalid value for 'available' at <Node {}>"
					raise Exception(message.format(dnode.tagName))
			elif dnode.tagName == DAMAGE_TAG:
				level = get_attibute_value(dnode, LEVEL_ATTR)
				if level is not None:
					level = int(level)
				self.weapons[-1]['damage'] = int(dnode.firstChild.nodeValue)
				self.weapons[-1]['damage_level'] = level
			elif dnode.tagName == ACCURACY_TAG:
				level = get_attibute_value(dnode, LEVEL_ATTR)
				if level is not None:
					level = int(level)
				self.weapons[-1]['accuracy'] = float(dnode.firstChild.nodeValue)
				self.weapons[-1]['accuracy_level'] = level
			elif dnode.tagName == DELAY_TAG:
				level = get_attibute_value(dnode, LEVEL_ATTR)
				if level is not None:
					level = int(level)
				self.weapons[-1]['delay'] = float(dnode.firstChild.nodeValue)
				self.weapons[-1]['delay_level'] = level
			elif dnode.tagName == NUMBER_OF_PELLETS_TAG:
				level = get_attibute_value(dnode, LEVEL_ATTR)
				if level is not None:
					level = int(level)
				self.weapons[-1]['number_of_pellets'] = int(dnode.firstChild.nodeValue)
				self.weapons[-1]['number_of_pellets_level'] = level
			elif dnode.tagName == EXPLOSION_DAMAGE_TAG:
				level = get_attibute_value(dnode, LEVEL_ATTR)
				if level is not None:
					level = int(level)
				self.weapons[-1]['explosion_damage'] = int(dnode.firstChild.nodeValue)
				self.weapons[-1]['explosion_damage_level'] = level
			elif dnode.tagName == COST_MULTIPLIER_TAG:
				cost_multiplier = int(dnode.firstChild.nodeValue)
				self.weapons[-1]['cost_multiplier'] = cost_multiplier
			
			self.parse_xml(filter(lambda x: isinstance(node, Node), node.content),
				filter(lambda x: x.nodeType != x.TEXT_NODE, dnode.childNodes))

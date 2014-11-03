#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TechParser import habrahabr
from TechParser import venturebeat
from TechParser import engadget
from TechParser import techcrunch
from TechParser import techrepublic
from TechParser import readwrite
from TechParser import smashingmagazine
from TechParser import gizmodo
from TechParser import slashdot
from TechParser import androidcentral
from TechParser import verge
from TechParser import topdesignmag
from TechParser import flowa
from TechParser import ittoolbox
from TechParser import dzone
from TechParser import codeproject
from TechParser import hackernews
from TechParser import mashable
from TechParser import maketecheasier
from TechParser import digg
from TechParser import wired
from TechParser import medium
from TechParser import planetclojure
from TechParser import reddit
from TechParser import trashbox
from TechParser import droider
from TechParser import redroid
from TechParser import threednews
from TechParser import ixbt
from TechParser import mobilereview
from TechParser import helpix
from TechParser import recode
from TechParser import zdnet
from TechParser import geektimes

sites_to_parse = {
	"Habrahabr": { # habrahabr.ru
		"module": habrahabr,
		"kwargs": {"hubs": ['programming', 'python', 'javascript', 'c',
			'webdev', 'linux', 'open_source', 'development', 'web_design',
			'mobile', 'css', 'html5', 'crazydev', 'jquery', 'funcprog']}
	},
	
	"VentureBeat": { # venturebeat.com
		"module": venturebeat,
		"kwargs": {}
	},
	
	"Engadget": { # engadget.com
		"module": engadget,
		"kwargs": {}
	},
	
	"Slashdot": { # slashdot.org
		"module": slashdot,
		"kwargs": {}
	},
	
	"Gizmodo": { # gizmodo.com
		"module": gizmodo,
		"kwargs": {}
	},
	
	"TechCrunch": { # techcrunch.com
		"module": techcrunch,
		"kwargs": {}
	},
	
	"Read/Write Web": { # readwrite.com
		"module": readwrite,
		"kwargs": {}
	},
	
	"Tech Republic": { # techrepublic.com
		"module": techrepublic,
		"kwargs": {}
	},
	
	"Smashing Magazine": { # www.smashingmagazine.com
		"module": smashingmagazine,
		"kwargs": {}
	},
	
	"Android Central": { # www.androidcentral.com
		"module": androidcentral,
		"kwargs": {}
	},
	
	"The Verge": { # www.theverge.com
		"module": verge,
		"kwargs": {}
	},
	
	"Top Design Magazine": { # www.topdesignmag.com
		"module": topdesignmag,
		"kwargs": {}
	},
	
	"Flowa": { # flowa.fi
		"module": flowa,
		"kwargs": {}
	},
	
	"IT Toolbox": { # it.toolbox.com
		"module": ittoolbox,
		"kwargs": {}
	},
	
	"DZone": { # www.dzone.com
		"module": dzone,
		"kwargs": {}
	},
	
	"Code Project": { # www.codeproject.com
		"module": codeproject,
		"kwargs": {'categories': ['android', 'web']}
	},
	
	"Hacker News": { # news.ycombinator.com
		"module": hackernews,
		"kwargs": {}
	},
	
	"Mashable": { # mashable.com
		"module": mashable,
		"kwargs": {}
	},
	
	"Make Tech Easier": { # www.maketecheasier.com
		"module": maketecheasier,
		"kwargs": {}
	},
	
	"Digg": { # digg.com
		"module": digg,
		"kwargs": {}
	},
	
	"Wired": { # www.wired.com
		"module": wired,
		"kwargs": {}
	},
	
	"Medium": { # medium.com
		"module": medium,
		"kwargs": {"collections": ["programming-stories",
			"python-programming-language",
			"programming-ideas-tutorial-and-experience",
			"software-development-2", "developer-developers-developers",
			"web-design-and-development", "desenvolvimento-web",
			"web-development-9", "coding-design", "cool-code-pal",
			"html-css-and-happiness", "html-css", "front-end-developers",
			"web-design-tutorials", "written-in-code", "ui-designs",
			"design-creativity-1", "this-could-be-better",
			"user-experience-design-1", "design-ui-and-shenanigans"]}
	},
	
	"Planet Clojure": { # planet.clojure.in
		"module": planetclojure,
		"kwargs": {}
	},
	
	"Reddit": { # www.reddit.com
		"module": reddit,
		"kwargs": {"reddits": ["tech", "programming",
			"clojure", "python", "html", "css",
			"html5", "java", "javascript", "google",
			"django", "functionalprogramming"]}
	},
	
	"Trashbox": { # trashbox.ru
		"module": trashbox,
		"kwargs": {}
	},
	
	"Droider": { # droider.ru
		"module": droider,
		"kwargs": {}
	},
	
	"Redroid": { # redroid.ru
		"module": redroid,
		"kwargs": {}
	},
	
	"3DNews": { # www.3dnews.ru
		"module": threednews,
		"kwargs": {}
	},
	
	"IXBT": { # www.ixbt.ru
		"module": ixbt,
		"kwargs": {}
	},
	
	"Mobile Review": { # mobile-review.com
		"module": mobilereview,
		"kwargs": {}
	},
	
	"Helpix": { # helpix.ru
		"module": helpix,
		"kwargs": {}
	},
	
	"Re/code": { # recode.net
		"module": recode,
		"kwargs": {}
	},
	
	"ZDNet": { # www.zdnet.com
		"module": zdnet,
		"kwargs": {'categories': ['reviews', 'news']}
	},
	
	"Geektimes": { # geektimes.ru
		"module": geektimes,
		"kwargs": {'hubs': ['android', 'hr', 'yandex', 'history', 'google',
			'soft', 'infographics', 'browsers', 'smartphones', 'geektimes',
			'iTablet', 'business-laws', 'os', 'internet_of_things',
			'design', 'gmail', 'statistics', 'internet_regulation',
			'mailru', 'youtube', 'cpu', 'linux', 'announcements', 'closet',
			'mozilla', 'wikipedia', 'cyberpunk', 'ascii', 'e_gov', 'rkn']}
	}
}

rss_feeds = {'CSS-tricks': {
		'short-name': 'css-tricks',
		'url': 'http://feeds.feedburner.com/CssTricks?format=xml',
		'icon': 'http://css-tricks.com/favicon.ico',
		'color': '#DA8817'
	},
	
	'The Next Web':	{
		'url': 'http://feeds2.feedburner.com/thenextweb',
		'short-name': 'nextweb',
		'icon': 'http://thenextweb.com/favicon.ico',
		'color': '#F15A2F'
	},
	
	'XKCD': {
		'url': 'http://xkcd.com/rss.xml',
		'short-name': 'xkcd',
		'icon': 'http://xkcd.com/favicon.ico',
		'color': '#000'
	}
}

filters = {
	"All": {
		"has": [],
		"or": [],
		"not": []
	}
}

interesting_words = {('python', 10.0), ('django', 2.0), ('css3', 3.0),
	'javascript', 'android', 'clojure', ('google', 3.0), 'jquery',
	('fortran', 10.0), ('forth', 7.0), ('linux', 10.0), 'unix', ('html5', 3.0),
	'bash', 'web', 'development', 'programming', 'ibm', ('sass', 3.0),
	('c', 2.0), ('gtk', 1.5), 'yandex', 'яндекс', 'postgresql', 'git',
	('cython', 3.0), 'functional programming', 'xml', 'assembler',
	'youtube', 'algorithm', 'optimisation', ('vim', 5.0)}

boring_words = {('php', 3.0), 'ruby', ('microsoft', 2.0), ('apple', 5.0),
	'mysql', 'iphone', 'ipad', 'ios', 'mercurial', 'subversion', ('.net', 3.0),
	('joomla', 2.0), ('wordpress', 2.0), 'ruby on rails', 'delphi', 'pascal'}

update_interval = 1800 # Parse articles every 30 minutes

db = 'postgresql'
host = "0.0.0.0" # Server host
port = "8080" # Server port

num_threads = 3 # Number of threads for parsing articles

# Server to use
server = "tornado" # See http://bottlepy.org/docs/dev/deployment.html#switching-the-server-backend

save_articles = True # Save articles into db.
# Can be found at ~/.tech-parser/archive.db

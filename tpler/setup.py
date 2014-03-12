#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name="tpler",
version="1.3",
author="Ivan Konovalov",
author_email="rvan.mega@gmail.com",
description="A templater",
packages=["tpler"],
package_data={"tpler": ["templates/*"]})

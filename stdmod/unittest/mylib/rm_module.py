#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

def rm(filename):
    if os.path.isfile(filename):
        os.remove(filename)


class ProductionClass():
    def method(self):
        return 100

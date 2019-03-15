# -*- coding: UTF-8 -*-
"""
Created on 2018-01-16

@author: hcz
"""

from tabulate import tabulate

table = [["spamtest", 42], ["egg", 451], ["ba\ncon", 0]]
headers = ["item", "qty"]

print "plain:"
print tabulate(table, headers, tablefmt="plain")

print "simple:"
print tabulate(table, headers, tablefmt="simple")

print "grid:"
print tabulate(table, headers, tablefmt="grid")

print "fancy_grid:"
print tabulate(table, headers, tablefmt="fancy_grid")
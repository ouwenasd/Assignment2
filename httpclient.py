#! /usr/bin/env python
# Copyright 2014 Ouwen Zha
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# This is the code for CS410 Assignment2
#


# name:               Ouwen Zha
# Unix id:            ouwen
# lecture section:    A1
# instructor's name:  Abram Hindle
# lab section:        H01
# TA's name:          li Sajedi Badashian 
# Homework:           A2
# Date:               Februrary 3, 2014
# Collaboration:      None
# External source:    None 

import sys
import socket

def help():
    	print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    	def __init__(self, code=200, body=""):
        	self.code = int(code)
        	self.body = body
		print self.code
		print self.body

class HTTPClient(object):
	# get the host ,port and path from url
    	def get_host_port_path(self,url):
		url_array = url.split('/')
		host_port = url_array[2]
		host_port_array = host_port.split(':')
		# get the host
		host = host_port_array[0]
		# if url contains port
		if len(host_port_array) == 2:
			port = host_port_array[1]
		else:
			# the default port
			port = 80
		# get the path
		path = '/'.join(url_array[3:])
		path = '/'+path
		return (host,port,path)

	# connect the server
	def connect(self, host, port):
		# change port to integer
		port = int(port)
        	try:
    			#create an AF_INET, STREAM socket (TCP)
    			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error:
    			print ('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
   			sys.exit();      
		try:
			# get the ip of host
    			remote_ip = socket.gethostbyname( host )
		except socket.gaierror:
    			#could not resolve
    			print ('Hostname could not be resolved. Exiting')
    			sys.exit()
		#Connect to remote server
		s.connect((remote_ip , port))
        	return s

	# get the code from data
    	def get_code(self, data):
		data_array = data.split(' ')
		code = data_array[1]
        	return code

	# get the header from receive data
    	def get_headers(self,data):
        	data_array = data.split('\r\n')
        	header = data_array[0]
		code = self.get_code(header)
		body = self.get_body(data)
        	return (code,body)

	# get the body from receive data
   	def get_body(self, data):
		data_array = data.split('\r\n\r\n')
		body = data_array[1]
        	return body

    	# read everything from the socket
    	def recvall(self, sock):
       		buffer = bytearray()
        	done = False
        	while not done:
            		part = sock.recv(1024)
            		if (part):
                		buffer.extend(part)
            		else:
                		done = not part
        	return str(buffer)

	# create get request
    	def GET(self, url, args=None):
		# get host, port and path
		host,port,path = self.get_host_port_path(url)
		# use host and port to connect server
		s = self.connect(host,port)
		# create get request
		message = "GET "+path+" HTTP/1.1\r\nHost: "+host+"\r\n\r\n"
		try:
    			# send the request   
    			s.sendall(message.encode("UTF8"))
		except socket.error:
    			#Send failed
    			print ('Send failed')
    			sys.exit()
		# get the receive data
		data = self.recvall(s)
		# get the code and body from receive data
		code,body = self.get_headers(data)
		# close socket
		s.close()  
        	return HTTPRequest(code, body)
	
	# create post request
    	def POST(self, url, args=None):
		new_massage =''
		if args!=None:
			for i in args:
				# get parameter from args
				new_massage = new_massage + i + '=' + args[i] + '&'
			new_massage = new_massage[:-1]
		# get host, port and path from url
		host,port,path = self.get_host_port_path(url)
		# use host and port to connect server
		s = self.connect(host,port)
		# get the content-length
		content_length = len(new_massage)
		# create post request
		message = "POST "+path+" HTTP/1.1\r\nHost: "+host+"\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-length: "+ str(content_length) + '\r\n\r\n'+new_massage
		try:
    			# send request   
    			s.sendall(message.encode("UTF8"))
		except socket.error:
    			# send failed
    			print ('Send failed')
    			sys.exit()
		# receive data
		data = self.recvall(s)
		# get code and body from data
		code,body = self.get_headers(data)
		# close socket
		s.close()  
        	return HTTPRequest(code, body)

    	def command(self, url, command="GET", args=None):
        	if (command == "POST"):
            		return self.POST( url, args )
        	else:
            		return self.GET( url, args )
    
if __name__ == "__main__":
    	client = HTTPClient()
    	command = "GET"
    	if (len(sys.argv) <= 1):
        	help()
        	sys.exit(1)
    	elif (len(sys.argv) == 3):
        	print client.command( sys.argv[2], sys.argv[1] )
    	else:
        	print client.command( sys.argv[1], command ) 

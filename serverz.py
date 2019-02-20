################################################
# @Python-Venom                                #
# All rights reserved: >>>>> Zulqarnain <<<<<  #
# Please do not eidt or remove credits         #
################################################

import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import urlparse
import os



with open('fnamed', 'rU') as docu:
     answer = {}
     for line in docu:	     
	     if not line.startswith("#"):
	             if line.strip():
        	             key, value = line.split(':', 1)
        	             answer[key] = value.split()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
	test = self.path
        try:
	    mainfile = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'html')
	    if self.path.endswith('/'):
            	filename = mainfile + 'index.html'
		with open(filename, 'rb') as fh:
         	    html = fh.read()
                    self.wfile.write(html)	    

            elif 	self.path.endswith(test):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
		if 'favicon' not in test:
		    if '/' in test:
		        test = test.replace('/','')
                    output = ""
		    output += '{"nodes":['
                    output += '{"name": "'+test+'","group":1},'
		    #print (output)
		    test2 = '"'+test+'"'
		    data = answer[eval(test2)]
                    outp = json.dumps(data)
		    outp = outp.replace(',"', '"')
		    #print(outp)
		    #output += ' : '
		    #output += '</br>'
		    #output += '"children": ['
		    #disp = str(answer[test])
		    disp = outp.split(",")
		    i = 0
		    counting = 0
		    for i in range(len(disp)):
		    	#print(i)
			l = disp[i]
			#output += "</br>"
			l = l.replace('[', '')
			l = l.replace('"', '')
			l = l.replace(']', '')
			l = l.replace(',', '')
		        output += '{"name": "'+l+'", "group": 2}'
			if i < len(disp)-1:
				output += ','
			i +=1
		    output += '],"links":['
		    for counting in range(len(disp)+1):
			output += '{"source":0,"target":'+str(counting)+',"weight":'+str(counting)+'}'
			if counting< len(disp):
				output += ','
			counting += 1
		    output += ']}'
		    self.wfile.write(output.encode(encoding = 'utf_8'))
		    #print(output)
		    with open('graphFile.json', 'w') as filehandle:
			filehandle.write(output)

		    return
            
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:
            self.send_response(201)
            print("Sent response")
            self.send_header('Content-type', 'text/html')
            print("Sent headers")
            self.end_headers()
            print("Ended header")
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            print("Parsed headers")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            print("Receiver message content")
            output = ""
            self.wfile.write(output.encode(encoding = 'utf_8'))
            print ("Wrote through CGI")
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('localhost', port), webServerHandler)
        print ("Web Server running on port", port)
        server.serve_forever()
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()

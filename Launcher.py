# Copyright (C) 2019 Andy C. (github.com/xndc)
# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

import sys, os, threading, subprocess
from random import randint
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

LastRetrievedPath = ""

class Handler (SimpleHTTPRequestHandler, object):
    def do_HEAD (self):
        if self.path == "/pdf" and len(sys.argv) > 1:
            filename = sys.argv[1]
            with open(filename, "rb") as file:
                fs = os.fstat(file.fileno())
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Length", str(fs.st_size))
                basename = os.path.basename(filename)
                self.send_header("Content-Disposition", 'attachment; filename="' + basename + '"')
                self.end_headers()
        else:
            super(Handler, self).do_GET()

    def do_GET (self):
        global LastRetrievedPath
        LastRetrievedPath = self.path
        if self.path == "/":
            # If we send Safari straight to the viewer, it will open any existing viewer tab instead of creating a new
            # one. Using a redirect ensures we can open multiple instances of the viewer.
            self.send_response(301)
            self.send_header("Location", "/pdfjs-dist/web/viewer.html")
            self.end_headers()
        if self.path == "/pdf" and len(sys.argv) > 1:
            filename = sys.argv[1]
            with open(filename, "rb") as file:
                fs = os.fstat(file.fileno())
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Length", str(fs.st_size))
                basename = os.path.basename(filename)
                self.send_header("Content-Disposition", 'attachment; filename="' + basename + '"')
                self.end_headers()
                self.copyfile(file, self.wfile)
        else:
            super(Handler, self).do_GET()

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 10733  # 10-PDF
    httpd = HTTPServer((host, port), Handler)
    
    t1 = None
    t2 = None
    # This *should* be enough to quit the script:
    def kill():
        httpd.socket.close() # crashes the main thread, which is good enough for me
        t1.cancel()
        t2.cancel()
    
    # Fallback: we should quit in 30 seconds at most
    t1 = threading.Timer(30.0, kill)
    t1.start()

    # Launch the browser:
    subprocess.call(["/usr/bin/open", "http://127.0.0.1:" + str(port) + "/"])

    while 1:
        if LastRetrievedPath == "/pdf":
            # We want to give pdf.js some time to retrieve icons and whatnot after downloading the file:
            t2 = threading.Timer(3.0, kill)
            t2.start()
        httpd.handle_request()

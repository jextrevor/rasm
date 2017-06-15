import SimpleHTTPServer
import SocketServer

PORT = 8000
handler = SimpleHTTPServer.SimpleHTTPRequestHandler
SocketServer.TCPServer.allow_reuse_address = True
httpd = SocketServer.TCPServer(("127.0.0.1", PORT), handler)
httpd.timeout = None
httpd.handle_request()
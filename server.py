from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3
import cgi
import hashlib

connection = sqlite3.connect('health.db')
cursor = connection.cursor()

table_user = (
    "CREATE TABLE IF NOT EXISTS `users` ("
    "  `user_id` INT AUTO_INCREMENT,"
    "  `username` VARCHAR(50) NOT NULL,"
    "  `password_hashed` VARCHAR(50) NOT NULL,"
    "  PRIMARY KEY (`user_id`))"
)

cursor.execute(table_user)

class SimpleRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path.endswith('/'):
            self._set_response()
            output = ''
            output += '<html><body>'
            output += '<h1>Welcome to Personal Health Record</h1>'
            output += '<h3><a href="/login">Login</a></h3>'
            output += '<h3><a href="/signup">Signup</a></h3>'
            output += '</body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('/home'):
            self._set_response()
            output = ''
            output += '<html><body>'
            output += '<h1>Logged In as</h1>'
            output += '</body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('/login'):
            self._set_response()
            output = ''
            output += '<html><body>'
            output += '<h1>Log In</h1>'
            output += '<form method="POST" enctype="multipart/form-data" action="/login">'
            output += '<input name="username" type="text" placeholder="Enter Username" /><br/>'
            output += '<input name="password" type="password" placeholder="Enter Password" /><br/>'
            output += '<input type="submit" value="Log In" />'
            output += '</form>'
            output += '</body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('/signup'):
            self._set_response()
            output = ''
            output += '<html><body>'
            output += '<h1>Sign Up</h1>'
            output += '<form method="POST" enctype="multipart/form-data" action="/signup">'
            output += '<input name="username" type="text" placeholder="Enter Username" /><br/>'
            output += '<input name="password" type="password" placeholder="Enter Password" /><br/>'
            output += '<input type="submit" value="Sign Up" />'
            output += '</form>'
            output += '</body></html>'
            self.wfile.write(output.encode())

    def do_POST(self):
        if self.path.endswith('/login'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            content_len = int(self.headers.get('content-length'))
            pdict['content-length'] = content_len

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                username = fields.get('username')[0]
                password = fields.get('password')[0]
                password_hashed = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute("SELECT * FROM users WHERE username = ? AND password_hashed = ?", (username, password_hashed))

                if cursor.fetchall():
                    self.send_response(301)
                    self.send_header('content-type', 'text/html')
                    self.send_header('Location', "/home")
                    self.end_headers()

        if self.path.endswith('/signup'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            content_len = int(self.headers.get('content-length'))
            pdict['content-length'] = content_len

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                username = fields.get('username')[0]
                password = fields.get('password')[0]
                password_hashed = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute("INSERT INTO users (username, password_hashed) VALUES (?, ?)", (username, password_hashed))

                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/login')
                self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd server..')


if __name__ == '__main__':
    run()

cursor.close()
connection.close()


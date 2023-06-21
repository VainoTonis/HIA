"""
This file is part of EIA.

EIA is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

EIA is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with EIA. If not, see <https://www.gnu.org/licenses/>. 
"""
from http.server import SimpleHTTPRequestHandler
from threading import Thread
from socketserver import TCPServer
from urllib import parse
from hashlib import sha256
from base64 import urlsafe_b64encode
from secrets import token_bytes, choice
from string import ascii_letters, digits
import webbrowser


clientId = "005c31013efd450baab6adaa11e88c0d"
localCallbackUrl = "http://localhost:8000/callback"
scope = "esi-characters.read_blueprints.v1"

# This is partly AI generated and does not work ,and im too tired to fix it right now

class OAuthCallbackHandler(SimpleHTTPRequestHandler):
    def __init__(self, httpd, *args, **kwargs):
        self.httpd = httpd
        self.auth_successful = False
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path.startswith("/callback"):
            self.handleCallback()
        elif self.path.startswith("/status"):
            self.handle_status()
        else:
            self.send_error(404, "Not Found")

    def handleCallback(self):
        # Parse the query parameters from the callback URL
        query_params = parse.urlparse(self.path).query
        query_dict = parse.parse_qs(query_params)

        # Extract the authorization code from the query parameters
        if "code" in query_dict:
            authorization_code = query_dict['code'][0]
            self.auth_successful = True
            # Perform the rest of the OAuth2 flow (e.g., exchange the code for an access token)
            # ...
        else:
            self.auth_successful = False

        # Redirect the user to the status page
        self.send_response(302)
        self.send_header("Location", "/status")
        self.end_headers()

    def handle_status(self):
        # Serve the status page based on the authentication status
        if self.auth_successful:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"Authentication successful!")
        else:
            self.send_error(401, "Authentication failed")
        
        print("Authorization code request sent and responce was handeled, callback server no longer nessesary")
        print("Shutting down callback server")
        self.httpd.shutdown()


def generateRandomString(length):
    alphabet = ascii_letters + digits
    return ''.join(choice(alphabet) for _ in range(length))

def startWebServer(port):
    with TCPServer(("", port), lambda *args, **kwargs: OAuthCallbackHandler(httpd, *args, **kwargs)) as httpd:
        print(f"Serving on port {port}")
        httpd.serve_forever()



def startSSOAuthentication():
    # Start the local web server in a separate thread
    port = 8000
    Thread(target=startWebServer, args=(port,)).start()

    # Generate the PKCE code challenge
    base64urlSafeToken = urlsafe_b64encode(token_bytes(32))
    sha256Token = sha256()
    sha256Token.update(base64urlSafeToken)
    sha256ByteArrayToken = sha256Token.digest()
    finalPKCEChallenge = urlsafe_b64encode(sha256ByteArrayToken).decode().replace("=", "")
    state = generateRandomString(12)
    
    base_auth_url = "https://login.eveonline.com/v2/oauth/authorize/"
    params = {
        "response_type": "code",
        "redirect_uri": localCallbackUrl,
        "client_id": clientId,
        # "scope": scope,
        "state": state,
        "code_challenge": finalPKCEChallenge,
        "code_challenge_method": "S256"
    }

    string_params = parse.urlencode(params)
    fullAuthUrl = "{}?{}".format(base_auth_url, string_params)

    # Open the authorization URL in the user's default web browser
    webbrowser.open(fullAuthUrl)

startSSOAuthentication()
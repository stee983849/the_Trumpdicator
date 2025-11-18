#!/usr/bin/env python3
"""
Simple HTTP proxy server for The Trumpdicator application.
This script creates a proxy that forwards requests to the Flask application
running on port 5001.
"""

import http.server
import socketserver
import urllib.request
import urllib.error
import sys

# Configuration
LISTEN_PORT = 8080  # Port this proxy listens on
TARGET_HOST = "http://localhost:5001"  # The Flask application

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests by forwarding them to the Flask app"""
        try:
            # Forward the request to the Flask application
            url = f"{TARGET_HOST}{self.path}"
            print(f"Forwarding request to: {url}")
            
            # Make the request to the Flask app
            response = urllib.request.urlopen(url)
            
            # Send the response status code
            self.send_response(response.status)
            
            # Send the headers
            for header in response.getheaders():
                self.send_header(header[0], header[1])
            self.end_headers()
            
            # Send the content
            self.wfile.write(response.read())
            
        except urllib.error.URLError as e:
            self.send_error(500, f"Error forwarding request: {str(e)}")
            print(f"Error: {str(e)}")
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")
            print(f"Server error: {str(e)}")

    def do_POST(self):
        """Handle POST requests by forwarding them to the Flask app"""
        try:
            # Get the content length
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # Forward the request to the Flask application
            url = f"{TARGET_HOST}{self.path}"
            print(f"Forwarding POST request to: {url}")
            
            # Create a request with the same headers and data
            req = urllib.request.Request(
                url, 
                data=post_data,
                headers=dict(self.headers),
                method='POST'
            )
            
            # Make the request to the Flask app
            response = urllib.request.urlopen(req)
            
            # Send the response status code
            self.send_response(response.status)
            
            # Send the headers
            for header in response.getheaders():
                self.send_header(header[0], header[1])
            self.end_headers()
            
            # Send the content
            self.wfile.write(response.read())
            
        except urllib.error.URLError as e:
            self.send_error(500, f"Error forwarding request: {str(e)}")
            print(f"Error: {str(e)}")
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")
            print(f"Server error: {str(e)}")

def main():
    try:
        # Create the server
        with socketserver.TCPServer(("", LISTEN_PORT), ProxyHandler) as httpd:
            print(f"Proxy server started at http://localhost:{LISTEN_PORT}")
            print(f"Forwarding requests to {TARGET_HOST}")
            print("Press Ctrl+C to stop the server")
            
            # Start the server
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the proxy server")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting proxy server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
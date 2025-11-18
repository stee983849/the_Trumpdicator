# The Trumpdicator - Access Guide

This document explains how to access and use The Trumpdicator application.

## Local Access Options

The Trumpdicator application can be accessed in two ways:

### 1. Direct Flask Access
- **URL**: http://localhost:5001
- **Description**: This is the main Flask application running directly.

### 2. Proxy Server Access
- **URL**: http://localhost:8080
- **Description**: This is a proxy server that forwards requests to the Flask application.

## Starting the Application

To start the application, follow these steps:

1. Start the Flask application:
   ```
   python3 app.py
   ```
   This will start the application on port 5001.

2. Start the proxy server (optional):
   ```
   python3 proxy.py
   ```
   This will start a proxy server on port 8080 that forwards requests to the Flask application.

## Remote Access

For remote access, you have two options:

### Option 1: Duck DNS (Requires Port Forwarding)

1. Ensure your Duck DNS updater is running:
   ```
   ~/duckdns/duck.sh
   ```

2. Set up port forwarding on your router (port 80 → 5001).

3. Access the application at: http://trumpdicator.duckdns.org

### Option 2: Ngrok (Easiest for Remote Access)

1. Sign up for a free ngrok account at https://dashboard.ngrok.com/signup

2. Get your authtoken from the ngrok dashboard.

3. Configure ngrok with your authtoken:
   ```
   ./ngrok config add-authtoken YOUR_AUTHTOKEN
   ```

4. Start an ngrok tunnel:
   ```
   ./ngrok http 5001
   ```

5. Access the application using the URL provided by ngrok (looks like https://xxxx-xxxx-xxxx.ngrok.io).

## Troubleshooting

- If you cannot access the application, ensure that both the Flask application and the proxy server (if used) are running.
- Check the terminal output for any error messages.
- If using Duck DNS, verify that your port forwarding is set up correctly.
- If using ngrok, ensure that you have configured it with a valid authtoken.

## Security Considerations

- The current setup is for development and testing purposes only.
- For production use, consider implementing HTTPS and proper authentication.
- Do not expose sensitive data through this application without proper security measures.
# Port Forwarding Guide for The Trumpdicator

## Your Current Setup
- **Duck DNS Domain**: trumpdicator.duckdns.org
- **Your Public IP**: 144.82.8.192 (according to Duck DNS)
- **Flask App Port**: 5001

## Step-by-Step Port Forwarding Instructions

1. **Find your router's IP address**
   - On macOS: Open Terminal and type `netstat -nr | grep default`
   - The IP address next to "default" is your router's IP (typically 192.168.1.1 or 192.168.0.1)

2. **Access your router's admin panel**
   - Open a web browser and enter your router's IP address
   - Log in with your router's admin credentials
   - If you don't know them, check the router label or contact your ISP

3. **Find the port forwarding section**
   - Look for: "Port Forwarding", "Virtual Server", or "NAT"
   - This is usually under "Advanced Settings"

4. **Add a new port forwarding rule**
   - **External/Public Port**: 80 (standard HTTP port)
   - **Internal/Private Port**: 5001 (your Flask app port)
   - **Internal IP Address**: Your computer's local IP address
     - Find this by running `ifconfig | grep "inet " | grep -v 127.0.0.1` in Terminal
   - **Protocol**: TCP or Both (TCP/UDP)
   - **Name/Description**: Trumpdicator

5. **Save the settings**
   - Apply or save the changes
   - Some routers may require a restart

## Testing Your Setup

1. **Run the Duck DNS updater**
   ```
   ~/duckdns/duck.sh
   ```

2. **Make sure your Flask app is running**
   ```
   python3 app.py
   ```

3. **Test your domain**
   - Open a web browser on a different device (not connected to your WiFi)
   - Visit: http://trumpdicator.duckdns.org
   - Or use an online port checking tool like https://www.yougetsignal.com/tools/open-ports/

## Common Issues

1. **ISP Blocking Port 80**
   - Some ISPs block port 80 for residential connections
   - Solution: Try using port 8080 instead (forward external port 8080 to internal port 5001)

2. **Multiple Routers**
   - If you have multiple routers (e.g., ISP router + your own), you need to set up port forwarding on both

3. **Firewall Blocking**
   - Check if your computer's firewall is blocking incoming connections
   - On macOS: System Preferences > Security & Privacy > Firewall > Firewall Options
   - Allow incoming connections for Python/Flask

4. **Router Security Settings**
   - Some routers have additional security features that block incoming connections
   - Check for settings like "SPI Firewall" or "DoS Protection"

## Security Note
Port forwarding opens your computer to the internet. For better security:
- Consider using a reverse proxy like Nginx
- Set up HTTPS with Let's Encrypt
- Implement proper authentication for your app
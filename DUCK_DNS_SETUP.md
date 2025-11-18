# Setting Up Trumpdicator with Duck DNS

This guide will help you make your Trumpdicator application accessible online using your Duck DNS domain.

## Duck DNS Information
- **Domain**: trumpdicator.duckdns.org
- **Token**: df1052e8-b233-428a-bbd8-512678815990
- **Current IP**: 144.82.8.192

## Step 1: Restart Your Flask Application

The Flask application has been updated to accept connections from any IP address. Restart it with:

```
python3 app.py
```

## Step 2: Set Up Port Forwarding on Your Router

1. Access your router's admin panel (typically at 192.168.1.1 or 192.168.0.1)
2. Find the "Port Forwarding" section (might be under "Advanced Settings")
3. Add a new port forwarding rule:
   - External Port: 80 (standard HTTP port)
   - Internal Port: 5000 (Flask app port)
   - Internal IP: Your computer's local IP (find with `ifconfig` on Mac)
   - Protocol: TCP

## Step 3: Set Up Duck DNS Updater

### Option 1: Manual Update
Visit this URL to update your Duck DNS record:
```
https://www.duckdns.org/update?domains=trumpdicator&token=df1052e8-b233-428a-bbd8-512678815990&ip=
```
(Leave the IP blank to use your current public IP)

### Option 2: Automatic Updates (Recommended)

#### On macOS:

1. Create a script file:

```bash
#!/bin/bash

# Duck DNS update script
echo url="https://www.duckdns.org/update?domains=trumpdicator&token=df1052e8-b233-428a-bbd8-512678815990&ip=" | curl -k -o ~/duckdns/duck.log -K -
```

2. Make it executable:
```
chmod +x ~/duckdns/duck.sh
```

3. Set up a cron job to run it every 5 minutes:
```
crontab -e
```

4. Add this line:
```
*/5 * * * * ~/duckdns/duck.sh
```

## Step 4: Access Your Application

Once everything is set up, you can access your application at:

http://trumpdicator.duckdns.org

## Troubleshooting

1. **Can't access from outside your network**: Check port forwarding settings
2. **Domain not updating**: Verify Duck DNS token and update URL
3. **Application not responding**: Ensure Flask app is running with host='0.0.0.0'

## Security Considerations

For a production environment, consider:
1. Setting up HTTPS with Let's Encrypt
2. Using a proper web server like Nginx or Apache
3. Running Flask behind a WSGI server like Gunicorn
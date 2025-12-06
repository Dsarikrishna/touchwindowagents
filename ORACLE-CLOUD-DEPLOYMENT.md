# Oracle Cloud Deployment Guide for Touch Window AI Agents

## Prerequisites
1. Oracle Cloud account (free tier): https://www.oracle.com/cloud/free/
2. SSH key pair for VM access
3. Git installed on your local machine

## Deployment Steps

### 1. Create Oracle Cloud Account
1. Go to https://www.oracle.com/cloud/free/
2. Sign up for Always Free tier
3. Verify your email and set up your account

### 2. Create a Compute Instance (VM)

#### Option A: ARM-based VM (Recommended - More Powerful)
- **Shape**: VM.Standard.A1.Flex
- **OCPU**: 2 (you can use up to 4 with free tier)
- **Memory**: 12 GB (you can use up to 24 GB total)
- **OS**: Ubuntu 22.04 LTS
- **Storage**: 100 GB

#### Option B: AMD-based VM
- **Shape**: VM.Standard.E2.1.Micro
- **OCPU**: 1/8
- **Memory**: 1 GB
- **OS**: Ubuntu 22.04 LTS
- **Storage**: 50 GB

**Steps in Oracle Console:**
1. Navigate to: Compute → Instances → Create Instance
2. Name: `touchwindow-ai-agents`
3. Select your preferred shape (ARM recommended)
4. Choose Ubuntu 22.04 image
5. Add your SSH public key
6. Note the public IP address
7. Click "Create"

### 3. Configure Network Security

**Open Required Ports:**

In Oracle Console:
1. Go to: Networking → Virtual Cloud Networks → Your VCN → Security Lists
2. Add Ingress Rules:
   - Port 7071 (Azure Functions API)
   - Port 8501 (Admin Dashboard)
   - Port 8502 (User Dashboard)
   - Port 22 (SSH - already open)

**Ingress Rule Example:**
- Source CIDR: 0.0.0.0/0
- IP Protocol: TCP
- Destination Port: 8501
- Description: Streamlit Admin Dashboard

### 4. Connect to Your VM

```bash
ssh -i /path/to/your/private-key ubuntu@<YOUR_VM_PUBLIC_IP>
```

### 5. Install Docker on VM

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose -y

# Verify installation
docker --version
docker-compose --version

# Logout and login again for group changes to take effect
exit
```

### 6. Configure VM Firewall (Ubuntu)

```bash
# SSH back into the VM
ssh -i /path/to/your/private-key ubuntu@<YOUR_VM_PUBLIC_IP>

# Configure iptables to allow traffic
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 7071 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8501 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8502 -j ACCEPT

# Save iptables rules
sudo netfilter-persistent save

# Or install netfilter-persistent if needed
sudo apt install iptables-persistent -y
```

### 7. Deploy Your Application

```bash
# Clone your repository
git clone https://github.com/Dsarikrishna/touchwindowagents.git
cd touchwindowagents

# Start the application
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 8. Access Your Application

Once deployed, access your dashboards at:
- **Admin Dashboard**: http://YOUR_VM_PUBLIC_IP:8501
- **User Dashboard**: http://YOUR_VM_PUBLIC_IP:8502
- **Functions API**: http://YOUR_VM_PUBLIC_IP:7071

### 9. Set Up Domain (Optional)

If you want a custom domain instead of IP:
1. Register a domain (free options: Freenom, or use your own)
2. Point A record to your VM public IP
3. Set up reverse proxy with Nginx (see below)

### 10. Enable Auto-Start on Reboot

```bash
# Create systemd service
sudo nano /etc/systemd/system/touchwindow-agents.service
```

Add this content:
```ini
[Unit]
Description=Touch Window AI Agents
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/touchwindowagents
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
User=ubuntu

[Install]
WantedBy=multi-user.target
```

Enable the service:
```bash
sudo systemctl enable touchwindow-agents.service
sudo systemctl start touchwindow-agents.service
```

## Optional: Set Up Nginx Reverse Proxy with SSL

### Install Nginx and Certbot
```bash
sudo apt install nginx certbot python3-certbot-nginx -y
```

### Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/touchwindow
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8502;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 80;
    server_name admin.yourdomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/touchwindow /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Get SSL Certificate (Free with Let's Encrypt)
```bash
sudo certbot --nginx -d yourdomain.com -d admin.yourdomain.com
```

## Monitoring and Maintenance

### Check Application Status
```bash
docker-compose ps
docker-compose logs -f
```

### Update Application
```bash
cd /home/ubuntu/touchwindowagents
git pull origin main
docker-compose down
docker-compose up --build -d
```

### Monitor Resource Usage
```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check running containers
docker stats
```

## Cost: $0/month
Everything runs on Oracle Cloud Always Free tier!

## Troubleshooting

### Can't Access Dashboards
1. Check Oracle Cloud Security Lists (port ingress rules)
2. Check VM firewall: `sudo iptables -L`
3. Check containers: `docker-compose ps`
4. Check logs: `docker-compose logs`

### Containers Not Starting
```bash
# Check Docker daemon
sudo systemctl status docker

# Restart Docker
sudo systemctl restart docker

# Rebuild containers
docker-compose down
docker-compose up --build -d
```

### Out of Memory
- Upgrade to ARM-based VM (up to 24 GB RAM free)
- Monitor with: `docker stats`
- Optimize container resources in docker-compose.yml

## Support
- Oracle Cloud Docs: https://docs.oracle.com/en-us/iaas/
- Oracle Free Tier: https://www.oracle.com/cloud/free/
- Project GitHub: https://github.com/Dsarikrishna/touchwindowagents

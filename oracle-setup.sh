#!/bin/bash

# Oracle Cloud VM Setup Script for Touch Window AI Agents
# Run this script on your Oracle Cloud Ubuntu VM after SSH connection

echo "=================================="
echo "Touch Window AI Agents - Oracle Cloud Setup"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Update system
echo -e "${YELLOW}Step 1: Updating system...${NC}"
sudo apt update && sudo apt upgrade -y

# Install Docker
echo -e "${YELLOW}Step 2: Installing Docker...${NC}"
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
rm get-docker.sh

# Install Docker Compose
echo -e "${YELLOW}Step 3: Installing Docker Compose...${NC}"
sudo apt install docker-compose -y

# Install Git
echo -e "${YELLOW}Step 4: Installing Git...${NC}"
sudo apt install git -y

# Install iptables-persistent for firewall rules
echo -e "${YELLOW}Step 5: Configuring firewall...${NC}"
sudo apt install iptables-persistent -y

# Configure firewall rules
echo -e "${YELLOW}Step 6: Opening required ports...${NC}"
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 7071 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8501 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8502 -j ACCEPT
sudo netfilter-persistent save

# Install useful tools
echo -e "${YELLOW}Step 7: Installing additional tools...${NC}"
sudo apt install htop curl wget nano -y

# Get VM public IP
PUBLIC_IP=$(curl -s ifconfig.me)

echo ""
echo -e "${GREEN}=================================="
echo "Setup Complete!"
echo "==================================${NC}"
echo ""
echo "Next steps:"
echo "1. Log out and log back in (to apply Docker group changes)"
echo "   Command: exit"
echo ""
echo "2. SSH back in and clone your repository:"
echo "   git clone https://github.com/Dsarikrishna/touchwindowagents.git"
echo "   cd touchwindowagents"
echo ""
echo "3. Start your application:"
echo "   docker-compose up -d"
echo ""
echo "4. Access your dashboards at:"
echo "   Admin Dashboard: http://$PUBLIC_IP:8501"
echo "   User Dashboard: http://$PUBLIC_IP:8502"
echo "   Functions API: http://$PUBLIC_IP:7071"
echo ""
echo -e "${YELLOW}Important: Make sure ports 7071, 8501, and 8502 are open in Oracle Cloud Security Lists!${NC}"
echo ""

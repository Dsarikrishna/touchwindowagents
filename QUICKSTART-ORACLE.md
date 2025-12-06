# Quick Start Guide - Oracle Cloud Deployment

## 🚀 Deploy in 5 Minutes

### 1. Create Oracle Cloud Account
👉 Go to: https://www.oracle.com/cloud/free/
- Sign up for **Always Free tier** (no credit card required)
- Verify email and complete setup

### 2. Create a Virtual Machine

**In Oracle Cloud Console:**
1. Click **"Compute"** → **"Instances"** → **"Create Instance"**

2. **Configuration:**
   - **Name**: `touchwindow-ai-agents`
   - **Image**: Ubuntu 22.04 (Oracle Linux also works)
   - **Shape**: VM.Standard.A1.Flex (ARM - Recommended)
     - OCPU: 2
     - Memory: 12 GB
   - **Network**: Use default VCN
   - **SSH Key**: Upload your public SSH key or generate one
   - **Boot Volume**: 100 GB

3. Click **"Create"** and wait 2-3 minutes

4. **Note your VM's Public IP address** (shows on instance details page)

### 3. Open Firewall Ports

**In Oracle Cloud Console:**
1. Go to: **Networking** → **Virtual Cloud Networks** → **Your VCN Name**
2. Click **Security Lists** → **Default Security List**
3. Click **"Add Ingress Rules"** and add these 3 rules:

**Rule 1: Admin Dashboard**
- Source CIDR: `0.0.0.0/0`
- IP Protocol: TCP
- Destination Port: `8501`

**Rule 2: User Dashboard**
- Source CIDR: `0.0.0.0/0`
- IP Protocol: TCP
- Destination Port: `8502`

**Rule 3: Functions API**
- Source CIDR: `0.0.0.0/0`
- IP Protocol: TCP
- Destination Port: `7071`

### 4. Connect to Your VM

**From your local computer (PowerShell):**
```powershell
# Replace with your actual IP and key path
ssh -i path\to\your\private-key ubuntu@YOUR_VM_PUBLIC_IP
```

### 5. Run Setup Script

**On the VM (after SSH connection):**
```bash
# Download and run setup script
curl -o setup.sh https://raw.githubusercontent.com/Dsarikrishna/touchwindowagents/main/oracle-setup.sh
chmod +x setup.sh
./setup.sh

# After setup completes, logout and login again
exit
```

### 6. Deploy Application

**SSH back in and deploy:**
```bash
ssh -i path\to\your\private-key ubuntu@YOUR_VM_PUBLIC_IP

# Clone repository
git clone https://github.com/Dsarikrishna/touchwindowagents.git
cd touchwindowagents

# Start application (takes 2-3 minutes first time)
docker-compose up -d

# Check status
docker-compose ps
```

### 7. Access Your Dashboards

Open in your browser:
- **Admin Dashboard**: `http://YOUR_VM_PUBLIC_IP:8501`
- **User Dashboard**: `http://YOUR_VM_PUBLIC_IP:8502`

🎉 **Done! Your AI Agents are now running on Oracle Cloud!**

---

## 📋 Quick Commands

### Check Application Status
```bash
docker-compose ps
docker-compose logs -f
```

### Stop Application
```bash
docker-compose down
```

### Restart Application
```bash
docker-compose restart
```

### Update Application
```bash
cd touchwindowagents
git pull origin main
docker-compose down
docker-compose up --build -d
```

### View Resource Usage
```bash
docker stats
```

---

## 🔧 Troubleshooting

### Can't access dashboards?
1. ✅ Check Oracle Security Lists (ingress rules for ports 8501, 8502, 7071)
2. ✅ Check VM firewall: `sudo iptables -L | grep -E '8501|8502|7071'`
3. ✅ Check containers: `docker-compose ps` (all should show "Up")
4. ✅ Try accessing: `curl http://localhost:8501` from VM itself

### Containers not starting?
```bash
# Check Docker service
sudo systemctl status docker

# View detailed logs
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose up --build -d
```

### Need more resources?
- Upgrade to ARM VM shape (up to 24 GB RAM free!)
- Oracle allows up to 4 ARM CPUs and 24 GB RAM on free tier

---

## 💰 Cost

**$0/month** - Completely free on Oracle Cloud Always Free tier!

---

## 📞 Support

- Full Guide: See `ORACLE-CLOUD-DEPLOYMENT.md`
- GitHub: https://github.com/Dsarikrishna/touchwindowagents
- Oracle Cloud Docs: https://docs.oracle.com/iaas/

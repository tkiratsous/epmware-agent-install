# Appendix C - Agent Commands

Complete command reference for EPMware Agent operations, including installation, configuration, management, and troubleshooting commands.

## Command Categories

<div class="grid cards" markdown>

- :material-console: **Installation Commands**  
  Commands for setting up the agent
  
- :material-cog: **Configuration Commands**  
  Commands for configuring the agent
  
- :material-play-pause: **Operation Commands**  
  Start, stop, and manage the agent
  
- :material-magnify: **Diagnostic Commands**  
  Troubleshooting and testing commands
  
- :material-chart-line: **Monitoring Commands**  
  Performance and health monitoring

</div>

## Quick Command Reference

### Essential Commands

| Command | Purpose | Platform |
|---------|---------|----------|
| `java -jar epmware-agent.jar --test` | Test connection | All |
| `./ew_target_service.sh` | Start agent | Linux/Cygwin |
| `ps aux \| grep epmware` | Check if running | Linux |
| `tail -f logs/agent.log` | View logs | All |
| `pkill -f epmware-agent` | Stop agent | Linux |

## Installation Commands

### System Preparation

#### Linux

```bash
# Update system
sudo yum update -y                    # RHEL/CentOS
sudo apt-get update && sudo apt-get upgrade -y  # Ubuntu

# Install Java
sudo yum install java-1.8.0-openjdk   # RHEL/CentOS
sudo apt-get install openjdk-8-jdk    # Ubuntu

# Create user
sudo useradd -m -s /bin/bash epmware_agent
sudo passwd epmware_agent

# Set up directory
sudo mkdir -p /opt/epmware/agent
sudo chown epmware_agent:epmware_agent /opt/epmware/agent
```

#### Windows

```powershell
# Check Java installation
java -version

# Install Cygwin (download and run setup-x86_64.exe)
# Then in Cygwin:
cd ~
pwd  # Should show /home/username
```

### Agent Installation

```bash
# Extract agent files
cd ~
unzip ew_agent_files.zip

# Set permissions (Linux)
chmod 755 ew_target_service.sh
chmod 600 agent.properties
chmod 644 epmware-agent.jar

# Set permissions (Cygwin)
chmod +x ew_target_service.sh
```

## Configuration Commands

### Property File Management

```bash
# Edit configuration
vi agent.properties           # Linux
nano agent.properties         # Linux alternative
notepad agent.properties      # Windows

# Backup configuration
cp agent.properties agent.properties.backup.$(date +%Y%m%d)

# Validate configuration syntax
grep -E "^[^#].*=" agent.properties

# Check for required properties
for prop in ew.portal.server ew.portal.url ew.portal.token; do
    grep "^$prop=" agent.properties || echo "Missing: $prop"
done
```

### Token Management

```bash
# Check current token
grep ew.portal.token agent.properties

# Update token (Linux)
sed -i 's/ew.portal.token=.*/ew.portal.token=NEW-TOKEN-HERE/' agent.properties

# Update token (backup first)
cp agent.properties agent.properties.bak
sed -i 's/ew.portal.token=.*/ew.portal.token=NEW-TOKEN-HERE/' agent.properties

# Secure token file
chmod 600 agent.properties
```

### Service Script Configuration

```bash
# Update HOME directory in service script
sed -i 's|HOME=.*|HOME=/home/epmware_agent|' ew_target_service.sh

# Add Java options
cat >> ew_target_service.sh << 'EOF'
JAVA_OPTS="-Xms1024m -Xmx2048m"
java $JAVA_OPTS -jar epmware-agent.jar --spring.config.name=agent
EOF
```

## Operation Commands

### Starting the Agent

#### Linux

```bash
# Start in foreground (testing)
./ew_target_service.sh

# Start in background
nohup ./ew_target_service.sh > agent.out 2>&1 &

# Start with specific Java options
java -Xmx2048m -jar epmware-agent.jar --spring.config.name=agent

# Start as systemd service
sudo systemctl start epmware-agent

# Start with debug
java -Dlogging.level.root=DEBUG -jar epmware-agent.jar --spring.config.name=agent
```

#### Windows

```powershell
# Start via Task Scheduler
Start-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"

# Start via Cygwin
C:\cygwin64\bin\bash.exe -l -c "cd ~ && ./ew_target_service.sh"

# Start manually
cd C:\cygwin64\home\Administrator
java -jar epmware-agent.jar --spring.config.name=agent
```

### Stopping the Agent

#### Linux

```bash
# Find and kill process
ps aux | grep epmware-agent
kill -15 <PID>  # Graceful shutdown
kill -9 <PID>   # Force kill

# Kill by name
pkill -f epmware-agent

# Stop systemd service
sudo systemctl stop epmware-agent

# Kill all Java processes (careful!)
killall java
```

#### Windows

```powershell
# Stop scheduled task
Stop-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"

# Find and stop process
Get-Process | Where {$_.ProcessName -eq "java"} | Stop-Process

# Force stop
Get-Process java | Where {$_.CommandLine -like "*epmware*"} | Stop-Process -Force
```

### Restarting the Agent

```bash
# Simple restart
pkill -f epmware-agent && sleep 5 && ./ew_target_service.sh &

# systemd restart
sudo systemctl restart epmware-agent

# Windows restart
Stop-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"
Start-Sleep -Seconds 5
Start-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"
```

## Diagnostic Commands

### Testing Connectivity

```bash
# Test agent connection
java -jar epmware-agent.jar --test

# Test with specific config
java -jar epmware-agent.jar --spring.config.location=./test.properties --test

# Test network connectivity
ping epmware-server.com
telnet epmware-server.com 443
nc -zv epmware-server.com 443

# Test with curl
curl -I https://epmware-server.com
curl -H "Authorization: Bearer TOKEN" https://epmware-server.com/api/health
```

### Process Verification

```bash
# Check if agent is running
ps aux | grep epmware-agent
pgrep -f epmware-agent

# Get process details
ps -ef | grep java | grep epmware
lsof -p $(pgrep -f epmware-agent)

# Check Windows process
tasklist | findstr java
Get-Process java | Where {$_.CommandLine -like "*epmware*"}
```

### Log Analysis

```bash
# View recent logs
tail -50 logs/agent.log
tail -f logs/agent.log  # Follow log

# Search for errors
grep ERROR logs/agent.log
grep -i error logs/agent.log | tail -20

# Count errors
grep -c ERROR logs/agent.log

# View logs by date
grep "2023-11-15" logs/agent.log

# Find specific operations
grep -i deploy logs/agent.log
grep -i "connection" logs/agent.log
```

### Version Information

```bash
# Check agent version
java -jar epmware-agent.jar --version

# Check Java version
java -version
$JAVA_HOME/bin/java -version

# Check OS version
uname -a           # Linux
systeminfo         # Windows
cat /etc/os-release  # Linux distro info
```

## Monitoring Commands

### Resource Monitoring

```bash
# Memory usage
free -h                    # Linux system memory
ps aux | grep epmware | awk '{print $6}'  # Agent memory (KB)

# CPU usage
top -p $(pgrep -f epmware)  # Interactive
ps aux | grep epmware | awk '{print $3}'  # CPU percentage

# Disk usage
df -h /home/epmware_agent
du -sh logs/
du -sh temp/

# Network connections
netstat -an | grep ESTABLISHED | grep -E "443|8080"
ss -tunap | grep epmware
```

### Performance Monitoring

```bash
# Java heap usage
jps -v | grep epmware
jmap -heap $(pgrep -f epmware)

# Thread dump
jstack $(pgrep -f epmware) > thread_dump.txt

# Heap dump
jmap -dump:format=b,file=heap.bin $(pgrep -f epmware)

# GC statistics
jstat -gc $(pgrep -f epmware) 1000 10  # Every 1 second, 10 times
```

### Health Check Commands

```bash
#!/bin/bash
# health_check.sh

# Check if running
if pgrep -f epmware-agent > /dev/null; then
    echo "✓ Agent is running"
else
    echo "✗ Agent is NOT running"
    exit 1
fi

# Check last poll
LAST_POLL=$(tail -1 logs/agent-poll.log | awk '{print $1" "$2}')
echo "Last poll: $LAST_POLL"

# Check for recent errors
ERRORS=$(tail -100 logs/agent.log | grep -c ERROR)
echo "Recent errors: $ERRORS"
```

## Maintenance Commands

### Log Management

```bash
# Rotate logs manually
mv logs/agent.log logs/agent.log.$(date +%Y%m%d)
touch logs/agent.log

# Compress old logs
gzip logs/*.log.2023*

# Delete old logs
find logs/ -name "*.log" -mtime +30 -delete
find logs/ -name "*.gz" -mtime +90 -delete

# Archive logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz logs/
```

### Cleanup Commands

```bash
# Clean temporary files
rm -rf temp/*
find temp/ -type f -mtime +7 -delete

# Clean old backups
find . -name "*.backup.*" -mtime +30 -delete

# Remove PID files
rm -f *.pid
rm -f *.lock
```

### Backup Commands

```bash
# Backup configuration
cp agent.properties backups/agent.properties.$(date +%Y%m%d_%H%M%S)

# Full backup
tar -czf epmware_backup_$(date +%Y%m%d).tar.gz \
    agent.properties ew_target_service.sh logs/

# Backup with encryption
tar -czf - agent.properties | \
    openssl enc -e -aes256 -out backup.tar.gz.enc
```

## Security Commands

### Permission Management

```bash
# Set secure permissions (Linux)
chmod 600 agent.properties
chmod 700 ew_target_service.sh
chmod 755 logs/
chown -R epmware_agent:epmware_agent /home/epmware_agent

# Check permissions
ls -la agent.properties
find . -type f -perm 777  # Find world-writable files
```

### Security Scanning

```bash
# Check for passwords in files
grep -r "password\|pwd" . --exclude-dir=logs

# Check open ports
netstat -tulpn | grep LISTEN
lsof -i -P -n | grep LISTEN

# Check running processes
ps aux | grep epmware

# Audit file access
auditctl -w /home/epmware_agent/agent.properties -p rwa
```

## Application-Specific Commands

### HFM Commands

```bash
# Test HFM connection
$HFM_HOME/bin/LoadMetadata.bat -test -app:APPNAME -user:USER

# Copy registry properties
cp $MIDDLEWARE/user_projects/config/foundation/11.1.2.0/reg.properties \
   $MIDDLEWARE/user_projects/epmsystem1/config/foundation/11.1.2.0/
```

### Planning Commands

```bash
# Generate encrypted password
cd $PLANNING_HOME
./PasswordEncryption.sh password_file.txt

# Test Planning connection
./OutlineLoad.sh -test /A:APPNAME /U:USER
```

### Cloud EPM Commands

```bash
# EPM Automate login
epmautomate login username password URL

# List files
epmautomate listfiles

# Test deployment
epmautomate uploadfile test.zip
epmautomate importmetadata test.zip

# Logout
epmautomate logout
```

## Troubleshooting Commands

### Network Diagnostics

```bash
# DNS resolution
nslookup epmware-server.com
dig epmware-server.com

# Route tracing
traceroute epmware-server.com  # Linux
tracert epmware-server.com      # Windows

# Port testing
telnet server.com 443
nc -zv server.com 443

# Firewall check
iptables -L -n -v              # Linux
netsh advfirewall show all     # Windows
```

### Java Troubleshooting

```bash
# Check Java installation
which java
whereis java
java -version

# Check JAVA_HOME
echo $JAVA_HOME
ls -la $JAVA_HOME/bin/java

# Test Java execution
java -cp . -version

# Check Java process limits
ulimit -a  # All limits
ulimit -n  # File descriptors
```

## Scripting Examples

### Complete Management Script

```bash
#!/bin/bash
# agent_manager.sh - Complete agent management

case "$1" in
    start)
        echo "Starting EPMware Agent..."
        nohup ./ew_target_service.sh > logs/startup.log 2>&1 &
        echo $! > agent.pid
        echo "Started with PID: $(cat agent.pid)"
        ;;
    
    stop)
        echo "Stopping EPMware Agent..."
        if [ -f agent.pid ]; then
            kill $(cat agent.pid)
            rm agent.pid
            echo "Agent stopped"
        else
            echo "No PID file found"
        fi
        ;;
    
    restart)
        $0 stop
        sleep 5
        $0 start
        ;;
    
    status)
        if [ -f agent.pid ] && ps -p $(cat agent.pid) > /dev/null; then
            echo "Agent is running (PID: $(cat agent.pid))"
        else
            echo "Agent is not running"
        fi
        ;;
    
    logs)
        tail -f logs/agent.log
        ;;
    
    test)
        java -jar epmware-agent.jar --test
        ;;
    
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|test}"
        exit 1
        ;;
esac
```

### Monitoring Script

```bash
#!/bin/bash
# monitor.sh - Monitor agent health

while true; do
    # Check process
    if ! pgrep -f epmware-agent > /dev/null; then
        echo "[$(date)] Agent not running - restarting..."
        ./ew_target_service.sh &
    fi
    
    # Check logs for errors
    if tail -100 logs/agent.log | grep -q "FATAL"; then
        echo "[$(date)] Fatal error detected!"
        # Send alert
    fi
    
    sleep 60
done
```

## Command Aliases

### Useful Bash Aliases

```bash
# Add to ~/.bashrc or ~/.bash_profile

# Agent commands
alias agstart='cd /home/epmware_agent && ./ew_target_service.sh &'
alias agstop='pkill -f epmware-agent'
alias agstatus='ps aux | grep epmware-agent'
alias aglogs='tail -f /home/epmware_agent/logs/agent.log'
alias agtest='java -jar /home/epmware_agent/epmware-agent.jar --test'

# Quick navigation
alias aghome='cd /home/epmware_agent'
alias aglogs='cd /home/epmware_agent/logs'

# Monitoring
alias agmon='watch -n 5 "ps aux | grep epmware"'
alias agerrors='grep ERROR /home/epmware_agent/logs/agent.log | tail -20'
```

!!! tip "Command Documentation"
    Always document custom commands and scripts in your operational runbooks. Include examples and expected outputs for training purposes.

!!! warning "Destructive Commands"
    Be extremely careful with commands like `rm -rf`, `kill -9`, and `chmod 777`. Always verify the target before executing destructive commands.

## Next Steps

- [Port Requirements](ports.md) - Network port reference
- [Security Checklist](security.md) - Security configuration
- [Error Codes](error-codes.md) - Error resolution
- [Return to Appendices](index.md) - Main appendices page
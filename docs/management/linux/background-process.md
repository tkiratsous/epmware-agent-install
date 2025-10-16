# Running Agent as Background Process

This guide covers methods to run the EPMware Agent as a background process on Linux servers, ensuring continuous operation even after terminal sessions end.

## Background Execution Methods

### Method 1: Using Ampersand (&)

The simplest method to run the agent in the background:

```bash
cd /home/[username]
./ew_target_service.sh &
```

The `&` symbol runs the process in the background, returning control to the terminal immediately.

**Advantages:**
- Simple and quick
- No additional tools required

**Disadvantages:**
- Process may terminate when terminal session ends
- No automatic restart on failure
- Limited process management capabilities

### Method 2: Using nohup

Run the agent immune to hangups (terminal closure):

```bash
cd /home/[username]
nohup ./ew_target_service.sh > /dev/null 2>&1 &
```

**Breaking down the command:**
- `nohup` - Prevents process termination on terminal logout
- `> /dev/null` - Redirects standard output to null device
- `2>&1` - Redirects error output to standard output
- `&` - Runs in background

**Save output to log file:**
```bash
nohup ./ew_target_service.sh > agent-nohup.log 2>&1 &
echo $! > agent.pid  # Save process ID for later reference
```

### Method 3: Using screen

Screen provides a virtual terminal that persists after disconnection:

**Install screen (if needed):**
```bash
# RHEL/CentOS
sudo yum install screen

# Ubuntu/Debian
sudo apt-get install screen
```

**Start agent in screen session:**
```bash
# Create new screen session named 'epmware-agent'
screen -S epmware-agent

# Inside screen session, start the agent
cd /home/[username]
./ew_target_service.sh

# Detach from screen (Ctrl+A, then D)
```

**Screen session management:**
```bash
# List active sessions
screen -ls

# Reattach to session
screen -r epmware-agent

# Kill a session
screen -X -S epmware-agent quit
```

### Method 4: Using tmux

Tmux is a modern alternative to screen:

**Install tmux:**
```bash
# RHEL/CentOS
sudo yum install tmux

# Ubuntu/Debian
sudo apt-get install tmux
```

**Start agent in tmux:**
```bash
# Create new tmux session
tmux new -s epmware-agent

# Start the agent
cd /home/[username]
./ew_target_service.sh

# Detach from tmux (Ctrl+B, then D)
```

**Tmux session management:**
```bash
# List sessions
tmux ls

# Attach to session
tmux attach -t epmware-agent

# Kill session
tmux kill-session -t epmware-agent
```

## System Service Configuration

### Creating a systemd Service (Recommended)

For production environments, configure the agent as a systemd service:

**Create service file:**
```bash
sudo nano /etc/systemd/system/epmware-agent.service
```

**Service file content:**
```ini
[Unit]
Description=EPMware Agent Service
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=30
User=[username]
WorkingDirectory=/home/[username]
ExecStart=/usr/bin/java -jar /home/[username]/epmware-agent.jar --spring.config.name=agent
StandardOutput=append:/home/[username]/logs/agent-service.log
StandardError=append:/home/[username]/logs/agent-service-error.log

# Environment variables
Environment="JAVA_HOME=/usr/lib/jvm/java-1.8.0"
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin"

# Resource limits
LimitNOFILE=65536
LimitNPROC=32768

[Install]
WantedBy=multi-user.target
```

**Enable and start service:**
```bash
# Reload systemd configuration
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable epmware-agent

# Start the service
sudo systemctl start epmware-agent

# Check service status
sudo systemctl status epmware-agent
```

**Service management commands:**
```bash
# Stop service
sudo systemctl stop epmware-agent

# Restart service
sudo systemctl restart epmware-agent

# View logs
sudo journalctl -u epmware-agent -f

# Disable auto-start
sudo systemctl disable epmware-agent
```

### Creating an init.d Script (Legacy Systems)

For older systems without systemd:

**Create init script:**
```bash
sudo nano /etc/init.d/epmware-agent
```

**Script content:**
```bash
#!/bin/bash
# chkconfig: 2345 95 05
# description: EPMware Agent Service

AGENT_USER="[username]"
AGENT_HOME="/home/$AGENT_USER"
PIDFILE="$AGENT_HOME/agent.pid"
LOGFILE="$AGENT_HOME/logs/agent-init.log"

start() {
    if [ -f $PIDFILE ]; then
        echo "Agent already running (PID: $(cat $PIDFILE))"
        exit 1
    fi
    
    echo "Starting EPMware Agent..."
    su - $AGENT_USER -c "cd $AGENT_HOME && nohup ./ew_target_service.sh > $LOGFILE 2>&1 & echo \$! > $PIDFILE"
    echo "Agent started (PID: $(cat $PIDFILE))"
}

stop() {
    if [ ! -f $PIDFILE ]; then
        echo "Agent is not running"
        exit 1
    fi
    
    echo "Stopping EPMware Agent..."
    kill $(cat $PIDFILE)
    rm -f $PIDFILE
    echo "Agent stopped"
}

status() {
    if [ -f $PIDFILE ]; then
        PID=$(cat $PIDFILE)
        if ps -p $PID > /dev/null; then
            echo "Agent is running (PID: $PID)"
        else
            echo "Agent is not running (stale PID file)"
            rm -f $PIDFILE
        fi
    else
        echo "Agent is not running"
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 2
        start
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
```

**Make script executable and enable:**
```bash
# Make executable
sudo chmod +x /etc/init.d/epmware-agent

# Add to startup
sudo chkconfig --add epmware-agent
sudo chkconfig epmware-agent on

# Start service
sudo service epmware-agent start
```

## Process Management

### Finding the Agent Process

```bash
# Find by process name
ps -ef | grep -i epmware-agent | grep -v grep

# Find by user
ps -u [username] | grep java

# Get detailed information
ps aux | grep epmware-agent

# Using pgrep
pgrep -f epmware-agent
```

### Monitoring Process Status

```bash
# Check if process is running
if pgrep -f epmware-agent > /dev/null; then
    echo "Agent is running"
else
    echo "Agent is not running"
fi

# Monitor in real-time
top -p $(pgrep -f epmware-agent)

# Check process tree
pstree -p $(pgrep -f epmware-agent)
```

### Managing Process Priority

```bash
# Run with lower priority (nice value 10)
nice -n 10 ./ew_target_service.sh &

# Change priority of running process
renice -n 5 -p $(pgrep -f epmware-agent)

# Run with real-time priority (requires root)
sudo chrt -f 50 ./ew_target_service.sh
```

## Auto-Restart Configuration

### Using Supervisor

Install and configure Supervisor for process management:

**Install Supervisor:**
```bash
# RHEL/CentOS
sudo yum install supervisor

# Ubuntu/Debian
sudo apt-get install supervisor
```

**Configure agent in Supervisor:**
```ini
# /etc/supervisor/conf.d/epmware-agent.conf
[program:epmware-agent]
command=/home/[username]/ew_target_service.sh
directory=/home/[username]
user=[username]
autostart=true
autorestart=true
startsecs=10
startretries=3
stdout_logfile=/home/[username]/logs/agent-supervisor.log
stderr_logfile=/home/[username]/logs/agent-supervisor-error.log
environment=JAVA_HOME="/usr/lib/jvm/java-1.8.0",PATH="/usr/bin:/usr/local/bin"
```

**Manage with Supervisor:**
```bash
# Reload configuration
sudo supervisorctl reread
sudo supervisorctl update

# Start/stop/restart
sudo supervisorctl start epmware-agent
sudo supervisorctl stop epmware-agent
sudo supervisorctl restart epmware-agent

# Check status
sudo supervisorctl status epmware-agent
```

### Using a Watchdog Script

Create a custom watchdog to monitor and restart the agent:

```bash
#!/bin/bash
# /home/[username]/agent-watchdog.sh

AGENT_HOME="/home/[username]"
PIDFILE="$AGENT_HOME/agent.pid"
LOGFILE="$AGENT_HOME/logs/watchdog.log"

while true; do
    if [ -f $PIDFILE ]; then
        PID=$(cat $PIDFILE)
        if ! ps -p $PID > /dev/null; then
            echo "$(date): Agent died, restarting..." >> $LOGFILE
            cd $AGENT_HOME
            ./ew_target_service.sh &
            echo $! > $PIDFILE
        fi
    else
        echo "$(date): No PID file, starting agent..." >> $LOGFILE
        cd $AGENT_HOME
        ./ew_target_service.sh &
        echo $! > $PIDFILE
    fi
    sleep 60
done
```

**Run watchdog in background:**
```bash
nohup ./agent-watchdog.sh > /dev/null 2>&1 &
```

## Resource Limits and Tuning

### Setting Resource Limits

Configure system limits for the agent process:

**Edit limits configuration:**
```bash
# /etc/security/limits.d/epmware-agent.conf
[username] soft nofile 65536
[username] hard nofile 65536
[username] soft nproc 32768
[username] hard nproc 32768
[username] soft memlock unlimited
[username] hard memlock unlimited
```

### JVM Tuning for Background Operation

Optimize Java settings in the service script:

```bash
# Modified ew_target_service.sh
JAVA_OPTS="-Xms512m -Xmx2g -XX:+UseG1GC -XX:MaxGCPauseMillis=100"
java $JAVA_OPTS -jar epmware-agent.jar --spring.config.name=agent
```

## Troubleshooting Background Processes

### Process Won't Stay Running

1. **Check for errors in logs:**
   ```bash
   tail -100 logs/agent.log
   ```

2. **Verify Java is in PATH:**
   ```bash
   which java
   echo $JAVA_HOME
   ```

3. **Check file permissions:**
   ```bash
   ls -la ew_target_service.sh
   ls -la epmware-agent.jar
   ```

### Process Consumes Too Many Resources

1. **Limit CPU usage:**
   ```bash
   cpulimit -p $(pgrep -f epmware-agent) -l 50
   ```

2. **Limit memory in service file:**
   ```ini
   # Add to systemd service
   MemoryLimit=2G
   ```

### Can't Find Running Process

```bash
# Check all Java processes
jps -l

# Check by port (if agent uses specific port)
netstat -tlnp | grep [port]

# Check system logs
journalctl -xe | grep epmware
```

## Best Practices

1. **Always use a service manager** (systemd, init.d, or Supervisor) for production
2. **Configure automatic restart** on failure
3. **Set appropriate resource limits** to prevent system impact
4. **Monitor process health** with external tools
5. **Maintain separate log files** for service and application
6. **Document your configuration** for team reference
7. **Test failover scenarios** regularly

## Related Topics

- [Start and Stop Procedures](start-stop.md)
- [Agent Installation](../../installation/linux.md)
- [Monitoring](../monitoring.md)
- [Troubleshooting](../../troubleshooting/index.md)
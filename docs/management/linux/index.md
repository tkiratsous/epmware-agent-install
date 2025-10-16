# Linux Services Management

This section covers managing the EPMware Agent on Linux servers, including systemd services, background processes, and Linux-specific considerations.

## Linux Management Options

The EPMware Agent can run on Linux as:

<div class="grid cards" markdown>

- :material-cog-refresh: **systemd Service**  
  Modern Linux distributions (recommended)
  
- :material-console: **[Background Process](background-process.md)**  
  Traditional approach using nohup
  
- :material-play-pause: **[Start/Stop Scripts](start-stop.md)**  
  Manual control procedures

</div>

## Management Overview

### systemd Service (Recommended)

For modern Linux distributions:
- Automatic startup on boot
- Process supervision
- Dependency management
- Integrated logging

### Background Process

Traditional Unix approach:
- Simple to implement
- Works on all systems
- Manual management
- Less robust

### Init.d Scripts

For older systems:
- SysV init compatibility
- Legacy system support
- Manual dependency handling

## Quick Management Commands

### Check Agent Status

```bash
# systemd status
systemctl status epmware-agent

# Process check
ps aux | grep epmware-agent

# Recent logs
tail -n 20 /home/epmadmin/logs/agent.log
```

### Start Agent

```bash
# Via systemd
sudo systemctl start epmware-agent

# Via background process
cd /home/epmadmin
nohup ./ew_target_service.sh > agent.out 2>&1 &
```

### Stop Agent

```bash
# Via systemd
sudo systemctl stop epmware-agent

# Via process kill
pkill -f epmware-agent
```

## systemd Service Configuration

### Creating Service File

Create `/etc/systemd/system/epmware-agent.service`:

```ini
[Unit]
Description=EPMware Agent Service
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=epmadmin
Group=epmadmin
WorkingDirectory=/home/epmadmin
ExecStart=/usr/bin/java -jar /home/epmadmin/epmware-agent.jar --spring.config.name=agent
ExecStop=/bin/kill -TERM $MAINPID
Restart=always
RestartSec=30
StandardOutput=journal
StandardError=journal
SyslogIdentifier=epmware-agent

# Environment variables
Environment="JAVA_HOME=/usr/java/latest"
Environment="PATH=/usr/java/latest/bin:/usr/local/bin:/usr/bin:/bin"

# Resource limits
LimitNOFILE=65536
LimitNPROC=32768

# Memory limits
MemoryLimit=2G

[Install]
WantedBy=multi-user.target
```

### Enabling Service

```bash
# Reload systemd configuration
sudo systemctl daemon-reload

# Enable service for auto-start
sudo systemctl enable epmware-agent

# Start the service
sudo systemctl start epmware-agent

# Check status
systemctl status epmware-agent
```

## Process Management

### Process Monitoring

Monitor agent process:

```bash
#!/bin/bash
# monitor_agent.sh

# Check if running
if pgrep -f "epmware-agent" > /dev/null; then
    echo "Agent is running"
    
    # Get process details
    ps aux | grep epmware-agent | grep -v grep
    
    # Check resource usage
    pid=$(pgrep -f "epmware-agent")
    echo "Memory usage:"
    ps -o pid,vsz,rss,comm -p $pid
    
    echo "CPU usage:"
    top -b -n 1 -p $pid | tail -1
else
    echo "Agent is NOT running"
    exit 1
fi
```

### Process Limits

Configure resource limits:

```bash
# /etc/security/limits.d/epmware.conf
epmadmin soft nofile 65536
epmadmin hard nofile 65536
epmadmin soft nproc 32768
epmadmin hard nproc 32768
epmadmin soft memlock unlimited
epmadmin hard memlock unlimited
```

## Log Management

### systemd Journal

View logs with journalctl:

```bash
# View all agent logs
journalctl -u epmware-agent

# Follow logs in real-time
journalctl -u epmware-agent -f

# View logs since boot
journalctl -u epmware-agent -b

# View last 100 lines
journalctl -u epmware-agent -n 100

# Export logs
journalctl -u epmware-agent > agent-systemd.log
```

### rsyslog Integration

Configure rsyslog for agent:

```bash
# /etc/rsyslog.d/epmware-agent.conf
if $programname == 'epmware-agent' then /var/log/epmware/agent.log
& stop
```

### logrotate Configuration

Manage log rotation:

```bash
# /etc/logrotate.d/epmware-agent
/home/epmadmin/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 epmadmin epmadmin
    sharedscripts
    postrotate
        systemctl reload epmware-agent
    endscript
}
```

## Init.d Script (Legacy Systems)

For older Linux distributions:

```bash
#!/bin/bash
# /etc/init.d/epmware-agent
### BEGIN INIT INFO
# Provides:          epmware-agent
# Required-Start:    $network $syslog
# Required-Stop:     $network $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: EPMware Agent
# Description:       EPMware metadata deployment agent
### END INIT INFO

AGENT_USER=epmadmin
AGENT_HOME=/home/$AGENT_USER
AGENT_SCRIPT=$AGENT_HOME/ew_target_service.sh
PID_FILE=/var/run/epmware-agent.pid

case "$1" in
    start)
        echo "Starting EPMware Agent..."
        su - $AGENT_USER -c "cd $AGENT_HOME && nohup $AGENT_SCRIPT > /dev/null 2>&1 &"
        echo $! > $PID_FILE
        echo "Agent started."
        ;;
    stop)
        echo "Stopping EPMware Agent..."
        if [ -f $PID_FILE ]; then
            kill $(cat $PID_FILE)
            rm $PID_FILE
        fi
        echo "Agent stopped."
        ;;
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    status)
        if [ -f $PID_FILE ] && ps -p $(cat $PID_FILE) > /dev/null; then
            echo "Agent is running (PID: $(cat $PID_FILE))"
        else
            echo "Agent is not running"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
exit 0
```

## Monitoring and Alerting

### Health Check Script

Automated health monitoring:

```bash
#!/bin/bash
# health_check.sh

# Configuration
AGENT_USER="epmadmin"
AGENT_HOME="/home/$AGENT_USER"
ALERT_EMAIL="admin@company.com"
MAX_MEMORY=2048  # MB
MAX_CPU=80       # Percent

# Check process
if ! pgrep -f "epmware-agent" > /dev/null; then
    echo "CRITICAL: Agent not running" | mail -s "EPMware Agent Down" $ALERT_EMAIL
    exit 2
fi

# Check memory usage
PID=$(pgrep -f "epmware-agent")
MEMORY=$(ps -o rss= -p $PID | awk '{print int($1/1024)}')
if [ $MEMORY -gt $MAX_MEMORY ]; then
    echo "WARNING: High memory usage: ${MEMORY}MB" | mail -s "EPMware Agent Memory Alert" $ALERT_EMAIL
fi

# Check CPU usage
CPU=$(top -b -n 1 -p $PID | tail -1 | awk '{print int($9)}')
if [ $CPU -gt $MAX_CPU ]; then
    echo "WARNING: High CPU usage: ${CPU}%" | mail -s "EPMware Agent CPU Alert" $ALERT_EMAIL
fi

# Check last poll time
LAST_POLL=$(tail -1 $AGENT_HOME/logs/agent-poll.log | awk '{print $1" "$2}')
LAST_EPOCH=$(date -d "$LAST_POLL" +%s)
NOW_EPOCH=$(date +%s)
DIFF=$((NOW_EPOCH - LAST_EPOCH))

if [ $DIFF -gt 300 ]; then  # More than 5 minutes
    echo "WARNING: No polling for $DIFF seconds" | mail -s "EPMware Agent Polling Alert" $ALERT_EMAIL
fi

echo "Agent health check completed"
```

### Integration with Monitoring Systems

#### Nagios/Icinga

```bash
#!/bin/bash
# check_epmware_agent.sh - Nagios plugin

STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3

# Check if process is running
if pgrep -f "epmware-agent" > /dev/null; then
    # Check last poll time
    LAST_POLL=$(stat -c %Y /home/epmadmin/logs/agent-poll.log)
    NOW=$(date +%s)
    DIFF=$((NOW - LAST_POLL))
    
    if [ $DIFF -lt 60 ]; then
        echo "OK - Agent running and polling"
        exit $STATE_OK
    elif [ $DIFF -lt 300 ]; then
        echo "WARNING - Agent running but slow polling ($DIFF seconds)"
        exit $STATE_WARNING
    else
        echo "CRITICAL - Agent running but not polling ($DIFF seconds)"
        exit $STATE_CRITICAL
    fi
else
    echo "CRITICAL - Agent not running"
    exit $STATE_CRITICAL
fi
```

#### Zabbix

```json
{
    "zabbix_export": {
        "version": "5.0",
        "templates": [{
            "template": "EPMware Agent",
            "name": "EPMware Agent Monitoring",
            "items": [{
                "name": "Agent process running",
                "key": "proc.num[java,epmadmin,,epmware-agent]",
                "value_type": "UNSIGNED",
                "triggers": [{
                    "expression": "{last()}=0",
                    "name": "EPMware Agent is down",
                    "priority": "HIGH"
                }]
            }]
        }]
    }
}
```

## Performance Tuning

### JVM Options

Optimize Java settings:

```bash
# In ew_target_service.sh or systemd service
JAVA_OPTS="-server"
JAVA_OPTS="$JAVA_OPTS -Xms1024m -Xmx2048m"
JAVA_OPTS="$JAVA_OPTS -XX:+UseG1GC"
JAVA_OPTS="$JAVA_OPTS -XX:MaxGCPauseMillis=200"
JAVA_OPTS="$JAVA_OPTS -XX:+HeapDumpOnOutOfMemoryError"
JAVA_OPTS="$JAVA_OPTS -XX:HeapDumpPath=/var/log/epmware"

java $JAVA_OPTS -jar epmware-agent.jar --spring.config.name=agent
```

### System Tuning

Kernel parameters for performance:

```bash
# /etc/sysctl.d/epmware.conf
# Network tuning
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 87380 134217728
net.ipv4.tcp_wmem = 4096 65536 134217728

# File handles
fs.file-max = 2097152

# Process limits
kernel.pid_max = 4194304

# Apply settings
sudo sysctl -p /etc/sysctl.d/epmware.conf
```

## Troubleshooting

### Common Linux Issues

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| Service won't start | Check systemctl status | Review journal logs |
| Permission denied | ls -la file permissions | Fix ownership/permissions |
| Cannot find Java | which java | Update PATH or JAVA_HOME |
| Out of memory | dmesg \| grep -i memory | Increase heap size or system RAM |

### Debug Mode

Enable detailed debugging:

```bash
# Add to systemd service or script
export LOGGING_LEVEL_ROOT=DEBUG
export LOGGING_LEVEL_COM_EPMWARE=TRACE

# Or in service file
Environment="LOGGING_LEVEL_ROOT=DEBUG"
Environment="LOGGING_LEVEL_COM_EPMWARE=TRACE"
```

## Security Hardening

### SELinux Configuration

For Red Hat/CentOS with SELinux:

```bash
# Create custom policy
cat > epmware_agent.te << EOF
module epmware_agent 1.0;

require {
    type java_exec_t;
    type user_home_t;
    class file { read write execute };
    class process { transition };
}

allow java_exec_t user_home_t:file { read write execute };
EOF

# Compile and install policy
checkmodule -M -m -o epmware_agent.mod epmware_agent.te
semodule_package -o epmware_agent.pp -m epmware_agent.mod
semodule -i epmware_agent.pp
```

### AppArmor Profile

For Ubuntu/Debian with AppArmor:

```bash
# /etc/apparmor.d/epmware-agent
#include <tunables/global>

/home/epmadmin/epmware-agent.jar {
  #include <abstractions/base>
  #include <abstractions/java>
  
  /home/epmadmin/ r,
  /home/epmadmin/** rw,
  /var/log/epmware/** rw,
  
  network inet stream,
  network inet6 stream,
}
```

## Best Practices

### Linux-Specific Recommendations

1. **Use systemd** - For modern distributions
2. **Monitor with journalctl** - Centralized logging
3. **Configure limits** - Set appropriate resource limits
4. **Regular updates** - Keep system packages updated
5. **Security hardening** - Implement SELinux/AppArmor

### Maintenance Guidelines

1. **Log rotation** - Configure logrotate
2. **Resource monitoring** - Track memory and CPU
3. **Backup configurations** - Regular config backups
4. **Update documentation** - Keep runbooks current
5. **Test recovery** - Verify restart procedures

## Next Steps

- [Background Process Setup](background-process.md) - Traditional process management
- [Start and Stop Procedures](start-stop.md) - Operation procedures
- [Agent Logs](../logs.md) - Log management
- [Monitoring](../monitoring.md) - Monitoring setup
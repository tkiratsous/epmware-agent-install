# Agent Monitoring

Comprehensive monitoring of EPMware Agents ensures reliable metadata deployments and helps identify issues before they impact operations. This guide covers monitoring strategies, health checks, and alerting configurations.

## Monitoring Overview

The EPMware Agent monitoring encompasses:
- Agent availability and uptime
- Connection status to EPMware server
- Deployment success rates
- Resource utilization
- Response times and performance metrics

## Agent Status Monitoring

### From EPMware Application

Monitor agent status directly from the EPMware web interface:

1. Navigate to **Infrastructure → Servers**
2. View the **Agent Status** column for each server
3. Right-click any server and select **Test Connection**

Status indicators:
- 🟢 **Online** - Agent is connected and responding
- 🟡 **Warning** - Agent responding slowly or intermittently
- 🔴 **Offline** - Agent is not responding
- ⚫ **Unknown** - No recent status update

### Command Line Health Check

**Linux:**
```bash
#!/bin/bash
# Agent health check script
PID=$(ps -ef | grep -i epmware-agent | grep -v grep | awk '{print $2}')
if [ -z "$PID" ]; then
    echo "ERROR: Agent is not running"
    exit 1
else
    echo "OK: Agent is running (PID: $PID)"
    exit 0
fi
```

**Windows (PowerShell):**
```powershell
# Check if agent is running
$agent = Get-Process java | Where-Object {$_.CommandLine -like "*epmware-agent.jar*"}
if ($agent) {
    Write-Host "OK: Agent is running (PID: $($agent.Id))"
    exit 0
} else {
    Write-Host "ERROR: Agent is not running"
    exit 1
}
```

## Performance Monitoring

### Resource Utilization

Monitor CPU and memory usage of the agent process:

**Linux:**
```bash
# Real-time monitoring
top -p $(pgrep -f epmware-agent)

# Memory usage
ps aux | grep epmware-agent | grep -v grep | awk '{print "Memory: "$4"%"}'

# CPU usage
ps aux | grep epmware-agent | grep -v grep | awk '{print "CPU: "$3"%"}'
```

**Windows (Task Manager):**
1. Open Task Manager
2. Find the java.exe process running epmware-agent.jar
3. Monitor CPU and Memory columns

### Response Time Monitoring

Track agent response times by analyzing logs:

```bash
# Calculate average response time for deployments
grep "Deployment.*completed" agent.log | \
  awk '{print $1, $2}' | \
  while read start_time; do
    # Calculate duration
    echo "Response time calculation..."
  done
```

## Automated Monitoring Scripts

### Continuous Monitoring Script

Create a monitoring script that runs continuously:

**monitor-agent.sh (Linux):**
```bash
#!/bin/bash

AGENT_HOME="/home/[username]"
LOG_FILE="$AGENT_HOME/logs/agent-monitor.log"
ALERT_EMAIL="admin@company.com"

while true; do
    # Check if agent is running
    PID=$(ps -ef | grep -i epmware-agent | grep -v grep | awk '{print $2}')
    
    if [ -z "$PID" ]; then
        echo "$(date): Agent DOWN - Attempting restart" >> $LOG_FILE
        cd $AGENT_HOME
        ./ew_target_service.sh &
        
        # Send alert
        echo "EPMware Agent down on $(hostname)" | mail -s "Agent Alert" $ALERT_EMAIL
    else
        echo "$(date): Agent UP - PID: $PID" >> $LOG_FILE
    fi
    
    # Check every 5 minutes
    sleep 300
done
```

### Windows Scheduled Task Monitoring

Create a PowerShell script and schedule it to run every 5 minutes:

**Monitor-Agent.ps1:**
```powershell
$agentProcess = Get-Process java -ErrorAction SilentlyContinue | 
    Where-Object {$_.CommandLine -like "*epmware-agent.jar*"}

if (-not $agentProcess) {
    # Agent is not running - restart it
    Write-EventLog -LogName Application -Source "EPMware Agent" `
        -EventId 1001 -EntryType Error `
        -Message "Agent not running - attempting restart"
    
    # Start the scheduled task
    Start-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"
    
    # Send email alert (requires configured SMTP)
    Send-MailMessage -To "admin@company.com" `
        -From "epmware@company.com" `
        -Subject "EPMware Agent Down" `
        -Body "Agent was down on $env:COMPUTERNAME and has been restarted" `
        -SmtpServer "smtp.company.com"
}
```

## Key Metrics to Monitor

### Availability Metrics
- **Uptime percentage** - Target: >99.5%
- **Mean time between failures (MTBF)**
- **Mean time to recovery (MTTR)**
- **Number of restarts required**

### Performance Metrics
- **Average response time** - Target: <2 seconds
- **Deployment success rate** - Target: >98%
- **Queue processing time**
- **Memory usage** - Alert if >1GB
- **CPU usage** - Alert if >80% sustained

### Business Metrics
- **Deployments per day/hour**
- **Failed deployments**
- **Deployment duration trends**
- **Peak usage times**

## Alerting Configuration

### Log-based Alerts

Monitor specific patterns in log files:

```bash
#!/bin/bash
# Alert on errors
tail -F agent.log | while read line; do
    if echo "$line" | grep -q "ERROR\|FATAL"; then
        echo "$line" | mail -s "EPMware Agent Error" admin@company.com
    fi
done
```

### Threshold Alerts

Set up alerts for resource thresholds:

```bash
# CPU usage alert
CPU_USAGE=$(ps aux | grep epmware-agent | grep -v grep | awk '{print $3}')
if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    echo "High CPU usage: $CPU_USAGE%" | mail -s "Agent CPU Alert" admin@company.com
fi
```

## Integration with Monitoring Tools

### Nagios Plugin

Create a custom Nagios plugin for agent monitoring:

```bash
#!/bin/bash
# check_epmware_agent.sh

# Check if agent is running
PID=$(ps -ef | grep -i epmware-agent | grep -v grep | awk '{print $2}')

if [ -z "$PID" ]; then
    echo "CRITICAL: EPMware Agent is not running"
    exit 2
fi

# Check last poll time (should be within last 60 seconds)
LAST_POLL=$(tail -1 ~/logs/agent-poll.log | awk '{print $1, $2}')
# Add logic to check if within threshold

echo "OK: EPMware Agent is running (PID: $PID)"
exit 0
```

### Zabbix Monitoring

Configure Zabbix items for agent monitoring:

1. **Process monitoring:**
   - Key: `proc.num[java,,,epmware-agent.jar]`
   - Trigger: Process count < 1

2. **Log monitoring:**
   - Key: `log[/home/username/logs/agent.log,"ERROR"]`
   - Trigger: Error count > 0

3. **Port monitoring:**
   - Monitor agent communication port
   - Alert on connection failures

### Splunk Integration

Forward agent logs to Splunk for advanced analytics:

**inputs.conf:**
```ini
[monitor:///home/*/logs/agent*.log]
sourcetype = epmware_agent
index = epmware
```

Create Splunk alerts for:
- Error patterns in logs
- Deployment failures
- Connection issues
- Performance degradation

## Dashboard Creation

### Monitoring Dashboard Components

Create a comprehensive monitoring dashboard including:

1. **Agent Status Panel**
   - Current status (Up/Down)
   - Uptime percentage
   - Last successful poll time

2. **Performance Metrics**
   - Response time graph
   - CPU/Memory usage trends
   - Queue size over time

3. **Deployment Statistics**
   - Success/failure rates
   - Average deployment duration
   - Deployments by application

4. **Alert Summary**
   - Recent errors
   - Critical alerts
   - Warning notifications

## Troubleshooting Monitoring Issues

### Agent Shows Offline but Is Running

1. Check network connectivity:
   ```bash
   ping epmware-server.com
   telnet epmware-server.com 443
   ```

2. Verify agent configuration:
   ```bash
   grep "ew.portal" agent.properties
   ```

3. Check firewall rules:
   ```bash
   sudo iptables -L | grep 443
   ```

### False Alerts

- Adjust polling intervals in monitoring scripts
- Increase timeout thresholds
- Implement alert suppression during maintenance

### Missing Metrics

- Verify log file permissions
- Check disk space for log storage
- Ensure monitoring scripts have proper execution rights

## Best Practices

1. **Establish Baselines**
   - Document normal performance metrics
   - Set realistic thresholds based on baselines
   - Review and adjust thresholds quarterly

2. **Implement Redundancy**
   - Use multiple monitoring methods
   - Configure backup alerting channels
   - Test failover procedures regularly

3. **Document Procedures**
   - Create runbooks for common issues
   - Document escalation procedures
   - Maintain contact lists for alerts

4. **Regular Testing**
   - Test monitoring scripts monthly
   - Verify alert delivery
   - Conduct failure scenario drills

## Related Topics

- [Agent Logs](logs.md)
- [Start and Stop Procedures](linux/start-stop.md)
- [Troubleshooting](../troubleshooting/index.md)
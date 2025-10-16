# Agent Logs

The EPMware Agent generates comprehensive log files that track all agent activities, commands, and polling operations. These logs are essential for monitoring agent health, troubleshooting issues, and auditing deployment activities.

## Log Files Location

Agent log files are automatically created in the `logs` directory under the agent installation home directory:

- **Windows**: `C:\cygwin64\home\[username]\logs\`
- **Linux**: `/home/[username]/logs/`

## Log File Types

The agent generates two primary log files:

### agent.log

The main operational log that records:
- All commands received from the EPMware application
- Command execution details and results
- Deployment activities and their outcomes
- Error messages and exceptions
- Connection establishment and termination events

**Example agent.log content:**
```
2023-11-15 10:30:45 INFO  - Agent started successfully
2023-11-15 10:30:46 INFO  - Connected to EPMware server: epmware1.epmware.com
2023-11-15 10:31:15 INFO  - Received deployment command for application: HFM_PROD
2023-11-15 10:31:16 INFO  - Executing deployment task ID: 12345
2023-11-15 10:32:30 INFO  - Deployment completed successfully
2023-11-15 10:32:31 INFO  - Response sent to EPMware server
```

### agent-poll.log

The polling activity log that records:
- Periodic polling checks (based on `agent.interval.millisecond` setting)
- Connection status confirmations
- Heartbeat messages to EPMware server
- Network connectivity issues

**Example agent-poll.log content:**
```
2023-11-15 10:30:45 INFO  - Polling started - interval: 30000ms
2023-11-15 10:31:15 INFO  - Poll check - Status: Connected
2023-11-15 10:31:45 INFO  - Poll check - Status: Connected
2023-11-15 10:32:15 INFO  - Poll check - Status: Connected
```

## Log Rotation and Management

### Manual Log Rotation

To manually rotate or archive log files:

1. **Stop the agent** (see [Start and Stop Guide](linux/start-stop.md))
2. Navigate to the logs directory
3. Archive or delete existing log files:
   ```bash
   # Archive logs with timestamp
   tar -czf agent-logs-$(date +%Y%m%d).tar.gz *.log
   
   # Remove old log files
   rm agent*.log
   ```
4. Restart the agent - new log files will be created automatically

!!! warning "Active Process Check"
    If you receive an error when trying to delete log files, the agent process is still running. Stop the agent before managing log files.

### Automatic Log Rotation

For production environments, configure automatic log rotation:

**Linux (using logrotate):**
Create `/etc/logrotate.d/epmware-agent`:
```
/home/[username]/logs/agent*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 [username] [group]
    postrotate
        # No need to restart agent for log rotation
    endscript
}
```

**Windows (using Task Scheduler):**
Create a PowerShell script for log rotation and schedule it to run daily.

## Log Level Configuration

The agent supports multiple log levels for different verbosity:

- **ERROR** - Only critical errors
- **WARN** - Warnings and errors
- **INFO** - Standard operational information (default)
- **DEBUG** - Detailed debugging information

To change the log level, add to `agent.properties`:
```properties
agent.log.level=DEBUG
```

## Viewing Logs

### Real-time Monitoring

**Linux:**
```bash
# Monitor agent.log in real-time
tail -f ~/logs/agent.log

# Monitor both logs simultaneously
tail -f ~/logs/agent*.log
```

**Windows (Cygwin):**
```bash
# Monitor agent.log
tail -f /home/Administrator/logs/agent.log

# Monitor polling log
tail -f /home/Administrator/logs/agent-poll.log
```

### Log Analysis

Common commands for log analysis:

```bash
# View last 100 lines
tail -n 100 agent.log

# Search for errors
grep ERROR agent.log

# Count deployments
grep "Deployment completed" agent.log | wc -l

# View logs for specific date
grep "2023-11-15" agent.log

# Find failed deployments
grep -E "Deployment failed|ERROR.*deployment" agent.log
```

## Common Log Patterns

### Successful Operations
- `Connected to EPMware server` - Agent successfully connected
- `Deployment completed successfully` - Deployment succeeded
- `Import completed successfully` - Application import succeeded
- `Response sent to EPMware server` - Command result sent back

### Warning Indicators
- `Connection timeout` - Network issues
- `Retry attempt` - Operation being retried
- `Queue full` - Too many pending operations
- `Slow response` - Performance issues

### Error Patterns
- `Connection refused` - Server not reachable
- `Authentication failed` - Invalid token or credentials
- `Deployment failed` - Deployment error occurred
- `Command execution failed` - Command could not be executed
- `OutOfMemoryError` - Java heap space issue

## Troubleshooting with Logs

### Connection Issues

Check `agent-poll.log` for connection patterns:
```bash
grep -i "connection\|timeout\|refused" agent-poll.log
```

### Deployment Failures

Search `agent.log` for deployment details:
```bash
grep -B5 -A5 "Deployment failed" agent.log
```

### Performance Analysis

Analyze command execution times:
```bash
grep "Executing\|completed" agent.log | grep "task ID: 12345"
```

## Log File Permissions

Ensure proper permissions for log files:

**Linux:**
```bash
chmod 644 ~/logs/*.log
chown [username]:[group] ~/logs/*.log
```

**Windows:**
Logs inherit permissions from the Cygwin user's home directory.

## Best Practices

1. **Regular Monitoring**
   - Check logs daily for errors
   - Set up alerts for critical errors
   - Monitor log file sizes

2. **Retention Policy**
   - Keep logs for at least 30 days
   - Archive older logs to separate storage
   - Compress archived logs to save space

3. **Security**
   - Ensure logs don't contain sensitive passwords
   - Restrict log file access to authorized users
   - Regularly review access permissions

4. **Disk Space Management**
   - Monitor available disk space
   - Implement automatic cleanup for old logs
   - Set maximum log file sizes if needed

## Integration with Monitoring Tools

The agent logs can be integrated with enterprise monitoring solutions:

- **Splunk** - Forward logs for centralized analysis
- **ELK Stack** - Use Filebeat to ship logs to Elasticsearch
- **Nagios** - Monitor log patterns for alerts
- **Zabbix** - Set up log monitoring items

## Related Topics

- [Monitoring](monitoring.md)
- [Troubleshooting](../troubleshooting/index.md)
- [Debug Mode](../troubleshooting/debug.md)
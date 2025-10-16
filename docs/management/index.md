# Agent Management Overview

This section covers the ongoing management, monitoring, and maintenance of the EPMware Agent after installation and configuration. Proper management ensures reliable operation and quick issue resolution.

## Management Components

<div class="grid cards" markdown>

- :material-microsoft-windows: **[Windows Services](windows/index.md)**  
  Managing agent as Windows scheduled task or service
  
- :material-linux: **[Linux Services](linux/index.md)**  
  Managing agent as Linux background process or systemd service
  
- :material-file-document-multiple: **[Agent Logs](logs.md)**  
  Understanding and managing agent log files
  
- :material-monitor-dashboard: **[Monitoring](monitoring.md)**  
  Implementing monitoring and alerting for agent health

</div>

## Daily Management Tasks

### Health Checks

Regular checks to ensure agent health:

```bash
# Quick health check
ps aux | grep epmware-agent  # Is it running?
tail -n 20 logs/agent-poll.log  # Is it polling?
grep ERROR logs/agent.log | tail -n 10  # Any errors?
```

### Log Review

Daily log review routine:

1. Check for errors or warnings
2. Verify successful deployments
3. Monitor polling frequency
4. Review resource usage

### Performance Monitoring

Track key metrics:
- CPU usage
- Memory consumption
- Network connectivity
- Deployment success rate

## Weekly Management Tasks

### Log Maintenance

Manage log file growth:

```bash
# Archive old logs
find logs/ -name "*.log" -mtime +7 -exec gzip {} \;

# Remove very old logs
find logs/ -name "*.gz" -mtime +30 -delete

# Check disk usage
du -sh logs/
```

### Configuration Backup

Weekly backup routine:

```bash
#!/bin/bash
# Weekly backup script
BACKUP_DIR="/backup/epmware/$(date +%Y-%W)"
mkdir -p $BACKUP_DIR

# Backup configuration
cp agent.properties $BACKUP_DIR/
cp ew_target_service.sh $BACKUP_DIR/

# Create archive
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
```

### Service Validation

Verify service configuration:
- Check scheduled task (Windows)
- Verify systemd service (Linux)
- Test auto-restart capability
- Review service dependencies

## Monthly Management Tasks

### Security Review

Monthly security checks:

1. **Token Rotation** - Consider refreshing REST tokens
2. **Permission Audit** - Verify file permissions
3. **Access Review** - Check user access levels
4. **Update Check** - Look for security patches

### Performance Analysis

Analyze monthly trends:

```bash
# Deployment statistics
grep "Deployment completed" logs/agent.log | wc -l

# Error frequency
grep ERROR logs/agent.log | awk '{print $1}' | uniq -c

# Average response time
grep "Response time" logs/agent.log | awk '{sum+=$NF; count++} END {print sum/count}'
```

### Capacity Planning

Review resource usage:
- Disk space trends
- Memory usage patterns
- Network bandwidth usage
- Deployment volumes

## Service Management

### Starting the Agent

Platform-specific start procedures:

**Windows:**
- Task Scheduler → Run task
- Or PowerShell command

**Linux:**
- systemctl start epmware-agent
- Or background process start

### Stopping the Agent

Graceful shutdown procedures:

**Windows:**
- Stop scheduled task
- Kill Java process

**Linux:**
- systemctl stop epmware-agent
- Or kill process

### Restarting the Agent

When to restart:
- After configuration changes
- After agent updates
- To resolve stuck processes
- As part of maintenance

## Troubleshooting Management Issues

### Agent Not Starting

Common causes and solutions:

| Issue | Check | Solution |
|-------|-------|----------|
| Java not found | `java -version` | Fix PATH or JAVA_HOME |
| Port in use | `netstat -an` | Find and stop conflicting process |
| Permission denied | File ownership | Fix with chown/chmod |
| Configuration error | agent.properties | Validate configuration syntax |

### Agent Stops Unexpectedly

Investigate unexpected stops:

```bash
# Check system logs
journalctl -u epmware-agent  # Linux systemd
eventvwr.msc  # Windows Event Viewer

# Check agent logs
tail -100 logs/agent.log | grep -E "ERROR|FATAL"

# Check memory issues
dmesg | grep -i "out of memory"
```

### Performance Degradation

Address performance issues:

1. **Check Resources**
   ```bash
   top  # Linux
   taskmgr  # Windows
   ```

2. **Review Logs**
   - Large log files?
   - Excessive errors?
   - Slow response times?

3. **Optimize Configuration**
   - Adjust polling interval
   - Tune JVM settings
   - Clean temporary files

## Automation Scripts

### Health Check Script

Automated health monitoring:

```bash
#!/bin/bash
# health_check.sh

STATUS=0
REPORT=""

# Check process
if pgrep -f epmware-agent > /dev/null; then
    REPORT="✓ Agent running\n"
else
    REPORT="✗ Agent NOT running\n"
    STATUS=1
fi

# Check recent activity
LAST_POLL=$(tail -1 logs/agent-poll.log | cut -d' ' -f1-2)
REPORT="${REPORT}Last poll: $LAST_POLL\n"

# Check errors
ERRORS=$(tail -1000 logs/agent.log | grep -c ERROR)
REPORT="${REPORT}Recent errors: $ERRORS\n"

# Send alert if issues
if [ $STATUS -ne 0 ]; then
    echo -e "$REPORT" | mail -s "EPMware Agent Alert" admin@company.com
fi

echo -e "$REPORT"
exit $STATUS
```

### Maintenance Script

Regular maintenance automation:

```bash
#!/bin/bash
# maintenance.sh

# Rotate logs
find logs/ -name "*.log" -size +100M -exec mv {} {}.old \;
find logs/ -name "*.log.old" -mtime +7 -delete

# Clean temp files
find temp/ -type f -mtime +7 -delete

# Compact database (if applicable)
# Add database maintenance here

# Restart if needed
if [ -f /tmp/agent_restart_required ]; then
    systemctl restart epmware-agent
    rm /tmp/agent_restart_required
fi
```

## Monitoring Setup

### Key Metrics to Monitor

Essential monitoring points:

| Metric | Warning Threshold | Critical Threshold |
|--------|------------------|-------------------|
| Agent Process | - | Not running |
| Polling Frequency | >60 seconds | >300 seconds |
| Error Rate | >5/hour | >20/hour |
| Deployment Success | <95% | <80% |
| Response Time | >5 seconds | >30 seconds |
| Disk Usage | >80% | >90% |

### Alerting Configuration

Set up alerts for:
- Agent process failure
- Deployment failures
- Connection timeouts
- Disk space warnings
- Memory exhaustion

## Best Practices

### Operational Excellence

1. **Regular Monitoring** - Check agent daily
2. **Proactive Maintenance** - Schedule regular tasks
3. **Documentation** - Keep runbooks updated
4. **Change Management** - Track all changes
5. **Incident Response** - Have procedures ready

### Security Management

1. **Regular Updates** - Apply security patches
2. **Access Control** - Limit agent access
3. **Audit Logging** - Monitor all activities
4. **Token Rotation** - Refresh tokens periodically
5. **Backup Encryption** - Secure backup files

### Performance Management

1. **Resource Monitoring** - Track usage trends
2. **Capacity Planning** - Plan for growth
3. **Performance Tuning** - Optimize settings
4. **Load Distribution** - Balance workloads
5. **Regular Reviews** - Analyze metrics

## Documentation Requirements

Maintain documentation for:

### Operational Documentation
- Start/stop procedures
- Troubleshooting guides
- Contact information
- Escalation procedures

### Configuration Documentation
- Current settings
- Change history
- Integration details
- Network diagrams

### Recovery Documentation
- Backup procedures
- Restore procedures
- Disaster recovery plan
- Business continuity plan

## Management Tools

### Built-in Tools

EPMware provides:
- Agent status in UI
- Deployment history
- Error reporting
- Connection testing

### External Tools

Consider integrating:
- Monitoring systems (Nagios, Zabbix)
- Log aggregators (ELK, Splunk)
- Alerting systems (PagerDuty)
- Automation tools (Ansible, Puppet)

## Upgrade Management

### Planning Upgrades

Consider when upgrading:
1. Release notes review
2. Testing in non-production
3. Backup current version
4. Maintenance window scheduling
5. Rollback plan preparation

### Upgrade Process

Standard upgrade steps:
1. Stop agent
2. Backup configuration
3. Deploy new version
4. Restore configuration
5. Test functionality
6. Monitor closely

## Next Steps

Explore specific management topics:

1. [Windows Services](windows/index.md) - Windows-specific management
2. [Linux Services](linux/index.md) - Linux-specific management
3. [Agent Logs](logs.md) - Log management details
4. [Monitoring](monitoring.md) - Monitoring implementation

!!! tip "Automation is Key"
    Automate repetitive management tasks to ensure consistency and reduce manual effort. This improves reliability and frees time for strategic work.

!!! warning "Regular Maintenance"
    Neglecting regular maintenance can lead to performance degradation, disk space issues, and unexpected failures. Establish and follow a maintenance schedule.
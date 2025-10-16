# Agent File Structure

## Overview

Understanding the EPMware Agent file structure is essential for proper configuration, troubleshooting, and maintenance. This section details each component and its purpose.

## Directory Layout

### Complete File Structure

```
home/[username]/                    # Agent root directory
├── epmware-agent.jar               # Main agent executable
├── agent.properties                # Primary configuration file
├── ew_target_service.sh            # Service startup script
├── logs/                           # Log directory
│   ├── agent.log                   # Main activity log
│   ├── agent-poll.log              # Polling activity log
│   └── agent-[date].log.gz        # Archived logs
├── temp/                           # Temporary working directory
│   ├── deploy_[timestamp]/         # Deployment staging
│   └── import_[timestamp]/         # Import staging
├── lib/                            # Additional libraries (optional)
│   └── *.jar                       # Supporting JAR files
├── config/                         # Additional configurations (optional)
│   ├── application.yml             # Spring Boot config
│   └── logback.xml                 # Logging configuration
├── scripts/                        # Custom scripts (optional)
│   ├── pre_deploy.sh              # Pre-deployment hooks
│   └── post_deploy.sh             # Post-deployment hooks
└── backup/                         # Configuration backups
    └── agent.properties.[date]     # Backed up configs
```

## Core Components

### epmware-agent.jar

The main executable JAR file containing the agent application.

**Purpose:**
- Core agent functionality
- REST API client
- Task execution engine
- Logging framework

**Details:**
```bash
# Check JAR contents
jar tf epmware-agent.jar | head -20

# Verify integrity
jar tf epmware-agent.jar > /dev/null && echo "JAR is valid"

# Check version
java -jar epmware-agent.jar --version
```

**Size:** Typically 25-30 MB

### agent.properties

Primary configuration file containing all agent settings.

**Key Sections:**
- EPMware connection settings
- Authentication tokens
- Polling intervals
- Directory paths

**Example Structure:**
```properties
# EPMware Connection
ew.portal.server=servername
ew.portal.url=https://url
ew.portal.token=token-value

# Agent Configuration
agent.interval.millisecond=30000
agent.root.dir=/home/user
```

!!! warning "Security"
    This file contains sensitive information. Always restrict access with appropriate permissions.

### ew_target_service.sh

Shell script that starts the agent service.

**Purpose:**
- Sets environment variables
- Configures Java options
- Launches the agent JAR
- Manages process lifecycle

**Default Content:**
```bash
#!/bin/bash
#mvn spring-boot:run
HOME=/home/Administrator
cd $HOME
java -jar epmware-agent.jar --spring.config.name=agent
```

**Customization Points:**
- HOME path adjustment
- Java memory settings
- Additional JVM options

## Log Directory

### agent.log

Main activity log containing:
- Deployment operations
- Import/export activities
- Error messages
- Debug information

**Sample Content:**
```
2023-11-15 10:30:00 INFO  Starting deployment for HFM_PROD
2023-11-15 10:30:05 INFO  Connecting to target application
2023-11-15 10:30:10 INFO  Deploying metadata file: entity.xml
2023-11-15 10:31:00 INFO  Deployment completed successfully
```

### agent-poll.log

Polling activity log showing:
- Regular polling intervals
- Connection status
- Task retrieval

**Sample Content:**
```
2023-11-15 10:30:00 Polling EPMware for tasks...
2023-11-15 10:30:01 No pending tasks
2023-11-15 10:30:31 Polling EPMware for tasks...
2023-11-15 10:30:32 Retrieved 1 task(s)
```

### Log Rotation

Logs are automatically rotated based on:
- Size (default: 10MB)
- Age (default: 30 days)
- Count (default: 10 files)

**Archive Format:**
```
agent-2023-11-15.log.gz
agent-poll-2023-11-15.log.gz
```

## Temporary Directory

### Purpose

The `temp/` directory is used for:
- Staging deployment files
- Processing import/export operations
- Caching downloaded content
- Working space for transformations

### Structure

```
temp/
├── deploy_20231115_103000/
│   ├── metadata.xml
│   └── validation.log
├── import_20231115_110000/
│   ├── extracted_data.csv
│   └── transform.log
└── cache/
    └── templates/
```

### Cleanup

Temporary files are cleaned up:
- After successful operation completion
- On agent restart
- Based on retention policy (default: 7 days)

## Optional Directories

### lib/ Directory

Contains additional JAR files for:
- Database drivers
- Custom extensions
- Third-party libraries

**Example:**
```
lib/
├── ojdbc8.jar          # Oracle JDBC driver
├── mysql-connector.jar  # MySQL driver
└── custom-utils.jar    # Custom utilities
```

### config/ Directory

Additional configuration files:

**application.yml:**
```yaml
spring:
  application:
    name: epmware-agent
  profiles:
    active: production
    
logging:
  level:
    root: INFO
    com.epmware: DEBUG
```

**logback.xml:**
```xml
<configuration>
    <appender name="FILE" class="ch.qos.logback.core.FileAppender">
        <file>logs/agent.log</file>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} %-5level %msg%n</pattern>
        </encoder>
    </appender>
</configuration>
```

### scripts/ Directory

Custom automation scripts:

**pre_deploy.sh:**
```bash
#!/bin/bash
# Pre-deployment validation
echo "Validating deployment package..."
# Custom validation logic
```

**post_deploy.sh:**
```bash
#!/bin/bash
# Post-deployment cleanup
echo "Cleaning up temporary files..."
# Cleanup logic
```

## File Permissions

### Recommended Permissions

| File/Directory | Windows (Cygwin) | Linux | Notes |
|---------------|------------------|-------|-------|
| `agent.properties` | 644 | 600 | Restrict access to sensitive data |
| `*.sh` scripts | 755 | 755 | Execute permission required |
| `*.jar` files | 644 | 644 | Read access sufficient |
| `logs/` | 755 | 755 | Write permission for agent user |
| `temp/` | 755 | 755 | Write permission for agent user |

### Setting Permissions

**Linux:**
```bash
# Set permissions
chmod 600 agent.properties
chmod 755 *.sh
chmod 644 *.jar
chmod 755 logs temp

# Set ownership
chown -R epmadmin:epmadmin /home/epmadmin
```

**Windows (Cygwin):**
```bash
# Set permissions
chmod 644 agent.properties
chmod 755 *.sh
chmod 644 *.jar
```

## File Size Management

### Monitoring Disk Usage

```bash
# Check overall usage
du -sh ~/

# Check specific directories
du -sh logs/
du -sh temp/

# Find large files
find ~ -type f -size +100M
```

### Space Requirements

| Component | Typical Size | Maximum Size |
|-----------|-------------|--------------|
| Agent files | 50 MB | 100 MB |
| Logs (active) | 100 MB | 1 GB |
| Logs (archived) | 500 MB | 5 GB |
| Temp files | 100 MB | 2 GB |
| **Total** | **750 MB** | **8 GB** |

## Backup Strategy

### What to Backup

Priority files for backup:
1. `agent.properties` - Critical configuration
2. `*.sh` scripts - Customized scripts
3. `config/` directory - Additional configs
4. `scripts/` directory - Custom automation

### Backup Script

```bash
#!/bin/bash
# Agent backup script
BACKUP_DIR="/backup/epmware/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Backup critical files
cp agent.properties $BACKUP_DIR/
cp *.sh $BACKUP_DIR/
cp -r config/ $BACKUP_DIR/ 2>/dev/null
cp -r scripts/ $BACKUP_DIR/ 2>/dev/null

# Create archive
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
rm -rf $BACKUP_DIR

echo "Backup created: $BACKUP_DIR.tar.gz"
```

## Troubleshooting File Issues

### Missing Files

| Missing File | Impact | Resolution |
|-------------|---------|------------|
| `epmware-agent.jar` | Agent won't start | Re-extract from zip |
| `agent.properties` | No configuration | Create from template |
| `ew_target_service.sh` | Can't start service | Re-extract or recreate |

### Corrupted Files

**Check JAR integrity:**
```bash
# Test JAR file
java -jar epmware-agent.jar --test
# Or
jar tf epmware-agent.jar > /dev/null
echo "Exit code: $?"  # Should be 0
```

**Verify configuration:**
```bash
# Check properties syntax
grep -E "^[^#].*=" agent.properties
```

### Permission Issues

**Common problems and fixes:**

```bash
# Fix: Cannot execute script
chmod +x ew_target_service.sh

# Fix: Cannot write logs
chmod 755 logs
mkdir -p logs

# Fix: Cannot read properties
chmod 644 agent.properties
```

## Best Practices

### File Organization

1. **Keep root clean** - Only essential files in home directory
2. **Use subdirectories** - Organize custom content
3. **Regular cleanup** - Remove old logs and temp files
4. **Document changes** - Track modifications to scripts

### Security

1. **Restrict access** - Limit file permissions
2. **Protect tokens** - Secure agent.properties
3. **Audit access** - Monitor file access logs
4. **Encrypt backups** - Protect backed up configurations

### Maintenance

1. **Monitor growth** - Watch log and temp directories
2. **Archive old logs** - Compress and move old files
3. **Update documentation** - Keep file inventory current
4. **Test recovery** - Verify backup restoration

## Environment-Specific Structures

### Development Environment

Simplified structure for development:
```
home/dev_user/
├── epmware-agent.jar
├── agent.properties
├── ew_target_service.sh
└── logs/
```

### Production Environment

Complete structure with monitoring:
```
home/prod_user/
├── epmware-agent.jar
├── agent.properties
├── ew_target_service.sh
├── logs/
├── config/
├── scripts/
├── backup/
└── monitoring/
    ├── health_check.sh
    └── metrics.log
```

## Next Steps

After understanding the file structure:

1. [Configure Agent Properties](../../configuration/agent-properties.md)
2. [Set Up Service Configuration](../../configuration/service-config.md)
3. [Generate REST Token](../../configuration/rest-token.md)
4. [Test the Installation](../../configuration/testing.md)
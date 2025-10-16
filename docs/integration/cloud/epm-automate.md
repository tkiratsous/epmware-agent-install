# EPM Automate Configuration

Comprehensive guide for installing, configuring, and using EPM Automate utility with the EPMware Agent for Oracle Cloud EPM integration.

## Overview

EPM Automate is Oracle's command-line utility that enables:
- Remote task execution in Oracle Cloud EPM
- Automated metadata and data management
- Scripted deployments and backups
- Integration with third-party tools

## Installation

### System Requirements

| Requirement | Specification |
|------------|--------------|
| **Operating System** | Windows, Linux, macOS |
| **Java** | JRE 1.8 or higher |
| **Memory** | 512 MB minimum |
| **Disk Space** | 500 MB |
| **Network** | Internet access, TLS 1.2+ |

### Windows Installation

#### Step 1: Download

1. Access your Oracle Cloud EPM environment
2. Click your username → **Downloads**
3. Select **Download for Windows** under EPM Automate

![EPM Automate Download](../../assets/images/integration/epm-automate-download.png)<br/>
*Downloading EPM Automate from Oracle Cloud*

#### Step 2: Install

```powershell
# Run installer as Administrator
EPM Automate.exe

# Default installation path
C:\Oracle\EPM Automate\

# Verify installation
C:\Oracle\EPM Automate\bin\epmautomate.bat --version
```

#### Step 3: Configure PATH

```powershell
# Add to system PATH
[Environment]::SetEnvironmentVariable(
    "Path",
    $env:Path + ";C:\Oracle\EPM Automate\bin",
    "Machine"
)

# Verify
epmautomate --version
```

### Linux Installation

#### Step 1: Download

```bash
# Download from Oracle Cloud
wget https://your-instance.oraclecloud.com/interop/epmautomate/EPMAutomate.tar

# Or download via browser and transfer
scp EPMAutomate.tar user@server:/tmp/
```

#### Step 2: Extract and Configure

```bash
# Extract to home directory
cd ~
tar xf /tmp/EPMAutomate.tar

# Set environment variables
export JAVA_HOME=/usr/java/latest
export PATH=$PATH:~/epmautomate/bin

# Make permanent (add to .bashrc)
echo 'export JAVA_HOME=/usr/java/latest' >> ~/.bashrc
echo 'export PATH=$PATH:~/epmautomate/bin' >> ~/.bashrc
source ~/.bashrc
```

#### Step 3: Verify Installation

```bash
# Check version
epmautomate.sh --version

# Test execution
epmautomate.sh help
```

### macOS Installation

```bash
# Extract archive
tar xf EPMAutomate.tar

# Configure environment
export JAVA_HOME=$(/usr/libexec/java_home)
export PATH=$PATH:~/epmautomate/bin

# Verify
epmautomate.sh --version
```

## Configuration for EPMware Agent

### Directory Structure

```
/home/epmware_agent/
├── agent.properties
├── ew_target_service.sh
├── epmware-agent.jar
└── epmautomate/
    ├── bin/
    │   ├── epmautomate.sh
    │   └── epmautomate.bat
    ├── lib/
    ├── jre/
    └── logs/
```

### Agent Properties Configuration

Add to `agent.properties`:

```properties
# EPM Automate configuration
epmautomate.enabled=true
epmautomate.path=/home/epmware_agent/epmautomate/bin
epmautomate.timeout=3600000
epmautomate.retry.count=3
epmautomate.retry.delay=30000

# Cloud connection settings
cloud.url=https://instance.oraclecloud.com
cloud.identity.domain=mycompany
cloud.user=ServiceAdmin
cloud.password.encrypted=true
```

### Environment Variables

```bash
# Set in ew_target_service.sh
export EPM_AUTOMATE_HOME=/home/epmware_agent/epmautomate
export PATH=$EPM_AUTOMATE_HOME/bin:$PATH
export JAVA_HOME=/usr/java/latest

# EPM Automate specific
export EPM_AUTOMATE_LOG_LEVEL=INFO
export EPM_AUTOMATE_TIMEOUT=3600
```

## Authentication Configuration

### Password File Method

```bash
# Create encrypted password file
echo "myPassword" > .password
chmod 600 .password

# Use in scripts
epmautomate login username .password $URL $DOMAIN
```

### OAuth Configuration

```bash
# Initial OAuth setup
epmautomate login username password $URL $DOMAIN AuthType=OAuth

# Save refresh token
epmautomate getrefreshtoken > .refresh_token

# Use refresh token
epmautomate login username .refresh_token $URL $DOMAIN AuthType=OAuth RefreshToken=true
```

### SSO Configuration

```properties
# For SSO-enabled environments
cloud.auth.type=SSO
cloud.sso.provider=OKTA
cloud.sso.endpoint=https://company.okta.com
```

## EPM Automate Commands

### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `login` | Connect to service | `epmautomate login user pwd url domain` |
| `logout` | Disconnect | `epmautomate logout` |
| `uploadfile` | Upload file | `epmautomate uploadfile data.zip` |
| `downloadfile` | Download file | `epmautomate downloadfile report.pdf` |
| `listfiles` | List files | `epmautomate listfiles` |
| `deletefile` | Delete file | `epmautomate deletefile old.zip` |

### Metadata Commands

```bash
# Import metadata
epmautomate uploadfile metadata.zip
epmautomate importmetadata metadata.zip
epmautomate deletefile metadata.zip

# Export metadata
epmautomate exportmetadata ALL
epmautomate downloadfile metadata.zip

# Validate metadata
epmautomate validatemetadata metadata.zip
```

### Data Management

```bash
# Import data
epmautomate uploadfile data.csv
epmautomate importdata data.csv
epmautomate runbatch

# Export data
epmautomate exportdata dataexport.csv
epmautomate downloadfile dataexport.csv

# Clear data
epmautomate cleardata "Year=FY21,Scenario=Actual"
```

### Application Management

```bash
# Application snapshot
epmautomate exportsnapshot snapshot_$(date +%Y%m%d)

# Import snapshot
epmautomate importsnapshot backup_snapshot

# Refresh database
epmautomate refreshcube

# Run calculation
epmautomate runbusinessrule "Calculate Revenue"
```

## Scripting with EPM Automate

### Basic Script Template

```bash
#!/bin/bash
# epm_automate_template.sh

# Configuration
URL="https://instance.oraclecloud.com"
DOMAIN="mycompany"
USER="ServiceAdmin"
PASSWORD_FILE=".password"

# Functions
login() {
    echo "Logging in..."
    epmautomate login $USER $PASSWORD_FILE $URL $DOMAIN
}

logout() {
    echo "Logging out..."
    epmautomate logout
}

handle_error() {
    echo "Error occurred: $1"
    logout
    exit 1
}

# Main execution
trap 'handle_error "Script interrupted"' INT TERM

login || handle_error "Login failed"

# Your operations here
epmautomate listfiles || handle_error "List files failed"

logout
echo "Script completed successfully"
```

### Advanced Deployment Script

```bash
#!/bin/bash
# deploy_metadata.sh

set -e  # Exit on error

# Configuration
source config.env

# Logging
LOG_FILE="deployment_$(date +%Y%m%d_%H%M%S).log"
exec 1> >(tee -a "$LOG_FILE")
exec 2>&1

echo "=== EPM Deployment Started: $(date) ==="

# Login with retry
MAX_RETRIES=3
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if epmautomate login $USER $PWD_FILE $URL $DOMAIN; then
        echo "Login successful"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        echo "Login attempt $RETRY_COUNT failed"
        sleep 30
    fi
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "Login failed after $MAX_RETRIES attempts"
    exit 1
fi

# Backup before deployment
echo "Creating backup..."
epmautomate exportsnapshot "backup_pre_deploy_$(date +%Y%m%d)"

# Deploy metadata
for file in metadata/*.zip; do
    echo "Processing $file..."
    epmautomate uploadfile "$file"
    epmautomate importmetadata "$(basename $file)"
    epmautomate deletefile "$(basename $file)"
done

# Validate
echo "Validating deployment..."
epmautomate refreshcube
epmautomate validatedata

# Cleanup and logout
epmautomate logout
echo "=== Deployment Completed: $(date) ==="
```

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `EPMCSS-00001` | Invalid credentials | Check username/password |
| `EPMCSS-00301` | Session timeout | Re-login |
| `EPMCSS-20004` | File not found | Verify file path |
| `EPMCSS-20705` | Import failed | Check file format |
| `Connection refused` | Network issue | Check firewall/proxy |

### Error Handling in Scripts

```bash
# Function to handle EPM Automate errors
check_error() {
    local exit_code=$?
    local operation=$1
    
    if [ $exit_code -ne 0 ]; then
        echo "Error: $operation failed with exit code $exit_code"
        
        # Get detailed error
        epmautomate getlogs > error_detail.log 2>&1
        
        # Send alert
        mail -s "EPM Deployment Failed" admin@company.com < error_detail.log
        
        # Cleanup
        epmautomate logout 2>/dev/null
        exit $exit_code
    fi
}

# Usage
epmautomate login $USER $PWD $URL $DOMAIN
check_error "Login"

epmautomate importmetadata metadata.zip
check_error "Metadata import"
```

## Performance Optimization

### Connection Optimization

```bash
# Keep connection alive
epmautomate setsubstvars keepAlive=true

# Increase timeout for large operations
epmautomate setsubstvars operationTimeout=7200

# Enable compression
epmautomate setsubstvars compression=true
```

### Batch Processing

```bash
# Process files in batches
find . -name "*.csv" -print0 | \
    xargs -0 -n 10 -P 2 -I {} epmautomate uploadfile {}
```

### Parallel Execution

```bash
#!/bin/bash
# parallel_deploy.sh

# Function for parallel processing
process_file() {
    local file=$1
    epmautomate uploadfile "$file"
    epmautomate importdata "$(basename $file)"
    epmautomate deletefile "$(basename $file)"
}

export -f process_file

# Process files in parallel (max 4 concurrent)
find data/ -name "*.csv" | parallel -j 4 process_file
```

## Security Best Practices

### Credential Security

```bash
# Encrypt password file
openssl enc -aes-256-cbc -salt -in password.txt -out password.enc

# Decrypt for use
openssl enc -aes-256-cbc -d -in password.enc | epmautomate login $USER - $URL $DOMAIN

# Use environment variables
export EPM_PASSWORD=$(openssl enc -aes-256-cbc -d -in password.enc)
epmautomate login $USER $EPM_PASSWORD $URL $DOMAIN
unset EPM_PASSWORD
```

### Audit Logging

```bash
# Enable detailed logging
export EPM_AUTOMATE_LOG_LEVEL=DEBUG
export EPM_AUTOMATE_LOG_FILE=/var/log/epm/epm_automate.log

# Log all operations
epmautomate() {
    echo "[$(date)] Executing: epmautomate $*" >> $EPM_AUTOMATE_LOG_FILE
    command epmautomate "$@"
    echo "[$(date)] Exit code: $?" >> $EPM_AUTOMATE_LOG_FILE
}
```

## Monitoring and Logging

### Log Configuration

```properties
# Log settings
epmautomate.log.enabled=true
epmautomate.log.level=INFO
epmautomate.log.file=/var/log/epmware/epmautomate.log
epmautomate.log.max.size=100MB
epmautomate.log.max.files=10
```

### Monitoring Script

```bash
#!/bin/bash
# monitor_epm_automate.sh

LOG_FILE="/var/log/epmware/epmautomate.log"
ERROR_COUNT=0

# Monitor for errors
tail -f $LOG_FILE | while read line; do
    if echo "$line" | grep -q "ERROR\|FAILED"; then
        ERROR_COUNT=$((ERROR_COUNT + 1))
        
        # Alert if threshold exceeded
        if [ $ERROR_COUNT -gt 5 ]; then
            echo "High error rate detected" | \
                mail -s "EPM Automate Alert" admin@company.com
            ERROR_COUNT=0
        fi
    fi
done
```

## Upgrading EPM Automate

### Check for Updates

```bash
# Check current version
epmautomate --version

# Check for available updates
epmautomate upgrade -c
```

### Upgrade Process

```bash
# Automatic upgrade
epmautomate upgrade -f

# Manual upgrade
# 1. Download new version
# 2. Backup current installation
cp -r ~/epmautomate ~/epmautomate.backup

# 3. Extract new version
tar xf EPMAutomate_new.tar

# 4. Verify upgrade
epmautomate --version
```

## Integration with EPMware Agent

### Agent Script Integration

```bash
#!/bin/bash
# agent_epm_automate.sh

# Called by EPMware Agent
OPERATION=$1
PARAMETERS=$2

case $OPERATION in
    deploy)
        epmautomate login $USER $PWD $URL $DOMAIN
        epmautomate uploadfile $PARAMETERS
        epmautomate importmetadata $(basename $PARAMETERS)
        epmautomate logout
        ;;
    
    backup)
        epmautomate login $USER $PWD $URL $DOMAIN
        epmautomate exportsnapshot $PARAMETERS
        epmautomate downloadfile "$PARAMETERS.zip"
        epmautomate logout
        ;;
    
    *)
        echo "Unknown operation: $OPERATION"
        exit 1
        ;;
esac
```

## Troubleshooting

### Debug Mode

```bash
# Enable debug output
export EPM_AUTOMATE_LOG_LEVEL=DEBUG

# Verbose output
epmautomate login $USER $PWD $URL $DOMAIN -v

# Trace network calls
export EPM_AUTOMATE_TRACE=true
```

### Common Issues

```bash
# SSL/TLS issues
epmautomate login $USER $PWD $URL $DOMAIN TrustAll=true

# Proxy issues
export HTTPS_PROXY=http://proxy:8080
epmautomate login $USER $PWD $URL $DOMAIN

# Timeout issues
epmautomate setsubstvars connectionTimeout=120
```

## Best Practices Checklist

- [ ] Always use encrypted password files
- [ ] Implement error handling in scripts
- [ ] Log all operations for audit
- [ ] Test scripts in non-production first
- [ ] Keep EPM Automate updated
- [ ] Use version control for scripts
- [ ] Document custom scripts
- [ ] Implement monitoring
- [ ] Regular backup before changes
- [ ] Clean up temporary files

!!! tip "Script Library"
    Build a library of reusable EPM Automate scripts for common operations. This speeds up development and ensures consistency.

!!! warning "Rate Limits"
    Be aware of Oracle Cloud rate limits. Implement throttling in scripts to avoid hitting API limits.

## Next Steps

- [PCMCS Configuration](pcmcs.md) - PCMCS-specific setup
- [Upgrade Process](upgrade.md) - Keep EPM Automate current
- [Cloud Integration](index.md) - Cloud services overview
- [Troubleshooting](../../troubleshooting/index.md) - Resolve issues
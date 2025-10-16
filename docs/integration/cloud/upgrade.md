# EPM Automate Upgrade Process

This guide covers the upgrade process for EPM Automate utility and maintaining compatibility with Oracle Cloud EPM services.

## Overview

Oracle releases EPM Automate updates monthly with:
- New features and commands
- Bug fixes and performance improvements
- Security patches
- Compatibility updates for cloud services

## Upgrade Strategy

### Why Upgrade Regularly

1. **Compatibility** - Cloud services evolve, requiring client updates
2. **Security** - Critical security patches
3. **Features** - New functionality and improvements
4. **Performance** - Optimization and bug fixes
5. **Support** - Oracle only supports recent versions

### Upgrade Frequency

| Environment | Recommended Frequency | Notes |
|-------------|---------------------|-------|
| **Production** | Monthly | After testing in non-prod |
| **UAT/Test** | Monthly | Before production |
| **Development** | As available | Test new features |

## Pre-Upgrade Checklist

### Before You Upgrade

- [ ] Check current version
- [ ] Review release notes
- [ ] Backup current installation
- [ ] Document custom configurations
- [ ] Test in non-production
- [ ] Schedule maintenance window
- [ ] Notify stakeholders
- [ ] Prepare rollback plan

### Version Check

```bash
# Check current version
epmautomate --version

# Sample output
EPM Automate version 23.11.75
Build: 2023-11-15 10:30:00
```

## Upgrade Methods

### Method 1: Auto-Upgrade (Recommended)

#### Check for Updates

```bash
# Check if update available
epmautomate upgrade -c

# Output if update available
A new version of EPM Automate is available: 23.11.76
Current version: 23.11.75
```

#### Perform Auto-Upgrade

```bash
# Auto-upgrade with confirmation
epmautomate upgrade

# Force upgrade without confirmation
epmautomate upgrade -f

# Upgrade with proxy
epmautomate upgrade -f ProxyHost=proxy.company.com ProxyPort=8080
```

### Method 2: Manual Download and Install

#### Windows Manual Upgrade

```powershell
# 1. Download new version from Oracle Cloud
# 2. Backup current installation
Copy-Item "C:\Oracle\EPM Automate" "C:\Oracle\EPM Automate_backup" -Recurse

# 3. Run new installer
.\EPMAutomate.exe

# 4. Verify upgrade
epmautomate --version
```

#### Linux Manual Upgrade

```bash
# 1. Download new version
wget https://download-url/EPMAutomate.tar

# 2. Backup current installation
cp -r ~/epmautomate ~/epmautomate_backup_$(date +%Y%m%d)

# 3. Extract new version
tar xf EPMAutomate.tar -C ~/

# 4. Verify upgrade
~/epmautomate/bin/epmautomate.sh --version
```

### Method 3: Scripted Upgrade

```bash
#!/bin/bash
# upgrade_epm_automate.sh

# Configuration
EPM_HOME="/opt/epmware/epmautomate"
BACKUP_DIR="/opt/backup/epmautomate"
LOG_FILE="/var/log/epm_upgrade_$(date +%Y%m%d).log"

# Logging
exec 1> >(tee -a "$LOG_FILE")
exec 2>&1

echo "=== EPM Automate Upgrade Started: $(date) ==="

# Check current version
CURRENT_VERSION=$(epmautomate --version | head -1)
echo "Current version: $CURRENT_VERSION"

# Check for updates
if epmautomate upgrade -c | grep -q "new version"; then
    echo "Update available"
    
    # Backup current installation
    echo "Creating backup..."
    mkdir -p $BACKUP_DIR
    cp -r $EPM_HOME $BACKUP_DIR/epmautomate_$(date +%Y%m%d_%H%M%S)
    
    # Perform upgrade
    echo "Upgrading EPM Automate..."
    epmautomate upgrade -f
    
    # Verify upgrade
    NEW_VERSION=$(epmautomate --version | head -1)
    echo "New version: $NEW_VERSION"
    
    # Test basic functionality
    echo "Testing upgraded version..."
    epmautomate help > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Upgrade successful"
    else
        echo "Upgrade failed - rolling back"
        # Rollback logic here
    fi
else
    echo "No updates available"
fi

echo "=== Upgrade Process Completed: $(date) ==="
```

## Post-Upgrade Validation

### Validation Steps

#### Step 1: Version Verification

```bash
# Verify version updated
epmautomate --version

# Check build date
epmautomate --version | grep Build
```

#### Step 2: Functionality Test

```bash
#!/bin/bash
# test_epm_automate.sh

echo "Testing EPM Automate functionality..."

# Test help command
if epmautomate help > /dev/null 2>&1; then
    echo "✓ Help command works"
else
    echo "✗ Help command failed"
fi

# Test login (if credentials available)
if [ -f .credentials ]; then
    source .credentials
    if epmautomate login $USER $PASSWORD $URL $DOMAIN; then
        echo "✓ Login successful"
        epmautomate logout
    else
        echo "✗ Login failed"
    fi
fi
```

#### Step 3: Script Compatibility

```bash
# Test existing scripts
for script in scripts/*.sh; do
    echo "Testing $script..."
    bash -n $script  # Syntax check
    if [ $? -eq 0 ]; then
        echo "✓ $script syntax OK"
    else
        echo "✗ $script has syntax errors"
    fi
done
```

### Integration Testing

```bash
#!/bin/bash
# integration_test.sh

# Test with EPMware Agent
echo "Testing EPMware Agent integration..."

# Check if agent can find EPM Automate
if $AGENT_HOME/ew_target_service.sh test-epm; then
    echo "✓ Agent integration successful"
else
    echo "✗ Agent integration failed"
fi

# Test deployment
if $AGENT_HOME/test_deployment.sh; then
    echo "✓ Test deployment successful"
else
    echo "✗ Test deployment failed"
fi
```

## Rollback Procedure

### When to Rollback

- Upgrade fails to complete
- Critical functionality broken
- Integration issues with EPMware Agent
- Performance degradation

### Rollback Steps

```bash
#!/bin/bash
# rollback_epm_automate.sh

BACKUP_DIR="/opt/backup/epmautomate"
EPM_HOME="/opt/epmware/epmautomate"

echo "Starting EPM Automate rollback..."

# Find most recent backup
LATEST_BACKUP=$(ls -t $BACKUP_DIR | head -1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "No backup found!"
    exit 1
fi

echo "Rolling back to: $LATEST_BACKUP"

# Remove current installation
rm -rf $EPM_HOME

# Restore backup
cp -r $BACKUP_DIR/$LATEST_BACKUP $EPM_HOME

# Verify rollback
epmautomate --version

echo "Rollback completed"
```

## Automated Upgrade Management

### Scheduled Upgrade Script

```bash
#!/bin/bash
# scheduled_upgrade.sh
# Run monthly via cron

# Configuration
NOTIFICATION_EMAIL="admin@company.com"
TEST_FIRST=true

# Function to send notification
notify() {
    local subject=$1
    local message=$2
    echo "$message" | mail -s "$subject" $NOTIFICATION_EMAIL
}

# Check for updates
UPDATE_CHECK=$(epmautomate upgrade -c 2>&1)

if echo "$UPDATE_CHECK" | grep -q "new version"; then
    notify "EPM Automate Update Available" "$UPDATE_CHECK"
    
    if [ "$TEST_FIRST" = true ]; then
        # Test in development first
        ssh dev-server "/opt/scripts/upgrade_epm_automate.sh"
        
        if [ $? -eq 0 ]; then
            notify "EPM Automate Upgrade" "Dev upgrade successful, proceeding with production"
            # Proceed with production upgrade
            /opt/scripts/upgrade_epm_automate.sh
        else
            notify "EPM Automate Upgrade Failed" "Dev upgrade failed, skipping production"
        fi
    else
        # Direct upgrade
        /opt/scripts/upgrade_epm_automate.sh
    fi
fi
```

### Cron Configuration

```bash
# Add to crontab
# Check for updates weekly, upgrade monthly

# Weekly update check (Mondays at 9 AM)
0 9 * * 1 /opt/scripts/check_epm_updates.sh

# Monthly upgrade (First Sunday at 2 AM)
0 2 1-7 * 0 /opt/scripts/scheduled_upgrade.sh
```

## Version Compatibility Matrix

### EPM Automate vs Cloud Services

| EPM Automate Version | Compatible Cloud Versions | Notes |
|---------------------|--------------------------|-------|
| 23.11.x | 23.10 - 23.12 | Current |
| 23.10.x | 23.09 - 23.11 | Supported |
| 23.09.x | 23.08 - 23.10 | Limited support |
| < 23.09 | Various | Upgrade required |

### Feature Availability

```bash
#!/bin/bash
# check_features.sh

VERSION=$(epmautomate --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
MAJOR=$(echo $VERSION | cut -d. -f1)
MINOR=$(echo $VERSION | cut -d. -f2)

echo "Version: $VERSION"

# Check feature availability
if [ $MAJOR -ge 23 ] && [ $MINOR -ge 11 ]; then
    echo "✓ OAuth 2.0 support"
    echo "✓ Parallel processing"
    echo "✓ Enhanced encryption"
else
    echo "✗ Missing latest features - upgrade recommended"
fi
```

## Troubleshooting Upgrade Issues

### Common Upgrade Problems

| Issue | Cause | Solution |
|-------|-------|----------|
| Upgrade fails | Network issues | Check proxy/firewall settings |
| Version mismatch | Partial upgrade | Clean install |
| Scripts break | API changes | Review release notes |
| Performance issues | Configuration reset | Restore custom settings |
| Connection errors | TLS version | Update Java/certificates |

### Debug Upgrade Process

```bash
# Enable debug logging
export EPM_AUTOMATE_LOG_LEVEL=DEBUG

# Verbose upgrade
epmautomate upgrade -f -v

# Check upgrade logs
tail -f ~/epmautomate/logs/upgrade.log
```

### Fix Corrupted Installation

```bash
#!/bin/bash
# fix_installation.sh

echo "Fixing EPM Automate installation..."

# Remove corrupted installation
rm -rf ~/epmautomate

# Download fresh copy
wget https://download-url/EPMAutomate.tar

# Extract
tar xf EPMAutomate.tar

# Configure
export JAVA_HOME=/usr/java/latest
export PATH=$PATH:~/epmautomate/bin

# Verify
epmautomate --version
```

## Best Practices

### Upgrade Guidelines

1. **Test First** - Always test in non-production
2. **Backup Always** - Keep installation backups
3. **Document Changes** - Track version history
4. **Review Notes** - Read release notes carefully
5. **Plan Rollback** - Have recovery plan ready

### Version Management

```bash
# Track version history
echo "$(date),$(epmautomate --version)" >> /var/log/epm_versions.csv

# Maintain version documentation
cat > version_history.md << EOF
# EPM Automate Version History

| Date | Version | Changes | Issues |
|------|---------|---------|--------|
| $(date +%Y-%m-%d) | $(epmautomate --version | head -1) | Upgraded | None |
EOF
```

### Testing Framework

```bash
#!/bin/bash
# test_framework.sh

# Test suite for EPM Automate
run_tests() {
    local status=0
    
    # Basic tests
    test_command "help"
    test_command "listcommands"
    
    # Connection tests
    if [ -f .test_credentials ]; then
        source .test_credentials
        test_login
        test_operations
    fi
    
    return $status
}

test_command() {
    local cmd=$1
    if epmautomate $cmd > /dev/null 2>&1; then
        echo "✓ Command '$cmd' passed"
    else
        echo "✗ Command '$cmd' failed"
        status=1
    fi
}

# Run tests
run_tests
exit $status
```

## Monitoring Upgrade Status

### Health Check Script

```bash
#!/bin/bash
# health_check_post_upgrade.sh

echo "=== Post-Upgrade Health Check ==="

# Version info
echo "Version: $(epmautomate --version | head -1)"

# Check core functionality
CHECKS_PASSED=0
CHECKS_TOTAL=0

# Check 1: Help command
((CHECKS_TOTAL++))
if epmautomate help > /dev/null 2>&1; then
    echo "✓ Help command"
    ((CHECKS_PASSED++))
else
    echo "✗ Help command"
fi

# Check 2: List commands
((CHECKS_TOTAL++))
if epmautomate listcommands > /dev/null 2>&1; then
    echo "✓ List commands"
    ((CHECKS_PASSED++))
else
    echo "✗ List commands"
fi

# Summary
echo "Health Check: $CHECKS_PASSED/$CHECKS_TOTAL passed"

if [ $CHECKS_PASSED -eq $CHECKS_TOTAL ]; then
    echo "Status: HEALTHY"
    exit 0
else
    echo "Status: DEGRADED"
    exit 1
fi
```

!!! tip "Staging Upgrades"
    Maintain separate EPM Automate installations for different environments to test upgrades progressively through dev → test → production.

!!! warning "Breaking Changes"
    Always review release notes for breaking changes. Oracle occasionally deprecates commands or changes syntax.

## Next Steps

- [EPM Automate Configuration](epm-automate.md) - Detailed setup
- [PCMCS Configuration](pcmcs.md) - PCMCS integration
- [Cloud Integration](index.md) - Cloud services overview
- [Troubleshooting](../../troubleshooting/index.md) - Resolve issues
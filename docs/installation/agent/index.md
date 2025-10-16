# Agent Installation Overview

This section covers the deployment and setup of EPMware Agent files on your server. The agent installation involves extracting files to the appropriate location and verifying the installation structure.

## Installation Process

<div class="grid cards" markdown>

- :material-download: **[Download and Extract](download.md)**  
  Obtain and deploy agent files to the server
  
- :material-folder-outline: **[File Structure](file-structure.md)**  
  Understand agent components and directory layout

</div>

## Installation Steps Summary

### Step 1: Obtain Agent Package

- Download `ew_agent_files.zip` from EPMware
- Transfer to target server
- Verify file integrity

### Step 2: Extract Files

- Extract to user home directory
- Verify extraction location
- Check file permissions

### Step 3: Verify Structure

- Confirm all files present
- Review directory layout
- Set appropriate permissions

## Pre-Installation Checklist

Before installing the agent files:

### Prerequisites Completed
- [ ] Cygwin installed (Windows only)
- [ ] Java configured and accessible
- [ ] User account created for agent
- [ ] Home directory accessible

### Information Ready
- [ ] Know installation directory path
- [ ] Have agent package file
- [ ] Understand file structure requirements

### System Prepared
- [ ] Sufficient disk space (minimum 1GB)
- [ ] Required permissions available
- [ ] Network connectivity verified

## Installation Locations

### Standard Installation Paths

**Windows (with Cygwin):**
```
C:\cygwin64\home\[username]\
```

**Linux:**
```
/home/[username]/
or
/opt/epmware/agent/
```

### Directory Structure After Installation

```
[installation_directory]/
├── epmware-agent.jar
├── agent.properties
├── ew_target_service.sh
├── logs/
├── temp/
└── [optional directories]
```

## Quick Installation Commands

### Windows (Cygwin)

```bash
# Navigate to home
cd ~

# Extract agent
unzip ew_agent_files.zip

# Set permissions
chmod +x ew_target_service.sh

# Verify
ls -la
```

### Linux

```bash
# Navigate to home
cd /home/epmadmin

# Extract agent
unzip ew_agent_files.zip

# Set permissions
chmod 755 ew_target_service.sh
chmod 600 agent.properties

# Verify
ls -la
```

## Installation Methods

### Method 1: Direct Extraction

Extract directly to the target location:

```bash
# Direct extraction
cd /home/epmadmin
unzip /tmp/ew_agent_files.zip
```

### Method 2: Extract and Move

Extract to temporary location then move:

```bash
# Extract to temp
cd /tmp
unzip ew_agent_files.zip

# Move to final location
mv ew_agent_files/* /home/epmadmin/
```

### Method 3: Automated Installation

Use a script for consistent installation:

```bash
#!/bin/bash
# install_agent.sh

AGENT_USER="epmadmin"
AGENT_HOME="/home/$AGENT_USER"
AGENT_ZIP="/tmp/ew_agent_files.zip"

# Extract files
su - $AGENT_USER -c "cd ~ && unzip $AGENT_ZIP"

# Set permissions
chown -R $AGENT_USER:$AGENT_USER $AGENT_HOME
chmod 755 $AGENT_HOME/*.sh
chmod 600 $AGENT_HOME/*.properties

echo "Agent installed successfully"
```

## Post-Installation Verification

### File Verification

Check that all required files are present:

```bash
# Required files checklist
for file in epmware-agent.jar agent.properties ew_target_service.sh; do
  if [ -f "$file" ]; then
    echo "✓ $file exists"
  else
    echo "✗ $file missing"
  fi
done
```

### Permission Verification

Ensure correct permissions:

```bash
# Check permissions
ls -la | grep -E "agent\.properties|\.sh|\.jar"

# Expected output:
# -rw------- agent.properties (600)
# -rwxr-xr-x ew_target_service.sh (755)
# -rw-r--r-- epmware-agent.jar (644)
```

### Structure Verification

Confirm directory structure:

```bash
# Display structure
tree -L 2 ~/

# Or simple listing
find ~ -maxdepth 2 -type d | sort
```

## Common Installation Scenarios

### Scenario 1: Fresh Installation

New agent installation on clean system:

1. Install prerequisites
2. Create agent user
3. Extract agent files
4. Configure properties
5. Start agent

### Scenario 2: Upgrade Installation

Upgrading existing agent:

1. Stop current agent
2. Backup configuration
3. Extract new files
4. Restore configuration
5. Restart agent

### Scenario 3: Migration Installation

Moving agent to new server:

1. Backup old configuration
2. Install on new server
3. Copy configuration
4. Update server-specific settings
5. Test and cutover

## Installation Best Practices

### Security Practices

1. **Use Dedicated User** - Don't use root/Administrator
2. **Restrict Permissions** - Limit file access
3. **Secure Transfer** - Use SCP/SFTP for file transfer
4. **Verify Integrity** - Check file checksums

### Organization Practices

1. **Consistent Paths** - Use standard directories
2. **Clear Naming** - Use descriptive names
3. **Document Setup** - Record installation details
4. **Version Control** - Track configuration files

### Maintenance Practices

1. **Regular Backups** - Backup before changes
2. **Clean Installation** - Remove old files
3. **Log Rotation** - Plan for log management
4. **Update Schedule** - Plan agent updates

## Troubleshooting Installation

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Files in wrong location | Extracted with path | Move to correct directory |
| Permission denied | Incorrect ownership | Fix with chown/chmod |
| Missing files | Incomplete extraction | Re-extract from zip |
| Cannot find Java | PATH not set | Configure environment |

### Installation Validation Script

```bash
#!/bin/bash
# validate_installation.sh

echo "=== EPMware Agent Installation Validation ==="

# Check Java
if command -v java &> /dev/null; then
    echo "✓ Java found: $(java -version 2>&1 | head -1)"
else
    echo "✗ Java not found"
fi

# Check agent files
for file in epmware-agent.jar agent.properties ew_target_service.sh; do
    if [ -f "$file" ]; then
        echo "✓ $file present"
    else
        echo "✗ $file missing"
    fi
done

# Check permissions
if [ -x "ew_target_service.sh" ]; then
    echo "✓ Service script is executable"
else
    echo "✗ Service script not executable"
fi

# Check disk space
AVAILABLE=$(df -h . | awk 'NR==2 {print $4}')
echo "ℹ Available disk space: $AVAILABLE"
```

## Multiple Agent Installations

### Installing Multiple Agents

For multiple agents on one server:

```bash
# Create separate users
for app in hfm planning essbase; do
    sudo useradd -m agent_$app
    sudo -u agent_$app -i bash -c "cd ~ && unzip /tmp/ew_agent_files.zip"
done

# Each agent has own:
# - User account
# - Home directory
# - Configuration
# - Log files
```

### Managing Multiple Agents

```bash
# Start all agents
for user in agent_*; do
    sudo -u $user -i ./ew_target_service.sh &
done

# Check status
ps aux | grep epmware-agent
```

## Next Steps

After installing agent files:

1. [Review File Structure](file-structure.md) - Understand components
2. [Configure Properties](../../configuration/agent-properties.md) - Set up configuration
3. [Configure Service](../../configuration/service-config.md) - Prepare startup script
4. [Test Installation](../../configuration/testing.md) - Verify functionality

!!! success "Installation Progress"
    Once files are extracted and verified, the agent installation is complete. Proceed to configuration to enable agent functionality.

!!! tip "Installation Automation"
    Consider creating installation scripts for consistent deployment across multiple servers. This ensures standardization and reduces errors.
# Download and Extract Agent

## Overview

This section covers downloading the EPMware Agent package and extracting it to the appropriate location on your server. The agent files must be placed in the home directory of the user account that will run the agent service.

## Obtaining the Agent Package

### Download Sources

The EPMware Agent package (`ew_agent_files.zip`) can be obtained from:

1. **EPMware Support Portal**
   - Login to support.epmware.com
   - Navigate to Downloads section
   - Download latest agent version

2. **Direct from EPMware Support**
   - Contact support@epmware.com
   - Request agent installation files
   - Receive secure download link

3. **Your EPMware Implementation Team**
   - Provided during initial setup
   - Available from your consultant

### Package Information

| File Name | Size | Contents |
|-----------|------|----------|
| `ew_agent_files.zip` | ~50 MB | Agent JAR, scripts, configuration templates |

### Version Verification

Check the agent version before installation:

```bash
# After extraction, check version
java -jar epmware-agent.jar --version
```

## Pre-Extraction Setup

### Identify Installation Directory

The agent must be installed in the user's home directory:

**Windows (Cygwin):**
- Default: `C:\cygwin64\home\[username]\`
- Example: `C:\cygwin64\home\Administrator\`

**Linux:**
- Default: `/home/[username]/`
- Example: `/home/epmadmin/`

### Create User Directory (if needed)

**Windows:**
```bash
# Open Cygwin Terminal as target user
# Directory created automatically on first login
cd ~
pwd
```

**Linux:**
```bash
# Create user if not exists
sudo useradd -m epmadmin
sudo passwd epmadmin

# Verify directory
ls -la /home/epmadmin
```

## Extraction Process

### Windows Extraction

#### Method 1: Using Windows Explorer

1. Navigate to the home directory:
   - Open File Explorer
   - Go to `C:\cygwin64\home\[username]\`

2. Copy the agent zip file to this location

3. Right-click `ew_agent_files.zip`

4. Select **Extract All...**

5. **Important**: Set extraction path to the home directory itself
   - Remove any subfolder from the path
   - Should extract directly to `C:\cygwin64\home\[username]\`

![Windows Extraction](../../assets/images/installation/windows-extract-dialog.png)<br/>
*Windows extraction dialog - ensure correct path*

#### Method 2: Using Cygwin Terminal

```bash
# Navigate to home directory
cd ~

# Copy zip file to home directory (adjust source path)
cp /cygdrive/c/Users/[WindowsUser]/Downloads/ew_agent_files.zip .

# Extract files
unzip ew_agent_files.zip

# Verify extraction
ls -la
```

### Linux Extraction

```bash
# Navigate to home directory
cd ~

# Copy agent zip file (adjust source path)
cp /tmp/ew_agent_files.zip .

# Extract files
unzip ew_agent_files.zip

# If unzip not available, install it
# RHEL/CentOS: sudo yum install unzip
# Ubuntu: sudo apt-get install unzip

# Verify extraction
ls -la
```

## Post-Extraction Verification

### Expected Directory Structure

After extraction, verify the following structure:

```
home/[username]/
├── epmware-agent.jar       # Main agent executable
├── agent.properties         # Configuration file
├── ew_target_service.sh     # Service startup script
├── logs/                    # Log directory (created on first run)
│   ├── agent.log           
│   └── agent-poll.log      
├── temp/                    # Temporary files directory
└── lib/                     # Additional libraries (if any)
```

![Agent File Structure](../../assets/images/installation/agent-file-structure.png)<br/>
*Extracted agent files in home directory*

### File Permissions

#### Windows (Cygwin)

```bash
# Check permissions
ls -la ~/

# Set execute permission for script
chmod +x ew_target_service.sh

# Ensure read/write for properties
chmod 644 agent.properties
```

#### Linux

```bash
# Set appropriate permissions
chmod 755 ~/
chmod 755 ew_target_service.sh
chmod 600 agent.properties  # Restrict access to properties file
chmod 644 epmware-agent.jar

# Set ownership
chown -R epmadmin:epmadmin ~/
```

## Common Extraction Issues

### Issue: Files in Wrong Directory

**Problem**: Files extracted to subfolder like `home/[username]/ew_agent_files/`

**Solution**:
```bash
# Move files to correct location
cd ~
mv ew_agent_files/* .
mv ew_agent_files/.* . 2>/dev/null  # Hidden files if any
rmdir ew_agent_files
```

### Issue: Permissions Error

**Problem**: Cannot extract or access files

**Windows Solution**:
- Run Cygwin Terminal as Administrator
- Ensure Windows user has full control of Cygwin directory

**Linux Solution**:
```bash
# Extract as the target user
su - epmadmin
unzip ew_agent_files.zip

# Or fix permissions after
sudo chown -R epmadmin:epmadmin /home/epmadmin/
```

### Issue: Corrupted ZIP File

**Problem**: Extraction fails with errors

**Solution**:
1. Verify file integrity:
```bash
# Test zip file
unzip -t ew_agent_files.zip

# Check file size
ls -lh ew_agent_files.zip
```

2. Re-download if corrupted

3. Try alternative extraction tool:
```bash
# Using jar command (if available)
jar xvf ew_agent_files.zip

# Using 7zip (if available)
7z x ew_agent_files.zip
```

## Multiple Agent Installations

### Single Server, Multiple Agents

To run multiple agents on one server:

1. Create separate users:
```bash
# Linux
sudo useradd -m epmadmin_hfm
sudo useradd -m epmadmin_planning

# Windows - Create Windows users and login to Cygwin
```

2. Extract agent to each home directory:
```bash
# As each user
su - epmadmin_hfm
cd ~
unzip /tmp/ew_agent_files.zip

su - epmadmin_planning
cd ~
unzip /tmp/ew_agent_files.zip
```

3. Configure unique settings per agent

### Shared Installation (Not Recommended)

While possible, sharing agent files is not recommended:
- Complicates configuration management
- Log files will conflict
- Updates affect all instances

## Backup Original Files

Before configuration, backup the original files:

```bash
# Create backup directory
mkdir ~/agent_backup_$(date +%Y%m%d)

# Copy original files
cp agent.properties ~/agent_backup_$(date +%Y%m%d)/
cp ew_target_service.sh ~/agent_backup_$(date +%Y%m%d)/

# List backups
ls -la ~/agent_backup_*
```

## Security Considerations

### File Security

1. **Protect Configuration Files**:
```bash
# Restrict access to properties
chmod 600 agent.properties

# Verify no sensitive data in world-readable files
find ~ -type f -perm /004 -name "*.properties"
```

2. **Remove Installation Files**:
```bash
# Remove zip file after extraction
rm ew_agent_files.zip

# Clear command history if it contains passwords
history -c
```

3. **Audit File Access**:
```bash
# Linux - Enable auditing
auditctl -w /home/epmadmin -p rwa -k epmware_agent
```

### Network Security

Verify firewall allows required connections:

```bash
# Test connectivity to EPMware
curl -I https://your-epmware-server.com

# Check open ports
netstat -an | grep LISTEN
```

## Verification Checklist

After extraction, verify:

- [ ] All files extracted to correct directory
- [ ] No nested `ew_agent_files` subfolder
- [ ] `epmware-agent.jar` is present
- [ ] `agent.properties` is present
- [ ] `ew_target_service.sh` is present
- [ ] File permissions are correct
- [ ] User owns all agent files
- [ ] Original files are backed up

## Updating Agent Files

### Update Process

When updating to a new agent version:

1. **Stop Current Agent**:
```bash
# Stop the running agent
# Method varies by OS and configuration
```

2. **Backup Current Installation**:
```bash
mkdir ~/agent_backup_$(date +%Y%m%d_%H%M%S)
cp -r *.jar *.properties *.sh ~/agent_backup_$(date +%Y%m%d_%H%M%S)/
```

3. **Extract New Version**:
```bash
# Extract new files, preserving configurations
unzip -o ew_agent_files_new.zip -x agent.properties
```

4. **Verify and Restart**:
```bash
# Check version
java -jar epmware-agent.jar --version

# Restart agent
./ew_target_service.sh
```

!!! warning "Configuration Preservation"
    Always preserve your customized `agent.properties` file when updating. The `-x agent.properties` flag in the unzip command excludes it from being overwritten.

## Next Steps

After successfully extracting the agent files:

1. [Review File Structure](file-structure.md) - Understand agent components
2. [Configure Agent Properties](../../configuration/agent-properties.md) - Set up configuration
3. [Generate REST Token](../../configuration/rest-token.md) - Set up authentication
4. [Test Connection](../../configuration/testing.md) - Verify setup
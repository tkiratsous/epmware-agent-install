# Planning Password Encryption

This guide covers the generation and management of encrypted password files required for Hyperion Planning integration with EPMware Agent.

## Overview

Planning requires encrypted password files for:
- Secure authentication without exposing passwords
- Automated deployments without hardcoding credentials
- Compliance with security policies
- Integration with EPMware Agent

## Password Encryption Utility

### Locating the Utility

The PasswordEncryption utility is located in the Planning installation:

**Windows:**
```
D:\Oracle\Middleware\user_projects\epmsystem1\Planning\planning1\PasswordEncryption.cmd
```

**Linux:**
```
/opt/Oracle/Middleware/user_projects/epmsystem1/Planning/planning1/PasswordEncryption.sh
```

### Utility Syntax

```bash
# Basic syntax
PasswordEncryption.[cmd|sh] [passwordFile]

# Parameters:
# passwordFile - Path where encrypted file will be created
```

## Generating Encrypted Password Files

### Windows Process

```cmd
REM Navigate to Planning directory
cd D:\Oracle\Middleware\user_projects\epmsystem1\Planning\planning1

REM Run encryption utility
PasswordEncryption.cmd D:\secure\planning_pwd.txt

REM You will be prompted:
Enter password to encrypt:

REM Type password (not visible) and press Enter
REM Output:
Password has been encrypted and written to the file D:\secure\planning_pwd.txt successfully!
```

### Linux Process

```bash
# Navigate to Planning directory
cd /opt/Oracle/Middleware/user_projects/epmsystem1/Planning/planning1

# Run encryption utility
./PasswordEncryption.sh /opt/secure/planning_pwd.txt

# You will be prompted:
# Enter password to encrypt:

# Type password (not visible) and press Enter
# Output:
# Password has been encrypted and written to the file /opt/secure/planning_pwd.txt successfully!
```

### Automated Generation Script

```bash
#!/bin/bash
# generate_planning_password.sh

# Configuration
PLANNING_HOME="/opt/Oracle/Middleware/user_projects/epmsystem1/Planning/planning1"
PASSWORD_DIR="/opt/secure/planning"
PASSWORD_FILE="$PASSWORD_DIR/planning_pwd.txt"

# Create secure directory
mkdir -p $PASSWORD_DIR
chmod 700 $PASSWORD_DIR

# Navigate to Planning directory
cd $PLANNING_HOME

# Generate password file
echo "Generating encrypted password file..."
echo "Enter Planning admin password when prompted:"

./PasswordEncryption.sh $PASSWORD_FILE

# Secure the file
if [ -f "$PASSWORD_FILE" ]; then
    chmod 600 $PASSWORD_FILE
    chown oracle:dba $PASSWORD_FILE
    echo "✓ Password file created: $PASSWORD_FILE"
    ls -la $PASSWORD_FILE
else
    echo "✗ Password file generation failed!"
    exit 1
fi
```

## Password File Management

### File Location Best Practices

```bash
# Recommended directory structure
/opt/secure/
├── planning/
│   ├── prod_pwd.txt       # Production password
│   ├── uat_pwd.txt        # UAT password
│   └── dev_pwd.txt        # Development password
├── backup/
│   └── pwd_backup_[date].txt
└── archive/
    └── old_passwords/
```

### Securing Password Files

#### Linux Security

```bash
# Set restrictive permissions
chmod 600 /opt/secure/planning/planning_pwd.txt

# Set ownership
chown oracle:dba /opt/secure/planning/planning_pwd.txt

# Prevent modification
chattr +i /opt/secure/planning/planning_pwd.txt  # Immutable flag

# SELinux context (if applicable)
chcon -t oracle_secure_t /opt/secure/planning/planning_pwd.txt
```

#### Windows Security

```powershell
# Remove inheritance
icacls "D:\secure\planning_pwd.txt" /inheritance:r

# Grant specific permissions
icacls "D:\secure\planning_pwd.txt" /grant "DOMAIN\svc_planning:R"
icacls "D:\secure\planning_pwd.txt" /grant "DOMAIN\Administrators:F"

# Remove Everyone group
icacls "D:\secure\planning_pwd.txt" /remove "Everyone"

# Audit access
auditpol /set /subcategory:"File System" /success:enable /failure:enable
```

## Multiple Environment Configuration

### Environment-Specific Passwords

```bash
#!/bin/bash
# multi_env_passwords.sh

ENVIRONMENTS=("dev" "test" "uat" "prod")
PLANNING_HOME="/opt/Oracle/Middleware/user_projects/epmsystem1/Planning/planning1"

for ENV in "${ENVIRONMENTS[@]}"; do
    echo "=== Generating password for $ENV environment ==="
    
    PASSWORD_FILE="/opt/secure/planning/${ENV}_pwd.txt"
    
    cd $PLANNING_HOME
    echo "Enter password for $ENV:"
    ./PasswordEncryption.sh $PASSWORD_FILE
    
    # Secure the file
    chmod 600 $PASSWORD_FILE
    echo "Created: $PASSWORD_FILE"
done
```

### Agent Configuration for Multiple Environments

```properties
# agent.properties

# Development
planning.dev.passwordFile=/opt/secure/planning/dev_pwd.txt
planning.dev.application=PLANDEV

# Test
planning.test.passwordFile=/opt/secure/planning/test_pwd.txt
planning.test.application=PLANTEST

# Production
planning.prod.passwordFile=/opt/secure/planning/prod_pwd.txt
planning.prod.application=PLANPROD
```

## Using Password Files

### With OutlineLoad Utility

```bash
# Use password file with OutlineLoad
OutlineLoad.sh -f:/opt/secure/planning/planning_pwd.txt \
    /A:PlanApp /U:admin /I:metadata.csv /D:Entity /L

# Windows
OutlineLoad.cmd -f:D:\secure\planning_pwd.txt ^
    /A:PlanApp /U:admin /I:metadata.csv /D:Entity /L
```

### In EPMware Configuration

1. Navigate to **Configuration** → **Applications**
2. Select Planning application
3. Edit properties:
   - Parameter: `PASSWORD_FILE`
   - Value: `/opt/secure/planning/planning_pwd.txt`

![Password File Configuration](../../assets/images/integration/planning-password-config.png)<br/>
*Configuring password file path in EPMware*

### In Scripts

```bash
#!/bin/bash
# deploy_planning.sh

# Configuration
PASSWORD_FILE="/opt/secure/planning/planning_pwd.txt"
USER="admin"
APP="PLANPROD"

# Verify password file exists
if [ ! -f "$PASSWORD_FILE" ]; then
    echo "Error: Password file not found: $PASSWORD_FILE"
    exit 1
fi

# Use password file
OutlineLoad.sh -f:$PASSWORD_FILE /A:$APP /U:$USER /I:data.csv /L
```

## Password Rotation

### Rotation Process

```bash
#!/bin/bash
# rotate_planning_password.sh

# Configuration
PLANNING_HOME="/opt/Oracle/Middleware/user_projects/epmsystem1/Planning/planning1"
PASSWORD_DIR="/opt/secure/planning"
BACKUP_DIR="/opt/secure/backup"

# Backup current password
DATE=$(date +%Y%m%d_%H%M%S)
cp $PASSWORD_DIR/planning_pwd.txt $BACKUP_DIR/planning_pwd_$DATE.txt

# Generate new password file
cd $PLANNING_HOME
echo "Enter new Planning password:"
./PasswordEncryption.sh $PASSWORD_DIR/planning_pwd_new.txt

# Test new password
if OutlineLoad.sh -f:$PASSWORD_DIR/planning_pwd_new.txt /A:PLANAPP /U:admin /V; then
    echo "✓ New password verified"
    
    # Replace old with new
    mv $PASSWORD_DIR/planning_pwd.txt $PASSWORD_DIR/planning_pwd_old.txt
    mv $PASSWORD_DIR/planning_pwd_new.txt $PASSWORD_DIR/planning_pwd.txt
    
    echo "✓ Password rotation complete"
else
    echo "✗ New password validation failed"
    rm $PASSWORD_DIR/planning_pwd_new.txt
    exit 1
fi
```

### Scheduled Rotation

```bash
# Crontab entry for quarterly rotation
0 2 1 */3 * /opt/scripts/rotate_planning_password.sh

# Or use systemd timer
[Unit]
Description=Rotate Planning Password

[Timer]
OnCalendar=quarterly
Persistent=true

[Install]
WantedBy=timers.target
```

## Troubleshooting Password Issues

### Common Problems

| Issue | Symptom | Solution |
|-------|---------|----------|
| Wrong password | "Invalid credentials" | Regenerate password file |
| File not found | "Cannot read password file" | Check path and permissions |
| Corrupted file | "Invalid password file format" | Regenerate file |
| Permission denied | "Access denied" | Fix file permissions |
| Encoding issues | Special characters fail | Use ASCII characters only |

### Password File Validation

```bash
#!/bin/bash
# validate_password.sh

PASSWORD_FILE="/opt/secure/planning/planning_pwd.txt"

echo "=== Password File Validation ==="

# Check file exists
if [ ! -f "$PASSWORD_FILE" ]; then
    echo "✗ File not found: $PASSWORD_FILE"
    exit 1
fi
echo "✓ File exists"

# Check file size
SIZE=$(stat -c%s "$PASSWORD_FILE")
if [ $SIZE -gt 0 ]; then
    echo "✓ File size: $SIZE bytes"
else
    echo "✗ File is empty"
    exit 1
fi

# Check permissions
PERMS=$(stat -c%a "$PASSWORD_FILE")
if [ "$PERMS" = "600" ]; then
    echo "✓ Permissions: $PERMS (secure)"
else
    echo "⚠ Permissions: $PERMS (should be 600)"
fi

# Test password file
echo "Testing password file..."
if OutlineLoad.sh -f:$PASSWORD_FILE /A:PLANAPP /U:admin /V 2>/dev/null; then
    echo "✓ Password file is valid"
else
    echo "✗ Password file test failed"
fi
```

### Debug Password Issues

```bash
# Enable debug logging
export ODL_LOG_LEVEL=TRACE

# Test with verbose output
OutlineLoad.sh -f:password.txt /A:App /U:user /V -debug

# Check Planning logs
tail -f $EPM_ORACLE_INSTANCE/diagnostics/logs/Planning/planning_0.log
```

## Security Best Practices

### Password File Security Checklist

- [ ] File permissions set to 600 (read/write owner only)
- [ ] Ownership set to service account
- [ ] Stored outside web root
- [ ] Directory access restricted
- [ ] Regular rotation schedule
- [ ] Backup before rotation
- [ ] Audit file access
- [ ] Encrypt backups
- [ ] No passwords in scripts
- [ ] No passwords in version control

### Additional Security Measures

```bash
# Encrypt password file at rest
openssl enc -aes-256-cbc -salt -in planning_pwd.txt -out planning_pwd.enc

# Decrypt when needed
openssl enc -aes-256-cbc -d -in planning_pwd.enc -out planning_pwd.txt

# Use with script
decrypt_and_use() {
    TEMP_PWD=$(mktemp)
    openssl enc -aes-256-cbc -d -in planning_pwd.enc -out $TEMP_PWD
    OutlineLoad.sh -f:$TEMP_PWD /A:App /U:user /I:data.csv
    shred -u $TEMP_PWD  # Secure deletion
}
```

## Integration with EPMware Agent

### Agent Configuration

```properties
# agent.properties
planning.passwordFile=/opt/secure/planning/planning_pwd.txt
planning.passwordFile.encrypted=false
planning.user=admin
planning.application=PLANPROD
```

### Agent Script Integration

```bash
#!/bin/bash
# agent_planning_deploy.sh

# Called by EPMware Agent
METADATA_FILE=$1
PASSWORD_FILE=$(grep planning.passwordFile agent.properties | cut -d= -f2)
USER=$(grep planning.user agent.properties | cut -d= -f2)
APP=$(grep planning.application agent.properties | cut -d= -f2)

# Validate password file
if [ ! -f "$PASSWORD_FILE" ]; then
    echo "ERROR: Password file not found"
    exit 1
fi

# Deploy using password file
OutlineLoad.sh -f:$PASSWORD_FILE /A:$APP /U:$USER /I:$METADATA_FILE /L
```

## Password File Monitoring

### Monitor File Changes

```bash
#!/bin/bash
# monitor_password_file.sh

PASSWORD_FILE="/opt/secure/planning/planning_pwd.txt"
CHECKSUM_FILE="/var/lib/planning/pwd.md5"

# Calculate checksum
CURRENT_SUM=$(md5sum "$PASSWORD_FILE" | cut -d' ' -f1)

# Compare with stored
if [ -f "$CHECKSUM_FILE" ]; then
    STORED_SUM=$(cat "$CHECKSUM_FILE")
    
    if [ "$CURRENT_SUM" != "$STORED_SUM" ]; then
        echo "WARNING: Password file changed!"
        # Alert administrators
        mail -s "Planning Password File Modified" admin@company.com
    fi
fi

# Update checksum
echo "$CURRENT_SUM" > "$CHECKSUM_FILE"
```

### Audit Access

```bash
# Linux audit rule
auditctl -w /opt/secure/planning/planning_pwd.txt -p rwa -k planning_password

# Check audit log
ausearch -k planning_password
```

!!! danger "Never Share Password Files"
    Password files contain sensitive credentials. Never copy them to unsecured locations, email them, or commit them to version control.

!!! tip "Test After Generation"
    Always test the password file immediately after generation to ensure it works before deploying to production.

## Next Steps

- [Application Properties](properties.md) - Configure Planning settings
- [Planning Integration Overview](index.md) - Complete Planning setup
- [HFM Integration](../hfm/index.md) - HFM configuration
- [Troubleshooting](../../troubleshooting/passwords.md) - Password issues
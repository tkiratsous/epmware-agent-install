# Password Issues

This guide covers common password-related issues with EPMware Agent and target applications, including troubleshooting steps and solutions.

## Common Password Issues

### Special Characters in Passwords

#### Problem: Ampersand (&) in Password

Passwords containing ampersand characters cause deployment and import failures.

**Symptoms:**
- Application import fails with authentication error
- Deployment fails despite correct credentials
- Agent logs show command parsing errors

**Solution:**
```bash
# Change password to exclude ampersand
# Avoid these characters: & | < > ; ` $ ! \ " '
```

**Best Practice Password Characters:**
- Letters (uppercase and lowercase)
- Numbers (0-9)
- Safe special characters: @ # % ^ * ( ) - _ = + [ ] { } : , . ? /

#### Problem: Quote Characters in Password

Single or double quotes in passwords cause parsing issues.

**Solution for Different Shells:**

Linux/Bash:
```bash
# Escape quotes in configuration
password="mypass\"word"  # For double quote
password='mypass'\''word'  # For single quote
```

Windows/PowerShell:
```powershell
# Use backtick to escape
$password = "mypass`"word"
```

### Password Encryption Issues

#### Hyperion Planning Password Encryption

**Problem:** Planning deployment fails with encrypted password error.

**Solution:**

1. **Generate encrypted password file:**
   ```cmd
   cd D:\Oracle\Middleware\user_projects\epmsystem1\Planning\planning1
   PasswordEncryption.cmd d:\ew\app\ew_hp_cl_pwd.txt
   ```

2. **Verify file creation:**
   ```cmd
   dir d:\ew\app\ew_hp_cl_pwd.txt
   type d:\ew\app\ew_hp_cl_pwd.txt
   ```
   The file should contain encrypted text, not plaintext.

3. **Update EPMware configuration:**
   - Navigate to Configuration → Applications
   - Select the Planning application
   - Edit PASSWORD_FILE property
   - Enter full path: `d:\ew\app\ew_hp_cl_pwd.txt`

**Common Errors:**
- "Invalid password file" - File path is incorrect
- "Cannot decrypt password" - File was corrupted or manually edited
- "Access denied" - Agent user lacks read permissions

#### PCMCS/EPM Cloud Password Issues

**Problem:** EPM Automate login fails with password error.

**Troubleshooting Steps:**

1. **Test password directly:**
   ```bash
   cd ~/epmautomate/bin
   ./epmautomate login username "password" https://instance.oraclecloud.com
   ```

2. **Check for special characters:**
   ```bash
   # If password has spaces or special chars, use quotes
   ./epmautomate login user "p@ss word!" https://instance.oraclecloud.com
   ```

3. **Verify identity domain:**
   ```bash
   # Some instances require identity domain
   ./epmautomate login user.domain password https://instance.oraclecloud.com
   ```

### Authentication Token Issues

#### Problem: REST API Token Invalid

**Symptoms:**
- Agent shows "Authentication failed"
- Token rejected by EPMware server
- Agent unable to establish connection

**Solution:**

1. **Regenerate token in EPMware:**
   - Navigate to Security → Users
   - Select the agent user
   - Right-click and select "Generate Token"
   - Copy the new 36-character token

2. **Update agent.properties:**
   ```properties
   ew.portal.token=new-token-value-here
   ```

3. **Restart agent:**
   ```bash
   # Linux
   kill -9 $(pgrep -f epmware-agent)
   ./ew_target_service.sh &
   
   # Windows
   Stop-Process -Name java -Force
   schtasks /Run /TN "EPMWARE TARGET AGENT SERVICE"
   ```

#### Problem: Token Expiration

**Identifying expired tokens:**
```bash
grep "401\|Unauthorized" logs/agent.log
```

**Solution:**
- Tokens don't expire by default
- If organization has token expiry policy:
  1. Set up token rotation schedule
  2. Generate new token before expiry
  3. Update all affected agents
  4. Document token generation date

### Windows Credential Storage

#### Problem: Cached Credentials Conflict

Windows may cache old credentials causing authentication failures.

**Solution:**

1. **Clear credential manager:**
   ```cmd
   cmdkey /list
   cmdkey /delete:targetname
   ```

2. **Reset service account password:**
   ```powershell
   net user serviceaccount newpassword
   ```

3. **Update scheduled task credentials:**
   - Open Task Scheduler
   - Edit EPMWARE TARGET AGENT SERVICE
   - Update credentials
   - Save and restart task

### Linux Password Storage

#### Problem: Password Visible in Process List

Passwords may be visible when viewing process details.

**Solution:**

1. **Use environment variables:**
   ```bash
   # Set in agent user's .bashrc
   export EW_APP_PASSWORD='secretpass'
   
   # Reference in scripts
   password=$EW_APP_PASSWORD
   ```

2. **Use password file with restricted permissions:**
   ```bash
   # Create password file
   echo "password" > ~/.ew_pass
   chmod 600 ~/.ew_pass
   
   # Read in script
   password=$(cat ~/.ew_pass)
   ```

3. **Use keyring/secret management:**
   ```bash
   # Store using secret-tool
   echo -n "password" | secret-tool store --label="EPMware" account epmware
   
   # Retrieve in script
   password=$(secret-tool lookup account epmware)
   ```

## Password Validation Scripts

### Test Authentication Script

Create a script to validate credentials:

**test-auth.sh (Linux):**
```bash
#!/bin/bash

echo "=== EPMware Authentication Test ==="
echo

# Test 1: Agent Token
echo "Testing Agent Token..."
TOKEN=$(grep "ew.portal.token" agent.properties | cut -d'=' -f2)
PORTAL=$(grep "ew.portal.url" agent.properties | cut -d'=' -f2)

response=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $TOKEN" \
  "$PORTAL/api/health")

if [ "$response" = "200" ]; then
    echo "✓ Token authentication successful"
else
    echo "✗ Token authentication failed (HTTP $response)"
fi

# Test 2: Application Credentials
echo
echo "Testing Application Credentials..."
# Add application-specific tests here

echo
echo "=== Test Complete ==="
```

**Test-Auth.ps1 (Windows):**
```powershell
Write-Host "=== EPMware Authentication Test ===" -ForegroundColor Cyan
Write-Host

# Test Agent Token
Write-Host "Testing Agent Token..." -ForegroundColor Yellow
$config = Get-Content "agent.properties"
$token = ($config | Select-String "ew.portal.token=").Line.Split('=')[1]
$portal = ($config | Select-String "ew.portal.url=").Line.Split('=')[1]

try {
    $response = Invoke-WebRequest -Uri "$portal/api/health" `
        -Headers @{"Authorization"="Bearer $token"} `
        -Method GET -UseBasicParsing
    
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Token authentication successful" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Token authentication failed" -ForegroundColor Red
    Write-Host $_.Exception.Message
}

Write-Host
Write-Host "=== Test Complete ===" -ForegroundColor Cyan
```

## Password Security Best Practices

### 1. Password Complexity Requirements

Implement strong password policy:
- Minimum 12 characters
- Mix of upper/lowercase letters
- Include numbers
- Include special characters (avoiding problematic ones)
- No dictionary words
- No personal information

### 2. Password Rotation

Schedule regular password updates:
```bash
# Password rotation reminder script
#!/bin/bash

PASSWORD_AGE_DAYS=90
LAST_CHANGE_FILE=".password_change_date"

if [ -f $LAST_CHANGE_FILE ]; then
    LAST_CHANGE=$(cat $LAST_CHANGE_FILE)
    DAYS_SINCE=$((( $(date +%s) - $LAST_CHANGE ) / 86400))
    
    if [ $DAYS_SINCE -gt $PASSWORD_AGE_DAYS ]; then
        echo "WARNING: Password is $DAYS_SINCE days old. Please rotate."
        # Send alert email
    fi
else
    date +%s > $LAST_CHANGE_FILE
fi
```

### 3. Secure Storage

Never store passwords in:
- Plain text files
- Source code
- Version control systems
- Unencrypted databases
- Email or chat logs

### 4. Access Control

Restrict password file permissions:
```bash
# Linux
chmod 600 password_file
chown agent_user:agent_group password_file

# Windows
icacls password_file /grant:r "agent_user:(R)" /inheritance:r
```

## Troubleshooting Checklist

When experiencing password issues:

- [ ] Verify no special characters causing issues (especially &, quotes)
- [ ] Check password hasn't expired
- [ ] Confirm correct username/password combination
- [ ] Verify proper encryption for Planning applications
- [ ] Check token validity for REST API
- [ ] Review agent logs for specific error messages
- [ ] Test authentication outside of EPMware
- [ ] Verify network connectivity to target systems
- [ ] Check firewall rules aren't blocking authentication
- [ ] Confirm service account isn't locked
- [ ] Validate password file permissions
- [ ] Ensure no cached/stale credentials

## Error Messages and Solutions

| Error Message | Likely Cause | Solution |
|--------------|--------------|----------|
| "Invalid credentials" | Wrong username/password | Verify credentials with application admin |
| "Token authentication failed" | Invalid or expired token | Regenerate token in EPMware |
| "Cannot decrypt password" | Corrupted password file | Regenerate encrypted password file |
| "Access denied" | Account locked or disabled | Unlock account in directory service |
| "Authentication timeout" | Network issues | Check firewall and network connectivity |
| "Password expired" | Password needs rotation | Update password per organization policy |
| "Special character error" | Unsupported character in password | Change password to exclude problematic characters |

## Related Topics

- [Service Errors](service-errors.md)
- [Debug Mode](debug.md)
- [Agent Configuration](../configuration/agent-properties.md)
- [Security Configuration](../configuration/security.md)
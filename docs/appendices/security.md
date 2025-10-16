# Appendix B - Security Checklist

This comprehensive security checklist ensures your EPMware Agent deployment follows security best practices and meets compliance requirements.

## Security Assessment Matrix

| Category | Priority | Status | Notes |
|----------|----------|--------|-------|
| **Access Control** | Critical | ⬜ | User permissions and authentication |
| **Network Security** | Critical | ⬜ | Firewall and communication security |
| **Data Protection** | Critical | ⬜ | Encryption and data handling |
| **Credential Management** | Critical | ⬜ | Password and token security |
| **System Hardening** | High | ⬜ | OS and application hardening |
| **Monitoring & Audit** | High | ⬜ | Logging and detection |
| **Compliance** | Medium | ⬜ | Regulatory requirements |
| **Disaster Recovery** | Medium | ⬜ | Backup and recovery |

## Pre-Installation Security

### System Preparation

- [ ] **Operating System Updates**
  ```bash
  # Linux
  sudo yum update -y  # RHEL/CentOS
  sudo apt update && sudo apt upgrade -y  # Ubuntu
  
  # Windows
  Install-WindowsUpdate -AcceptAll -AutoReboot
  ```

- [ ] **Security Patches Applied**
  - OS security patches current
  - Java security updates installed
  - Third-party software patched

- [ ] **Antivirus/Anti-malware**
  - Antivirus software installed
  - Real-time scanning enabled
  - Exclusions configured for agent directories

- [ ] **System Hardening**
  - Unnecessary services disabled
  - Default accounts disabled/renamed
  - Security baseline applied

### Network Security Preparation

- [ ] **Network Segmentation**
  - Agent in appropriate network zone
  - VLANs properly configured
  - Network isolation implemented

- [ ] **Firewall Configuration**
  - Default deny rule in place
  - Only required ports open
  - Source IP restrictions configured

## Access Control Security

### User Account Management

- [ ] **Dedicated Service Account**
  ```bash
  # Linux
  sudo useradd -r -s /bin/false -m epmware_agent
  
  # Windows
  New-LocalUser -Name "svc_epmware" -NoPassword
  ```

- [ ] **Account Permissions**
  - [ ] Minimum required privileges
  - [ ] No administrator/root access unless necessary
  - [ ] No interactive login capability
  - [ ] Account locked to specific host

- [ ] **Password Policy**
  - [ ] Strong password (15+ characters)
  - [ ] Password complexity enforced
  - [ ] Password expiration policy
  - [ ] Password history enforced

### File System Permissions

#### Linux Permissions

```bash
# Set restrictive permissions
chmod 700 /home/epmware_agent
chmod 600 /home/epmware_agent/agent.properties
chmod 700 /home/epmware_agent/ew_target_service.sh
chmod 600 /home/epmware_agent/logs/*

# Set ownership
chown -R epmware_agent:epmware_agent /home/epmware_agent
```

#### Windows Permissions

```powershell
# Remove inherited permissions
icacls "C:\epmware" /inheritance:r

# Grant specific permissions
icacls "C:\epmware" /grant "svc_epmware:(OI)(CI)F"
icacls "C:\epmware\agent.properties" /grant "svc_epmware:R"
icacls "C:\epmware" /grant "Administrators:(OI)(CI)F"

# Remove Everyone group
icacls "C:\epmware" /remove "Everyone"
```

### Authentication Security

- [ ] **REST Token Management**
  - [ ] Tokens stored securely
  - [ ] Tokens rotated every 90 days
  - [ ] Old tokens revoked immediately
  - [ ] Token usage monitored

- [ ] **Multi-Factor Authentication**
  - [ ] MFA enabled for EPMware access
  - [ ] MFA for administrative accounts
  - [ ] MFA bypass documented and limited

## Data Protection

### Encryption at Rest

- [ ] **Configuration File Encryption**
  ```bash
  # Encrypt sensitive files
  openssl enc -aes-256-cbc -salt -in agent.properties \
    -out agent.properties.enc -k password
  
  # Decrypt when needed
  openssl enc -aes-256-cbc -d -in agent.properties.enc \
    -out agent.properties -k password
  ```

- [ ] **Password File Encryption**
  - [ ] Passwords never in plain text
  - [ ] Using encrypted password files
  - [ ] Encryption keys protected

- [ ] **Log File Protection**
  - [ ] Sensitive data masked in logs
  - [ ] Log files permissions restricted
  - [ ] Log encryption if required

### Encryption in Transit

- [ ] **TLS/SSL Configuration**
  ```properties
  # Enforce TLS 1.2+
  https.protocols=TLSv1.2,TLSv1.3
  https.cipherSuites=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
  ```

- [ ] **Certificate Management**
  - [ ] Valid SSL certificates
  - [ ] Certificates not expired
  - [ ] Certificate chain complete
  - [ ] Private keys protected

## Credential Management

### Password Security Checklist

- [ ] **No Hard-coded Passwords**
  ```bash
  # Check for passwords in files
  grep -r "password" /home/epmware_agent/ --exclude-dir=logs
  grep -r "pwd" /home/epmware_agent/ --exclude-dir=logs
  ```

- [ ] **Secure Password Storage**
  - [ ] Use credential vaults when possible
  - [ ] Encrypted password files
  - [ ] Restricted file permissions
  - [ ] No passwords in version control

### Token Security

- [ ] **Token Protection**
  ```bash
  # Secure token file
  echo "export EPMWARE_TOKEN=your-token" > ~/.epmware_token
  chmod 600 ~/.epmware_token
  source ~/.epmware_token
  ```

- [ ] **Token Rotation Schedule**
  - [ ] Quarterly rotation minimum
  - [ ] Immediate rotation on compromise
  - [ ] Rotation documented
  - [ ] Old tokens revoked

## Network Security

### Firewall Rules

- [ ] **Inbound Rules**
  - [ ] All inbound ports closed (agent only needs outbound)
  - [ ] Management access restricted by source IP
  - [ ] Default deny rule in place

- [ ] **Outbound Rules**
  - [ ] Only required ports open
  - [ ] Destination IPs restricted when possible
  - [ ] Egress filtering implemented

### Network Communication

- [ ] **Secure Protocols**
  - [ ] HTTPS preferred over HTTP
  - [ ] SSH for file transfers
  - [ ] No telnet or FTP
  - [ ] No unencrypted protocols

- [ ] **Proxy Security**
  - [ ] Proxy authentication required
  - [ ] Proxy logs monitored
  - [ ] Proxy bypass limited

## System Hardening

### Operating System Hardening

#### Linux Hardening

```bash
# Kernel parameters
cat >> /etc/sysctl.d/99-epmware-security.conf << EOF
# IP Spoofing protection
net.ipv4.conf.all.rp_filter = 1

# Ignore ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0

# Ignore send redirects
net.ipv4.conf.all.send_redirects = 0

# Disable source packet routing
net.ipv4.conf.all.accept_source_route = 0

# Log Martians
net.ipv4.conf.all.log_martians = 1

# Ignore ICMP ping requests
net.ipv4.icmp_echo_ignore_all = 1
EOF

sysctl -p /etc/sysctl.d/99-epmware-security.conf
```

#### Windows Hardening

```powershell
# Disable unnecessary services
Stop-Service -Name "RemoteRegistry" -Force
Set-Service -Name "RemoteRegistry" -StartupType Disabled

# Enable Windows Defender
Set-MpPreference -DisableRealtimeMonitoring $false

# Configure audit policy
auditpol /set /category:"Logon/Logoff" /success:enable /failure:enable
```

### Application Hardening

- [ ] **Java Security**
  ```bash
  # Update Java security properties
  echo "jdk.tls.disabledAlgorithms=SSLv3, RC4, DES, MD5withRSA, DH keySize < 2048" \
    >> $JAVA_HOME/lib/security/java.security
  ```

- [ ] **Agent Configuration Security**
  - [ ] Debug mode disabled in production
  - [ ] Verbose logging disabled
  - [ ] Test endpoints disabled
  - [ ] Development features removed

## Monitoring and Audit

### Logging Configuration

- [ ] **Comprehensive Logging**
  ```properties
  # Enable security logging
  logging.level.security=INFO
  logging.audit.enabled=true
  logging.audit.include-headers=true
  logging.audit.include-payload=false
  ```

- [ ] **Log Management**
  - [ ] Centralized log collection
  - [ ] Log retention policy defined
  - [ ] Log rotation configured
  - [ ] Logs backed up regularly

### Security Monitoring

- [ ] **Real-time Monitoring**
  - [ ] Failed authentication alerts
  - [ ] Unusual activity detection
  - [ ] Resource usage monitoring
  - [ ] Network anomaly detection

- [ ] **Security Alerts**
  ```bash
  #!/bin/bash
  # security_monitor.sh
  
  # Check for failed authentications
  if grep -q "401 Unauthorized" /var/log/epmware/agent.log; then
      echo "Authentication failure detected" | \
        mail -s "Security Alert" security@company.com
  fi
  
  # Check for suspicious commands
  if grep -E "rm -rf|chmod 777|sudo" /var/log/secure; then
      echo "Suspicious command detected" | \
        mail -s "Security Alert" security@company.com
  fi
  ```

### Audit Trail

- [ ] **Audit Requirements**
  - [ ] All configuration changes logged
  - [ ] User access logged
  - [ ] Deployment activities logged
  - [ ] Security events logged

- [ ] **Audit Log Protection**
  - [ ] Audit logs write-only
  - [ ] Audit logs on separate storage
  - [ ] Audit logs encrypted
  - [ ] Tamper detection enabled

## Compliance Requirements

### Regulatory Compliance

- [ ] **SOX Compliance**
  - [ ] Change control process
  - [ ] Separation of duties
  - [ ] Access reviews quarterly
  - [ ] Audit trail maintained

- [ ] **PCI DSS** (if applicable)
  - [ ] Cardholder data protected
  - [ ] Strong access controls
  - [ ] Regular security testing
  - [ ] Security policies maintained

- [ ] **GDPR** (if applicable)
  - [ ] Data privacy controls
  - [ ] Data retention policies
  - [ ] Right to erasure capability
  - [ ] Data breach procedures

### Security Policies

- [ ] **Password Policy**
  ```yaml
  Minimum Length: 15 characters
  Complexity: Upper + Lower + Number + Special
  History: 12 passwords
  Max Age: 90 days
  Lockout: 5 attempts / 30 minutes
  ```

- [ ] **Access Control Policy**
  - [ ] Least privilege principle
  - [ ] Regular access reviews
  - [ ] Timely deprovisioning
  - [ ] Documented approvals

## Incident Response

### Incident Response Plan

- [ ] **Response Procedures**
  - [ ] Incident detection process
  - [ ] Escalation procedures defined
  - [ ] Communication plan ready
  - [ ] Recovery procedures documented

- [ ] **Security Incident Checklist**
  1. Detect and analyze incident
  2. Contain the incident
  3. Eradicate the threat
  4. Recover systems
  5. Document lessons learned

### Backup and Recovery

- [ ] **Backup Strategy**
  ```bash
  #!/bin/bash
  # backup_security.sh
  
  BACKUP_DIR="/secure/backup/$(date +%Y%m%d)"
  mkdir -p $BACKUP_DIR
  
  # Backup configurations
  tar -czf $BACKUP_DIR/config.tar.gz /home/epmware_agent/*.properties
  
  # Backup logs
  tar -czf $BACKUP_DIR/logs.tar.gz /home/epmware_agent/logs/
  
  # Encrypt backups
  openssl enc -aes-256-cbc -salt -in $BACKUP_DIR/config.tar.gz \
    -out $BACKUP_DIR/config.tar.gz.enc -k $BACKUP_PASSWORD
  ```

- [ ] **Recovery Testing**
  - [ ] Recovery procedures documented
  - [ ] Recovery time objectives defined
  - [ ] Regular recovery drills
  - [ ] Backup integrity verified

## Security Testing

### Vulnerability Assessment

- [ ] **Regular Security Scans**
  ```bash
  # Network vulnerability scan
  nmap -sV -O -A server.com
  
  # Web vulnerability scan
  nikto -h https://epmware-server.com
  
  # SSL/TLS scan
  testssl.sh https://epmware-server.com
  ```

- [ ] **Penetration Testing**
  - [ ] Annual penetration tests
  - [ ] Remediation tracking
  - [ ] Retest after fixes
  - [ ] Report to management

### Security Review Schedule

| Review Type | Frequency | Last Completed | Next Due |
|------------|-----------|----------------|----------|
| Access Review | Quarterly | | |
| Security Patches | Monthly | | |
| Password Rotation | Quarterly | | |
| Certificate Review | Monthly | | |
| Firewall Rules | Quarterly | | |
| Security Scan | Monthly | | |
| Penetration Test | Annually | | |

## Security Hardening Scripts

### Comprehensive Security Check

```bash
#!/bin/bash
# security_audit.sh

echo "=== EPMware Agent Security Audit ==="
echo "Date: $(date)"
echo "Server: $(hostname)"
echo ""

# Check file permissions
echo "=== File Permissions ==="
ls -la /home/epmware_agent/ | grep -E "properties|\.sh"

# Check for plain text passwords
echo "=== Password Check ==="
grep -l "password\|pwd" /home/epmware_agent/*.properties

# Check open ports
echo "=== Open Ports ==="
netstat -tulpn | grep LISTEN

# Check failed logins
echo "=== Failed Logins (last 24h) ==="
grep "Failed" /var/log/secure | tail -20

# Check sudo usage
echo "=== Recent Sudo Commands ==="
grep sudo /var/log/secure | tail -10

# Check for security updates
echo "=== Available Security Updates ==="
yum list-security  # RHEL/CentOS
# apt list --upgradable  # Ubuntu

echo "=== Audit Complete ==="
```

## Security Documentation

### Required Documentation

- [ ] **Security Architecture Diagram**
- [ ] **Data Flow Diagram**
- [ ] **Network Topology**
- [ ] **Access Control Matrix**
- [ ] **Incident Response Plan**
- [ ] **Disaster Recovery Plan**
- [ ] **Security Policies and Procedures**

### Security Contact Information

```yaml
Security Team:
  Email: security@company.com
  Phone: +1-555-SEC-TEAM
  On-Call: +1-555-911-SEC

Incident Response:
  Email: incident-response@company.com
  Hotline: +1-555-INCIDENT
  
Management:
  CISO: ciso@company.com
  Security Manager: sec-manager@company.com
```

!!! danger "Critical Security Note"
    Never compromise security for convenience. If a security control seems burdensome, work to find a secure alternative rather than bypassing the control.

!!! warning "Regular Reviews"
    Security is not a one-time activity. Schedule regular reviews and updates of all security controls to maintain effectiveness against evolving threats.

## Next Steps

- [Port Requirements](ports.md) - Network port reference
- [Agent Commands](commands.md) - Command reference
- [Error Codes](error-codes.md) - Error resolution
- [Return to Appendices](index.md) - Main appendices page
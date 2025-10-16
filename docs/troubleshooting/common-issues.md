# Common Issues and Solutions

This page covers the most frequently encountered issues with EPMware Agent installation, configuration, and operation, along with their solutions.

## Installation Issues

### Issue: Java Not Found

**Error Message:**
```
'java' is not recognized as an internal or external command
bash: java: command not found
```

**Cause:** Java is not installed or not in the system PATH.

**Solution:**

1. **Verify Java installation:**
```bash
# Check if Java is installed
ls /usr/bin/java*  # Linux
dir "C:\Program Files\Java"  # Windows
```

2. **Install Java if missing:**
```bash
# Linux
sudo yum install java-1.8.0-openjdk  # RHEL/CentOS
sudo apt install openjdk-8-jdk  # Ubuntu

# Windows - Download from Oracle or OpenJDK
```

3. **Fix PATH:**
```bash
# Linux - Add to ~/.bashrc
export JAVA_HOME=/usr/java/latest
export PATH=$JAVA_HOME/bin:$PATH

# Windows - Add to System Environment Variables
JAVA_HOME=C:\Program Files\Java\jdk1.8.0_291
PATH=%JAVA_HOME%\bin;%PATH%
```

---

### Issue: Cygwin Not Working (Windows)

**Error Message:**
```
The system cannot find the path specified: C:\cygwin64\bin\bash.exe
```

**Cause:** Cygwin not installed or installed in different location.

**Solution:**

1. **Verify Cygwin installation:**
```powershell
Test-Path "C:\cygwin64\bin\bash.exe"
```

2. **Reinstall if missing:**
   - Download from www.cygwin.com
   - Install to default location C:\cygwin64
   - Select default packages

3. **Update agent configuration if different path:**
```bash
# Update ew_target_service.sh
HOME=/cygdrive/d/cygwin64/home/Administrator  # If on D: drive
```

---

### Issue: Permission Denied During Installation

**Error Message:**
```
mkdir: cannot create directory: Permission denied
unzip: cannot create extraction directory: Permission denied
```

**Cause:** Insufficient user permissions.

**Solution:**

**Linux:**
```bash
# Switch to correct user
sudo su - epmadmin

# Or fix ownership
sudo chown -R epmadmin:epmadmin /home/epmadmin

# Fix permissions
chmod 755 /home/epmadmin
```

**Windows:**
- Run Cygwin Terminal as Administrator
- Check Windows file permissions on Cygwin directory

---

## Configuration Issues

### Issue: Invalid Token Format

**Error Message:**
```
ERROR: Authentication failed - Invalid token format
ERROR: Token must be 36 characters
```

**Cause:** Token is malformed, has extra spaces, or wrong length.

**Solution:**

1. **Verify token format:**
```bash
# Check token in config
grep ew.portal.token agent.properties

# Token should be: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
# Example: 2e6d4103-5145-4c30-9837-ac6d14797523
```

2. **Remove extra characters:**
```bash
# Remove spaces, quotes, or line breaks
sed -i 's/ew.portal.token=.*/ew.portal.token=YOUR-TOKEN-HERE/' agent.properties
```

3. **Regenerate if needed:**
   - Log into EPMware
   - Navigate to Users
   - Right-click → Generate Token
   - Copy exactly 36 characters

---

### Issue: Wrong Server URL

**Error Message:**
```
ERROR: Connection refused - Unable to connect to server
ERROR: UnknownHostException: epmware-server.com
```

**Cause:** Incorrect server URL or hostname.

**Solution:**

1. **Verify URL format:**
```properties
# Cloud
ew.portal.url=https://client.epmwarecloud.com

# On-premise (note the port)
ew.portal.url=http://internal-server.com:8080/epmware
```

2. **Test connectivity:**
```bash
# Test DNS
nslookup your-server.com

# Test HTTPS
curl -I https://your-server.com

# Test with browser
# Navigate to the URL in a web browser
```

3. **Check for typos:**
   - No spaces in URL
   - Correct protocol (http:// or https://)
   - Correct port number if required

---

### Issue: Path Format Problems

**Error Message:**
```
ERROR: Invalid path: C:cygwin64homeAdministrator
ERROR: Cannot find directory: /home/Administrator
```

**Cause:** Incorrect path format in configuration.

**Solution:**

**Windows paths in agent.properties:**
```properties
# Use four backslashes
agent.root.dir=C:\\\\cygwin64\\\\home\\\\Administrator

# Or use forward slashes
agent.root.dir=C:/cygwin64/home/Administrator
```

**Linux paths:**
```properties
agent.root.dir=/home/epmadmin
```

---

## Runtime Issues

### Issue: Agent Starts Then Immediately Stops

**Error Messages:**
```
Agent started with PID: 12345
Process terminated unexpectedly
```

**Cause:** Configuration error, missing files, or resource issues.

**Solution:**

1. **Check configuration syntax:**
```bash
# Validate properties file
grep -E "^[^#].*=" agent.properties | while read line; do
    echo "Checking: $line"
done
```

2. **Verify all files present:**
```bash
ls -la epmware-agent.jar agent.properties ew_target_service.sh
```

3. **Check Java heap:**
```bash
# Increase memory if needed
java -Xmx2048m -jar epmware-agent.jar --spring.config.name=agent
```

4. **Review logs immediately:**
```bash
tail -50 logs/agent.log
```

---

### Issue: High Memory Usage

**Symptoms:**
- Agent consuming excessive RAM
- System becoming slow
- OutOfMemoryError in logs

**Solution:**

1. **Adjust JVM settings:**
```bash
# In ew_target_service.sh
JAVA_OPTS="-Xms512m -Xmx1024m"  # Reduce from defaults
JAVA_OPTS="$JAVA_OPTS -XX:+UseG1GC"
JAVA_OPTS="$JAVA_OPTS -XX:MaxGCPauseMillis=200"
```

2. **Monitor memory usage:**
```bash
# Check current usage
ps aux | grep epmware | awk '{print $4, $6}'

# Monitor over time
top -p $(pgrep -f epmware)
```

3. **Implement memory limits:**
```bash
# Linux systemd
MemoryLimit=1G
MemoryMax=1G

# Or use ulimit
ulimit -v 1048576  # 1GB in KB
```

---

### Issue: Agent Not Polling

**Symptoms:**
- No entries in agent-poll.log
- Deployments not processing
- Agent running but inactive

**Solution:**

1. **Check polling configuration:**
```properties
# Verify interval is set (milliseconds)
agent.interval.millisecond=30000  # 30 seconds
```

2. **Check network connectivity:**
```bash
# Test connection to EPMware
curl -H "Authorization: Bearer YOUR-TOKEN" \
     https://your-server/api/v1/agent/tasks
```

3. **Review agent logs:**
```bash
grep -i poll logs/agent.log | tail -20
```

4. **Restart agent:**
```bash
# Stop
pkill -f epmware-agent

# Start
./ew_target_service.sh &
```

---

## Network Issues

### Issue: Connection Timeout

**Error Message:**
```
java.net.SocketTimeoutException: Read timed out
ERROR: Connection timeout after 30000ms
```

**Cause:** Network latency, firewall blocking, or server not responding.

**Solution:**

1. **Increase timeout:**
```properties
# In agent.properties
agent.connection.timeout=60000  # 60 seconds
agent.read.timeout=60000
```

2. **Check firewall:**
```bash
# Linux
sudo iptables -L -n | grep 443

# Windows
netsh advfirewall firewall show rule name=all | find "443"
```

3. **Test with longer timeout:**
```bash
curl --max-time 60 -I https://your-server.com
```

---

### Issue: Proxy Configuration Problems

**Error Message:**
```
ERROR: Unable to tunnel through proxy
ERROR: Proxy authentication failed
```

**Solution:**

1. **Configure proxy in agent.properties:**
```properties
http.proxyHost=proxy.company.com
http.proxyPort=8080
https.proxyHost=proxy.company.com
https.proxyPort=8080

# With authentication
http.proxyUser=username
http.proxyPassword=password
```

2. **Set environment variables:**
```bash
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1
```

3. **Test proxy connectivity:**
```bash
curl -x proxy.company.com:8080 https://your-server.com
```

---

## Application-Specific Issues

### Issue: HFM Registry File Not Found

**Error Message:**
```
ERROR: Cannot find reg.properties file
ERROR: HFM initialization failed
```

**Solution:**

1. **Copy registry file:**
```bash
# Windows
copy D:\Oracle\Middleware\user_projects\config\foundation\11.1.2.0\reg.properties ^
     D:\Oracle\Middleware\user_projects\epmsystem1\config\foundation\11.1.2.0\

# Linux
cp /opt/Oracle/Middleware/user_projects/config/foundation/11.1.2.0/reg.properties \
   /opt/Oracle/Middleware/user_projects/epmsystem1/config/foundation/11.1.2.0/
```

2. **Verify permissions:**
```bash
ls -la /path/to/reg.properties
```

---

### Issue: Planning Password File Problems

**Error Message:**
```
ERROR: Cannot read password file
ERROR: Invalid encrypted password
```

**Solution:**

1. **Generate password file:**
```bash
cd /opt/Oracle/Middleware/user_projects/epmsystem1/Planning/planning1
./PasswordEncryption.sh password_file.txt
```

2. **Update configuration:**
```properties
# In EPMware application properties
PASSWORD_FILE=/opt/Oracle/password_file.txt
```

3. **Check file permissions:**
```bash
chmod 600 password_file.txt
chown planning_user password_file.txt
```

---

### Issue: EPM Automate Not Found (Cloud)

**Error Message:**
```
ERROR: epmautomate: command not found
ERROR: Cannot execute EPM Automate utility
```

**Solution:**

1. **Install EPM Automate:**
```bash
# Download from Oracle Cloud
wget https://cloud-url/epmautomate.tar

# Extract
tar xf epmautomate.tar -C /home/epmadmin/

# Add to PATH
export PATH=$PATH:/home/epmadmin/epmautomate/bin
```

2. **Test EPM Automate:**
```bash
epmautomate login username password url
```

---

## Quick Resolution Checklist

When encountering any issue, check these items in order:

1. ✓ **Java installed and in PATH**
```bash
java -version
```

2. ✓ **Agent files in correct location**
```bash
ls -la ~/epmware-agent.jar
```

3. ✓ **Configuration file valid**
```bash
grep -v "^#" agent.properties
```

4. ✓ **Token is valid**
```bash
# 36 characters, UUID format
```

5. ✓ **Network connectivity**
```bash
ping your-server.com
```

6. ✓ **Correct permissions**
```bash
ls -la agent.properties ew_target_service.sh
```

7. ✓ **Recent errors in logs**
```bash
tail -50 logs/agent.log | grep ERROR
```

8. ✓ **Process is running**
```bash
ps aux | grep epmware
```

9. ✓ **Sufficient resources**
```bash
free -h  # Memory
df -h    # Disk
```

10. ✓ **Service/task configured correctly**
```bash
# Windows: Task Scheduler
# Linux: systemctl status epmware-agent
```

!!! tip "Prevention"
    Most issues can be prevented by carefully following installation instructions and regularly reviewing agent logs for warnings before they become errors.

!!! note "Still Having Issues?"
    If problems persist after trying these solutions, collect diagnostic information and contact EPMware Support at support@epmware.com.

## Next Steps

- [Connection Problems](connection.md) - Network-specific issues
- [Password Issues](passwords.md) - Authentication problems
- [Service Errors](service-errors.md) - Service configuration issues
- [Debug Mode](debug.md) - Enable detailed logging
# Java Configuration

## Overview

The EPMware Agent requires Java Runtime Environment (JRE) or Java Development Kit (JDK) version 1.8 or higher. This guide covers Java installation, configuration, and verification for both Windows and Linux systems.

## Java Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|------------|
| **Version** | Java 1.8 (Java 8) or higher |
| **Type** | JRE or JDK |
| **Architecture** | 64-bit recommended |
| **Memory** | -Xmx2048m minimum heap size |

### Compatibility Matrix

| EPMware Agent Version | Minimum Java | Recommended Java |
|----------------------|--------------|------------------|
| 1.7.x | Java 1.8 | Java 11 LTS |
| 1.6.x | Java 1.8 | Java 8 |
| 1.5.x | Java 1.7 | Java 8 |

## Checking Existing Java Installation

### Windows Check

```cmd
# Command Prompt
java -version

# PowerShell
java -version
Get-Command java
```

### Linux Check

```bash
# Check Java version
java -version

# Find Java installation
which java
whereis java

# Check JAVA_HOME
echo $JAVA_HOME
```

### Cygwin Check (Windows)

```bash
# Open Cygwin Terminal
java -version

# Check path
which java
```

Expected output example:
```
java version "1.8.0_291"
Java(TM) SE Runtime Environment (build 1.8.0_291-b10)
Java HotSpot(TM) 64-Bit Server VM (build 25.291-b10, mixed mode)
```

![Java Version Check](../../assets/images/installation/java-version-check.png)<br/>
*Checking Java version in terminal*

## Installing Java

### Windows Installation

#### Step 1: Download Java

1. Visit [Oracle Java Downloads](https://www.oracle.com/java/technologies/downloads/)
   - Or use [OpenJDK](https://adoptium.net/) for open-source alternative
2. Select Java 8 or Java 11 LTS
3. Choose Windows x64 installer

#### Step 2: Run Installer

1. Right-click the downloaded file
2. Select **Run as administrator**
3. Follow installation wizard:
   - Accept license agreement
   - Choose installation directory (default: `C:\Program Files\Java\`)
   - Complete installation

![Java Installation Wizard](../../assets/images/installation/java-install-wizard.png)<br/>
*Java installation wizard on Windows*

#### Step 3: Set JAVA_HOME

1. Open System Properties:
   - Right-click **This PC** → **Properties**
   - Click **Advanced system settings**
   - Click **Environment Variables**

2. Create JAVA_HOME variable:
   - Click **New** under System variables
   - Variable name: `JAVA_HOME`
   - Variable value: `C:\Program Files\Java\jdk1.8.0_291`

![Setting JAVA_HOME](../../assets/images/installation/java-home-setup.png)<br/>
*Configuring JAVA_HOME environment variable*

#### Step 4: Update PATH

1. Edit the **Path** system variable
2. Add new entry: `%JAVA_HOME%\bin`
3. Click OK to save

### Linux Installation

#### Option 1: Package Manager

**Red Hat/CentOS/Oracle Linux:**
```bash
# Install OpenJDK 8
sudo yum install java-1.8.0-openjdk

# Install OpenJDK 11
sudo yum install java-11-openjdk

# Set default Java version
sudo alternatives --config java
```

**Ubuntu/Debian:**
```bash
# Update package index
sudo apt update

# Install OpenJDK 8
sudo apt install openjdk-8-jdk

# Install OpenJDK 11
sudo apt install openjdk-11-jdk

# Set default Java version
sudo update-alternatives --config java
```

#### Option 2: Manual Installation

```bash
# Download Java tar.gz from Oracle
wget https://download.oracle.com/java/8/latest/jdk-8u291-linux-x64.tar.gz

# Extract to /opt
sudo tar -xzf jdk-8u291-linux-x64.tar.gz -C /opt/

# Create symbolic link
sudo ln -s /opt/jdk1.8.0_291 /opt/java
```

#### Set Environment Variables (Linux)

Edit `/etc/profile` or `~/.bashrc`:

```bash
# Add to profile
export JAVA_HOME=/opt/java
export PATH=$JAVA_HOME/bin:$PATH

# Reload profile
source /etc/profile
```

## Configuring Java for EPMware Agent

### Memory Settings

Create or edit `java.properties` in agent directory:

```properties
# Java memory configuration
java.xms=512m
java.xmx=2048m
java.maxpermsize=256m
java.gc.type=G1GC
```

### Security Configuration

For secure environments, configure Java security:

```bash
# Edit java.security file
$JAVA_HOME/lib/security/java.security

# Add EPMware certificates to truststore
keytool -importcert -file epmware.crt -keystore $JAVA_HOME/lib/security/cacerts
```

## Verification Steps

### Step 1: Verify Java Installation

```bash
# Check version
java -version

# Check compiler (if JDK)
javac -version

# Check Java home
echo $JAVA_HOME
```

### Step 2: Test Java from Cygwin (Windows)

```bash
# Open Cygwin Terminal
$ java -version
$ echo $JAVA_HOME
$ which java
```

![Cygwin Java Test](../../assets/images/installation/cygwin-java-test.png)<br/>
*Testing Java accessibility from Cygwin*

### Step 3: Verify Classpath

```bash
# Check classpath
echo $CLASSPATH

# If empty, that's OK for EPMware Agent
```

### Step 4: Test Java Execution

Create a simple test:

```bash
# Create test file
echo 'public class Test { public static void main(String[] args) { System.out.println("Java is working!"); } }' > Test.java

# Compile (if JDK)
javac Test.java

# Run
java Test
```

Expected output:
```
Java is working!
```

## Java Configuration for Specific Applications

### HFM Integration

HFM may require specific Java versions:

```properties
# HFM-specific Java settings
hfm.java.home=/opt/java/jdk1.8.0_202
hfm.java.opts=-Xmx4096m -XX:MaxPermSize=512m
```

### Cloud EPM Integration

For EPM Automate compatibility:

```properties
# EPM Automate Java requirements
epmautomate.java.version=1.8
epmautomate.java.tls.version=TLSv1.2
```

## Troubleshooting Java Issues

### Common Problems

| Issue | Cause | Solution |
|-------|-------|----------|
| "java: command not found" | Java not in PATH | Add Java bin directory to PATH |
| "JAVA_HOME is not set" | Missing environment variable | Set JAVA_HOME to Java installation directory |
| "Unsupported major.minor version" | Wrong Java version | Install required Java version |
| "Could not create JVM" | Insufficient memory | Reduce -Xmx value or increase system memory |

### Windows-Specific Issues

#### Issue: Java Not Found in Cygwin

Solution:
```bash
# Add to ~/.bashrc in Cygwin
export JAVA_HOME="/cygdrive/c/Program Files/Java/jdk1.8.0_291"
export PATH=$JAVA_HOME/bin:$PATH

# Reload
source ~/.bashrc
```

#### Issue: Space in Path

Solution:
```bash
# Use quotes or escape spaces
export JAVA_HOME="/cygdrive/c/Program Files/Java/jdk1.8.0_291"
# Or
export JAVA_HOME=/cygdrive/c/Program\ Files/Java/jdk1.8.0_291
```

### Linux-Specific Issues

#### Issue: Multiple Java Versions

Solution:
```bash
# List all Java installations
update-alternatives --list java

# Set default
sudo update-alternatives --config java

# Verify
java -version
```

#### Issue: Permission Denied

Solution:
```bash
# Check permissions
ls -la $(which java)

# Fix if needed
sudo chmod 755 /usr/bin/java
```

## Performance Optimization

### JVM Tuning

For optimal agent performance:

```properties
# Recommended JVM settings
-Xms1024m
-Xmx2048m
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:ParallelGCThreads=4
-XX:ConcGCThreads=2
-XX:InitiatingHeapOccupancyPercent=70
```

### Monitoring Java Memory

```bash
# Check Java process memory
jps -v

# Monitor heap usage
jstat -gc <pid> 1000

# Generate heap dump if needed
jmap -dump:format=b,file=heap.bin <pid>
```

## Security Considerations

### TLS/SSL Configuration

For secure communications:

```bash
# Enable TLS 1.2 and 1.3
-Dhttps.protocols=TLSv1.2,TLSv1.3
-Djdk.tls.client.protocols=TLSv1.2,TLSv1.3

# Disable weak ciphers
-Djdk.tls.disabledAlgorithms=SSLv3,RC4,DES,MD5withRSA
```

### Certificate Management

```bash
# List certificates in truststore
keytool -list -keystore $JAVA_HOME/lib/security/cacerts

# Import certificate
keytool -importcert -alias epmware -file epmware.crt \
  -keystore $JAVA_HOME/lib/security/cacerts \
  -storepass changeit
```

## Best Practices

### Installation Guidelines

1. **Use LTS Versions** - Prefer Java 8 or 11 LTS for stability
2. **64-bit Architecture** - Always use 64-bit Java for better performance
3. **Consistent Versions** - Use same Java version across all agents
4. **Regular Updates** - Keep Java updated for security patches

### Environment Management

1. **Document Configuration** - Record Java version and settings
2. **Test Changes** - Verify Java changes in non-production first
3. **Monitor Performance** - Track JVM metrics regularly
4. **Plan Upgrades** - Schedule Java updates during maintenance windows

## Validation Checklist

Before proceeding with agent installation:

- [ ] Java 1.8+ is installed
- [ ] `java -version` returns expected version
- [ ] JAVA_HOME is set correctly
- [ ] Java is in system PATH
- [ ] Java works from Cygwin (Windows)
- [ ] Sufficient memory for JVM heap
- [ ] TLS 1.2 is supported
- [ ] Required certificates are installed

!!! success "Java Configuration Complete"
    Once Java is properly configured, proceed to [Agent Installation](../agent/index.md) to deploy the EPMware Agent files.

## Next Steps

1. [Download Agent Files](../agent/download.md) - Obtain the agent package
2. [Extract and Deploy](../agent/file-structure.md) - Set up agent structure
3. [Configure Properties](../../configuration/agent-properties.md) - Configure agent settings
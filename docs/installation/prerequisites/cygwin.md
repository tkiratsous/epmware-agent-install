# Installing Cygwin

## Overview

Cygwin is a required component for running the EPMware Agent on Windows servers. It provides a Linux-like environment that allows the agent's shell scripts to execute properly on Windows systems.

!!! note "Windows Only"
    Cygwin installation is only required for Windows servers. Linux servers can skip this section and proceed to [Java Configuration](java.md).

## Prerequisites

Before installing Cygwin:

- [ ] Windows Administrator privileges
- [ ] Internet connection for downloading packages
- [ ] At least 1 GB of free disk space
- [ ] Proxy server information (if applicable)

## Download Cygwin

### Step 1: Access Cygwin Website

1. Navigate to [www.cygwin.com](https://www.cygwin.com)
2. Click on "Install Cygwin" link
3. Choose the appropriate installer:
   - **setup-x86_64.exe** for 64-bit Windows (recommended)
   - **setup-x86.exe** for 32-bit Windows

### Step 2: Save the Installer

1. Download the setup file to your Desktop or Downloads folder
2. Right-click the downloaded file and select "Properties"
3. If blocked, check "Unblock" and click OK

![Cygwin Download Page](../../assets/images/installation/cygwin-download.png)<br/>
*Cygwin download page with installer options*

## Installation Process

### Step 1: Run the Installer

1. Right-click **setup-x86_64.exe**
2. Select **Run as administrator**
3. Click **Yes** on the User Account Control prompt

### Step 2: Installation Type

Select **Install from Internet** and click **Next**

![Installation Type](../../assets/images/installation/cygwin-install-type.png)<br/>
*Selecting installation type - Install from Internet*

### Step 3: Installation Directory

Configure the installation paths:

| Setting | Recommended Value | Notes |
|---------|------------------|-------|
| **Root Directory** | `C:\cygwin64` | Default location recommended |
| **Install For** | All Users | Ensures all users can access |

![Root Directory](../../assets/images/installation/cygwin-root-directory.png)<br/>
*Configuring Cygwin root directory*

!!! tip "Custom Installation Path"
    If installing to a different drive, ensure the EPMware Agent configuration reflects the correct path.

### Step 4: Local Package Directory

Specify where to store downloaded packages:

- **Recommended**: `C:\cygwin64\packages`
- **Important**: Do not use the Cygwin root folder

![Package Directory](../../assets/images/installation/cygwin-package-directory.png)<br/>
*Setting local package directory*

### Step 5: Connection Method

Configure your internet connection:

- **Direct Connection**: If connected directly to the internet
- **Use Proxy**: If behind a corporate proxy server

For proxy configuration:
```
Proxy Host: proxy.company.com
Port: 8080
```

![Connection Method](../../assets/images/installation/cygwin-connection-method.png)<br/>
*Selecting connection method*

### Step 6: Download Site Selection

Choose a mirror site for downloading packages:

1. Select any available mirror from the list
2. Prefer sites with good connectivity to your location
3. Click **Next** to proceed

![Mirror Selection](../../assets/images/installation/cygwin-mirror-site.png)<br/>
*Selecting a download mirror site*

### Step 7: Package Selection

For EPMware Agent, the default packages are sufficient:

1. Keep "Category" view
2. Leave all defaults selected
3. Click **Next** to begin installation

!!! note "Required Packages"
    The EPMware Agent requires only the base Cygwin packages. Additional packages are not necessary unless specified by your environment requirements.

### Step 8: Installation Progress

The installer will:
1. Download selected packages
2. Install Cygwin base system
3. Create shortcuts and icons
4. Configure the environment

![Installation Progress](../../assets/images/installation/cygwin-install-progress.png)<br/>
*Cygwin installation in progress*

### Step 9: Completion

1. Select **Create icon on Desktop** (optional)
2. Select **Add icon to Start Menu** (recommended)
3. Click **Finish**

## Post-Installation Verification

### Verify Installation

1. Open Windows Explorer
2. Navigate to `C:\cygwin64`
3. Verify the following directories exist:
   - `bin\`
   - `etc\`
   - `home\`
   - `usr\`
   - `var\`

### Test Cygwin Terminal

1. Double-click the Cygwin Terminal icon on desktop
2. The terminal should open with a prompt:
   ```bash
   username@hostname ~
   $
   ```

3. Test basic commands:
   ```bash
   # Check current directory
   pwd
   
   # List files
   ls -la
   
   # Check Cygwin version
   uname -a
   ```

![Cygwin Terminal](../../assets/images/installation/cygwin-terminal-test.png)<br/>
*Cygwin terminal showing successful installation*

## User Configuration

### Identify Cygwin User

The EPMware Agent will run under a specific Windows user. This user needs a Cygwin home directory:

1. Open Cygwin Terminal
2. Check current user:
   ```bash
   whoami
   ```
3. Verify home directory:
   ```bash
   echo $HOME
   ```

Expected output:
```
/home/Administrator
```

### Create Service Account Home (Optional)

If using a service account:

1. Open Cygwin Terminal as the service account
2. Cygwin will automatically create the home directory
3. Verify creation:
   ```bash
   ls -la /home/
   ```

## Environment Variables

### PATH Configuration

Cygwin's bin directory should be in the system PATH:

1. Open System Properties → Advanced → Environment Variables
2. Edit the **Path** variable
3. Add: `C:\cygwin64\bin`

### Verify PATH

```cmd
# In Windows Command Prompt
where bash
where ls
```

Expected output:
```
C:\cygwin64\bin\bash.exe
C:\cygwin64\bin\ls.exe
```

## Required Components for EPMware

### Essential Binaries

Verify these commands are available:

```bash
# In Cygwin Terminal
which bash
which java
which zip
which unzip
```

### File Permissions

Ensure proper permissions for the agent user:

```bash
# Check permissions
ls -la /home/$(whoami)

# Set correct permissions if needed
chmod 755 /home/$(whoami)
```

## Troubleshooting Cygwin Installation

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Setup fails to download | Proxy/firewall blocking | Configure proxy settings or try different mirror |
| "Permission denied" errors | Incorrect user permissions | Run installer as administrator |
| Missing home directory | User hasn't logged into Cygwin | Open Cygwin Terminal as that user |
| Commands not found | PATH not configured | Add Cygwin bin to system PATH |

### Reinstallation

If you need to reinstall Cygwin:

1. Backup any important files from `/home/` directories
2. Uninstall Cygwin through Control Panel
3. Delete the `C:\cygwin64` directory
4. Run the installer again

### Cygwin Updates

To update Cygwin packages:

1. Run the setup program again
2. Select "Keep" for existing packages
3. Update any packages marked with "New"

## Security Considerations

### File System Permissions

- Cygwin inherits Windows NTFS permissions
- Ensure only authorized users can access Cygwin directories
- Protect the agent installation directory

### Service Account Best Practices

- Use a dedicated service account for the agent
- Grant minimum necessary permissions
- Avoid using domain administrator accounts

## Special Considerations for EPMware

### Multiple Agents

If running multiple agents on the same server:

1. Use the same Cygwin installation
2. Create separate home directories for each agent
3. Configure unique properties for each instance

### Server-Specific Requirements

For specific EPM applications:

- **HFM Servers**: Ensure Cygwin user can access HFM utilities
- **Planning Servers**: Verify access to Planning utilities
- **Essbase Servers**: Check MaxL script execution capability

## Validation Checklist

Before proceeding to agent installation:

- [ ] Cygwin installed successfully
- [ ] Terminal opens without errors
- [ ] Home directory exists for agent user
- [ ] Basic commands work (ls, pwd, etc.)
- [ ] Java is accessible from Cygwin
- [ ] zip/unzip commands are available

!!! success "Installation Complete"
    Once Cygwin is installed and verified, proceed to [Java Configuration](java.md) to set up the Java environment.

## Next Steps

1. [Configure Java](java.md) - Set up Java environment
2. [Download Agent](../agent/download.md) - Get EPMware Agent files
3. [Extract Files](../agent/file-structure.md) - Deploy agent components
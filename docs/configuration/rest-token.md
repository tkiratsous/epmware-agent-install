# REST API Token Configuration

## Overview

EPMware Agents use REST API tokens for secure authentication with the EPMware application. This token-based approach eliminates the need to store passwords and provides a secure method for agent-to-application communication.

## Understanding REST Tokens

### What is a REST API Token?

A REST API token is a 36-character alphanumeric string that serves as a unique identifier for authentication. The agent uses this token to:

- Authenticate with the EPMware application
- Poll for pending deployment tasks
- Report deployment status and results
- Maintain secure communication

### Token Format

EPMware tokens follow the UUID format:
```
2e6d4103-5145-4c30-9837-ac6d14797523
```

### Security Benefits

- **No Password Storage** - Tokens eliminate password storage in configuration files
- **Revocable Access** - Tokens can be revoked without changing passwords
- **Audit Trail** - All token usage is logged for security auditing
- **Limited Scope** - Tokens have specific permissions unlike full user credentials

## Generating a REST Token

### Prerequisites

Before generating a token:
- [ ] Have administrator access to EPMware
- [ ] Created a dedicated user account for the agent
- [ ] Assigned appropriate permissions to the user

### Step-by-Step Token Generation

#### Step 1: Navigate to User Management

1. Log into the EPMware application
2. Navigate to **Administration** → **Security** → **Users**

![User Management](../assets/images/configuration/user-management.png)<br/>
*User Management screen in EPMware*

#### Step 2: Select the Agent User

1. Locate the user account designated for agent operations
2. Common naming conventions:
   - `svc_epmware_agent`
   - `agent_[servername]`
   - `epmware_service`

!!! tip "Dedicated Service Account"
    Always use a dedicated service account for the agent rather than personal user accounts. This ensures continuity and proper audit trails.

#### Step 3: Generate Token

1. Right-click on the user record
2. Select **Generate Token** from the context menu

![Generate Token Menu](../assets/images/configuration/generate-token-menu.png)<br/>
*Right-click menu showing Generate Token option*

#### Step 4: Copy and Save Token

1. The token will be displayed in a dialog box
2. **Important**: Copy the token immediately - it won't be shown again
3. Store the token securely

![Token Generated](../assets/images/configuration/token-generated-dialog.png)<br/>
*Token generation dialog - copy this token immediately*

## User Account Setup

### Creating an Agent User

If you haven't created a dedicated user for the agent:

1. Click **Add User** in the User Management screen
2. Configure the user with these recommended settings:

| Field | Recommended Value |
|-------|------------------|
| **Username** | `svc_epmware_agent` |
| **Full Name** | EPMware Agent Service |
| **Email** | `epmware-agent@company.com` |
| **User Type** | Service Account |
| **Password Never Expires** | ✓ Checked |
| **Account Enabled** | ✓ Checked |

### Required Permissions

The agent user needs specific permissions:

#### Minimum Permissions

- **Application Access** - Read access to target applications
- **Deployment Rights** - Execute deployment tasks
- **API Access** - REST API usage permission

#### Recommended Permissions

| Permission | Purpose |
|------------|---------|
| **Import Metadata** | Import hierarchies from target applications |
| **Deploy Metadata** | Deploy approved changes to targets |
| **View Requests** | Access deployment queue |
| **View Logs** | Read deployment logs |
| **Execute Scripts** | Run deployment scripts |

### Security Class Assignment

Assign the agent user to appropriate security classes:

```sql
-- Example security configuration
GRANT epmware_agent_role TO svc_epmware_agent;
GRANT deployment_executor TO svc_epmware_agent;
GRANT api_access TO svc_epmware_agent;
```

## Token Management

### Token Storage

Store tokens securely:

#### Do's
- ✓ Store in encrypted configuration management systems
- ✓ Use environment variables for sensitive data
- ✓ Implement file system permissions
- ✓ Keep backup in secure password manager

#### Don'ts
- ✗ Never commit tokens to version control
- ✗ Avoid storing in plain text files
- ✗ Don't share tokens between environments
- ✗ Never expose tokens in logs or error messages

### Token Rotation

Implement regular token rotation for security:

#### Rotation Schedule

| Environment | Rotation Frequency |
|-------------|-------------------|
| **Production** | Every 90 days |
| **UAT/Test** | Every 180 days |
| **Development** | As needed |

#### Rotation Process

1. **Generate New Token**
   - Create new token in EPMware
   - Note generation timestamp

2. **Update Configuration**
   ```properties
   # Update agent.properties
   ew.portal.token=new-token-value-here
   ```

3. **Restart Agent**
   - Stop the agent service
   - Update configuration file
   - Start the agent service

4. **Verify Operation**
   - Check agent logs for successful authentication
   - Monitor first deployment after rotation

5. **Revoke Old Token**
   - Wait 24 hours to ensure stability
   - Revoke previous token in EPMware

### Token Revocation

To revoke a compromised or expired token:

1. Navigate to **Administration** → **Security** → **Users**
2. Right-click on the user
3. Select **Revoke Token**
4. Confirm revocation

![Revoke Token](../assets/images/configuration/revoke-token.png)<br/>
*Revoking an existing token*

!!! warning "Immediate Effect"
    Token revocation takes effect immediately. Ensure you have a replacement token ready before revoking the active one.

## Using the Token

### Configuration File

Add the token to your `agent.properties` file:

```properties
# REST API Token Configuration
ew.portal.token=2e6d4103-5145-4c30-9837-ac6d14797523
```

### Environment Variables

For enhanced security, use environment variables:

```bash
# Set environment variable
export EPMWARE_TOKEN=2e6d4103-5145-4c30-9837-ac6d14797523

# Reference in agent.properties
ew.portal.token=${EPMWARE_TOKEN}
```

### Testing Token Authentication

Verify token validity before starting the agent:

```bash
# Test authentication
curl -H "Authorization: Bearer YOUR-TOKEN-HERE" \
     https://epmware-server.com/api/v1/auth/verify

# Expected response
{"status": "authenticated", "user": "svc_epmware_agent"}
```

## Troubleshooting Token Issues

### Common Problems

| Issue | Cause | Solution |
|-------|-------|----------|
| Authentication Failed | Invalid or expired token | Generate new token |
| Permission Denied | Insufficient user permissions | Review user security settings |
| Token Not Accepted | Wrong environment | Verify server URL matches token |
| Intermittent Failures | Token rate limited | Implement retry logic |

### Validation Checklist

- [ ] Token is exactly 36 characters
- [ ] No extra spaces or characters
- [ ] Token matches the server environment
- [ ] User account is active
- [ ] User has required permissions
- [ ] Token hasn't been revoked

### Debug Authentication

Enable debug logging to troubleshoot:

```properties
# Add to agent.properties
agent.log.level=DEBUG
agent.log.auth=true
```

Check logs for authentication details:
```bash
tail -f logs/agent.log | grep AUTH
```

## Security Best Practices

### Token Security Guidelines

1. **Principle of Least Privilege**
   - Grant only necessary permissions
   - Use separate tokens per environment
   - Implement role-based access control

2. **Token Lifecycle Management**
   - Document token creation/rotation dates
   - Maintain token inventory
   - Implement automated rotation reminders

3. **Monitoring and Auditing**
   - Monitor token usage patterns
   - Alert on authentication failures
   - Review audit logs regularly

4. **Incident Response**
   - Have revocation procedures ready
   - Maintain emergency token replacement process
   - Document security incident procedures

### Compliance Considerations

Ensure token management meets compliance requirements:

- **SOX**: Implement separation of duties
- **PCI-DSS**: Encrypt tokens at rest and in transit
- **GDPR**: Include tokens in data protection policies
- **HIPAA**: Ensure tokens meet security rule requirements

## Multi-Environment Token Management

### Environment Separation

Use different tokens for each environment:

```properties
# Development
ew.portal.token.dev=dev-token-value

# Test/UAT
ew.portal.token.uat=uat-token-value

# Production
ew.portal.token.prod=prod-token-value
```

### Token Naming Convention

Implement consistent naming:
- `[environment]-[application]-[purpose]-token`
- Example: `prod-hfm-deploy-token`

## API Token vs User Credentials

### Comparison

| Aspect | API Token | User Credentials |
|--------|-----------|------------------|
| **Security** | Higher (limited scope) | Lower (full access) |
| **Management** | Easier to rotate | Requires password changes |
| **Audit** | Clear service attribution | Mixed with user activity |
| **Automation** | Designed for automation | Not recommended |
| **Revocation** | Instant and specific | Affects all user access |

## Next Steps

After configuring your REST token:

1. [Update Agent Properties](agent-properties.md) with the token
2. [Test the Connection](testing.md) to verify authentication
3. [Configure Service](service-config.md) startup settings
4. [Monitor Agent Logs](../management/logs.md) for authentication status
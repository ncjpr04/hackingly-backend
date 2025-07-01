# Deployment Troubleshooting Guide

## Common Issues and Solutions

### 1. LinkedIn Login Challenge Error

**Error Message:**
```
{"detail":"Internal server error: 400: LinkedIn login challenge required, you're screwed 💀 (please contact the maintainer if this issue persists)."}
```

**Root Cause:** The LinkedIn agent failed to initialize during startup, but the error details were not properly captured.

**Solution:** 
- Check the `/api/startup-info` endpoint to see the actual initialization error
- Verify LinkedIn credentials are properly set in environment variables
- Check Render logs for detailed error information

### 2. Environment Variables Not Set

**Check:** Visit `/api/startup-info` endpoint

**Expected Response:**
```json
{
  "linkedin_agent_initialized": true,
  "initialization_error": null,
  "environment_variables": {
    "username_set": true,
    "password_set": true
  }
}
```

**If credentials are missing:**
- Go to Render Dashboard → Your Service → Environment
- Add environment variables:
  - `LINKEDIN_AGENT_USERNAME`
  - `LINKEDIN_AGENT_PASSWORD`

### 3. LinkedIn Authentication Issues

**Common Causes:**
- Invalid LinkedIn credentials
- LinkedIn account requires 2FA
- LinkedIn account is locked/suspended
- IP address blocked by LinkedIn

**Solutions:**
1. **Verify credentials** - Test with a fresh LinkedIn account
2. **Check LinkedIn account status** - Ensure account is active and not restricted
3. **Use residential IP** - LinkedIn may block datacenter IPs
4. **Enable 2FA properly** - Some LinkedIn accounts require 2FA setup

### 4. Network/Connection Issues

**Symptoms:**
- Timeout errors
- Connection refused
- SSL certificate errors

**Solutions:**
1. **Check Render service logs** for network errors
2. **Verify internet connectivity** from Render's servers
3. **Check firewall settings** if using custom networking

### 5. Memory/Resource Issues

**Symptoms:**
- Service crashes on startup
- Out of memory errors
- Slow response times

**Solutions:**
1. **Upgrade Render plan** to get more resources
2. **Check memory usage** in Render dashboard
3. **Optimize code** if memory usage is high

## Debugging Steps

### Step 1: Check Service Status
```bash
curl https://your-render-service.onrender.com/
```

### Step 2: Check Startup Information
```bash
curl https://your-render-service.onrender.com/api/startup-info
```

### Step 3: Check Health Status
```bash
curl https://your-render-service.onrender.com/api/health
```

### Step 4: Check Render Logs
1. Go to Render Dashboard
2. Select your service
3. Click on "Logs" tab
4. Look for error messages during startup

### Step 5: Test with Sample Request
```bash
curl https://your-render-service.onrender.com/api/profile/test-user
```

## Environment Variable Setup

### Required Variables
```bash
LINKEDIN_AGENT_USERNAME=your-linkedin-email@example.com
LINKEDIN_AGENT_PASSWORD=your-linkedin-password
```

### Optional Variables
```bash
# For additional debugging
DEBUG=true
LOG_LEVEL=DEBUG
```

## Render-Specific Configuration

### Build Command
```bash
pip install -r requirements.txt
```

### Start Command
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Environment
- **Python Version:** 3.9 or higher
- **Region:** Choose closest to your users
- **Plan:** Start with free tier, upgrade if needed

## Common Error Messages and Solutions

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `LinkedIn service unavailable: LinkedIn login challenge required` | LinkedIn authentication failed | Check credentials, account status |
| `LinkedIn service unavailable: Failed to initialize LinkedInAgent` | General initialization failure | Check logs, verify environment |
| `LinkedIn service not initialized` | Agent is None but no error stored | Check startup logs |
| `Failed to fetch profile: [details]` | LinkedIn API error | Check profile URL, account permissions |
| `Failed to parse profile data: [details]` | Data processing error | Check LinkedIn API response format |

## Getting Help

1. **Check Render logs** first
2. **Use the `/api/startup-info` endpoint** to get detailed status
3. **Test locally** to isolate deployment vs code issues
4. **Check LinkedIn account status** independently
5. **Contact support** with specific error messages and logs 
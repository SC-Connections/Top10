# Troubleshooting Guide

This guide helps you resolve common issues with the Top10 site generator.

## Issue: "RAPID_KEY environment variable is required"

This error means the GitHub workflow cannot find your RapidAPI key secret.

### Quick Fix

1. **Check Your Secret Names**
   - Go to: `Settings` > `Secrets and variables` > `Actions`
   - Verify you have a secret named **exactly** one of these:
     - `RAPIDAPI_KEY` (recommended)
     - `RAPID_API_KEY`
     - `RAPID_KEY`
     - `RAPIDAPIKEY`

2. **Verify Secret Has a Value**
   - You can't see the value of secrets after creation
   - If unsure, delete and recreate the secret with your RapidAPI key
   - Make sure you copied the entire key (no spaces before/after)

3. **Check Secret Scope**
   - Secrets must be **Repository secrets**, not Environment secrets
   - They should be under `Settings` > `Secrets and variables` > `Actions`
   - NOT under `Settings` > `Environments`

### Step-by-Step Verification

#### Step 1: Get Your RapidAPI Key

1. Log in to [RapidAPI](https://rapidapi.com/)
2. Subscribe to an Amazon product API (like Amazon23 or similar)
3. Go to the API's page
4. Look for the "Code Snippets" section
5. Find the header: `X-RapidAPI-Key: your-key-here`
6. Copy the value (everything after `X-RapidAPI-Key: `)

#### Step 2: Verify or Create the Secret

1. Go to your GitHub repository
2. Click `Settings` tab (top right)
3. In left sidebar: `Secrets and variables` > `Actions`
4. You should see your secrets listed

**If RAPIDAPI_KEY exists:**
- Click on it
- Click "Update secret"
- Paste your RapidAPI key
- Click "Update secret"

**If RAPIDAPI_KEY doesn't exist:**
- Click "New repository secret"
- Name: `RAPIDAPI_KEY` (exactly this, case-sensitive)
- Value: Paste your RapidAPI key
- Click "Add secret"

#### Step 3: Test Again

1. Go to `Actions` tab
2. Select "Generate Top10 Site"
3. Click "Run workflow"
4. Fill in the form:
   - Title: `Test Products`
   - Slug: `test-products`
   - Niche: `test`
   - Search Query: `coffee maker`
5. Click "Run workflow"
6. Wait for the workflow to complete
7. Check the logs

### Common Mistakes

❌ **Wrong name**: Creating secret as `RAPID_KEY` instead of `RAPIDAPI_KEY`
   - Fix: Our workflow now supports both! But `RAPIDAPI_KEY` is recommended.

❌ **Empty value**: Creating secret with no value or just spaces
   - Fix: Make sure you paste the actual API key from RapidAPI

❌ **Wrong scope**: Creating secret in Environments instead of Actions
   - Fix: Delete it and create under `Secrets and variables` > `Actions`

❌ **Trailing/leading spaces**: Copying key with extra spaces
   - Fix: Trim spaces from the beginning and end of your key

❌ **Wrong key**: Using a different API key (not from RapidAPI)
   - Fix: Get the key from RapidAPI after subscribing to an Amazon API

## Issue: "API returns errors" or "Exceeded rate limits"

### Possible Causes

1. **Free tier limits exceeded**
   - Most RapidAPI plans have request limits
   - Check your usage on RapidAPI dashboard
   - Wait for the limit to reset or upgrade your plan

2. **Invalid API subscription**
   - Your API subscription may have expired
   - Go to RapidAPI and verify your subscription status
   - Resubscribe if needed

3. **Wrong API endpoint**
   - The API endpoint in the workflow may not match your subscription
   - Check which Amazon API you subscribed to
   - Verify the endpoint URL in `.github/scripts/fill-template.js`

### Solutions

**Check RapidAPI Dashboard:**
1. Log in to [RapidAPI](https://rapidapi.com/)
2. Click your profile icon
3. Go to "My Apps"
4. Check your API usage and limits

**Verify API Subscription:**
1. Go to the API's page on RapidAPI
2. Check your subscription status
3. Make sure you're subscribed to a plan (even if it's free)

**Change API Provider:**
If your current API isn't working, you can use a different one:
1. Search for alternative Amazon product APIs on RapidAPI
2. Subscribe to a new one
3. Update the endpoint in `.github/scripts/fill-template.js`
4. Update the API host if needed

## Issue: "Affiliate links don't work"

### Verification Steps

1. **Check Affiliate ID Format**
   - Should look like: `yourname-20` or `yourname-21`
   - No spaces, special characters, or extra text

2. **Verify Amazon Associates Status**
   - Log in to [Amazon Associates](https://affiliate-program.amazon.com/)
   - Check if your account is approved
   - Some regions have different requirements

3. **Test a Generated Link**
   - After workflow runs, check the generated file
   - Copy one of the product links
   - Paste it in a browser
   - Verify it redirects to Amazon with your tag parameter

4. **Check Secret Configuration**
   - Go to `Settings` > `Secrets and variables` > `Actions`
   - Verify `AMAZON_AFFILIATE_ID` exists
   - Update if needed

## Issue: "Workflow won't start"

### Possible Causes

1. **No workflow dispatch permission**
   - You need write access to the repository
   - Contact the repository owner for access

2. **Branch protection rules**
   - Some repositories restrict who can run workflows
   - Check branch protection settings

3. **Workflow disabled**
   - Workflows can be disabled in Actions settings
   - Go to `Actions` tab and check if workflow is enabled

## Issue: "No products generated" or "Empty output"

### Troubleshooting

1. **Check Search Query**
   - Make sure your search query is valid
   - Try a common product like "laptop" or "headphones"
   - Don't use special characters or overly complex queries

2. **API Response Structure**
   - Different Amazon APIs return data in different formats
   - Check the logs to see the API response structure
   - May need to adjust the response parsing in `fill-template.js`

3. **Mock Data Fallback**
   - The script uses mock data if API fails
   - Check if you're seeing mock data (generic product names)
   - This indicates the API call failed but the workflow continued

## Still Having Issues?

If none of these solutions work:

1. **Check Workflow Logs**
   - Go to `Actions` tab
   - Click on the failed workflow run
   - Read the detailed logs for specific error messages

2. **Verify Prerequisites**
   - Node.js 20 is being used (automatically in GitHub Actions)
   - npm dependencies are installed (automatic in workflow)
   - Repository is not corrupted

3. **Start Fresh**
   - Delete all secrets
   - Follow [SETUP.md](SETUP.md) from scratch
   - Test with a simple product search

4. **Get Help**
   - Open an issue on GitHub
   - Include the workflow run logs
   - Describe what you've already tried

## Useful Commands

If running locally (not in GitHub Actions):

```bash
# Check if config.json exists
ls -la config.json

# Validate Node.js version
node --version  # Should be 20.x or higher

# Install dependencies
npm install

# Check for JavaScript errors
node --check .github/scripts/fill-template.js

# Run the script locally (requires config.json)
node .github/scripts/fill-template.js
```

## Security Reminders

⚠️ **Never**:
- Commit secrets to the repository
- Share your API keys publicly
- Post secret values in issues or discussions
- Use production keys for testing

✅ **Always**:
- Use GitHub secrets for sensitive data
- Rotate keys periodically
- Use separate keys for development and production
- Monitor your API usage

---

For setup instructions, see [SETUP.md](SETUP.md)

For usage examples, see [EXAMPLE.md](EXAMPLE.md)

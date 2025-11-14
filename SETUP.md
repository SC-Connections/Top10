# Setting Up GitHub Secrets

This guide walks you through setting up the required GitHub secrets for the Top10 site generator.

## Required Secrets

The generator requires two secrets to function:

1. **RAPIDAPI_KEY** - Your RapidAPI API key
2. **AMAZON_AFFILIATE_ID** - Your Amazon Associates affiliate tag

## Step 1: Get Your RapidAPI Key

1. **Sign up for RapidAPI**
   - Go to [https://rapidapi.com/](https://rapidapi.com/)
   - Click "Sign Up" and create a free account
   - Verify your email address

2. **Subscribe to Amazon23 API**
   - Search for "Amazon23" or "Amazon Product" in the RapidAPI marketplace
   - Navigate to [https://rapidapi.com/hub](https://rapidapi.com/hub)
   - Look for APIs that provide Amazon product search
   - Select a free or paid plan (most have free tiers)
   - Click "Subscribe to Test"

3. **Get Your API Key**
   - After subscribing, you'll see your API key in the "Code Snippets" section
   - Look for `X-RapidAPI-Key` in the headers
   - Copy this key - you'll need it in Step 3

## Step 2: Get Your Amazon Affiliate ID

1. **Join Amazon Associates**
   - Go to [https://affiliate-program.amazon.com/](https://affiliate-program.amazon.com/)
   - Click "Join Now for Free"
   - Sign in with your Amazon account or create a new one
   - Fill out the application form with your website/blog information
   - Note: You can use your GitHub Pages URL (e.g., `https://username.github.io/Top10/`)

2. **Get Your Affiliate Tag/ID**
   - Once approved (or during the trial period), go to your dashboard
   - Find your "Tracking ID" or "Associate ID"
   - It typically looks like: `yourname-20` or similar
   - Copy this ID - you'll need it in Step 3

## Step 3: Add Secrets to GitHub

1. **Navigate to Your Repository**
   - Go to `https://github.com/SC-Connections/Top10`
   - Make sure you're logged in and have write access

2. **Open Settings**
   - Click the "Settings" tab at the top of the repository
   - If you don't see this tab, you don't have the required permissions

3. **Navigate to Secrets**
   - In the left sidebar, click "Secrets and variables"
   - Click "Actions"

4. **Add RAPIDAPI_KEY**
   - Click "New repository secret"
   - Name: `RAPIDAPI_KEY`
   - Value: Paste your RapidAPI key from Step 1
   - Click "Add secret"

5. **Add AMAZON_AFFILIATE_ID**
   - Click "New repository secret" again
   - Name: `AMAZON_AFFILIATE_ID`
   - Value: Paste your Amazon Associates ID from Step 2
   - Click "Add secret"

## Step 4: Verify Setup

After adding both secrets, you should see them listed in the Secrets section:
- ✓ RAPIDAPI_KEY
- ✓ AMAZON_AFFILIATE_ID

**Important Notes:**
- Secret values are encrypted and cannot be viewed after creation
- You can update secrets by clicking on them and adding a new value
- Only repository admins and maintainers can manage secrets

## Step 5: Test the Workflow

1. Go to the "Actions" tab in your repository
2. Select "Generate Top10 Site"
3. Click "Run workflow"
4. Fill in test data and run
5. Check if the workflow completes successfully

If it fails, check:
- Secrets are spelled correctly (case-sensitive)
- RapidAPI key is valid and has available requests
- Amazon affiliate ID is correctly formatted

## Troubleshooting

### Workflow fails with "RAPID_KEY is required"
- Check that you named the secret `RAPIDAPI_KEY` (not `RAPID_KEY`)
- Verify the secret exists in Settings > Secrets and variables > Actions

### API returns errors
- Check your RapidAPI subscription status
- Verify you haven't exceeded your free tier limits
- Try a different Amazon product API if needed

### Affiliate links don't work
- Double-check your Amazon Associates ID format
- Ensure you're approved in the Associates program
- Test links manually to verify they work

## Security Best Practices

- ✓ **Never** commit API keys or secrets to your repository
- ✓ **Never** share your secrets publicly
- ✓ Rotate keys periodically
- ✓ Use GitHub secrets for all sensitive data
- ✓ Review who has access to your repository

## Need Help?

If you encounter issues:
1. Check the GitHub Actions logs for error messages
2. Verify your secrets are set correctly
3. Test your API key manually with a tool like Postman
4. Review the RapidAPI documentation for the specific Amazon API you're using

---

Once setup is complete, you can start generating Top10 sites! See [EXAMPLE.md](EXAMPLE.md) for usage examples.

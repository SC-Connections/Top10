# Example: Generating a Top10 Site

This guide shows you how to generate a new Top10 product review site using the GitHub Actions workflow.

## Step-by-Step Example

Let's create a "Best Wireless Headphones 2024" site:

### 1. Navigate to GitHub Actions

1. Go to your repository on GitHub
2. Click on the **Actions** tab
3. Select **Generate Top10 Site** from the workflows list
4. Click **Run workflow** button (on the right side)

### 2. Fill in the Form

```
Title: Best Wireless Headphones 2024
Slug: best-wireless-headphones
Niche: wireless headphones
Amazon Search: wireless bluetooth headphones
```

**Field Explanations:**

- **Title**: The full display title of your site (appears at the top of the page)
- **Slug**: URL-friendly identifier (lowercase, use hyphens instead of spaces)
- **Niche**: Product category name (used in subtitle)
- **Amazon Search**: The exact search query to use on Amazon API

### 3. Run the Workflow

Click the green **Run workflow** button at the bottom of the form.

### 4. Monitor Progress

- The workflow will appear in the workflow runs list
- Click on it to see real-time progress
- It typically takes 1-2 minutes to complete

### 5. View Your New Site

After completion:
- A new file will be created: `_posts/2025-11-14-best-wireless-headphones.md`
- Product data will be stored: `_data/best-wireless-headphones.json`
- If GitHub Pages is enabled, visit: `https://[username].github.io/Top10/`

## More Examples

### Coffee Makers

```
Title: Top 10 Coffee Makers for Home Brewing
Slug: top-coffee-makers
Niche: coffee makers
Amazon Search: coffee maker automatic
```

### Laptops

```
Title: Best Laptops for Students 2024
Slug: best-student-laptops
Niche: student laptops
Amazon Search: laptop student college
```

### Running Shoes

```
Title: Best Running Shoes for Marathon Training
Slug: best-marathon-shoes
Niche: running shoes
Amazon Search: running shoes marathon men
```

### Gaming Keyboards

```
Title: Top Gaming Keyboards Under $100
Slug: budget-gaming-keyboards
Niche: gaming keyboards
Amazon Search: mechanical gaming keyboard
```

## Tips for Best Results

1. **Be Specific**: Use detailed search queries for better product matches
2. **Check Regularly**: Run the workflow periodically to update prices and ratings
3. **Test First**: Start with one category to verify everything works
4. **SEO-Friendly Slugs**: Use descriptive, keyword-rich slugs for better search rankings

## Troubleshooting

### Workflow Fails

1. **Check Secrets**: Ensure `RAPIDAPI_KEY` and `AMAZON_AFFILIATE_ID` are set correctly
2. **API Limits**: Verify you haven't exceeded RapidAPI quota
3. **Search Query**: Try a simpler search term if no results are returned

### No Products Found

- The script will use mock data if the API fails
- Check your RapidAPI subscription status
- Verify the search query returns results on Amazon

### Site Not Showing

- Enable GitHub Pages in repository settings
- Wait 1-2 minutes for deployment after workflow completes
- Check that the build succeeded in the Pages section

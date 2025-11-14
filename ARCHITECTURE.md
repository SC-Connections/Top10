# Top10 Architecture

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERACTION                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     GitHub Actions Trigger                       │
│  User clicks "Run workflow" and enters:                         │
│  • Title: "Best Coffee Makers 2024"                             │
│  • Slug: "best-coffee-makers"                                   │
│  • Niche: "coffee makers"                                       │
│  • Amazon Search: "coffee maker automatic"                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              STEP 1: Checkout Repository                         │
│  actions/checkout@v4                                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│         STEP 2: Install Dependencies                            │
│  • Node.js 20                                                   │
│  • npm install -g axios mustache                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│       STEP 3: Fetch Amazon Data via RapidAPI                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  fill-template.js                                        │  │
│  │  • Reads: RAPIDAPI_KEY (from secrets)                   │  │
│  │  • Reads: AMAZON_AFFILIATE_ID (from secrets)            │  │
│  │  • Searches Amazon via RapidAPI                         │  │
│  │  • Gets top 10 products                                 │  │
│  │  • Transforms data                                      │  │
│  │  • Adds affiliate links                                 │  │
│  │  • Writes: _data/filled.json                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│           STEP 4: Create Jekyll Post                            │
│  • Rename filled.json to slug.json                             │
│  • Create _posts/YYYY-MM-DD-slug.md with frontmatter           │
│    ---                                                          │
│    layout: top10                                                │
│    data_file: slug                                              │
│    ---                                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│        STEP 5: Commit & Push Changes                            │
│  stefanzweifel/git-auto-commit-action@v5                       │
│  • Commits new files                                            │
│  • Pushes to repository                                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│           GitHub Pages Deployment (Automatic)                   │
│  Triggered on push to main                                      │
│  • Builds Jekyll site                                           │
│  • Processes _layouts/top10.html template                       │
│  • Injects data from _data/*.json                               │
│  • Publishes to GitHub Pages                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LIVE SITE AVAILABLE                          │
│  https://SC-Connections.github.io/Top10/                       │
│  • Index page lists all generated sites                         │
│  • Each site shows top 10 products                              │
│  • Affiliate links on all buy buttons                           │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. GitHub Actions Workflow
**File**: `.github/workflows/generate-site.yml`
- **Trigger**: Manual (workflow_dispatch)
- **Inputs**: Title, Slug, Niche, Amazon Search
- **Secrets Used**: RAPIDAPI_KEY, AMAZON_AFFILIATE_ID
- **Permissions**: contents: write

### 2. Data Fetcher
**File**: `.github/scripts/fill-template.js`
- **Language**: Node.js
- **Dependencies**: axios
- **Input**: Environment variables
- **Output**: `_data/filled.json`
- **API**: Amazon23 via RapidAPI
- **Fallback**: Mock data if API unavailable

### 3. Jekyll Template
**File**: `_layouts/top10.html`
- **Type**: HTML + Liquid templating
- **Data Source**: `site.data[page.data_file]`
- **Features**:
  - Responsive grid layout
  - Product cards with images
  - Rating stars and review counts
  - Affiliate buy buttons
  - Price display
  - Disclaimer

### 4. Jekyll Posts
**Location**: `_posts/`
**Format**: 
```yaml
---
layout: top10
data_file: slug-name
---
```

### 5. Product Data
**Location**: `_data/`
**Format**: JSON
```json
{
  "title": "Best Coffee Makers 2024",
  "slug": "best-coffee-makers",
  "niche": "coffee makers",
  "products": [
    {
      "rank": 1,
      "title": "Product Name",
      "asin": "B00EXAMPLE",
      "price": "99.99",
      "rating": "4.5",
      "reviews": 1234,
      "image": "https://...",
      "url": "https://amazon.com/...?tag=affiliate-20"
    }
  ]
}
```

## Data Flow

```
User Input → GitHub Actions → RapidAPI → Amazon Data
     ↓                              ↓
Workflow Params              Product Info (top 10)
     ↓                              ↓
Environment Variables        Transformed Data + Affiliate Links
     ↓                              ↓
fill-template.js  ←─────────────────┘
     ↓
filled.json
     ↓
Renamed to slug.json → _data/
     ↓
Post created → _posts/YYYY-MM-DD-slug.md
     ↓
Git commit & push
     ↓
GitHub Pages builds site
     ↓
Jekyll processes template + data
     ↓
Published HTML page
```

## Security Architecture

```
┌─────────────────────────────────────────┐
│        GitHub Secrets (Encrypted)        │
│  • RAPIDAPI_KEY                         │
│  • AMAZON_AFFILIATE_ID                  │
└───────────────┬─────────────────────────┘
                │ (Injected at runtime)
                ▼
┌─────────────────────────────────────────┐
│      GitHub Actions Environment         │
│  Environment Variables (Temporary)      │
│  • RAPID_KEY                            │
│  • AMAZON_AFFILIATE_ID                  │
│  • TITLE, SLUG, NICHE, SEARCH_QUERY     │
└───────────────┬─────────────────────────┘
                │ (Used by script)
                ▼
┌─────────────────────────────────────────┐
│       fill-template.js Process          │
│  Uses secrets only for API calls        │
│  Never logs or exposes secrets          │
└───────────────┬─────────────────────────┘
                │ (Data only)
                ▼
┌─────────────────────────────────────────┐
│         Output (Public)                 │
│  • Product data (safe)                  │
│  • Affiliate links (public)             │
│  • No secrets in output                 │
└─────────────────────────────────────────┘
```

## Technology Stack

- **CI/CD**: GitHub Actions
- **Static Site Generator**: Jekyll 4.3
- **Templating**: Liquid
- **Languages**: 
  - Node.js (data fetching)
  - Ruby (Jekyll)
  - HTML/CSS (templates)
  - YAML (configuration)
- **APIs**: Amazon23 via RapidAPI
- **Hosting**: GitHub Pages
- **Dependencies**:
  - axios (HTTP client)
  - mustache (templating - installed but optional)

## File Relationships

```
_config.yml
    ├── Defines Jekyll settings
    └── Excludes .github/, node_modules/

index.html
    └── Lists all posts (generated sites)

_posts/YYYY-MM-DD-slug.md
    ├── References: data_file: slug
    └── Uses: layout: top10

_data/slug.json
    └── Contains product data

_layouts/top10.html
    ├── Reads: site.data[page.data_file]
    └── Renders: Product cards with data

.github/workflows/generate-site.yml
    └── Runs: .github/scripts/fill-template.js

.github/workflows/deploy-pages.yml
    └── Builds Jekyll site and deploys
```

## Scalability Considerations

- **Multiple Sites**: Can generate unlimited sites in same repo
- **API Rate Limits**: RapidAPI free tier limits apply
- **Build Time**: Jekyll builds in ~1-2 minutes per deployment
- **Storage**: GitHub repo size limits (soft 1GB, hard 100GB)
- **Bandwidth**: GitHub Pages bandwidth limits apply

## Extension Points

1. **Custom Templates**: Modify `_layouts/top10.html`
2. **Different APIs**: Update `fill-template.js` to use other APIs
3. **Additional Data**: Extend JSON structure in script
4. **Styling**: Add custom CSS in template
5. **Analytics**: Add tracking scripts to template
6. **SEO**: Add metadata in frontmatter and template

---

This architecture provides a maintainable, scalable solution for automated product review site generation.

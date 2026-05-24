# GreenFix Exterior Care - Netlify Deployment

## Files Included for Netlify Deployment

### 1. `netlify.toml`
- **Purpose**: Main Netlify configuration file
- **Contains**: 
  - Build settings (no build command needed - static site)
  - Redirect rules for proper routing
  - Security headers (X-Content-Type-Options, X-Frame-Options, XSS Protection, etc.)
  - Cache control headers for optimal performance

### 2. `_redirects`
- **Purpose**: Alternative redirect configuration
- **Contains**: Rules to serve index.html for all routes

### 3. `_headers`
- **Purpose**: Custom HTTP headers
- **Contains**: Security and cache control headers

### 4. `.gitignore`
- **Purpose**: Tells Git which files to ignore
- **Contains**: OS files, IDE files, dependency folders, build outputs

---

## Deployment Instructions

### Option 1: Deploy via GitHub (Recommended)

1. **Create a GitHub Repository**
   - Go to github.com and create a new repository named `greenfix-website`
   - Clone it to your computer

2. **Add Your Files**
   - Copy all files from your `greenfix website` folder to the GitHub folder
   - Include: All `.html` files, `.png` images, `netlify.toml`, `_redirects`, `.gitignore`

3. **Push to GitHub**
   ```
   git add .
   git commit -m "Initial commit: GreenFix website"
   git push origin main
   ```

4. **Connect to Netlify**
   - Go to netlify.com (sign up if needed)
   - Click "New site from Git"
   - Select GitHub and authorize
   - Choose your `greenfix-website` repository
   - Netlify will detect `netlify.toml` automatically
   - Click "Deploy site"

### Option 2: Deploy via Drag & Drop

1. Go to netlify.com
2. Sign up/login
3. Drag and drop your entire `greenfix website` folder into Netlify
4. Site will deploy instantly

---

## After Deployment

### Custom Domain Setup
1. Go to Site Settings → Domain management
2. Add your custom domain (e.g., greenfixexterior-care.co.uk)
3. Update DNS records as instructed by Netlify

### Form Submissions (Netlify Forms)
- Your quote form will automatically work after deployment
- Form submissions appear in Netlify dashboard under "Forms"

### Analytics
- Enable Netlify Analytics in site settings to track visits

### SSL Certificate
- Automatically included with Netlify (HTTPS enabled by default)

---

## File Structure Expected by Netlify

```
greenfix website/
├── index.html
├── netlify.toml                    ← Configuration file
├── _redirects                      ← Redirect rules
├── .gitignore                      ← Git ignore file
├── Screenshot 2026-05-16 154245.png
├── ChatGPT Image May 16, 2026, 03_41_48 PM.png
├── grass-cutting-preston.html
├── garden-maintenance-preston.html
├── gutter-clearing-preston.html
├── garden-clearance-preston.html
├── jet-washing-preston.html
├── fence-repairs-preston.html
├── letting-agent-services.html
├── estate-agent-services.html
├── commercial-maintenance.html
├── garden-maintenance-penwortham.html
├── garden-maintenance-leyland.html
├── garden-maintenance-chorley.html
├── garden-clearance-penwortham.html
└── garden-clearance-leyland.html
```

---

## Important Notes

✅ **Static Site** - No build process required
✅ **Forms Enabled** - Netlify Forms integrated in quote form
✅ **Security Headers** - Configured in netlify.toml
✅ **Performance** - Cache headers optimized for images and HTML
✅ **Mobile Ready** - Responsive design included

All files are ready for immediate deployment!

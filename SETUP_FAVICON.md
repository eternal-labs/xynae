# Setting Up Favicon & Social Preview

## Quick Setup Guide

### Step 1: Add Your PNG Files

Place your PNG files in the `assets/images/` directory:

1. **`logo.png`** - Main logo for README
   - Recommended size: 200x200px or larger (square format works best)
   - This will appear at the top of your README

2. **`social-preview.png`** - Social preview for GitHub
   - **Required size: 1200x630px** (GitHub's standard size)
   - This appears when sharing your repository link

3. **`favicon.png`** - Favicon
   - Recommended: 32x32px or 64x64px
   - Optional: Convert to `.ico` format for web usage

### Step 2: Social Preview Image (GitHub Repository Image)

The social preview image is the image that appears when sharing your repository link on social media.

**Steps:**
1. Go to: https://github.com/eternal-labs/xynae/settings
2. Scroll down to **"Social preview"** section
3. Click **"Upload an image"**
4. Upload `assets/images/social-preview.png` (must be 1200x630px PNG)

### Step 3: Repository Logo in README

Once you add `logo.png` to `assets/images/`, it will automatically display in the README when you commit and push.

### Step 4: Optional - Convert Favicon to .ico

If you want a `.ico` file for web usage:

1. Use [favicon.io](https://favicon.io/) or [RealFaviconGenerator](https://realfavicongenerator.net/)
2. Upload your `favicon.png`
3. Download the generated `favicon.ico`
4. Place in root directory or `assets/images/`

### File Structure

```
assets/
└── images/
    ├── logo.png          ← Your logo (200x200px recommended)
    ├── social-preview.png ← Your social preview (1200x630px required)
    └── favicon.png       ← Your favicon (32x32px or 64x64px recommended)
```

### Current Status

⚠️ **Add your PNG files:**
- [ ] `assets/images/logo.png` - Logo for README
- [ ] `assets/images/social-preview.png` - Social preview (1200x630px)
- [ ] `assets/images/favicon.png` - Favicon

### Need Help?

- [GitHub Docs: Social Previews](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [GitHub Settings: Social Preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/configuring-the-default-about-page)


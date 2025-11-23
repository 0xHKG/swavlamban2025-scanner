# PWA Icons Guide

This app requires 3 icon sizes for proper PWA functionality:

## Required Icons

1. **icon-192.png** (192x192 pixels)
   - Standard PWA icon
   - Used on Android home screen

2. **icon-512.png** (512x512 pixels)
   - High-resolution PWA icon
   - Used for splash screens

3. **apple-touch-icon.png** (180x180 pixels)
   - iOS home screen icon
   - Apple-specific format

---

## Icon Design Specifications

**Theme**: Indian Navy - Swavlamban 2025 Event

**Design Elements**:
- Primary Color: Navy Blue (#1f2937)
- Accent: Gold/Yellow (#f59e0b)
- Icon: QR Code symbol or Scanner camera icon
- Text: "Scanner" or "S2025" (optional)

**Style**:
- Simple, recognizable at small sizes
- High contrast for visibility
- Professional military/government aesthetic

---

## Quick Icon Generation Methods

### Method 1: Using Figma/Canva (Recommended)
1. Create a 512x512 canvas
2. Add Navy Blue background (#1f2937)
3. Add white/gold QR code icon or scanner symbol
4. Add "Swavlamban 2025" or "Scanner" text
5. Export as PNG at 512x512, 192x192, and 180x180

### Method 2: Using Online Icon Generators
- **RealFaviconGenerator**: https://realfavicongenerator.net/
- **Favicon.io**: https://favicon.io/
- Upload a base design, auto-generate all sizes

### Method 3: Using ImageMagick (Command Line)
```bash
# Create from SVG or PNG source
convert source.png -resize 192x192 icon-192.png
convert source.png -resize 512x512 icon-512.png
convert source.png -resize 180x180 apple-touch-icon.png
```

### Method 4: Placeholder for Testing
For development/testing, use simple solid color icons:
```bash
# Create solid color placeholders
convert -size 192x192 xc:'#1f2937' icon-192.png
convert -size 512x512 xc:'#1f2937' icon-512.png
convert -size 180x180 xc:'#1f2937' apple-touch-icon.png
```

---

## Temporary Placeholder

**Current Status**: Using placeholder SVG (icon-template.svg)

**To Use**:
1. Open `icon-template.svg` in browser
2. Take screenshot
3. Crop and resize to required dimensions
4. Save as PNG files

**Or**: Copy existing Navy logo/QR scanner icon from main project

---

## Icon Checklist

- [ ] icon-192.png created
- [ ] icon-512.png created
- [ ] apple-touch-icon.png created
- [ ] Icons tested in browser
- [ ] Icons display correctly on mobile

---

**Note**: The app will work without custom icons (browser will use default), but custom icons greatly improve the professional appearance and user experience.

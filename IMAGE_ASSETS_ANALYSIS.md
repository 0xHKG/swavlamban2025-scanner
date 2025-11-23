# Swavlamban 2024 - Image Assets Analysis

## Summary of Current Design Assets

### 1. Homepage Logo (`logo.png`)

**Current Version (2024)**
- **File**: logo.png
- **Size**: 2000 x 1428 pixels (6MB)
- **Format**: PNG (high-resolution for print/digital)

**Visual Design Elements**:
- **Title Text**: "SWAYAM LAMBAN" (large, white, sans-serif font)
- **Subtitle**: "2024" in yellow/gold color
- **Background**: Blue gradient with digital/tech patterns
- **Military Equipment**:
  - Fighter jet on left
  - Tank in center
  - Spacecraft/satellite on right
- **Design Style**: Futuristic, military/defense technology theme
- **Network Graphics**: Lines, dots, radar-like patterns

**Color Palette**:
```
Primary: #0D47A1 (Navy Blue) - Background
Accent: #FFD700 (Gold/Yellow) - Year text
Text: #FFFFFF (White) - Main title
Equipment: #808080 (Gray) - Military hardware
```

**Required Changes for 2025**:
- [ ] Update "2024" → "2025"
- [ ] Consider refreshing military equipment imagery (if new tech showcased)
- [ ] Ensure Indian Navy emblem is prominent
- [ ] Maintain overall theme and color scheme

---

## 2. Entry Pass Templates

### Template 1: October 28 Pass (`28.png`)

**Specifications**:
- **Dimensions**: 1280 x 526 pixels (landscape)
- **File Size**: 103 KB
- **Format**: JPEG (note: filename says .png but file is JPEG)

**QR Code Configuration**:
```python
position: {
    x: 60px,  # left margin
    y: (526 - 220) / 2  # vertically centered
}
size: 220 x 220 pixels
colors: {
    foreground: "#8B4513",  # Brown
    background: "#F5DEB3"   # Beige/Wheat
}
```

**Required Updates**:
- [ ] Change "28 Oct 24" → "28 Oct 25" (or actual date)
- [ ] Update any year references
- [ ] Verify event details are current

---

### Template 2: Interactive Session Pass (`AM29.png`)

**Specifications**:
- **Dimensions**: 2000 x 826 pixels (landscape)
- **File Size**: 827 KB
- **Format**: PNG with RGBA (transparent background)

**QR Code Configuration**:
```python
position: {
    x: 60px,  # left margin
    y: (826 - 400) / 2  # vertically centered
}
size: 400 x 400 pixels
colors: {
    foreground: "#1D4E89",  # Navy Blue
    background: "#D3D3D3"   # Light Gray
}
```

**Required Updates**:
- [ ] Change "Interactive Session - 29 Oct 24" → "29 Oct 25"
- [ ] Update session timings if changed
- [ ] Verify venue details

---

### Template 3: Plenary Session Pass (`PM29.png`)

**Specifications**:
- **Dimensions**: 2000 x 826 pixels (landscape)
- **File Size**: 1.2 MB
- **Format**: PNG with RGBA (transparent background)

**QR Code Configuration**:
```python
position: {
    x: 60px,  # left margin
    y: (826 - 400) / 2  # vertically centered
}
size: 400 x 400 pixels
colors: {
    foreground: "#8B4513",  # Brown
    background: "#FFFFFF"   # White
}
```

**Required Updates**:
- [ ] Change "Plenary Session - 29 Oct 24" → "29 Oct 25"
- [ ] Update session timings if changed
- [ ] Verify venue details

---

## 3. Supporting Documents (Email Attachments)

### Event Guidelines

**DND (DOs & DON'Ts) Documents**:
1. `DND-28.png` (2000 x 1428, 2.6MB) - Guidelines for Day 1
2. `DND-Forenoon.png` (2000 x 1428, 1.8MB) - Morning session rules
3. `DND-Plenary.png` (2000 x 1428, 2.7MB) - Plenary session rules

**Event Flow Documents**:
1. `EF-AM29.png` (2000 x 1428, 1.6MB) - Morning session schedule
2. `EF-PM29.png` (2000 x 1428, 2.3MB) - Afternoon session schedule

**Required Updates**:
- [ ] Update all dates from 2024 to 2025
- [ ] Review and update event schedules
- [ ] Update speaker names if changed
- [ ] Verify venue and timings

---

## Design Consistency Guidelines

### Typography
- **Main Titles**: Sans-serif, bold, large
- **Subtitles**: Sans-serif, medium weight
- **Body Text**: Readable sans-serif at appropriate sizes

### Color Scheme (Indian Navy Theme)
```
Navy Blue:     #0D47A1  (Primary)
Gold/Yellow:   #FFD700  (Accent)
White:         #FFFFFF  (Text/Contrast)
Light Gray:    #D3D3D3  (Backgrounds)
Brown:         #8B4513  (Secondary accent)
```

### Logo Requirements
- Indian Navy emblem (mandatory)
- Government of India emblem
- NIIO logo
- Event sponsors (if applicable)

### QR Code Standards
- **Minimum Size**: 220x220 pixels for quick scanning
- **Quiet Zone**: 5 pixels border
- **Error Correction**: High (30% recovery)
- **Color Contrast**: Minimum 3:1 ratio for accessibility

---

## Technical Specifications for Designers

### Logo File (`logo.png`)
```
Input Requirements:
- Format: PNG (with transparency) or high-res JPEG
- Resolution: 2000 x 1428 pixels minimum
- DPI: 300 for print, 72 for digital
- Color Space: RGB for digital, CMYK for print
- File Size: Under 10MB
```

### Pass Templates
```
Input Requirements:
- Format: PNG with RGBA (transparency support)
- Dimensions:
  * Oct 28 pass: 1280 x 526 pixels
  * Oct 29 passes: 2000 x 826 pixels
- QR Code Area: Reserve 60px from left edge
- Safe Zone: Keep important text 50px from edges
- File Size: Under 2MB per template
```

### Design Elements to Preserve
- QR code positioning (left side, vertically centered)
- Overall layout structure
- Color-coding for different pass types
- Indian Navy branding elements
- Futuristic/tech aesthetic

### New Elements to Consider
- **Photo Space**: 150x150px area for attendee photo (top-right?)
- **Holographic Effect**: Gradient overlay for security
- **Barcode**: Additional backup scanning method
- **NFC Chip Icon**: If using NFC technology

---

## File Naming Convention (2025)

### Recommended Structure
```
logo_swavlamban_2025.png
pass_template_28oct2025.png
pass_template_interactive_29oct2025.png
pass_template_plenary_29oct2025.png
guidelines_dnd_28oct2025.png
guidelines_dnd_forenoon_29oct2025.png
guidelines_dnd_plenary_29oct2025.png
event_flow_morning_29oct2025.png
event_flow_afternoon_29oct2025.png
```

---

## Accessibility Requirements

### Color Contrast
- Text on backgrounds: Minimum 4.5:1 ratio
- Large text (18pt+): Minimum 3:1 ratio
- QR codes: High contrast for all scanning conditions

### Font Sizes
- Main titles: 48pt minimum
- Subtitles: 24pt minimum
- Body text: 14pt minimum
- Small print: 10pt minimum (legal text only)

### Readability
- Sans-serif fonts for clarity
- No decorative fonts for critical info
- High contrast for text
- Clear hierarchy

---

## Design Review Checklist

Before finalizing 2025 assets:

**Logo**:
- [ ] Year updated to 2025
- [ ] All emblems present and correct
- [ ] Colors match brand guidelines
- [ ] High-resolution (300 DPI for print)
- [ ] Transparent background version available
- [ ] File size optimized

**Pass Templates**:
- [ ] All dates updated to 2025
- [ ] QR code placement verified
- [ ] Color contrast meets standards
- [ ] Text is readable at actual size
- [ ] No spelling/grammar errors
- [ ] File format is PNG with transparency
- [ ] Templates tested with actual QR codes

**Supporting Documents**:
- [ ] All dates and timings updated
- [ ] Speaker/guest names verified
- [ ] Venue information correct
- [ ] Contact information updated
- [ ] File sizes optimized for email

---

## Assets Delivery Format

### For Development Team
```
/assets/
  /2025/
    /templates/
      logo.png
      pass_28oct.png
      pass_interactive_29oct.png
      pass_plenary_29oct.png
    /guidelines/
      dnd_28oct.png
      dnd_forenoon_29oct.png
      dnd_plenary_29oct.png
    /schedules/
      event_flow_morning.png
      event_flow_afternoon.png
    /source/
      [Editable source files: .ai, .psd, .sketch]
```

### Documentation Required
- Design brief with color codes
- Font specifications
- Logo usage guidelines
- Brand style guide

---

## Notes for Graphic Designer

1. **Consistency**: Maintain visual continuity with 2024 design
2. **Branding**: Indian Navy + Government of India branding is mandatory
3. **Security**: Consider anti-forgery elements (gradients, patterns)
4. **Scalability**: All assets must work at multiple sizes
5. **Formats**: Provide both print-ready (CMYK, 300 DPI) and web-optimized (RGB, 72 DPI) versions
6. **Source Files**: Deliver editable source files (.ai, .psd, .sketch) for future updates

---

## Timeline for Design Updates

**Week 1**: Design brief and date confirmation
**Week 2**: Logo update and pass template mockups
**Week 3**: Review and revisions
**Week 4**: Final delivery and integration testing

---

## Contact Points

For design-related questions:
- Technical specs: Development Team
- Brand guidelines: Indian Navy PR/Marketing
- Event details: Swavlamban Organizing Committee
- Printing requirements: Vendor specifications

---

*This document serves as a comprehensive guide for updating all visual assets for Swavlamban 2025.*

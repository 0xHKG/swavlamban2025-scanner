# ⚠️ CRITICAL: DND Images - Dos and Don'ts for Venue

**Last Updated**: 2025-10-19
**Status**: ⚠️ PLACEHOLDER FILES - MUST BE REPLACED BEFORE PRODUCTION

---

## 🔴 IMPORTANT REQUIREMENT

### DND = **Dos and Don'ts** (Venue Guidelines)

The `/images/DND/` folder contains **venue guideline images** showing dos and don'ts for attendees at different venues/sessions. These are currently **PLACEHOLDER images** that will be updated later with actual content.

---

## 📁 DND Folder Contents

Current files (4 images):

| # | Filename | Size | Purpose | Status |
|---|----------|------|---------|--------|
| 1 | `DND_Exhibition_25.png` | 2000 x 1428 | Dos/Don'ts for Exhibition (Day 1) | ⚠️ Placeholder |
| 2 | `DND_Exhibition_26.png` | 2000 x 1428 | Dos/Don'ts for Exhibition (Day 2) | ⚠️ Placeholder |
| 3 | `DND_interactive.png` | 2000 x 1428 | Dos/Don'ts for Panel Discussions | ⚠️ Placeholder |
| 4 | `DND_Plenary.png` | 2000 x 1428 | Dos/Don'ts for Plenary Session | ⚠️ Placeholder |

---

## 🚨 CRITICAL DEVELOPMENT REQUIREMENT

### ✅ MUST DO:

**Use these EXACT filenames in the code** - hardcode the filenames, do NOT change them!

```python
# Example - Email attachment code
DND_FILES = {
    'exhibition_day1': 'images/DND/DND_Exhibition_25.png',
    'exhibition_day2': 'images/DND/DND_Exhibition_26.png',
    'interactive': 'images/DND/DND_interactive.png',
    'plenary': 'images/DND/DND_Plenary.png'
}
```

### ⚠️ WHY:

User will **replace these files later** with actual content (updated venue dos/don'ts). By keeping the filenames constant in the code, user can simply:
1. Create new DND images with proper content
2. Replace the files with **same filenames**
3. **No code changes needed** - images automatically update

### ❌ DO NOT:

- ❌ Do NOT rename these files in code
- ❌ Do NOT use dynamic/generated filenames
- ❌ Do NOT reference by timestamp or version numbers
- ❌ Do NOT skip these in email attachments

---

## 📧 Email Attachment Mapping

### Email 1: Exhibition Day 1 Pass
**Attachments:**
- EP-25.png (pass with QR code)
- EF-25.png (Event Flow)
- **DND_Exhibition_25.png** ⚠️ Dos/Don'ts for Exhibition Hall
- Guidelines PDF
- Venue map

### Email 2: Exhibition Day 2 Pass
**Attachments:**
- EP-26.png (pass with QR code)
- EF-AM26.png (Event Flow AM)
- EF-PM26.png (Event Flow PM)
- **DND_Exhibition_26.png** ⚠️ Dos/Don'ts for Exhibition Hall
- Guidelines PDF
- Venue map

### Email 3: Exhibitor Pass (Both Days)
**Attachments:**
- EP-25n26.png (pass with QR code)
- EF-25.png, EF-AM26.png, EF-PM26.png
- **DND_Exhibition_25.png** ⚠️ Day 1 dos/don'ts
- **DND_Exhibition_26.png** ⚠️ Day 2 dos/don'ts
- Exhibitor guidelines
- Venue map

### Email 4: Interactive Sessions Pass
**Attachments:**
- EP-INTERACTIVE.png (pass with QR code)
- EF-AM26.png (Panel schedule)
- **DND_interactive.png** ⚠️ Dos/Don'ts for Zorawar Hall (Panel Discussions)
- Session guidelines
- Venue map

### Email 5: Plenary Session Pass
**Attachments:**
- EP-PLENARY.png (pass with QR code)
- EF-PM26.png (Plenary schedule)
- **DND_Plenary.png** ⚠️ Dos/Don'ts for Zorawar Hall (VIP Plenary)
- VIP guidelines
- Venue map

---

## 📝 What Should DND Images Contain?

**Expected Content (User to create later):**

### Exhibition Hall Dos/Don'ts:
- ✅ DO: Register at entry
- ✅ DO: Wear your pass visibly
- ✅ DO: Respect booth personnel
- ✅ DO: Take promotional materials
- ❌ DON'T: Touch displays without permission
- ❌ DON'T: Block walkways
- ❌ DON'T: Take photos without permission
- ❌ DON'T: Enter restricted areas

### Zorawar Hall (Panel Discussions) Dos/Don'ts:
- ✅ DO: Arrive 10 minutes early
- ✅ DO: Silent your mobile phones
- ✅ DO: Ask questions during Q&A only
- ✅ DO: Respect speakers
- ❌ DON'T: Enter late (disturbs session)
- ❌ DON'T: Leave during presentations
- ❌ DON'T: Record without permission
- ❌ DON'T: Talk during sessions

### Zorawar Hall (Plenary Session) Dos/Don'ts:
- ✅ DO: Be seated by 1620 hrs (before session starts)
- ✅ DO: Formal dress code mandatory
- ✅ DO: Follow security protocols
- ✅ DO: Stand for national anthem
- ❌ DON'T: Use mobile phones during session
- ❌ DON'T: Leave during Hon'ble RM address
- ❌ DON'T: Take photos/videos
- ❌ DON'T: Casual dress (formal required)

**Design Format:**
- Visual infographic style
- Icons for each do/don't
- Clear ✅ green checkmarks and ❌ red X marks
- Indian Navy branding
- Same decorative style as other event materials
- Size: 2000 x 1428 pixels (current standard)

---

## 🔧 Code Implementation Example

### Python (Backend - Email Service)

```python
import os

# CRITICAL: Use EXACT filenames - DO NOT CHANGE
DND_IMAGE_PATHS = {
    'exhibition_day1': 'images/DND/DND_Exhibition_25.png',
    'exhibition_day2': 'images/DND/DND_Exhibition_26.png',
    'interactive': 'images/DND/DND_interactive.png',
    'plenary': 'images/DND/DND_Plenary.png'
}

def get_email_attachments(pass_type):
    """
    Get list of attachments for email based on pass type
    """
    attachments = []

    if pass_type == 'exhibition_day1':
        attachments.append(DND_IMAGE_PATHS['exhibition_day1'])
    elif pass_type == 'exhibition_day2':
        attachments.append(DND_IMAGE_PATHS['exhibition_day2'])
    elif pass_type == 'exhibitor_both_days':
        attachments.append(DND_IMAGE_PATHS['exhibition_day1'])
        attachments.append(DND_IMAGE_PATHS['exhibition_day2'])
    elif pass_type == 'interactive':
        attachments.append(DND_IMAGE_PATHS['interactive'])
    elif pass_type == 'plenary':
        attachments.append(DND_IMAGE_PATHS['plenary'])

    return attachments

def send_pass_email(entry_id, pass_type):
    """
    Send email with pass and DND attachments
    """
    # Get pass image with QR code
    pass_image = generate_pass_with_qr(entry_id, pass_type)

    # Get DND images
    dnd_attachments = get_email_attachments(pass_type)

    # Check if DND files exist (they should, even if placeholders)
    for dnd_file in dnd_attachments:
        if not os.path.exists(dnd_file):
            logger.warning(f"DND file not found: {dnd_file}")
            # Continue anyway - user will replace later

    # Send email with attachments
    send_email(
        to=entry.email,
        subject=f"Swavlamban 2025 - {pass_type} Pass",
        attachments=[pass_image] + dnd_attachments + [event_flow, guidelines]
    )
```

### Configuration File (config.py)

```python
# DND Images Configuration
# CRITICAL: These filenames are FIXED - user will replace image content later
# DO NOT change these paths in code!

DND_IMAGES = {
    # Exhibition Hall Dos/Don'ts
    'EXHIBITION_DAY1': 'images/DND/DND_Exhibition_25.png',
    'EXHIBITION_DAY2': 'images/DND/DND_Exhibition_26.png',

    # Zorawar Hall Dos/Don'ts
    'INTERACTIVE_SESSIONS': 'images/DND/DND_interactive.png',
    'PLENARY_SESSION': 'images/DND/DND_Plenary.png'
}

# NOTE: Current DND images are placeholders
# User will update with actual venue dos/don'ts guidelines later
# Code should work with both placeholder and final images
```

---

## ✅ Development Checklist

### Code Requirements:

- [ ] Hardcode exact DND filenames in email service
- [ ] Add DND images as email attachments per pass type
- [ ] Add file existence check (warn if missing, but continue)
- [ ] Document DND image paths in configuration
- [ ] Add comments in code: "DND = Dos/Don'ts, will be replaced by user"
- [ ] Test email delivery with placeholder DND images
- [ ] Verify attachments appear correctly in received emails

### Documentation Requirements:

- [x] Document DND = Dos and Don'ts (venue guidelines)
- [x] List all 4 DND filenames
- [x] Specify exact filenames to use in code
- [x] Map DND images to pass types
- [x] Create code examples
- [x] Add warning about placeholder status

### Testing Requirements:

- [ ] Test emails include DND attachments
- [ ] Verify DND images are readable when attached
- [ ] Test with placeholder images (current)
- [ ] After user updates: Test with final images (no code changes needed)

---

## 🔄 Future Update Process

### When User Updates DND Images:

1. **User creates new DND images** with actual venue dos/don'ts content
2. **User saves with EXACT same filenames**:
   - `DND_Exhibition_25.png`
   - `DND_Exhibition_26.png`
   - `DND_interactive.png`
   - `DND_Plenary.png`
3. **User replaces files** in `/images/DND/` folder
4. **✅ No code changes needed** - system automatically uses new images
5. **New registrations** get updated DND images in emails
6. **Existing attendees** can be re-sent emails if needed

### Advantages of This Approach:

- ✅ Clean separation: content vs code
- ✅ User can update images independently
- ✅ No developer needed for image updates
- ✅ No redeployment required
- ✅ Maintains consistent filenames throughout system
- ✅ Easy to version control (Git tracks file changes)

---

## 📏 Technical Specifications

### Current DND Images (Placeholders):

| Property | Value |
|----------|-------|
| Format | PNG, 8-bit RGB |
| Dimensions | 2000 x 1428 pixels |
| Color Mode | Non-interlaced |
| File Size | ~2.6-2.7 MB each |

**Recommendation**: Keep same specifications for final images
- **Size**: 2000 x 1428 px (matches Event Flow documents)
- **Format**: PNG (good for graphics with text)
- **Quality**: High-res for readability when printed/viewed on mobile

---

## 📋 Summary

**DND Images Status:**

| Aspect | Current State | Final State |
|--------|---------------|-------------|
| **Purpose** | Venue Dos/Don'ts Guidelines | Same |
| **Count** | 4 files | 4 files |
| **Filenames** | Fixed | ✅ SAME (do not change!) |
| **Content** | ⚠️ Placeholder | To be updated by user |
| **Dimensions** | 2000 x 1428 | ✅ Keep same |
| **In Code** | Hardcoded paths | ✅ SAME (do not change!) |
| **Email Use** | Attached per pass type | Same |

**Development Action:**
✅ **Use exact filenames in code** - user will replace image content later

**User Action Later:**
⏳ Create actual venue dos/don'ts content and replace files with same names

---

## 🚨 CRITICAL REMINDER

### ⚠️ TO DEVELOPERS:

**DO NOT:**
- ❌ Remove or rename DND image files
- ❌ Change DND paths in code
- ❌ Make DND filenames dynamic
- ❌ Skip DND attachments in emails

**DO:**
- ✅ Hardcode exact filenames shown above
- ✅ Include DND images in email attachments
- ✅ Add code comments about placeholder status
- ✅ Test with current placeholder images
- ✅ Document that user will update later

### ⚠️ TO USER:

**REMEMBER:**
- ⏳ DND images are placeholders - need actual venue dos/don'ts
- ✅ Keep same filenames when replacing
- ✅ Keep same dimensions (2000 x 1428)
- ✅ Replace all 4 files before production launch

---

**Document Version**: 1.0
**Date**: 2025-10-19
**Status**: ⚠️ Critical requirement documented
**Action Required**: User to create actual DND content later
**Code Requirement**: Hardcode these exact filenames - DO NOT CHANGE

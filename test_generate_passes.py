#!/usr/bin/env python3
"""
Test script to generate passes with test data for QR code verification
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.services.pass_generator import PassGenerator
from app.models.entry import Entry

def create_test_entry():
    """Create a test entry object"""
    # Create a mock Entry object (not saving to DB)
    entry = Entry(
        id=999,  # Test ID
        username="admin",
        name="Abhishek Vardhan",
        phone="9999999999",
        email="abhishekvardhan86@gmail.com",
        id_type="Aadhar",
        id_number="111122223333",  # Will be formatted as 1111-2222-3333
        photo_url=None,
        # Enable all 4 event passes (not exhibitor pass)
        exhibition_day1=True,
        exhibition_day2=True,
        interactive_sessions=True,
        plenary=True
    )
    return entry

def main():
    print("=" * 60)
    print("TEST PASS GENERATION - QR Code Verification")
    print("=" * 60)
    print()
    print("Test Data:")
    print("  Name: Abhishek Vardhan")
    print("  ID Type: Aadhar")
    print("  ID No: 1111-2222-3333")
    print()
    print("Generating 4 event passes...")
    print("-" * 60)

    # Create test entry
    entry = create_test_entry()

    # Initialize pass generator
    generator = PassGenerator()

    # Determine which passes to generate
    passes_to_generate = []

    if entry.exhibition_day1:
        passes_to_generate.append(("exhibition_day1", "EP-25.png"))
    if entry.exhibition_day2:
        passes_to_generate.append(("exhibition_day2", "EP-26.png"))
    if entry.interactive_sessions:
        passes_to_generate.append(("interactive_sessions", "EP-INTERACTIVE.png"))
    if entry.plenary:
        passes_to_generate.append(("plenary", "EP-PLENARY.png"))

    # Generate each pass
    generated_files = []

    for pass_type, template_filename in passes_to_generate:
        print(f"\n📄 Generating: {template_filename}")

        # Get template path
        template_path = generator.passes_dir / template_filename

        if not template_path.exists():
            print(f"   ❌ Template not found: {template_path}")
            continue

        # Generate QR data
        qr_data = generator.generate_qr_data(entry, pass_type, "admin")
        print(f"   QR Data Preview:")
        print("   " + "\n   ".join(qr_data.split("\n")[:7]))

        # Create QR image
        qr_img = generator.create_qr_image(qr_data, pass_type, template_filename)

        # Output filename
        safe_name = entry.name.replace(" ", "_")
        output_filename = f"TEST_{safe_name}_{pass_type}.png"
        output_path = generator.output_dir / output_filename

        # Overlay QR on pass
        generator.overlay_qr_on_pass(template_path, qr_img, output_path, template_filename)

        generated_files.append(output_path)
        print(f"   ✅ Generated: {output_path.name}")
        print(f"   📍 Location: {output_path}")

    print()
    print("=" * 60)
    print("GENERATION COMPLETE!")
    print("=" * 60)
    print()
    print(f"✅ Generated {len(generated_files)} passes:")
    for file in generated_files:
        print(f"   - {file.name}")
    print()
    print(f"📂 Output directory: {generator.output_dir}")
    print()
    print("🔍 Next Steps:")
    print("   1. Check QR code color on each pass")
    print("   2. Verify QR code placement (60px from left, vertically centered)")
    print("   3. Scan QR codes to verify data readability")
    print()

if __name__ == "__main__":
    main()

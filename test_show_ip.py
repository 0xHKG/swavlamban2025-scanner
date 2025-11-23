"""
Show the public IP address that this server is using
This will help us whitelist Streamlit Cloud's IP in NIC Mail
"""

import requests

print("=" * 70)
print("IP ADDRESS DETECTOR - For NIC Mail Whitelisting")
print("=" * 70)
print()

try:
    # Get public IP address
    response = requests.get('https://api.ipify.org?format=json', timeout=10)
    ip_data = response.json()
    public_ip = ip_data['ip']

    print(f"✅ Public IP Address: {public_ip}")
    print()
    print("INSTRUCTIONS:")
    print("1. Copy this IP address")
    print("2. Go to NIC Mail security settings")
    print("3. Click 'Add Allowed IP Address'")
    print("4. Select 'Add static IP address'")
    print(f"5. Enter: {public_ip}")
    print("6. Save the settings")
    print()
    print("After whitelisting, NIC SMTP authentication will work!")
    print("=" * 70)

except Exception as e:
    print(f"❌ Error getting IP: {e}")
    print()
    print("Alternative method:")
    print("Deploy the app to Streamlit Cloud with this code included,")
    print("and it will display the IP address you need to whitelist.")

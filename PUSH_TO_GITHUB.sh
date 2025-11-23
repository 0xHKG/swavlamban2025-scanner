#!/bin/bash
# Swavlamban 2025 - Push to GitHub
# This script pushes all commits to GitHub

echo "🚀 Pushing Swavlamban 2025 to GitHub..."
echo ""
echo "Current directory: $(pwd)"
echo "Git status:"
git status
echo ""
echo "Commits to push:"
git log origin/main..HEAD --oneline
echo ""
echo "Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Code pushed to GitHub"
    echo ""
    echo "Next steps:"
    echo "1. Go to Streamlit Cloud: https://share.streamlit.io/"
    echo "2. Wait for auto-deployment (2-5 minutes)"
    echo "3. Add Supabase password to secrets"
    echo "4. Reboot app"
    echo ""
    echo "See DEPLOYMENT_READY.md for complete instructions."
else
    echo ""
    echo "❌ FAILED - Authentication required"
    echo ""
    echo "Use Personal Access Token:"
    echo "1. Go to: https://github.com/settings/tokens"
    echo "2. Generate new token (Classic)"
    echo "3. Select 'repo' scope"
    echo "4. Copy token"
    echo "5. Run: git push https://YOUR_TOKEN@github.com/YOUR_USERNAME/swavlamban2025.git main"
    echo ""
    echo "See DEPLOYMENT_READY.md for more help."
fi

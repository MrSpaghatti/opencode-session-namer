#!/bin/bash

set -e

echo "🚀 OpenCode Session Namer - GitHub Push Helper"
echo "=============================================="
echo ""

REPO_NAME="opencode-session-namer"
LOCAL_DIR="$(pwd)"
DEFAULT_REPO_URL="https://github.com/yourusername/$REPO_NAME.git"

echo "📁 Local repository: $LOCAL_DIR"
echo "📦 Repository name: $REPO_NAME"
echo ""

echo "🔧 Step 1: Create GitHub Repository"
echo "-----------------------------------"
echo ""
echo "1. Go to https://github.com/new"
echo "2. Set repository name: $REPO_NAME"
echo "3. Description: 'Intelligent session naming for OpenCode using local LLMs'"
echo "4. Choose Public or Private"
echo "5. DO NOT initialize with README, .gitignore, or license"
echo "6. Click 'Create repository'"
echo ""
echo "After creation, copy the repository URL (should look like:"
echo "  https://github.com/yourusername/$REPO_NAME.git"
echo "  or git@github.com:yourusername/$REPO_NAME.git)"
echo ""
read -p "📋 Paste your GitHub repository URL: " REPO_URL
REPO_URL=${REPO_URL:-$DEFAULT_REPO_URL}
echo ""

echo "🔧 Step 2: Add Remote and Push"
echo "------------------------------"
echo ""

git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"

if git branch | grep -q "master"; then
    git branch -M main
fi

if git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null; then
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🔗 Repository URL: $REPO_URL"
else
    echo "❌ Failed to push to GitHub."
    echo ""
    echo "📝 Manual push commands:"
    echo "  git remote add origin $REPO_URL"
    echo "  git branch -M main"
    echo "  git push -u origin main"
    echo ""
    echo "If using SSH instead of HTTPS:"
    echo "  git remote set-url origin git@github.com:yourusername/$REPO_NAME.git"
    echo "  git push -u origin main"
fi

echo ""
echo "🔧 Step 3: Verify"
echo "----------------"
echo ""
echo "Check your repository at:"
echo "  https://github.com/yourusername/$REPO_NAME"
echo ""
echo "✅ Setup complete!"
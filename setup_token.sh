#!/bin/bash

echo "🔑 Discord Bot Token Setup for Quotient"
echo "========================================"
echo ""

# Check if token is already set
if [ ! -z "$DISCORD_TOKEN" ] && [ "$DISCORD_TOKEN" != "your_discord_bot_token_here" ]; then
    echo "✅ DISCORD_TOKEN is already set!"
    echo "Current token: ${DISCORD_TOKEN:0:10}..."
    echo ""
    echo "To run the bot:"
    echo "  ./start_bot.sh"
    exit 0
fi

echo "📋 Instructions to get your Discord Bot Token:"
echo ""
echo "1. Go to: https://discord.com/developers/applications"
echo "2. Click 'New Application' (or select existing)"
echo "3. Give it a name (e.g., 'Quotient Bot')"
echo "4. Go to 'Bot' section in left sidebar"
echo "5. Click 'Add Bot' if not already added"
echo "6. Copy the token (click 'Copy' button)"
echo ""

read -p "🔑 Paste your Discord bot token here: " BOT_TOKEN

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ No token provided. Please run this script again."
    exit 1
fi

# Add to shell profile
SHELL_PROFILE=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_PROFILE="$HOME/.bashrc"
else
    SHELL_PROFILE="$HOME/.profile"
fi

# Check if already in profile
if grep -q "DISCORD_TOKEN" "$SHELL_PROFILE"; then
    echo "🔄 Updating existing DISCORD_TOKEN in $SHELL_PROFILE"
    # Remove old line and add new one
    sed -i.bak "/DISCORD_TOKEN/d" "$SHELL_PROFILE"
else
    echo "📝 Adding DISCORD_TOKEN to $SHELL_PROFILE"
fi

echo "export DISCORD_TOKEN='$BOT_TOKEN'" >> "$SHELL_PROFILE"

# Set for current session
export DISCORD_TOKEN="$BOT_TOKEN"

echo ""
echo "✅ Token set successfully!"
echo "🔄 Please restart your terminal or run: source $SHELL_PROFILE"
echo ""
echo "🚀 To run the bot:"
echo "  ./start_bot.sh"
echo ""
echo "🔒 Security note: Your token is now saved in $SHELL_PROFILE"
echo "   Never share this token publicly!"

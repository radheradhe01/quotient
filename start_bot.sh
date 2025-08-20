#!/bin/bash

# Quotient Bot Startup Script

echo "🚀 Starting Quotient Bot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run 'poetry install' first."
    exit 1
fi

# Check if PostgreSQL is running
if ! docker ps | grep -q "quotient-postgres"; then
    echo "📊 Starting PostgreSQL database..."
    docker-compose up postgres -d
    echo "⏳ Waiting for database to be ready..."
    sleep 10
fi

# Check if DISCORD_TOKEN is set
if [ -z "$DISCORD_TOKEN" ]; then
    echo "⚠️  DISCORD_TOKEN environment variable not set."
    echo "Please set it with: export DISCORD_TOKEN='your_bot_token_here'"
    echo ""
    echo "To get a bot token:"
    echo "1. Go to https://discord.com/developers/applications"
    echo "2. Create a new application or select existing one"
    echo "3. Go to 'Bot' section and copy the token"
    echo "4. Set the environment variable and run this script again"
    exit 1
fi

# Activate virtual environment and start bot
echo "🤖 Starting Quotient Bot..."
source venv/bin/activate
cd src
python bot.py

#!/usr/bin/env python3
"""
Quotient Bot - One-Command Setup Script
========================================

This script sets up the complete Quotient Discord bot application:
- Discord token configuration
- Database setup and initialization
- Environment configuration
- Service startup

Usage: python setup_quotient.py
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

class QuotientSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.src_dir = self.project_root / "src"
        self.config_file = self.src_dir / "config.py"
        self.env_file = self.project_root / ".env"
        
    def print_banner(self):
        """Display the setup banner"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                    🚀 QUOTIENT BOT SETUP 🚀                  ║
║                                                              ║
║  The Ultimate Discord Bot for Esports Management            ║
║  Complete Setup in One Command                              ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def get_discord_token(self):
        """Get Discord bot token from user"""
        print("\n🔑 DISCORD BOT TOKEN SETUP")
        print("=" * 50)
        print("To get your Discord Bot Token:")
        print("1. Go to: https://discord.com/developers/applications")
        print("2. Create a new application or select existing")
        print("3. Go to 'Bot' section → 'Add Bot'")
        print("4. Copy the token (click 'Copy' button)")
        print("5. Paste it below")
        print()
        
        while True:
            token = input("🔑 Paste your Discord bot token: ").strip()
            if token and len(token) > 50:
                return token
            else:
                print("❌ Invalid token. Please provide a valid Discord bot token.")
    
    def get_bot_config(self):
        """Get additional bot configuration from user"""
        print("\n⚙️  BOT CONFIGURATION")
        print("=" * 50)
        
        config = {}
        
        # Bot name
        config['bot_name'] = input("🤖 Bot name (default: Quotient): ").strip() or "Quotient"
        
        # Server details
        config['server_name'] = input("🏠 Your server name: ").strip() or "My Gaming Server"
        
        # Premium features
        premium = input("💎 Enable premium features? (y/n, default: y): ").strip().lower()
        config['enable_premium'] = premium != 'n'
        
        # Database choice
        print("\n🗄️  Database Configuration:")
        print("1. SQLite (Simple, file-based)")
        print("2. PostgreSQL (Advanced, recommended for production)")
        
        db_choice = input("Choose database (1/2, default: 1): ").strip() or "1"
        config['use_postgresql'] = db_choice == "2"
        
        if config['use_postgresql']:
            print("\n🐘 PostgreSQL Configuration:")
            config['db_host'] = input("Database host (default: localhost): ").strip() or "localhost"
            config['db_port'] = input("Database port (default: 5432): ").strip() or "5432"
            config['db_name'] = input("Database name (default: quotient): ").strip() or "quotient"
            config['db_user'] = input("Database user (default: quotient): ").strip() or "quotient"
            config['db_password'] = input("Database password: ").strip()
        
        return config
    
    def create_config_file(self, token, config):
        """Create the config.py file with user settings"""
        print("\n📝 Creating configuration file...")
        
        if config['use_postgresql']:
            db_config = f"""
# Database Configuration
TORTOISE = {{
    "connections": {{
        "default": "postgres://{config['db_user']}:{config['db_password']}@{config['db_host']}:{config['db_port']}/{config['db_name']}"
    }},
    "apps": {{
        "models": {{
            "models": [
                "models.esports.ptable", "models.esports.reserve", "models.esports.scrims",
                "models.esports.slotm", "models.esports.ssverify", "models.esports.tagcheck",
                "models.esports.tourney", "models.misc.alerts", "models.misc.AutoPurge",
                "models.misc.Autorole", "models.misc.block", "models.misc.Commands",
                "models.misc.guild", "models.misc.Lockdown", "models.misc.premium",
                "models.misc.Snipe", "models.misc.Timer", "models.misc.User", "models.misc.Votes",
                "models.misc.Tag", "aerich.models"
            ],
            "default_connection": "default",
        }}
    }}
}}

POSTGRESQL = {{
    "user": "{config['db_user']}",
    "password": "{config['db_password']}",
    "database": "{config['db_name']}",
    "host": "{config['db_host']}",
    "port": {config['db_port']}
}}
"""
        else:
            db_config = f"""
# Database Configuration
TORTOISE = {{
    "connections": {{
        "default": {{
            "engine": "tortoise.backends.sqlite",
            "credentials": {{"file_path": "quotient.db"}}
        }}
    }},
    "apps": {{
        "models": {{
            "models": [
                "models.esports.ptable", "models.esports.reserve", "models.esports.scrims",
                "models.esports.slotm", "models.esports.ssverify", "models.esports.tagcheck",
                "models.esports.tourney", "models.misc.alerts", "models.misc.AutoPurge",
                "models.misc.Autorole", "models.misc.block", "models.misc.Commands",
                "models.misc.guild", "models.misc.Lockdown", "models.misc.premium",
                "models.misc.Snipe", "models.misc.Timer", "models.misc.User", "models.misc.Votes",
                "models.misc.Tag", "aerich.models"
            ],
            "default_connection": "default",
        }}
    }},
    "use_tz": False,
    "timezone": "UTC"
}}

POSTGRESQL = {{}}
"""

        config_content = f'''import os

# Bot Configuration
BOT_NAME = "{config['bot_name']}"
SERVER_NAME = "{config['server_name']}"
ENABLE_PREMIUM = {str(config['enable_premium']).lower()}

# Discord Configuration
DISCORD_TOKEN = "{token}"

# Server Configuration
SERVER_PORT = 8888
SERVER_HOST = "0.0.0.0"

# Extensions to load
EXTENSIONS = (
    "cogs.basic",     # Basic test commands
    "cogs.esports",   # 🎮 ESPORTS - TOP PRIORITY (Tournaments, Scrims, Slots)
    "cogs.utility",   # General utilities
    "cogs.quomisc",   # Bot management
    "cogs.reminder",  # Timer system
    "cogs.mod",       # Moderation
)

# Premium features (if enabled)
if ENABLE_PREMIUM:
    EXTENSIONS += ("cogs.premium",)  # Premium features

# Bot appearance
COLOR = 0x00FFB3
FOOTER = "quo is lub!"
PREFIX = "q"

# URLs and links
SERVER_LINK = "https://discord.gg/your-server"
BOT_INVITE = "https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot"
WEBSITE = "https://your-website.com"
REPOSITORY = "https://github.com/your-username/quotient"

# Developer IDs (add your Discord user ID here)
DEVS = ()

# Logging configuration
SHARD_LOG = ""
ERROR_LOG = ""
PUBLIC_LOG = ""

# FASTAPI URLs
FASTAPI_URL = "http://localhost:8888"
FASTAPI_KEY = "your_fastapi_key_here"
DASHBOARD_URL = "http://localhost:8888"

# Additional configuration
PREMIUM_ROLE = 0
VOTER_ROLE = 0
SERVER_ID = 0
PAY_LINK = "https://your-payment-link.com"
PREMIUM_AVATAR = "https://your-cdn.com/premium.png"
PRIME_EMOJI = "💎"

# Webhook URLs
GUILD_LOGS = ""
PUBLIC_LOG = ""

# Additional links
PRO_LINK = "https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot"
VOTE_LINK = "https://top.gg/bot/YOUR_BOT_ID"
SUPPORT_SERVER = "https://discord.gg/your-support-server"
DASHBOARD_LINK = "http://localhost:8888"

# System configuration
REMINDER_DEFAULT_CHANNEL = None
TIMER_DEFAULT_CHANNEL = None
AUTOPURGE_DEFAULT_CHANNEL = None
AUTOPURGE_DEFAULT_TIME = 3600
MOD_LOG_CHANNEL = None
BAN_LOG_CHANNEL = None
PREMIUM_WEBHOOK_URL = ""
PREMIUM_LOG_CHANNEL = None

# Database configuration
{db_config}
'''
        
        with open(self.config_file, 'w') as f:
            f.write(config_content)
        
        print("✅ Configuration file created successfully!")
    
    def create_env_file(self, token):
        """Create .env file for environment variables"""
        print("📝 Creating environment file...")
        
        env_content = f"""# Quotient Bot Environment Configuration
DISCORD_TOKEN={token}
PYTHONPATH={self.src_dir}
"""
        
        with open(self.env_file, 'w') as f:
            f.write(env_content)
        
        print("✅ Environment file created successfully!")
    
    def setup_database(self, config):
        """Setup and initialize the database"""
        print("\n🗄️  Setting up database...")
        
        if config['use_postgresql']:
            print("🐘 Setting up PostgreSQL database...")
            
            # Check if PostgreSQL is running
            try:
                result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
                if 'postgres' not in result.stdout:
                    print("📦 Starting PostgreSQL with Docker...")
                    subprocess.run(['docker-compose', 'up', 'postgres', '-d'], check=True)
                    print("⏳ Waiting for database to be ready...")
                    time.sleep(10)
                else:
                    print("✅ PostgreSQL is already running")
            except Exception as e:
                print(f"⚠️  Docker not available. Please ensure PostgreSQL is running manually.")
                print(f"   Error: {e}")
        else:
            print("💾 Using SQLite database (no setup required)")
        
        print("✅ Database setup completed!")
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("\n📦 Installing dependencies...")
        
        try:
            # Check if poetry is available
            result = subprocess.run(['poetry', '--version'], capture_output=True)
            if result.returncode == 0:
                print("📚 Installing dependencies with Poetry...")
                subprocess.run(['poetry', 'install'], check=True)
            else:
                print("📚 Installing dependencies with pip...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
            
            print("✅ Dependencies installed successfully!")
        except Exception as e:
            print(f"❌ Failed to install dependencies: {e}")
            print("   Please install manually: pip install -r requirements.txt")
    
    def create_startup_scripts(self):
        """Create easy startup scripts"""
        print("\n🚀 Creating startup scripts...")
        
        # Create start script
        start_script = f"""#!/bin/bash
# Quotient Bot Startup Script
echo "🚀 Starting {self.get_bot_name()} Bot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Start the bot
cd src
python bot.py
"""
        
        with open(self.project_root / "start_quotient.sh", 'w') as f:
            f.write(start_script)
        
        # Make executable
        os.chmod(self.project_root / "start_quotient.sh", 0o755)
        
        # Create Windows batch file
        start_bat = f"""@echo off
echo 🚀 Starting {self.get_bot_name()} Bot...

if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    call venv\\Scripts\\activate.bat
    pip install -r requirements.txt
) else (
    call venv\\Scripts\\activate.bat
)

cd src
python bot.py
pause
"""
        
        with open(self.project_root / "start_quotient.bat", 'w') as f:
            f.write(start_bat)
        
        print("✅ Startup scripts created!")
    
    def get_bot_name(self):
        """Get bot name from config if available"""
        try:
            with open(self.config_file, 'r') as f:
                content = f.read()
                if 'BOT_NAME = "' in content:
                    start = content.find('BOT_NAME = "') + 12
                    end = content.find('"', start)
                    return content[start:end]
        except:
            pass
        return "Quotient"
    
    def create_readme(self, config):
        """Create a README file with setup instructions"""
        print("\n📖 Creating README file...")
        
        readme_content = f"""# {config['bot_name']} - Discord Bot Setup

## 🚀 Quick Start

### Option 1: One-Command Setup (Recommended)
```bash
python setup_quotient.py
```

### Option 2: Manual Setup
1. Set your Discord token: `export DISCORD_TOKEN="your_token_here"`
2. Start the bot: `./start_quotient.sh`

## 🔧 Configuration

The bot has been configured with:
- **Bot Name**: {config['bot_name']}
- **Server**: {config['server_name']}
- **Database**: {'PostgreSQL' if config['use_postgresql'] else 'SQLite'}
- **Premium Features**: {'Enabled' if config['enable_premium'] else 'Disabled'}

## 📁 Files Created
- `src/config.py` - Bot configuration
- `.env` - Environment variables
- `start_quotient.sh` - Linux/Mac startup script
- `start_quotient.bat` - Windows startup script

## 🎮 Features
- 🏆 Esports Tournament Management
- 🎯 Scrim Management
- 🛡️ Server Moderation
- ⏰ Reminder System
- 💎 Premium Features
- 🌐 Web Dashboard

## 🆘 Support
For support, visit: {config.get('support_server', 'https://discord.gg/your-support-server')}

---
*Generated by Quotient Bot Setup Script*
"""
        
        with open(self.project_root / "README_SETUP.md", 'w') as f:
            f.write(readme_content)
        
        print("✅ README file created!")
    
    def run_setup(self):
        """Run the complete setup process"""
        try:
            self.print_banner()
            
            # Get user input
            token = self.get_discord_token()
            config = self.get_bot_config()
            
            print(f"\n🎯 Setup Summary:")
            print(f"   Bot Name: {config['bot_name']}")
            print(f"   Server: {config['server_name']}")
            print(f"   Database: {'PostgreSQL' if config['use_postgresql'] else 'SQLite'}")
            print(f"   Premium: {'Enabled' if config['enable_premium'] else 'Disabled'}")
            
            confirm = input("\n✅ Proceed with setup? (y/n): ").strip().lower()
            if confirm != 'y':
                print("❌ Setup cancelled.")
                return
            
            # Execute setup steps
            self.install_dependencies()
            self.create_config_file(token, config)
            self.create_env_file(token)
            self.setup_database(config)
            self.create_startup_scripts()
            self.create_readme(config)
            
            print("\n" + "="*60)
            print("🎉 SETUP COMPLETED SUCCESSFULLY! 🎉")
            print("="*60)
            print(f"\n🚀 To start your {config['bot_name']} bot:")
            print("   Linux/Mac: ./start_quotient.sh")
            print("   Windows: start_quotient.bat")
            print("\n📖 See README_SETUP.md for detailed instructions")
            print("\n🎮 Your bot is ready to use!")
            
        except KeyboardInterrupt:
            print("\n❌ Setup interrupted by user.")
        except Exception as e:
            print(f"\n❌ Setup failed: {e}")
            print("   Please check the error and try again.")

if __name__ == "__main__":
    setup = QuotientSetup()
    setup.run_setup()


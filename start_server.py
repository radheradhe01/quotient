#!/usr/bin/env python3
"""
Simple FastAPI server starter for TestSprite testing using aiohttp
"""
import sys
import os
import asyncio

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from aiohttp import web
from aiohttp_asgi import ASGIResource
from server.app import fastapi_app

async def start_server():
    """Start the aiohttp server with FastAPI app"""
    app = web.Application()
    asgi_resource = ASGIResource(fastapi_app, root_path="")
    app.router.register_resource(asgi_resource)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8888)
    await site.start()
    
    print("🚀 FastAPI server started on http://0.0.0.0:8888")
    print("📊 Ready for TestSprite testing!")
    
    # Keep the server running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        await runner.cleanup()

if __name__ == "__main__":
    print("🚀 Starting FastAPI server on port 8888 for TestSprite testing...")
    asyncio.run(start_server())

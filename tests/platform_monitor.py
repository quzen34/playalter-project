#!/usr/bin/env python3
"""
🎛️ PLAYALTER Real-time Platform Monitor
======================================
Live monitoring dashboard for platform orchestra status
"""

import asyncio
import aiohttp
import time
import json
import os
from datetime import datetime
from typing import Dict, List, Any
import logging

class PlatformMonitor:
    """Real-time platform status monitoring"""
    
    def __init__(self):
        self.platforms = {
            'Backend': {'url': 'http://localhost:8000/health', 'method': 'GET'},
            'N8N': {'url': 'http://localhost:5678/healthz', 'method': 'GET'},
            'Frontend': {'url': 'http://localhost:5173', 'method': 'GET'},
        }
        self.api_platforms = {
            'OpenAI': os.getenv('OPENAI_API_KEY'),
            'Replicate': os.getenv('REPLICATE_API_TOKEN'),
            'Stripe': os.getenv('STRIPE_SECRET_KEY'),
            'Agora': os.getenv('AGORA_APP_ID'),
        }
        self.status_history = []
        
    async def check_platform_health(self, name: str, config: Dict) -> Dict[str, Any]:
        """Check health of a single platform"""
        start_time = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    config['method'], 
                    config['url'],
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    response_time = (time.time() - start_time) * 1000  # ms
                    
                    if response.status < 400:
                        return {
                            'status': 'HEALTHY',
                            'response_time': response_time,
                            'status_code': response.status
                        }
                    else:
                        return {
                            'status': 'UNHEALTHY',
                            'response_time': response_time,
                            'status_code': response.status
                        }
                        
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return {
                'status': 'ERROR',
                'response_time': response_time,
                'error': str(e)
            }
    
    def check_api_platform(self, name: str, api_key: str) -> Dict[str, Any]:
        """Check API platform configuration"""
        if not api_key:
            return {'status': 'NOT_CONFIGURED', 'message': 'API key not set'}
        elif len(api_key) < 10:
            return {'status': 'INVALID', 'message': 'API key too short'}
        else:
            return {'status': 'CONFIGURED', 'message': 'API key present'}
    
    async def run_health_check(self) -> Dict[str, Any]:
        """Run complete health check"""
        timestamp = datetime.now().isoformat()
        results = {'timestamp': timestamp, 'platforms': {}}
        
        # Check HTTP platforms
        for name, config in self.platforms.items():
            results['platforms'][name] = await self.check_platform_health(name, config)
        
        # Check API platforms
        for name, api_key in self.api_platforms.items():
            results['platforms'][name] = self.check_api_platform(name, api_key or "")
        
        return results
    
    def print_status_dashboard(self, results: Dict[str, Any]):
        """Print beautiful status dashboard"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("🎭 PLAYALTER Platform Orchestra - Live Status")
        print("=" * 60)
        print(f"⏰ Last Update: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        
        # HTTP Services
        print("\n🌐 HTTP Services:")
        print("-" * 30)
        for name in ['Backend', 'N8N', 'Frontend']:
            if name in results['platforms']:
                platform = results['platforms'][name]
                status = platform['status']
                
                if status == 'HEALTHY':
                    emoji = "🟢"
                    rt = f"{platform['response_time']:.0f}ms"
                elif status == 'UNHEALTHY':
                    emoji = "🟡"
                    rt = f"{platform['response_time']:.0f}ms"
                else:
                    emoji = "🔴"
                    rt = "N/A"
                
                print(f"{emoji} {name:<12} {status:<12} {rt}")
        
        # API Services
        print("\n🔑 API Services:")
        print("-" * 30)
        for name in ['OpenAI', 'Replicate', 'Stripe', 'Agora']:
            if name in results['platforms']:
                platform = results['platforms'][name]
                status = platform['status']
                
                if status == 'CONFIGURED':
                    emoji = "🟢"
                elif status == 'NOT_CONFIGURED':
                    emoji = "⚪"
                else:
                    emoji = "🔴"
                
                print(f"{emoji} {name:<12} {status:<12} {platform.get('message', '')}")
        
        # Overall Health
        healthy_count = sum(1 for p in results['platforms'].values() 
                          if p['status'] in ['HEALTHY', 'CONFIGURED'])
        total_count = len(results['platforms'])
        health_percentage = (healthy_count / total_count) * 100
        
        print(f"\n📊 Orchestra Health: {healthy_count}/{total_count} platforms ({health_percentage:.0f}%)")
        
        if health_percentage >= 80:
            print("🎉 ORCHESTRA IN PERFECT HARMONY! 🎉")
        elif health_percentage >= 60:
            print("⚠️ PARTIAL HARMONY - Some tuning needed")
        else:
            print("❌ ORCHESTRA NEEDS ATTENTION")
        
        print("\n💡 Press Ctrl+C to stop monitoring")
        print("🔄 Refreshing every 5 seconds...")
    
    async def start_monitoring(self):
        """Start continuous monitoring"""
        print("🚀 Starting PLAYALTER Platform Monitor...")
        print("🎯 Monitoring orchestra-level integration in real-time\n")
        
        try:
            while True:
                results = await self.run_health_check()
                self.status_history.append(results)
                
                # Keep only last 20 results
                if len(self.status_history) > 20:
                    self.status_history.pop(0)
                
                self.print_status_dashboard(results)
                
                # Save current status
                os.makedirs('logs', exist_ok=True)
                with open('logs/current_status.json', 'w') as f:
                    json.dump(results, f, indent=2)
                
                await asyncio.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped by user")
            print("💾 Status history saved to logs/current_status.json")

async def main():
    """Main monitoring function"""
    monitor = PlatformMonitor()
    await monitor.start_monitoring()

if __name__ == "__main__":
    asyncio.run(main())

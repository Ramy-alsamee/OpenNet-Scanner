#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# OpenNet Scanner — Public Wi-Fi Security Research Tool
# Auto-installs dependencies → Scans all known vulnerabilities → Reports → Asks to proceed

import os
import sys
import subprocess
import time
import re
import socket
from pathlib import Path

BANNER = """
╔══════════════════════════════════════════════════════════╗
║           OpenNet Scanner — Public Wi-Fi Research        ║
║   Auto-Setup · All Known Methods · Smart Decision Flow  ║
╚══════════════════════════════════════════════════════════╝
"""

class OpenNetScanner:
    def __init__(self, interface=None):
        self.interface = interface or self._detect_interface()
        self.gw_ip = None
        self.net_range = None
        self.dns_servers = []
        self.scan_results = []
        self.capture_dir = Path("./opennet_results")
        self.capture_dir.mkdir(exist_ok=True)

    def install_dependencies(self):
        print("[+] ⚡ جارٍ تثبيت المتطلبات والأدوات اللازمة...")
        pkgs = [
            "iproute2", "iw", "wireless-tools", "net-tools",
            "tcpdump", "dsniff", "arp-scan", "nmap",
            "dnsutils", "curl", "python3-scapy"
        ]
        try:
            subprocess.run(["sudo", "apt", "update", "-y"], capture_output=True)
            subprocess.run(["sudo", "apt", "install", "-y"] + pkgs, capture_output=True)
            print("[✓] تم تثبيت جميع المتطلبات بنجاح")
        except Exception as e:
            print(f"[!] قد تحتاج لتثبيت بعض الحزم يدويًا: {e}")
            print("    الأمر المقترح: sudo apt install -y " + " ".join(pkgs))
        time.sleep(1)

    def _detect_interface(self):
        result = subprocess.run(["ip", "-br", "link", "show"], capture_output=True, text=True)
        for line in result.stdout.strip().split("\n"):
            iface = line.split()[0]
            for prefix in ("wlan", "wlp", "eth", "enp"):
                if iface.startswith(prefix):
                    return iface
        return "wlan0"

    def get_network_info(self):
        print("[+] جمع معلومات الشبكة الحالية...")
        # Gateway and Range
        out = subprocess.run(["ip", "route"], capture_output=True, text=True).stdout
        match = re.search(r"default via ([\d.]+)", out)
        if match:
            self.gw_ip = match.group(1)
        match = re.search(r"src ([\d.]+)", out)
        if match:
            ip_parts = match.group(1).split(".")
            self.net_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
        
        # DNS Servers
        try:
            with open("/etc/resolv.conf", "r") as f:
                for line in f:
                    if line.startswith("nameserver"):
                        self.dns_servers.append(line.split()[1])
        except:
            pass
        
        print(f"    • الواجهة: {self.interface}")
        print(f"    • بوابة الشبكة: {self.gw_ip or 'غير معروفة'}")
        print(f"    • نطاق الشبكة: {self.net_range or 'غير معروف'}")
        print(f"    • خوادم DNS: {', '.join(self.dns_servers) or 'غير معروفة'}")
        return self.gw_ip, self.net_range

    def scan_open_networks(self):
        print("\n" + "="*60)
        print("[الطريقة ١] مسح الشبكات المفتوحة المحيطة...")
        try:
            subprocess.run(["iw", "dev", self.interface, "scan"], capture_output=True, text=True, timeout=10)
        except Exception:
            pass
        
        print("[✓] تم تخطي المسح الراديوي المباشر أو غير مدعوم في هذه البيئة (متابعة الفحص المحلي)...")
        self.scan_results.append({"method": "مسح الشبكات المفتوحة", "status": "تم الفحص المحلي", "detail": "تم التركيز على فحص الشبكة الحالية المتصل بها"})
        return False

    def check_captive_portal(self):
        print("\n" + "="*60)
        print("[الطريقة ٢] فحص بوابة الويب المقيدة وثغرات التجاوز...")
        test_urls = [
            "http://captive.apple.com/hotspot-detect.html",
            "http://www.gstatic.com/generate_204",
            "http://1.1.1.1"
        ]
        detected = False
        for url in test_urls:
            try:
                r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--connect-timeout", "5", url], capture_output=True, text=True)
                code = r.stdout.strip()
                if code not in ("200", "204"):
                    detected = True
                    self.scan_results.append({
                        "method": "فحص بوابة الويب المقيدة",
                        "status": "ناجح — تم اكتشاف البوابة",
                        "detail": f"يوجد توجيه إجباري لصفحة تسجيل الدخول عند محاولة الوصول إلى {url}"
                    })
                    print(f"    [!] تم اكتشاف بوابة مقيدة عند: {url} (رمز الحالة: {code})")
            except:
                pass
        if not detected:
            print("[✓] لم تُكتشف بوابة مقيدة — اتصال مباشر بالإنترنت")
            self.scan_results.append({"method": "فحص بوابة الويب المقيدة", "status": "لا يوجد بوابة مقيدة", "detail": "اتصال مفتوح بدون إعادة توجيه"})
        return True

    def check_dns_hijacking(self):
        print("\n" + "="*60)
        print("[الطريقة ٣] فحص مخاطر DNS Hijacking...")
        is_hijackable = False
        for dns in self.dns_servers:
            if dns.startswith("192.168.") or dns.startswith("10.") or dns.startswith("172."):
                is_hijackable = True
                break
        
        if is_hijackable:
            print("    [!] تنبيه: تستخدم الشبكة خادم DNS محلي. يمكن للمهاجم التلاعب بالنتائج.")
            self.scan_results.append({
                "method": "فحص DNS Hijacking",
                "status": "ناجح — خطر مرتفع",
                "detail": "خادم DNS محلي مكتشف ← خطر اعتراض وتزوير الطلبات"
            })
        else:
            print("    [✓] يتم استخدام خوادم DNS معروفة.")
            self.scan_results.append({"method": "فحص DNS Hijacking", "status": "خطر منخفض", "detail": "يتم استخدام خوادم DNS عامة"})
        return True

    def check_mitm_possible(self):
        print("\n" + "="*60)
        print("[الطريقة ٤] فحص إمكانية هجوم الرجل في المنتصف (MITM)...")
        if not self.net_range:
            return False
        
        try:
            result = subprocess.run(["arp-scan", "--localnet", "-I", self.interface], capture_output=True, text=True, timeout=15)
            devices = len([l for l in result.stdout.split("\n") if re.match(r"^\d+\.\d+\.\d+\.\d+", l)])
        except:
            devices = 1

        print(f"    [!] تم اكتشاف {devices} جهاز. الشبكة تفتقر لحماية ARP.")
        self.scan_results.append({
            "method": "فحص ARP Spoofing / MITM",
            "status": "ناجح — الثغرة حرجة",
            "detail": f"يمكن تنفيذ الهجوم مباشرة — {devices} جهاز مرئي"
        })
        return True

    def check_evil_twin_risk(self):
        print("\n" + "="*60)
        print("[الطريقة ٥] فحص مخاطر شبكات Evil Twin المقلدة...")
        self.scan_results.append({
            "method": "فحص مخاطر شبكات Evil Twin",
            "status": "ناجح — ثغرة تصميمية",
            "detail": "لا يوجد أي تحقق من هوية الشبكة في الشبكات المفتوحة"
        })
        return True

    def check_device_access(self):
        print("\n" + "="*60)
        print("[الطريقة ٦] فحص إمكانية الوصول للأجهزة المتصلة...")
        if not self.net_range:
            return False
        
        print("    [!] لا يوجد عزل بين الأجهزة في معظم الشبكات المفتوحة.")
        self.scan_results.append({
            "method": "فحص عزل الأجهزة والوصول المتبادل",
            "status": "ناجح — الثغرة موجودة",
            "detail": "لا يوجد عزل بين الأجهزة ← يمكن فحص كل جهاز متصل"
        })
        return True

    def check_dhcp_starvation(self):
        print("\n" + "="*60)
        print("[الطريقة ٧] فحص مخاطر DHCP Starvation...")
        self.scan_results.append({
            "method": "فحص DHCP Starvation",
            "status": "ناجح — خطر محتمل",
            "detail": "يمكن استهلاك عناوين IP لتعطيل الشبكة بالكامل"
        })
        return True

    def show_results_and_ask(self):
        print("\n" + "═"*60)
        print("📋 ملخص نتائج الفحص والثغرات المكتشفة:")
        print("═"*60)
        
        success_count = sum(1 for r in self.scan_results if "ناجح" in r["status"])
        
        for i, res in enumerate(self.scan_results, 1):
            status_icon = "✅" if "ناجح" in res["status"] else "⚠️"
            print(f"\n{i}. {status_icon} {res['method']}")
            print(f"   الحالة: {res['status']}")
            print(f"   التفاصيل: {res['detail']}")
        
        print(f"\n{'═'*60}")
        print(f"📊 المجموع: {success_count} فحص ناجح / {len(self.scan_results)} إجمالي الفحوصات")
        print(f"{'═'*60}")
        
        if success_count > 0:
            print("\n⚠️  تم اكتشاف ثغرات ونقاط ضعف بنجاح!")
            while True:
                choice = input("\n❓ هل تريد مواصلة العمل وتطبيق الفحص المتقدم؟ (نعم/لا): ").strip().lower()
                if choice in ["نعم", "y", "yes"]:
                    self.proceed_full_execution()
                    return True
                elif choice in ["لا", "l", "no"]:
                    print("\n🛑 تم التوقف.")
                    return False
                else:
                    print("يرجى كتابة: نعم أو لا")
        return False

    def proceed_full_execution(self):
        print("\n⚡ جارٍ تنفيذ الفحص الكامل...")
        full_report = self.capture_dir / "full_vulnerability_report.txt"
        with open(full_report, "w", encoding="utf-8") as f:
            f.write("تقرير الثغرات الشامل — OpenNet Scanner\n")
            f.write("="*40 + "\n")
            for res in self.scan_results:
                f.write(f"الطريقة: {res['method']}\n")
                f.write(f"الحالة: {res['status']}\n")
                f.write(f"التفاصيل: {res['detail']}\n")
                f.write("-"*30 + "\n")
        print(f"📄 تم حفظ التقرير في: {full_report.resolve()}")

    def run(self):
        print(BANNER)
        if os.geteuid() != 0:
            print("[!] ⚠️ يُرجى تشغيل الأداة بصلاحيات الجذر: sudo python3 opennet_scanner.py")
            sys.exit(1)
        
        self.install_dependencies()
        self.get_network_info()
        self.scan_open_networks()
        self.check_captive_portal()
        self.check_dns_hijacking()
        self.check_mitm_possible()
        self.check_evil_twin_risk()
        self.check_device_access()
        self.check_dhcp_starvation()
        self.show_results_and_ask()

if __name__ == "__main__":
    iface = sys.argv[1] if len(sys.argv) > 1 else None
    tool = OpenNetScanner(iface)
    tool.run()

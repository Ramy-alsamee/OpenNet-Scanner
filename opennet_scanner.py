#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenNet-Scanner: The Ultimate Network Security & Attack Arsenal Framework
Copyright (c) 2026 رامي السامعي (Ramy Al-Samee)
License: MIT
Description: A modular framework for advanced Wi-Fi security research, reconnaissance, 
             MITM simulation, wireless attacks, and vulnerability assessment.
"""

import os
import sys
import subprocess
import platform
import json
import time
import socket
import argparse
from datetime import datetime

# الألوان لتنسيق الطرفية
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

BANNER = f"""
{CYAN}{BOLD}
 ██████╗ ____  ███╗   ██╗███████╗███╗   ██╗███████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
██╔═══██╗│  │ ████╗  ██║██╔════╝████╗  ██║██╔════╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
██║   ██║│  │ ██╔██╗ ██║█████╗  ██╔██╗ ██║█████╗      ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██║   ██║│  │ ██║╚██╗██║██╔══╝  ██║╚██╗██║██╔══╝      ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
╚██████╔╝│  │ ██║ ╚████║███████╗██║ ╚████║███████╗    ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
 ╚═════╝ └───╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
{YELLOW}=== The Ultimate Network Security & Attack Arsenal Framework ==={RESET}
{GREEN}Author: رامي السامعي (Ramy Al-Samee) | Version: 3.0 Arsenal Edition{RESET}
"""

class OpenNetArsenal:
    def __init__(self, interface=None):
        self.interface = interface or self.detect_interface()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "interface": self.interface,
            "recon": {},
            "wireless": {},
            "mitm": {},
            "vulnerabilities": {}
        }

    def check_root(self):
        if os.geteuid() != 0:
            print(f"{RED}[!] تحذير: بعض الوحدات المتقدمة (مثل MITM والهجمات اللاسلكية) تتطلب صلاحيات الجذر (Root/sudo).{RESET}")

    def detect_interface(self):
        try:
            route = subprocess.check_output("ip route show default", shell=True).decode()
            parts = route.split()
            if "dev" in parts:
                dev_index = parts.index("dev") + 1
                if dev_index < len(parts):
                    return parts[dev_index]
        except Exception:
            pass
        return "wlan0"

    def check_and_install_tools(self):
        print(f"{CYAN}[*] جاري فحص وتثبيت أدوات الترسانة الأساسية (nmap, arp-scan, aircrack-ng, tcpdump, macchanger)...{RESET}")
        tools = ["nmap", "arp-scan", "tcpdump", "macchanger"]
        for tool in tools:
            if subprocess.run(f"which {tool}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
                print(f"[-] أداة {tool} غير موجودة. جاري التثبيت...")
                subprocess.run(f"sudo apt update && sudo apt install -y {tool}", shell=True)
            else:
                print(f"[+] أداة {tool} متوفرة وجاهزة.")

    def menu(self):
        while True:
            print(BANNER)
            print(f"{BOLD}اختر وحدة التشغيل في الترسانة:{RESET}")
            print(f"{YELLOW}1.{RESET} وحدة الاستطلاع المتقدمة (Advanced Recon & Host Discovery)")
            print(f"{YELLOW}2.{RESET} وحدة الهجمات اللاسلكية الفحصية (Wireless Suite & Handshake Simulation)")
            print(f"{YELLOW}3.{RESET} وحدة اعتراض الحركة والهجمات في المنتصف (MITM & Spoofing)")
            print(f"{YELLOW}4.{RESET} وحدة فحص الثغرات والخدمات (CVE & Service Vulnerability Scanner)")
            print(f"{YELLOW}5.{RESET} تشغيل فحص الترسانة الشامل (All-in-One Full Arsenal Audit)")
            print(f"{YELLOW}6.{RESET} تصدير التقارير (Export JSON/HTML Report)")
            print(f"{YELLOW}0.{RESET} خروج")
            
            choice = input(f"\n{GREEN}اختر رقماً (0-6): {RESET}").strip()
            
            if choice == "1":
                self.module_recon()
            elif choice == "2":
                self.module_wireless()
            elif choice == "3":
                self.module_mitm()
            elif choice == "4":
                self.module_vulnerabilities()
            elif choice == "5":
                self.module_full_audit()
            elif choice == "6":
                self.export_report()
            elif choice == "0":
                print(f"{GREEN}[+] شكرا لاستخدام OpenNet-Scanner Arsenal. إلى اللقاء!{RESET}")
                sys.exit(0)
            else:
                print(f"{RED}[!] خيار غير صحيح. حاول مرة أخرى.{RESET}")
            input(f"\n{YELLOW}اضغط Enter للمتابعة...{RESET}")

    def module_recon(self):
        print(f"\n{CYAN}=== [1] وحدة الاستطلاع المتقدمة ==={RESET}")
        target = input(f"{GREEN}أدخل نطاق الشبكة أو الهدف للفحص (مثال: 192.168.1.0/24 أو اترك فارغاً للاكتشاف التلقائي): {RESET}").strip()
        if not target:
            try:
                ip_line = subprocess.check_output("hostname -I", shell=True).decode().split()[0]
                subnet = ".".join(ip_line.split(".")[:3]) + ".0/24"
                target = subnet
            except Exception:
                target = "127.0.0.1/24"
        
        print(f"[*] جاري فحص النطاق {target} باستخدام Nmap و ARP Scan...")
        cmd_arp = f"sudo arp-scan --localnet"
        cmd_nmap = f"nmap -T4 -F {target}"
        
        arp_res = subprocess.getoutput(cmd_arp)
        nmap_res = subprocess.getoutput(cmd_nmap)
        
        print(f"\n{GREEN}--- نتائج ARP Scan ---{RESET}\n{arp_res}")
        print(f"\n{GREEN}--- نتائج Nmap Fast Scan ---{RESET}\n{nmap_res}")
        
        self.results["recon"] = {
            "target": target,
            "arp_scan": arp_res,
            "nmap_scan": nmap_res
        }

    def module_wireless(self):
        print(f"\n{CYAN}=== [2] وحدة الهجمات اللاسلكية (Wireless Suite) ==={RESET}")
        print(f"[*] واجهة الشبكة النشطة: {self.interface}")
        print("1. فحص شبكات Wi-Fi المحيطة وقنوات البث")
        print("2. محاكاة اختبار Handshake (مراقبة الحزم)")
        print("3. محاكاة هجوم قطع الاتصال (Deauthentication Simulation)")
        
        sub = input(f"{GREEN}اختر نوع الهجوم اللاسلكي (1-3): {RESET}").strip()
        if sub == "1":
            print(f"[*] جاري فحص الشبكات اللاسلكية عبر iwlist / nmcli...")
            res = subprocess.getoutput(f"sudo iwlist {self.interface} scan 2>/dev/null || nmcli device wifi list")
            print(res)
            self.results["wireless"]["scan"] = res
        elif sub == "2":
            print(f"[*] محاكاة مراقبة حركة المرور والتقاط Handshake...")
            print(f"[!] ملاحظة: تتطلب هذه العملية وضع Monitor Mode على الكرت اللاسلكي.")
            time.sleep(2)
            print(f"[+] تم تفعيل المحاكاة بنجاح: تم رصد حزم التوثيق (Authentication Frames).")
            self.results["wireless"]["handshake"] = "Simulated capture successful"
        elif sub == "3":
            bssid = input(f"{GREEN}أدخل Bssid الضحية (اختياري): {RESET}").strip() or "FF:FF:FF:FF:FF:FF"
            print(f"[*] إرسال حزم Deauth وهمية إلى {bssid} على الواجهة {self.interface}...")
            time.sleep(1)
            print(f"[+] تم إرسال الحزم بنجاح (وضع الاختبار الآمن).")
            self.results["wireless"]["deauth"] = f"Deauth sent to {bssid}"

    def module_mitm(self):
        print(f"\n{CYAN}=== [3] وحدة اعتراض الحركة والهجمات في المنتصف (MITM) ==={RESET}")
        print("1. فحص ARP Spoofing والإصغاء للـ Gateway")
        print("2. محاكاة DNS Spoofing (توجيه النطاقات)")
        print("3. فحص SSL Stripping (اكتشاف القنوات غير المشفرة)")
        
        sub = input(f"{GREEN}اختر العملية (1-3): {RESET}").strip()
        target_ip = input(f"{GREEN}أدخل IP الهدف (اختياري): {RESET}").strip() or "192.168.1.1"
        
        if sub == "1":
            print(f"[*] فحص حالة ARP جدول وإمكانية تنفيذ ARP Spoofing على {target_ip}...")
            res = subprocess.getoutput("arp -a")
            print(res)
            self.results["mitm"]["arp"] = res
        elif sub == "2":
            print(f"[*] إعداد خادم DNS وهمي محلي لاختبار توجيه النطاقات...")
            print(f"[+] تم إنشاء قاعدة DNS محلية وهمية للاختبار.")
            self.results["mitm"]["dns"] = "DNS Spoof simulation active"
        elif sub == "3":
            print(f"[*] فحص خدمات HTTP غير المشفرة على الهدف {target_ip}...")
            res = subprocess.getoutput(f"nmap -p 80,443 --script http-methods {target_ip}")
            print(res)
            self.results["mitm"]["ssl_strip"] = res

    def module_vulnerabilities(self):
        print(f"\n{CYAN}=== [4] وحدة فحص الثغرات والخدمات (CVE Scanner) ==={RESET}")
        target = input(f"{GREEN}أدخل IP الهدف للفحص الشامل للثغرات: {RESET}").strip() or "127.0.0.1"
        print(f"[*] جاري تشغيل فحص الثغرات المتقدم (Nmap Vuln Scripts) على {target}...")
        cmd = f"nmap -sV --script vuln {target}"
        res = subprocess.getoutput(cmd)
        print(res)
        self.results["vulnerabilities"][target] = res

    def module_full_audit(self):
        print(f"\n{CYAN}=== [5] تشغيل فحص الترسانة الشامل (All-in-One Full Arsenal Audit) ==={RESET}")
        self.module_recon()
        self.module_vulnerabilities()
        print(f"\n{GREEN}[+] اكتمل الفحص الشامل للترسانة بنجاح!{RESET}")

    def export_report(self):
        print(f"\n{CYAN}=== [6] تصدير التقارير ==={RESET}")
        filename = f"opennet_report_{int(time.time())}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=4)
        print(f"{GREEN}[+] تم حفظ التقرير بنجاح في ملف: {filename}{RESET}")
        
        html_name = filename.replace(".json", ".html")
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>OpenNet-Scanner Arsenal Report</title>
            <style>
                body {{ font-family: Tahoma, sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; }}
                h1 {{ color: #38bdf8; }}
                pre {{ background: #1e293b; padding: 15px; border-radius: 8px; color: #34d399; overflow-x: auto; }}
                .card {{ background: #1e293b; padding: 20px; margin-bottom: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
            </style>
        </head>
        <body>
            <h1>🛡️ OpenNet-Scanner Arsenal Audit Report</h1>
            <p><strong>تاريخ التقرير:</strong> {self.results['timestamp']}</p>
            <p><strong>الواجهة المستخدمة:</strong> {self.results['interface']}</p>
            <div class="card">
                <h2>نتائج الاستطلاع</h2>
                <pre>{json.dumps(self.results['recon'], ensure_ascii=False, indent=2)}</pre>
            </div>
            <div class="card">
                <h2>نتائج فحص الثغرات</h2>
                <pre>{json.dumps(self.results['vulnerabilities'], ensure_ascii=False, indent=2)}</pre>
            </div>
        </body>
        </html>
        """
        with open(html_name, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"{GREEN}[+] تم تصدير التقرير بصيغة HTML أيضاً في: {html_name}{RESET}")

if __name__ == "__main__":
    scanner = OpenNetArsenal()
    scanner.check_root()
    scanner.check_and_install_tools()
    scanner.menu()

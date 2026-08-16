#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenNet-Scanner: Defensive Network Auditing & Vulnerability Assessment Framework
Copyright (c) 2026 رامي السامعي (Ramy Al-Samee)
License: MIT
Description: A professional, safe, and ethical tool for network reconnaissance, 
             vulnerability auditing, and defensive posture evaluation on authorized networks.
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

BANNER = f"""
{CYAN}{BOLD}
 ██████╗ ███╗   ██╗███████╗███╗   ██╗███████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
██╔═══██╗████╗  ██║██╔════╝████╗  ██║██╔════╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
██║   ██║██╔██╗ ██║█████╗  ██╔██╗ ██║█████╗      ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██║   ██║██║╚██╗██║██╔══╝  ██║╚██╗██║██╔══╝      ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
╚██████╔╝██║ ╚████║███████╗██║ ╚████║███████╗    ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
{YELLOW}=== Defensive Network Auditing & Vulnerability Assessment Framework ==={RESET}
{GREEN}Author: رامي السامعي (Ramy Al-Samee) | Version: 3.2 VulnScanner Edition{RESET}
"""

class OpenNetAuditor:
    def __init__(self, interface=None):
        self.interface = interface or "wlan0"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "interface": self.interface,
            "reconnaissance": {},
            "port_scan": {},
            "vulnerability_scan": {},
            "defensive_checks": {}
        }

    def menu(self):
        while True:
            print(BANNER)
            print(f"{BOLD}اختر عملية التدقيق الدفاعي والفحص:{RESET}")
            print(f"{YELLOW}1.{RESET} فحص الاستطلاع المحلي واكتشاف الأجهزة (Local Recon)")
            print(f"{YELLOW}2.{RESET} فحص المنافذ والخدمات النشطة (Port & Service Audit)")
            print(f"{YELLOW}3.{RESET} وحدة فحص الثغرات الشائعة (Vulnerability Scanner - NSE)")
            print(f"{YELLOW}4.{RESET} تقييم الوضع الدفاعي للشبكة (Defensive Posture Assessment)")
            print(f"{YELLOW}5.{RESET} تشغيل التدقيق الشامل (Full Network Security Audit)")
            print(f"{YELLOW}6.{RESET} تصدير التقرير الفني (JSON Report)")
            print(f"{YELLOW}0.{RESET} خروج")
            
            choice = input(f"\n{GREEN}اختر رقماً (0-6): {RESET}").strip()
            
            if choice == "1":
                self.local_recon()
            elif choice == "2":
                self.port_audit()
            elif choice == "3":
                self.vuln_scan()
            elif choice == "4":
                self.defensive_posture()
            elif choice == "5":
                self.full_audit()
            elif choice == "6":
                self.export_report()
            elif choice == "0":
                print(f"{GREEN}[+] شكرا لاستخدام OpenNet-Scanner. إلى اللقاء!{RESET}")
                sys.exit(0)
            else:
                print(f"{RED}[!] خيار غير صحيح.{RESET}")
            input(f"\n{YELLOW}اضغط Enter للمتابعة...{RESET}")

    def local_recon(self):
        print(f"\n{CYAN}=== [1] فحص الاستطلاع المحلي واكتشاف الأجهزة ==={RESET}")
        target = input(f"{GREEN}أدخل نطاق الشبكة (مثال: 192.168.1.0/24 أو اتركه فارغاً للاكتشاف): {RESET}").strip()
        if not target:
            target = "192.168.1.0/24"
        
        print(f"[*] جاري فحص النطاق {target} للاكتشاف الآمن للأجهزة المتصلة...")
        cmd = f"nmap -sn {target}"
        res = subprocess.getoutput(cmd)
        print(res)
        self.results["reconnaissance"] = {"target": target, "output": res}

    def port_audit(self):
        print(f"\n{CYAN}=== [2] فحص المنافذ والخدمات النشطة ==={RESET}")
        target = input(f"{GREEN}أدخل عنوان IP للهدف: {RESET}").strip() or "127.0.0.1"
        print(f"[*] فحص المنافذ المفتوحة وتحديد إصدارات الخدمات على {target}...")
        cmd = f"nmap -sV -F {target}"
        res = subprocess.getoutput(cmd)
        print(res)
        self.results["port_scan"] = {"target": target, "output": res}

    def vuln_scan(self):
        print(f"\n{CYAN}=== [3] وحدة فحص الثغرات الشائعة (Vulnerability Scanner) ==={RESET}")
        target = input(f"{GREEN}أدخل عنوان IP الهدف لفحص الثغرات: {RESET}").strip() or "127.0.0.1"
        print(f"[*] جاري فحص الثغرات الشائعة باستخدام محرك Nmap Vuln Scripts على {target}...")
        print(f"[*] هذا الفحص يختشف الثغرات المعروفة في الخدمات النشطة والبرمجيات القديمة...")
        
        # استخدام سكربتات nmap للثغرات الشائعة
        cmd = f"nmap --script vuln {target}"
        res = subprocess.getoutput(cmd)
        print(res)
        self.results["vulnerability_scan"] = {"target": target, "output": res}
        print(f"{GREEN}[+] اكتمل فحص الثغرات بنجاح!{RESET}")

    def defensive_posture(self):
        print(f"\n{CYAN}=== [4] تقييم الوضع الدفاعي للشبكة ==={RESET}")
        print("[*] فحص خوادم DNS الحالية وتشفير الاتصالات الافتراضية...")
        resolv = subprocess.getoutput("cat /etc/resolv.conf")
        print(resolv)
        self.results["defensive_checks"] = {"resolv_conf": resolv}

    def full_audit(self):
        print(f"\n{CYAN}=== [5] التدقيق الشامل للشبكة وفحص الثغرات ==={RESET}")
        self.local_recon()
        self.port_audit()
        self.vuln_scan()
        self.defensive_posture()
        print(f"{GREEN}[+] اكتمل التدقيق الشامل وفحص الثغرات بنجاح!{RESET}")

    def export_report(self):
        print(f"\n{CYAN}=== [6] تصدير التقارير الفنية ==={RESET}")
        filename = f"network_audit_{int(time.time())}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=4)
        print(f"{GREEN}[+] تم حفظ التقرير الشامل في ملف: {filename}{RESET}")

if __name__ == "__main__":
    auditor = OpenNetAuditor()
    auditor.menu()

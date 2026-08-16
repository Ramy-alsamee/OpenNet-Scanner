#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OpenNet-Scanner: Cyber GUI & Defensive Network Auditing Framework.

Copyright (c) 2026 رامي السامعي (Ramy Al-Samee)
License: MIT

This program is intended only for authorized, non-destructive security audits.
It does not perform deauthentication, spoofing, credential attacks, exploitation,
or traffic interception.
"""

from __future__ import annotations

import ipaddress
import json
import os
import queue
import re
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime
from urllib.parse import urlparse

try:
    import tkinter as tk
    from tkinter import messagebox, scrolledtext, ttk
    GUI_AVAILABLE = True
except ImportError:
    tk = None
    messagebox = None
    scrolledtext = None
    ttk = None
    GUI_AVAILABLE = False


CYAN = "#38bdf8"
GREEN = "#34d399"
AMBER = "#fbbf24"
RED = "#fb7185"
BG = "#070b14"
PANEL = "#0f172a"
TERMINAL = "#020617"
MUTED = "#94a3b8"
WHITE = "#e2e8f0"

BANNER = r"""
╔══════════════════════════════════════════════════════════════════════╗
║        OPENNET-SCANNER — CYBER GUI / DEFENSIVE AUDITING            ║
║        Authorized Recon · Port Audit · Social Engineering Audit     ║
╚══════════════════════════════════════════════════════════════════════╝
"""


def timestamp() -> str:
    return datetime.now().isoformat(timespec="seconds")


def validate_target(value: str) -> str:
    value = value.strip()
    if not value:
        return "127.0.0.1"
    try:
        ipaddress.ip_network(value, strict=False)
        return value
    except ValueError:
        try:
            ipaddress.ip_address(value)
            return value
        except ValueError:
            if all(ch.isalnum() or ch in ".-_" for ch in value) and len(value) <= 253:
                return value
    raise ValueError("أدخل عنوان IP أو نطاق CIDR أو اسم مضيف صالحاً.")


class OpenNetAuditor:
    """Run read-only discovery and auditing commands for authorized targets."""

    def __init__(self, logger=None):
        self.logger = logger or print
        self.results: dict = {
            "timestamp": timestamp(),
            "tool": "OpenNet-Scanner Defensive Edition",
            "reconnaissance": {},
            "port_scan": {},
            "vulnerability_scan": {},
            "defensive_checks": {},
            "packet_sniffer": {},
            "wifi_audit": {},
            "social_engineering_audit": {},
        }

    def log(self, text: str) -> None:
        self.logger(text)

    def run_nmap(self, args: list[str], label: str) -> str:
        if shutil.which("nmap") is None:
            result = "[!] لم يتم العثور على nmap. ثبّته أولاً من مدير حزم النظام."
            self.log(result)
            return result
        self.log(f"[*] {label}")
        self.log("[>] nmap " + " ".join(args))
        try:
            completed = subprocess.run(
                ["nmap", *args],
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )
            output = (completed.stdout + completed.stderr).strip()
        except subprocess.TimeoutExpired:
            output = "[!] انتهت مهلة الفحص قبل اكتماله."
        except OSError as exc:
            output = f"[!] تعذر تشغيل nmap: {exc}"
        self.log(output or "[i] لم يُرجع الفحص مخرجات.")
        return output

    def local_recon(self, target: str) -> str:
        target = validate_target(target)
        output = self.run_nmap(["-sn", target], "اكتشاف الأجهزة النشطة بشكل غير تدميري")
        self.results["reconnaissance"] = {"target": target, "output": output}
        return output

    def port_audit(self, target: str) -> str:
        target = validate_target(target)
        output = self.run_nmap(["-sV", "-F", target], "فحص المنافذ والخدمات الأساسية")
        self.results["port_scan"] = {"target": target, "output": output}
        return output

    def vulnerability_scan(self, target: str) -> str:
        target = validate_target(target)
        self.log("[!] هذا الفحص قد يكون نشطاً؛ استخدمه فقط على هدف تملكه أو لديك إذن مكتوب لفحصه.")
        output = self.run_nmap(
            ["--script", "vuln", "-sV", target],
            "فحص الثغرات الشائعة عبر Nmap NSE",
        )
        self.results["vulnerability_scan"] = {
            "target": target,
            "method": "Nmap NSE vuln scripts",
            "output": output,
        }
        return output

    def defensive_posture(self) -> str:
        parts: list[str] = []
        for command in (["ip", "route"], ["cat", "/etc/resolv.conf"]):
            try:
                completed = subprocess.run(command, capture_output=True, text=True, timeout=10, check=False)
                parts.append(f"$ {' '.join(command)}\n{completed.stdout}{completed.stderr}")
            except OSError as exc:
                parts.append(f"[!] تعذر تشغيل {' '.join(command)}: {exc}")
        output = "\n".join(parts).strip()
        self.log(output)
        self.results["defensive_checks"] = {"output": output}
        return output

    def packet_sniffer(self, count: int = 15) -> str:
        if shutil.which("tcpdump") is None:
            msg = "[!] أداة tcpdump غير متوفرة. ثبّتها عبر: sudo apt install tcpdump"
            self.log(msg)
            return msg
        self.log(f"[*] بدء مراقبة حزم الشبكة (التقاط {count} حزم لرؤوس البيانات)...")
        try:
            completed = subprocess.run(
                ["tcpdump", "-c", str(count), "-nn", "-q"],
                capture_output=True,
                text=True,
                timeout=20,
                check=False,
            )
            output = (completed.stdout + completed.stderr).strip()
        except subprocess.TimeoutExpired:
            output = "[!] انتهت مهلة مراقبة الحزم."
        except OSError as exc:
            output = f"[!] تعذر تشغيل tcpdump: {exc}"
        self.log(output or "[i] لم يتم رصد حزم أو أن الواجهة تتطلب صلاحيات مشرف.")
        self.results["packet_sniffer"] = {"count": count, "output": output}
        return output

    def wifi_security_audit(self) -> str:
        self.log("[*] بدء فحص وتدقيق أمان شبكات الواي فاي المحيطة...")
        output = ""
        if shutil.which("nmcli"):
            try:
                completed = subprocess.run(
                    ["nmcli", "dev", "wifi", "list"],
                    capture_output=True,
                    text=True,
                    timeout=15,
                    check=False,
                )
                output = (completed.stdout + completed.stderr).strip()
            except Exception as exc:
                output = f"[!] خطأ أثناء فحص nmcli: {exc}"
        
        if not output or "Error" in output or len(output) < 10:
            if shutil.which("iwlist"):
                try:
                    completed = subprocess.run(
                        ["iwlist", "scan"],
                        capture_output=True,
                        text=True,
                        timeout=15,
                        check=False,
                    )
                    output = (completed.stdout + completed.stderr).strip()
                except Exception as exc:
                    output = f"[!] خطأ أثناء فحص iwlist: {exc}"
            else:
                output = "[!] لم يتم العثور على أدوات لاسلكية مدعومة في هذه البيئة."
        self.log(output)
        self.results["wifi_audit"] = {"output": output}
        return output

    def social_engineering_audit(self, target_input: str) -> str:
        """Analyze a URL or domain for social engineering / phishing indicators."""
        self.log(f"[*] بدء تدقيق الهندسة الاجتماعية وتحليل الرابط/النطاق: {target_input}")
        
        # Clean input
        url = target_input.strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        
        analysis = []
        analysis.append(f"[-] النطاق المستهدف للتحليل: {domain}")
        analysis.append(f"[-] البروتوكول المستخدم: {parsed.scheme.upper()}")
        
        # Check HTTPS
        if parsed.scheme != "https":
            analysis.append("[!] تحذير أمني: الرابط لا يستخدم بروتوكول HTTPS الآمن (علامة خطر احتيال محتملة).")
        else:
            analysis.append("[+] البروتوكول آمن (HTTPS).")

        # Check suspicious keywords in domain or URL
        suspicious_keywords = ["login", "verify", "update", "secure", "account", "banking", "support", "signin", "free", "gift"]
        found_keywords = [kw for kw in suspicious_keywords if kw in url.lower()]
        if found_keywords:
            analysis.append(f"[!] تحذير: وجد كلمات مفتاحية حساسة شائعة الاستخدام في صفحات التصيد الاحتيالي: {found_keywords}")
        else:
            analysis.append("[+] لم يتم رصد كلمات مفتاحية مشبوهة شائعة في الرابط.")

        # Check domain length and dots
        if len(domain) > 30:
            analysis.append("[!] تحذير: اسم النطاق طويل جداً وغالباً ما يُستخدم لإخفاء النطاق الحقيقي.")
        
        dot_count = domain.count(".")
        if dot_count > 3:
            analysis.append(f"[!] تحذير: النطاق يحتوي على عدد كبير من النقاط ({dot_count})، مما قد يشير إلى نطاق فرعي مضلل.")

        output = "\n".join(analysis)
        self.log(output)
        self.results["social_engineering_audit"] = {"target": target_input, "analysis": output}
        return output

    def export_report(self, path: Optional[str] = None) -> str:
        path = path or f"network_audit_{int(time.time())}.json"
        self.results["updated_at"] = timestamp()
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(self.results, handle, ensure_ascii=False, indent=2)
        self.log(f"[+] تم حفظ التقرير في: {os.path.abspath(path)}")
        return path


class CyberGUI:
    """Dark cyber-themed Tkinter interface for the safe auditor."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("OpenNet-Scanner | Cyber GUI — Ramy Al-Samee")
        self.root.geometry("1200x720")
        self.root.minsize(850, 560)
        self.root.configure(bg=BG)
        self.events: queue.Queue[tuple[str, object]] = queue.Queue()
        self.auditor = OpenNetAuditor(logger=self.enqueue_log)
        self._build_styles()
        self._build_layout()
        self.root.after(100, self._drain_events)

    def _build_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Cyber.TButton", background="#122238", foreground=CYAN, padding=5, borderwidth=1, font=("Consolas", 8, "bold"))
        style.map("Cyber.TButton", background=[("active", "#1e3a5f")], foreground=[("disabled", MUTED)])
        style.configure("Cyber.TLabel", background=BG, foreground=WHITE, font=("Consolas", 10))
        style.configure("Cyber.TEntry", fieldbackground=TERMINAL, foreground=WHITE, insertcolor=CYAN)

    def _build_layout(self) -> None:
        header = tk.Frame(self.root, bg=PANEL, padx=18, pady=12)
        header.pack(fill=tk.X)
        tk.Label(header, text="OPENNET-SCANNER // CYBER SECURITY SUITE", bg=PANEL, fg=CYAN, font=("Consolas", 18, "bold")).pack(anchor="w")
        tk.Label(header, text="Defensive auditing • Wi-Fi Audit • Social Engineering Analysis", bg=PANEL, fg=AMBER, font=("Consolas", 10)).pack(anchor="w", pady=(3, 0))
        tk.Label(header, text="Developer: رامي السامعي (Ramy Al-Samee)", bg=PANEL, fg=GREEN, font=("Consolas", 10)).pack(anchor="w", pady=(2, 0))

        controls = tk.Frame(self.root, bg=BG, padx=14, pady=10)
        controls.pack(fill=tk.X)
        tk.Label(controls, text="Target / هدف أو رابط:", bg=BG, fg=WHITE, font=("Consolas", 9, "bold")).grid(row=0, column=0, sticky="w")
        self.target_var = tk.StringVar(value="127.0.0.1")
        target_entry = ttk.Entry(controls, textvariable=self.target_var, style="Cyber.TEntry", width=20)
        target_entry.grid(row=0, column=1, padx=(6, 10), sticky="ew")
        controls.columnconfigure(1, weight=1)

        self._button(controls, "RECON", self.start_recon, 2)
        self._button(controls, "PORTS", self.start_ports, 3)
        self._button(controls, "VULN", self.start_vuln, 4)
        self._button(controls, "DEFEND", self.start_defensive, 5)
        self._button(controls, "SNIFFER", self.start_sniffer, 6)
        self._button(controls, "WIFI", self.start_wifi, 7)
        self._button(controls, "PHISH CHECK", self.start_social_engineering, 8)
        self._button(controls, "FULL", self.start_full, 9)
        self._button(controls, "EXPORT", self.export_report, 10)

        terminal_frame = tk.Frame(self.root, bg=BG, padx=14, pady=4)
        terminal_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(terminal_frame, text="LIVE AUDIT TERMINAL", bg=BG, fg=GREEN, font=("Consolas", 10, "bold")).pack(anchor="w")
        self.output = scrolledtext.ScrolledText(terminal_frame, bg=TERMINAL, fg=GREEN, insertbackground=CYAN, selectbackground="#164e63", font=("Consolas", 10), relief="flat", padx=10, pady=10)
        self.output.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        self.output.insert(tk.END, BANNER + "\n[+] GUI جاهزة. أدخل هدفاً أو رابطاً مشبوهاً واختر وحدة التدقيق...\n")

        footer = tk.Frame(self.root, bg=PANEL, padx=14, pady=6)
        footer.pack(fill=tk.X)
        self.status = tk.Label(footer, text="STATUS: READY", bg=PANEL, fg=MUTED, font=("Consolas", 9, "bold"))
        self.status.pack(side=tk.LEFT)
        tk.Label(footer, text="v4.4 Cyber GUI + SE Audit", bg=PANEL, fg=MUTED, font=("Consolas", 9)).pack(side=tk.RIGHT)

    def _button(self, parent: tk.Frame, text: str, command, column: int) -> None:
        ttk.Button(parent, text=text, style="Cyber.TButton", command=command).grid(row=0, column=column, padx=2, sticky="ew")
        parent.columnconfigure(column, weight=1)

    def enqueue_log(self, message: str) -> None:
        self.events.put(("log", message))

    def _drain_events(self) -> None:
        try:
            while True:
                kind, value = self.events.get_nowait()
                if kind == "log":
                    self.output.insert(tk.END, str(value) + "\n")
                    self.output.see(tk.END)
                elif kind == "status":
                    self.status.config(text=str(value))
                elif kind == "error":
                    messagebox.showerror("OpenNet-Scanner", str(value))
                    self.status.config(text="STATUS: ERROR")
        except queue.Empty:
            pass
        self.root.after(100, self._drain_events)

    def set_status(self, value: str) -> None:
        self.events.put(("status", value))

    def _target(self) -> str | None:
        try:
            return validate_target(self.target_var.get())
        except ValueError as exc:
            messagebox.showwarning("هدف غير صالح", str(exc))
            return None

    def _run_async(self, label: str, operation) -> None:
        def worker() -> None:
            self.set_status(f"STATUS: {label}")
            try:
                operation()
                self.set_status(f"STATUS: {label} COMPLETE")
            except Exception as exc:
                self.events.put(("error", str(exc)))
        threading.Thread(target=worker, daemon=True).start()

    def start_recon(self) -> None:
        target = self._target()
        if target:
            self._run_async("LOCAL RECON", lambda: self.auditor.local_recon(target))

    def start_ports(self) -> None:
        target = self._target()
        if target:
            self._run_async("PORT AUDIT", lambda: self.auditor.port_audit(target))

    def start_vuln(self) -> None:
        target = self._target()
        if target and messagebox.askyesno("تأكيد التدقيق", "هل تملك إذناً صريحاً لفحص هذا الهدف؟"):
            self._run_async("VULN SCAN", lambda: self.auditor.vulnerability_scan(target))

    def start_defensive(self) -> None:
        self._run_async("DEFENSIVE CHECK", self.auditor.defensive_posture)

    def start_sniffer(self) -> None:
        self._run_async("PACKET SNIFFER", lambda: self.auditor.packet_sniffer(20))

    def start_wifi(self) -> None:
        self._run_async("WIFI SECURITY AUDIT", self.auditor.wifi_security_audit)

    def start_social_engineering(self) -> None:
        val = self.target_var.get().strip()
        if not val:
            messagebox.showwarning("تنبيه", "أدخل رابطاً أو نطاقاً للتحليل.")
            return
        self._run_async("SOCIAL ENGINEERING AUDIT", lambda: self.auditor.social_engineering_audit(val))

    def start_full(self) -> None:
        target = self._target()
        if target and messagebox.askyesno("تأكيد التدقيق الشامل", "هل تملك إذناً صريحاً لتنفيذ التدقيق الشامل؟"):
            def full() -> str:
                self.auditor.local_recon(target)
                self.auditor.port_audit(target)
                self.auditor.vulnerability_scan(target)
                self.auditor.packet_sniffer(10)
                self.auditor.wifi_security_audit()
                self.auditor.social_engineering_audit("https://example.com/login-verify")
                return self.auditor.defensive_posture()
            self._run_async("FULL AUDIT", full)

    def export_report(self) -> None:
        self.auditor.export_report()
        self.status.config(text="STATUS: REPORT EXPORTED")


def run_cli() -> None:
    print(BANNER)
    print("OpenNet-Scanner CLI — التدقيق الدفاعي وتدقيق الهندسة الاجتماعية")
    print("1) Local Recon  2) Port Audit  3) Vuln Scan  4) Defensive Check  5) Packet Sniffer  6) Wi-Fi Audit  7) Phishing Link Analysis  8) Export  0) Exit")
    auditor = OpenNetAuditor()
    while True:
        choice = input("\nاختر: ").strip()
        try:
            if choice == "1":
                auditor.local_recon(input("Target/CIDR: "))
            elif choice == "2":
                auditor.port_audit(input("Target: "))
            elif choice == "3":
                if input("أؤكد امتلاكي تصريحاً للفحص؟ (yes/no): ").strip().lower() in {"yes", "y"}:
                    auditor.vulnerability_scan(input("Target: "))
                else:
                    print("[!] تم الإلغاء.")
            elif choice == "4":
                auditor.defensive_posture()
            elif choice == "5":
                auditor.packet_sniffer(20)
            elif choice == "6":
                auditor.wifi_security_audit()
            elif choice == "7":
                auditor.social_engineering_audit(input("أدخل الرابط أو النطاق المراد فحصه: "))
            elif choice == "8":
                auditor.export_report()
            elif choice == "0":
                return
            else:
                print("[!] خيار غير صحيح.")
        except ValueError as exc:
            print(f"[!] {exc}")


def main() -> None:
    wants_gui = "--gui" in sys.argv
    if "--cli" in sys.argv or (not wants_gui and os.environ.get("DISPLAY") is None):
        run_cli()
        return
    if not GUI_AVAILABLE:
        print("[!] Tkinter غير متوفر. ثبّت حزمة python3-tk ثم أعد المحاولة.")
        return
    if not os.environ.get("DISPLAY") and sys.platform != "win32":
        print("[!] لا توجد شاشة عرض رسومية. استخدم وضع --cli.")
        return
    root = tk.Tk()
    CyberGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

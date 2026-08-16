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
import shutil
import subprocess
import sys
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, scrolledtext, ttk
from typing import Callable, Optional


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
║        Authorized Recon · Port Audit · Vulnerability Assessment     ║
╚══════════════════════════════════════════════════════════════════════╝
"""


def timestamp() -> str:
    return datetime.now().isoformat(timespec="seconds")


def validate_target(value: str) -> str:
    """Accept an IP, CIDR network, or hostname without shell interpolation."""
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

    def __init__(self, logger: Optional[Callable[[str], None]] = None):
        self.logger = logger or print
        self.results: dict = {
            "timestamp": timestamp(),
            "tool": "OpenNet-Scanner Defensive Edition",
            "reconnaissance": {},
            "port_scan": {},
            "vulnerability_scan": {},
            "defensive_checks": {},
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
        """Run Nmap's vulnerability-detection scripts; no exploitation is performed."""
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
        """Collect local resolver and routing information without changing the system."""
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
        self.root.geometry("1050x700")
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
        style.configure("Cyber.TButton", background="#122238", foreground=CYAN, padding=8, borderwidth=1, font=("Consolas", 10, "bold"))
        style.map("Cyber.TButton", background=[("active", "#1e3a5f")], foreground=[("disabled", MUTED)])
        style.configure("Cyber.TLabel", background=BG, foreground=WHITE, font=("Consolas", 10))
        style.configure("Cyber.TEntry", fieldbackground=TERMINAL, foreground=WHITE, insertcolor=CYAN)

    def _build_layout(self) -> None:
        header = tk.Frame(self.root, bg=PANEL, padx=18, pady=14)
        header.pack(fill=tk.X)
        tk.Label(header, text="OPENNET-SCANNER // CYBER SECURITY SUITE", bg=PANEL, fg=CYAN, font=("Consolas", 18, "bold")).pack(anchor="w")
        tk.Label(header, text="Defensive auditing only • Authorized targets • No exploitation or interception", bg=PANEL, fg=AMBER, font=("Consolas", 10)).pack(anchor="w", pady=(5, 0))
        tk.Label(header, text="Developer: رامي السامعي (Ramy Al-Samee)", bg=PANEL, fg=GREEN, font=("Consolas", 10)).pack(anchor="w", pady=(3, 0))

        controls = tk.Frame(self.root, bg=BG, padx=14, pady=12)
        controls.pack(fill=tk.X)
        tk.Label(controls, text="Target / نطاق مصرح به:", bg=BG, fg=WHITE, font=("Consolas", 10, "bold")).grid(row=0, column=0, sticky="w")
        self.target_var = tk.StringVar(value="127.0.0.1")
        target_entry = ttk.Entry(controls, textvariable=self.target_var, style="Cyber.TEntry", width=34)
        target_entry.grid(row=0, column=1, padx=(8, 20), sticky="ew")
        controls.columnconfigure(1, weight=1)
        self._button(controls, "LOCAL RECON", self.start_recon, 2)
        self._button(controls, "PORT AUDIT", self.start_ports, 3)
        self._button(controls, "VULN SCAN", self.start_vuln, 4)
        self._button(controls, "DEFENSIVE", self.start_defensive, 5)
        self._button(controls, "FULL AUDIT", self.start_full, 6)
        self._button(controls, "EXPORT JSON", self.export_report, 7)

        terminal_frame = tk.Frame(self.root, bg=BG, padx=14, pady=4)
        terminal_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(terminal_frame, text="LIVE AUDIT TERMINAL", bg=BG, fg=GREEN, font=("Consolas", 10, "bold")).pack(anchor="w")
        self.output = scrolledtext.ScrolledText(terminal_frame, bg=TERMINAL, fg=GREEN, insertbackground=CYAN, selectbackground="#164e63", font=("Consolas", 10), relief="flat", padx=10, pady=10)
        self.output.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        self.output.insert(tk.END, BANNER + "\n[+] GUI جاهزة. أدخل هدفاً مصرحاً به واختر عملية تدقيق.\n")

        footer = tk.Frame(self.root, bg=PANEL, padx=14, pady=7)
        footer.pack(fill=tk.X)
        self.status = tk.Label(footer, text="STATUS: READY", bg=PANEL, fg=MUTED, font=("Consolas", 9, "bold"))
        self.status.pack(side=tk.LEFT)
        tk.Label(footer, text="v4.1 Defensive GUI", bg=PANEL, fg=MUTED, font=("Consolas", 9)).pack(side=tk.RIGHT)

    def _button(self, parent: tk.Frame, text: str, command: Callable[[], None], column: int) -> None:
        ttk.Button(parent, text=text, style="Cyber.TButton", command=command).grid(row=0, column=column, padx=3, sticky="ew")
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

    def _target(self) -> Optional[str]:
        try:
            return validate_target(self.target_var.get())
        except ValueError as exc:
            messagebox.showwarning("هدف غير صالح", str(exc))
            return None

    def _run_async(self, label: str, operation: Callable[[], str]) -> None:
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

    def start_full(self) -> None:
        target = self._target()
        if target and messagebox.askyesno("تأكيد التدقيق الشامل", "هل تملك إذناً صريحاً لتنفيذ التدقيق الشامل على هذا الهدف؟"):
            def full() -> str:
                self.auditor.local_recon(target)
                self.auditor.port_audit(target)
                self.auditor.vulnerability_scan(target)
                return self.auditor.defensive_posture()
            self._run_async("FULL AUDIT", full)

    def export_report(self) -> None:
        self.auditor.export_report()
        self.status.config(text="STATUS: REPORT EXPORTED")


def run_cli() -> None:
    print(BANNER)
    print("OpenNet-Scanner CLI — التدقيق الدفاعي المصرح به فقط")
    print("1) Local Recon  2) Port Audit  3) Vulnerability Scan  4) Defensive Check  5) Export  0) Exit")
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
                    print("[!] تم الإلغاء: يلزم تصريح صريح.")
            elif choice == "4":
                auditor.defensive_posture()
            elif choice == "5":
                auditor.export_report()
            elif choice == "0":
                return
            else:
                print("[!] خيار غير صحيح.")
        except ValueError as exc:
            print(f"[!] {exc}")


def main() -> None:
    if "--cli" in sys.argv or os.environ.get("DISPLAY") is None and "--gui" not in sys.argv:
        run_cli()
        return
    root = tk.Tk()
    CyberGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

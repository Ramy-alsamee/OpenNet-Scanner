# OpenNet-Scanner: The Ultimate Network Security & Attack Arsenal Framework 🛡️

**OpenNet-Scanner (Arsenal Edition)** هو إطار عمل أمني متقدم ومفتوح المصدر، مخصص لأبحاث أمان الشبكات السلكية واللاسلكية، محاكاة هجمات الاختراق، الفحص الشامل للثغرات، واختبار قوة الحماية في البيئات المختلفة.

---

## وحدات الترسانة الأساسية (Arsenal Modules) 🌟

| وحدة التشغيل | الوصف والمهام |
|---|---|
| **1. وحدة الاستطلاع المتقدمة** | اكتشاف الأجهزة الحية على النطاق المحلي باستخدام `ARP Scan` و `Nmap` السريع. |
| **2. وحدة الهجمات اللاسلكية** | فحص الشبكات المحيطة، محاكاة التقاط حزم التوثيق (Handshake)، واختبار هجمات قطع الاتصال (Deauth). |
| **3. وحدة الاعتراض والهجمات في المنتصف (MITM)** | فحص جداول ARP، اختبار توجيه النطاقات (DNS Spoofing)، وفحص قنوات الاتصال غير المشفرة. |
| **4. وحدة فحص الثغرات والخدمات (CVE)** | تشغيل محرك Nmap Vuln Scripts لفحص الثغرات المعروفة في الخدمات النشطة. |
| **5. فحص الترسانة الشامل** | تنفيذ دورة فحص واستطلاع كاملة بضغطة زر واحدة. |
| **6. تصدير التقارير الذكية** | تصدير النتائج بصيغتي **JSON** و **HTML** بتصميم احترافي ومنظم. |

---

## المتطلبات ونظام التشغيل 💻

- **النظام المدعوم:** Linux (Kali Linux, Debian, Ubuntu, Termux مع الصلاحيات المناسبة).
- **الصلاحيات:** يتطلب تشغيل بعض الوحدات المتقدمة صلاحيات الجذر (`sudo`).
- **Python:** الإصدار 3.x مع الأدوات الأساسية.

---

## التثبيت والاستخدام 🛠️

### 1. استنساخ المستودع
```bash
git clone https://github.com/Ramy-alsamee/OpenNet-Scanner.git
cd OpenNet-Scanner
```

### 2. تشغيل الترسانة
```bash
sudo python3 opennet_scanner.py
```

---

## حقوق الملكية

حقوق الطبع والنشر © 2026 **رامي السامعي (Ramy Al-Samee)**. مرخّص بموجب رخصة MIT.

---

## English Summary

**OpenNet-Scanner (Arsenal Edition)** is a modular network security and attack simulation framework. It integrates advanced reconnaissance, wireless attack simulations, MITM inspection, CVE vulnerability scanning, and automated JSON/HTML report generation into a single interactive tool.

### Usage
```bash
git clone https://github.com/Ramy-alsamee/OpenNet-Scanner.git
cd OpenNet-Scanner
sudo python3 opennet_scanner.py
```

*Developed for educational and authorized security research purposes only.*

# OpenNet Scanner — Public Wi-Fi Security Research Tool 🛡️

**OpenNet Scanner** هو أداة متقدمة ومتكاملة لأبحاث أمان الشبكات اللاسلكية العامة والمفتوحة (Public Wi-Fi). تقوم الأداة بتثبيت المتطلبات تلقائياً، فحص جميع الثغرات المعروفة في الشبكات المفتوحة، تقديم تقارير تفصيلية، ومن ثم سؤال المستخدم حول ما إذا كان يريد مواصلة العمل وتطبيق الفحص المتقدم.

---

## الميزات الرئيسية 🌟

| الميزة | الوصف |
|---|---|
| **تثبيت تلقائي للمتطلبات** | تقوم الأداة تلقائياً بفحص وتثبيت جميع الأدوات اللازمة (`nmap`, `arp-scan`, `tcpdump`, `dsniff`, إلخ). |
| **مسح الشبكات المفتوحة** | اكتشاف شبكات Wi-Fi المحيطة غير المشفرة وتحليل حالتها. |
| **فحص بوابات الويب المقيدة** | الكشف عن بوابات Captive Portals وطرق تجاوزها المختلفة. |
| **كشف تسريب البيانات** | توضيح خطورة إرسال البيانات بدون تشفير على الشبكات العامة. |
| **فحص ARP Spoofing / MITM** | تقييم إمكانية تنفيذ هجمات الرجل في المنتصف واعتراض الحركة. |
| **مخاطر شبكات Evil Twin** | فحص مخاطر الشبكات الوهمية والمقلدة التي تخدع الأجهزة. |
| **فحص عزل الأجهزة** | اكتشاف مدى إمكانية الوصول إلى الأجهزة الأخرى المتصلة بنفس الشبكة. |
| **واجهة تفاعلية ذكية** | عرض ملخص شامل للثغرات وسؤال المستخدم قبل المتابعة في الاستغلال. |

---

## المتطلبات ونظام التشغيل 💻

- **النظام:** Linux (Kali Linux, Debian, Ubuntu, أو أي توزيعة تدعم أدوات الشبكات).
- **الصلاحيات:** يتطلب تشغيل الأداة بصلاحيات الجذر (`sudo`).
- **Python:** الإصدار 3.x مع مكتبة `requests` (إن وجدت).

---

## التثبيت والاستخدام 🛠️

### 1. استنساخ المستودع وتثبيت الأداة

```bash
git clone https://github.com/Ramy-alsamee/OpenNet-Scanner.git
cd OpenNet-Scanner
```

### 2. التشغيل

قم بتشغيل الأداة بصلاحيات الجذر:

```bash
sudo python3 opennet_scanner.py
```

أو لتحديد واجهة شبكة معينة (مثل `wlan0`):

```bash
sudo python3 opennet_scanner.py wlan0
```

---

## إخلاء مسؤولية قانونية ⚖️

هذه الأداة مخصصة حصرياً لأغراض البحث الأمني المشروع، اختبار أمان شبكاتك الخاصة، والوعي السيبراني. لا يتحمل المطور أي مسؤولية قانونية عن أي استخدام غير قانوني أو ضار لهذه الأداة. استخدمها فقط في الأجهزة والشبكات التي تملكها أو لديك إذن صريح لاختبارها.

---

## English Summary

**OpenNet Scanner** is an advanced open-source security research tool designed to analyze public and open Wi-Fi networks. It automatically installs required dependencies, scans for common vulnerabilities (such as lack of encryption, captive portals, MITM vulnerability, Evil Twin risks, and device isolation failures), generates detailed reports, and provides an interactive decision workflow for authorized security assessments.

### Installation & Usage

```bash
git clone https://github.com/Ramy-alsamee/OpenNet-Scanner.git
cd OpenNet-Scanner
sudo python3 opennet_scanner.py
```

---
*Developed for educational and authorized security research purposes only.*

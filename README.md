# OpenNet-Scanner: Cyber GUI & Defensive Auditing Framework 🛡️

**OpenNet-Scanner** هو إطار عمل مهني ومفتوح المصدر لتدقيق أمان الشبكات، الاستطلاع الآمن، فحص المنافذ، فحص الثغرات (Vulnerability Scanner)، مراقبة حزم الشبكة (Packet Sniffer)، تدقيق أمان شبكات الواي فاي (Wi-Fi Security Audit)، وتحليل روابط الهندسة الاجتماعية والتصيد الاحتيالي (Social Engineering Audit)، مع دعم **واجهة رسومية هكرية احترافية (Cyber Hacker GUI)** وإصدار تنفيذي مستقل لنظام ويندوز (`.exe`).

---

## الميزات الرئيسية 🌟

| الوحدة | الوصف |
|---|---|
| **الواجهة الرسومية (Cyber GUI)** | واجهة داكنة مخصصة للمختبرين الأمنيين مع أزرار تشغيل ومحطة عرض نتائج فورية. |
| **الاستطلاع المحلي** | اكتشاف الأجهزة النشطة داخل نطاق الشبكة بشكل آمن وغير تدميري. |
| **فحص المنافذ والخدمات** | رصد المنافذ المفتوحة وتحديد إصدارات الخدمات (Port & Service Audit). |
| **فحص الثغرات الشائعة** | تشغيل محرك سكربتات فحص الثغرات (Nmap Vuln Scripts) لاكتشاف الثغرات المعروفة (CVE). |
| **مراقبة الحزم (Packet Sniffer)** | التقاط وتحليل رؤوس حزم الشبكة الحية (Packet Headers) لاكتشاف النشاط المشبوه عبر `tcpdump`. |
| **تدقيق الواي فاي (Wi-Fi Audit)** | مسح الشبكات اللاسلكية المحيطة وتقييم أنواع التشفير وحالة الحماية عبر `nmcli` / `iwlist`. |
| **تدقيق الهندسة الاجتماعية** | تحليل الروابط والنطاقات المشبوهة واكتشاف مؤشرات التصيد الاحتيالي (Phishing Indicators). |
| **التقييم الدفاعي** | مراجعة إعدادات الشبكة وخوادم DNS والسياسات الأمنية. |

---

## كيفية الحصول على الملف التنفيذي (.exe) لويندوز 🪟

يوفر المشروع نظام بناء آلي عبر **GitHub Actions** لبناء ملف الـ `.exe` تلقائياً دون الحاجة لتثبيت بايثون:
1. اذهب إلى علامة التبويب **Actions** في أعلى مستودعك على GitHub.
2. اختر آخر عملية بناء ناجحة لـ **"Build Windows Executable (.exe)"**.
3. قم بتنزيل ملف الـ Artifact المسمى **OpenNet-Scanner-Windows-Exe** والذي يحتوي على ملف `opennet_scanner.exe` جاهزاً للتشغيل المباشر.

---

## المتطلبات والتشغيل 🛠️

### التشغيل كملف بايثون (Linux / Kali / Termux):
```bash
python3 opennet_scanner.py --gui   # للواجهة الرسومية
python3 opennet_scanner.py --cli   # لوضع الطرفية
```

---

## حقوق الملكية

حقوق الطبع والنشر © 2026 **رامي السامعي (Ramy Al-Samee)**. مرخّص بموجب رخصة MIT.

---

## English Summary

**OpenNet-Scanner** is a professional defensive network auditing and vulnerability assessment framework featuring a dedicated **Cyber Hacker GUI**, port scanner, vulnerability assessment, packet sniffer, Wi-Fi security audit, social engineering analysis, and automatic **Windows Executable (.exe)** build support via GitHub Actions.

*Developed for authorized security assessments and educational purposes only.*

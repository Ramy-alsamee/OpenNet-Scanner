# OpenNet-Scanner: Cyber GUI & Defensive Auditing Framework 🛡️

**OpenNet-Scanner** هو إطار عمل مهني ومفتوح المصدر لتدقيق أمان الشبكات، الاستطلاع الآمن، فحص المنافذ، فحص الثغرات (Vulnerability Scanner)، مراقبة حزم الشبكة (Packet Sniffer)، تدقيق أمان شبكات الواي فاي (Wi-Fi Security Audit)، وتحليل روابط الهندسة الاجتماعية والتصيد الاحتيالي (Social Engineering Audit)، مع دعم **واجهة رسومية هكرية احترافية (Cyber Hacker GUI)**.

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

## المتطلبات والتشغيل 🛠️

يتطلب تشغيل الفحوصات والأدوات تثبيت الحزم الأساسية التالية في نظامك (Debian/Ubuntu/Kali):

```bash
sudo apt update && sudo apt install -y python3-tk nmap tcpdump network-manager wireless-tools
```

### 1. تشغيل الوضع التفاعلي (CLI Mode)

```bash
python3 opennet_scanner.py --cli
```

### 2. تشغيل الواجهة الرسومية (Cyber GUI Mode)

```bash
python3 opennet_scanner.py --gui
```

أو شغّل `python3 opennet_scanner.py` داخل جلسة سطح مكتب. من الواجهة يمكنك إدخال رابط أو نطاق مشبوه والضغط على **PHISH CHECK** لتحليله أمنياً، أو تشغيل باقي الفحوصات وتصدير تقرير JSON.

---

## حقوق الملكية

حقوق الطبع والنشر © 2026 **رامي السامعي (Ramy Al-Samee)**. مرخّص بموجب رخصة MIT.

---

## English Summary

**OpenNet-Scanner** is a professional defensive network auditing and vulnerability assessment framework featuring a dedicated **Cyber Hacker GUI**, port scanner, vulnerability assessment, packet sniffer, Wi-Fi security audit, and **Social Engineering / Phishing Link Analysis** module.

*Developed for authorized security assessments and educational purposes only.*

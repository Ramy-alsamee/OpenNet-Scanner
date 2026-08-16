# OpenNet-Scanner: Cyber GUI & Defensive Auditing Framework 🛡️

**OpenNet-Scanner** هو إطار عمل مهني ومفتوح المصدر لتدقيق أمان الشبكات، الاستطلاع الآمن، فحص المنافذ، فحص الثغرات (Vulnerability Scanner)، مع دعم **واجهة رسومية هكرية احترافية (Cyber Hacker GUI)**.

---

## الميزات الرئيسية 🌟

| الوحدة | الوصف |
|---|---|
| **الواجهة الرسومية (Cyber GUI)** | واجهة داكنة مخصصة للمختبرين الأمنيين مع أزرار تشغيل ومحطة عرض نتائج فورية. |
| **الاستطلاع المحلي** | اكتشاف الأجهزة النشطة داخل نطاق الشبكة بشكل آمن وغير تدميري. |
| **فحص المنافذ والخدمات** | رصد المنافذ المفتوحة وتحديد إصدارات الخدمات (Port & Service Audit). |
| **فحص الثغرات الشائعة** | تشغيل محرك سكربتات فحص الثغرات (Nmap Vuln Scripts) لاكتشاف الثغرات المعروفة (CVE). |
| **التقييم الدفاعي** | مراجعة إعدادات الشبكة وخوادم DNS والسياسات الأمنية. |

---

## المتطلبات والتشغيل 🛠️

يتطلب وضع الواجهة الرسومية Python وTkinter وبيئة سطح مكتب تحتوي على شاشة عرض. في Debian/Ubuntu/Kali يمكنك تثبيت Tkinter بالأمر التالي:

```bash
sudo apt update && sudo apt install -y python3-tk nmap
```

### 1. تشغيل الوضع التفاعلي (CLI Mode)

```bash
python3 opennet_scanner.py --cli
```

يُستخدم هذا الوضع في Termux أو الخوادم أو أي بيئة لا تحتوي على شاشة رسومية.

### 2. تشغيل الواجهة الرسومية (Cyber GUI Mode)

```bash
python3 opennet_scanner.py --gui
```

أو شغّل `python3 opennet_scanner.py` داخل جلسة سطح مكتب؛ وفي البيئة الرسومية ستفتح الواجهة تلقائياً. من الواجهة يمكنك إدخال هدف مصرح به وتشغيل **Local Recon** و**Port Audit** و**Vuln Scan** و**Defensive Check** ثم تصدير تقرير JSON.

*(لا يعمل وضع GUI عبر جلسة SSH أو Termux النصية وحدها من دون خادم عرض مثل X11/VNC.)*

---

## حقوق الملكية

حقوق الطبع والنشر © 2026 **رامي السامعي (Ramy Al-Samee)**. مرخّص بموجب رخصة MIT.

---

## English Summary

**OpenNet-Scanner** is a professional defensive network auditing and vulnerability assessment framework featuring a dedicated **Cyber Hacker GUI** alongside the CLI mode.

*Developed for authorized security assessments and educational purposes only.*

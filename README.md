# 📱 IPTV Player - مشغل القنوات التلفزيونية

تطبيق Android بسيط وسريع لتشغيل قنوات IPTV من ملفات M3U

## ✨ المميزات

- ✅ تشغيل قوائم M3U من روابط مباشرة
- ✅ بحث سريع في القنوات
- ✅ واجهة عربية بسيطة
- ✅ دعم HTTP/HTTPS streaming
- ✅ حفظ آخر رابط مستخدم
- ✅ تشغيل تلقائي للقنوات

## 🚀 كيفية البناء

### الطريقة 1: باستخدام Buildozer (Linux)

```bash
# تثبيت المتطلبات
sudo apt update
sudo apt install -y python3-pip git zip unzip openjdk-17-jdk \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# تثبيت buildozer
pip3 install --user buildozer cython

# بناء APK
cd /opt/data/iptv_player
buildozer android debug
```

### الطريقة 2: عبر GitHub Actions (أسهل)

1. ارفع المشروع لـ GitHub
2. استخدم الـ workflow المرفق (`.github/workflows/build.yml`)
3. APK يُبنى تلقائياً في كل commit

### الطريقة 3: عبر خدمات أونلاين

استخدم خدمات مثل:
- **Replit** (مجاني)
- **Google Colab** (مجاني)
- **GitHub Codespaces** (مجاني محدود)

## 📦 تشغيل التطبيق محلياً (للتجربة)

```bash
# تثبيت kivy
pip3 install kivy requests

# تشغيل
python3 main.py
```

## 🎯 كيفية الاستخدام

1. **إضافة رابط M3U**: 
   - أدخل رابط قائمة M3U في الحقل العلوي
   - مثال: `http://example.com/playlist.m3u`

2. **تحميل القنوات**: 
   - اضغط على زر "تحميل"

3. **البحث**: 
   - استخدم حقل البحث للعثور على قناة معينة

4. **المشاهدة**: 
   - اضغط على اسم القناة لتشغيلها

## 🔧 ملاحظات تقنية

- **الحد الأدنى لنظام Android**: 5.0 (API 21)
- **الحجم التقريبي**: ~15-20 MB
- **الأذونات المطلوبة**:
  - الإنترنت (لتحميل القنوات)
  - الشبكة (للتحقق من الاتصال)
  - التخزين (لحفظ الإعدادات)

## ⚠️ إخلاء مسؤولية

هذا التطبيق مشغل فقط - لا يوفر محتوى IPTV. المستخدم مسؤول عن استخدام روابط قانونية ومصرح بها.

## 🛠️ التطوير المستقبلي

- [ ] دعم EPG (دليل البرامج)
- [ ] قوائم مفضلة
- [ ] التحكم في الجودة
- [ ] دعم Chromecast
- [ ] سجل المشاهدة
- [ ] وضع الصورة داخل صورة (PIP)

## 📄 الترخيص

MIT License - استخدم بحرية، طوّر، شارك!

---

**تم البناء بواسطة**: Hussam (حسام)  
**التاريخ**: نوفمبر 2026

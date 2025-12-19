# 🏢 YBS Apartmanı Şikayet Yönetim Sistemi

Apartman sakinlerinin şikayetlerini güvenli ve şeffaf bir şekilde yönetmelerine olanak sağlayan modern web uygulaması.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Demo-Live-success.svg)](https://serdarbayar.pythonanywhere.com)


## 🎯 Proje Hakkında

YBS Apartmanı Şikayet Yönetim Sistemi, apartman sakinlerinin günlük sorunlarını yöneticilere iletmesini ve takip etmesini kolaylaştıran bir web platformudur. Sistem, anonim şikayet özelliği, kategori bazlı filtreleme ve gerçek zamanlı durum takibi gibi özellikleriyle site yönetimini dijitalleştirir.

### ✨ Temel Özellikler

#### 👥 Kullanıcı Yönetimi
- Telefon numarası ile hızlı kayıt
- Güvenli giriş sistemi (Flask-Login)
- İki kullanıcı rolü: **Sakin** ve **Yönetici**
- Şifreler bcrypt ile hashlenmiş olarak saklanır

#### 📝 Şikayet Sistemi
- **Anonim** veya **açık** şikayet oluşturma
- Kategori seçimi (Temizlik, Aidat, Güvenlik, Teknik Arıza, Diğer)
- Durum takibi: Yeni, İşleniyor, Çözüldü, Reddedildi
- Detaylı açıklama ve başlık alanları

#### 🔧 Yönetici Paneli
- Tüm şikayetleri görüntüleme
- Durum ve kategoriye göre filtreleme
- Şikayet durumu güncelleme
- Not ekleme (görünür/gizli)
- Anonim şikayetleri yönetme

#### 🔒 Güvenlik ve Gizlilik
- Anonim şikayetlerde kullanıcı bilgisi saklanmaz
- Şifreler bcrypt ile şifrelenir
- Yönetici notlarının görünürlük kontrolü
- Oturum yönetimi (Flask-Login)

---

## 🛠️ Teknoloji Yığını

### Backend
- **Python 3.10+**
- **Flask 3.0.0** - Web Framework
- **SQLAlchemy** - ORM (Object-Relational Mapping)
- **Flask-Login** - Oturum Yönetimi
- **Flask-Bcrypt** - Şifreleme
- **SQLite** - Veritabanı

### Frontend
- **HTML5 & CSS3**
- **Bootstrap 5.3** - Responsive Design
- **Jinja2** - Template Engine
- **JavaScript** - İnteraktif Özellikler

### Deployment
- **PythonAnywhere** - Hosting Platform

---

## 📦 Kurulum

### Gereksinimler
- Python 3.10 veya üzeri
- pip (Python paket yöneticisi)

### Adım 1: Projeyi Klonlayın
```bash
git clone https://github.com/Serdarbayar0/bina-sikayet-sistemi.git
cd bina-sikayet-sistemi
```

### Adım 2: Sanal Ortam Oluşturun
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Adım 3: Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 4: Veritabanını Başlatın ve Uygulamayı Çalıştırın
```bash
python app.py
```

Uygulama varsayılan olarak `http://127.0.0.1:5000` adresinde çalışacaktır.

---

## 🗄️ Veritabanı Yapısı

### Tablolar

#### `kullanicilar`
| Alan | Tip | Açıklama |
|------|-----|----------|
| id | Integer | Birincil anahtar |
| telefon_no | String(20) | Benzersiz telefon numarası |
| sifre_hash | String(200) | Hashlenmiş şifre |
| daire_no | String(10) | Daire numarası |
| rol | String(20) | sakin veya yonetici |
| olusturma_tarihi | DateTime | Kayıt tarihi |

#### `kategoriler`
| Alan | Tip | Açıklama |
|------|-----|----------|
| id | Integer | Birincil anahtar |
| ad | String(50) | Kategori adı |

#### `sikayetler`
| Alan | Tip | Açıklama |
|------|-----|----------|
| id | Integer | Birincil anahtar |
| kullanici_id | Integer | Kullanıcı FK (NULL ise anonim) |
| kategori_id | Integer | Kategori FK |
| baslik | String(200) | Şikayet başlığı |
| aciklama | Text | Detaylı açıklama |
| durum | String(20) | Yeni/İşleniyor/Çözüldü/Reddedildi |
| is_anonymous | Boolean | Anonim mi? |
| olusturma_tarihi | DateTime | Oluşturma tarihi |
| guncelleme_tarihi | DateTime | Güncellenme tarihi |

#### `sikayet_notlari`
| Alan | Tip | Açıklama |
|------|-----|----------|
| id | Integer | Birincil anahtar |
| sikayet_id | Integer | Şikayet FK |
| kullanici_id | Integer | Yazan kullanıcı FK |
| not_icerigi | Text | Not içeriği |
| rol | String(20) | sakin veya yonetici |
| is_visible_to_sakin | Boolean | Sakine görünür mü? |
| olusturma_tarihi | DateTime | Oluşturma tarihi |

---

## 🚀 Kullanım

### Demo Hesap Bilgileri

#### Yönetici Girişi
```
Telefon: admin
Şifre: admin
```

#### Yeni Sakin Kaydı
1. Ana sayfadan "Kayıt Ol" butonuna tıklayın
2. Telefon numarası, daire numarası ve şifre girin
3. Kayıt olduktan sonra giriş yapabilirsiniz

### Temel İşlemler

#### Sakin Olarak:
1. Giriş yapın
2. "Yeni Şikayet Oluştur" butonuna tıklayın
3. Kategori seçin, başlık ve açıklama girin
4. İsterseniz "Anonim olarak bildir" seçeneğini işaretleyin
5. Şikayetinizin durumunu panelinden takip edin

#### Yönetici Olarak:
1. Admin hesabıyla giriş yapın
2. Tüm şikayetleri görüntüleyin
3. Filtreleme yapın (durum/kategori)
4. Şikayet detayına girin
5. Durum güncelleyin veya not ekleyin

---

## 📂 Proje Yapısı
```
bina-sikayet-sistemi/
│
├── app.py                      # Ana uygulama dosyası
├── models.py                   # Veritabanı modelleri
├── config.py                   # Yapılandırma ayarları (opsiyonel)
├── forms.py                    # Form sınıfları (opsiyonel)
├── requirements.txt            # Python bağımlılıkları
│
├── templates/                  # HTML şablonları
│   ├── base.html              # Ana şablon
│   ├── index.html             # Ana sayfa
│   ├── giris.html             # Giriş sayfası
│   ├── kayit.html             # Kayıt sayfası
│   ├── sakin_panel.html       # Sakin paneli
│   ├── yonetici_panel.html    # Yönetici paneli
│   ├── sikayet_olustur.html   # Şikayet oluşturma
│   └── sikayet_detay.html     # Şikayet detayları
│
├── static/                     # Statik dosyalar
│   ├── css/
│   │   └── style.css          # Özel stiller
│   ├── js/
│   │   └── main.js            # JavaScript dosyaları
│   └── uploads/               # Yüklenen dosyalar
│
└── instance/                   # Veritabanı (otomatik oluşur)
    └── database.db
```

---

## 🌐 Canlı Demo

Projenin canlı versiyonunu şu adresten test edebilirsiniz:

🔗 **[serdarbayar.pythonanywhere.com](https://serdarbayar.pythonanywhere.com)**

---

## 🔧 Geliştirme

### Yerel Geliştirme Ortamı
```bash
# Debug mode ile çalıştırma
python app.py

# Veritabanını sıfırlama
rm instance/database.db
python app.py
```

### Yeni Özellik Ekleme

1. `models.py` dosyasından veritabanı modelini güncelleyin
2. `app.py` dosyasına yeni route ekleyin
3. İlgili HTML template'ini `templates/` klasörüne ekleyin
4. Gerekirse `static/` klasöründe CSS/JS güncelleyin

---

## 📝 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 👤 Geliştirici

**Serdar BAYAR**

- GitHub: [@Serdarbayar0](https://github.com/Serdarbayar0)
- Website: [serdarbayar.pythonanywhere.com](https://serdarbayar.pythonanywhere.com)

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen aşağıdaki adımları izleyin:

1. Projeyi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`)
5. Pull Request oluşturun

---

## 📧 İletişim

Sorularınız veya önerileriniz için:
- **Email:** serdarbayar1305@gmail.com
- **Issue:** [GitHub Issues](https://github.com/Serdarbayar0/bina-sikayet-sistemi/issues)

---

## 🙏 Teşekkürler

Bu projeyi geliştirirken şu kaynaklardan faydalandım:
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [PythonAnywhere Documentation](https://help.pythonanywhere.com/)

---

## ⭐ Yıldız Vermeyi Unutmayın!

Projeyi beğendiyseniz, lütfen bir ⭐ vererek destek olun!

---

<div align="center">

**Created with ❤️ by Serdar BAYAR**

</div>
```

---

## 📋 Ek: README.md İçin Gerekli Dosyalar

### 1. `screenshots/` klasörü oluşturun ve ekran görüntülerini ekleyin:
```
screenshots/
├── homepage.png
├── admin-panel.png
└── complaint-detail.png
```

### 2. `LICENSE` dosyası oluşturun (MIT License):
```
MIT License

Copyright (c) 2025 Serdar BAYAR

Permission is hereby granted, free of charge, to any person obtaining a copy...
```

### 3. `.gitignore` dosyası oluşturun:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Flask
instance/
.webassets-cache

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite
*.sqlite3

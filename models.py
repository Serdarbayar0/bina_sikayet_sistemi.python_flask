from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Kullanici(UserMixin, db.Model):
    __tablename__ = 'kullanicilar'
    
    id = db.Column(db.Integer, primary_key=True)
    telefon_no = db.Column(db.String(20), unique=True, nullable=False)
    sifre_hash = db.Column(db.String(200), nullable=False)
    daire_no = db.Column(db.String(10), nullable=False)
    rol = db.Column(db.String(20), default='sakin')  # 'sakin' veya 'yonetici'
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    sikayetler = db.relationship('Sikayet', backref='kullanici', lazy=True)
    notlar = db.relationship('SikayetNotu', backref='yazar', lazy=True)

class Kategori(db.Model):
    __tablename__ = 'kategoriler'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(50), nullable=False)
    
    sikayetler = db.relationship('Sikayet', backref='kategori', lazy=True)

class Sikayet(db.Model):
    __tablename__ = 'sikayetler'
    
    id = db.Column(db.Integer, primary_key=True)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('kullanicilar.id'), nullable=True)
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategoriler.id'), nullable=False)
    baslik = db.Column(db.String(200), nullable=False)
    aciklama = db.Column(db.Text, nullable=False)
    durum = db.Column(db.String(20), default='Yeni')  # Yeni, İşleniyor, Çözüldü, Reddedildi
    is_anonymous = db.Column(db.Boolean, default=False)
    dosya_yolu = db.Column(db.String(300))
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    guncelleme_tarihi = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    notlar = db.relationship('SikayetNotu', backref='sikayet', lazy=True, cascade='all, delete-orphan')

class SikayetNotu(db.Model):
    __tablename__ = 'sikayet_notlari'
    
    id = db.Column(db.Integer, primary_key=True)
    sikayet_id = db.Column(db.Integer, db.ForeignKey('sikayetler.id'), nullable=False)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('kullanicilar.id'), nullable=False)
    not_icerigi = db.Column(db.Text, nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # 'sakin' veya 'yonetici'
    is_visible_to_sakin = db.Column(db.Boolean, default=True)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
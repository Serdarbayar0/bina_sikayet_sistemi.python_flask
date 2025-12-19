from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models import db, Kullanici, Kategori, Sikayet, SikayetNotu
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli-anahtar-buraya-rastgele-string-12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Uzantıları başlat
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'giris'
login_manager.login_message = 'Lütfen giriş yapın.'

@login_manager.user_loader
def load_user(user_id):
    return Kullanici.query.get(int(user_id))

# Ana sayfa
@app.route('/')
def index():
    return render_template('index.html')

# Kayıt olma
@app.route('/kayit', methods=['GET', 'POST'])
def kayit():
    if current_user.is_authenticated:
        return redirect(url_for('sakin_panel'))
    
    if request.method == 'POST':
        telefon = request.form.get('telefon')
        sifre = request.form.get('sifre')
        daire = request.form.get('daire')
        
        # Telefon kontrolü
        if Kullanici.query.filter_by(telefon_no=telefon).first():
            flash('Bu telefon numarası zaten kayıtlı!', 'danger')
            return redirect(url_for('kayit'))
        
        # Şifreyi hashle
        hashed_sifre = bcrypt.generate_password_hash(sifre).decode('utf-8')
        
        # Yeni kullanıcı oluştur
        yeni_kullanici = Kullanici(
            telefon_no=telefon,
            sifre_hash=hashed_sifre,
            daire_no=daire,
            rol='sakin'
        )
        
        db.session.add(yeni_kullanici)
        db.session.commit()
        
        flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
        return redirect(url_for('giris'))
    
    return render_template('kayit.html')

# Giriş yapma
@app.route('/giris', methods=['GET', 'POST'])
def giris():
    if current_user.is_authenticated:
        if current_user.rol == 'yonetici':
            return redirect(url_for('yonetici_panel'))
        return redirect(url_for('sakin_panel'))
    
    if request.method == 'POST':
        telefon = request.form.get('telefon')
        sifre = request.form.get('sifre')
        
        kullanici = Kullanici.query.filter_by(telefon_no=telefon).first()
        
        if kullanici and bcrypt.check_password_hash(kullanici.sifre_hash, sifre):
            login_user(kullanici)
            flash('Giriş başarılı!', 'success')
            
            if kullanici.rol == 'yonetici':
                return redirect(url_for('yonetici_panel'))
            return redirect(url_for('sakin_panel'))
        else:
            flash('Telefon veya şifre hatalı!', 'danger')
    
    return render_template('giris.html')

# Çıkış yapma
@app.route('/cikis')
@login_required
def cikis():
    logout_user()
    flash('Çıkış yaptınız.', 'info')
    return redirect(url_for('index'))

# Sakin Paneli
@app.route('/sakin-panel')
@login_required
def sakin_panel():
    if current_user.rol != 'sakin':
        return redirect(url_for('yonetici_panel'))
    
    # Sadece anonim olmayan şikayetleri getir
    sikayetler = Sikayet.query.filter_by(
        kullanici_id=current_user.id,
        is_anonymous=False
    ).order_by(Sikayet.olusturma_tarihi.desc()).all()
    
    return render_template('sakin_panel.html', sikayetler=sikayetler)

# Yönetici Paneli
@app.route('/yonetici-panel')
@login_required
def yonetici_panel():
    if current_user.rol != 'yonetici':
        return redirect(url_for('sakin_panel'))
    
    durum_filtre = request.args.get('durum')
    kategori_filtre = request.args.get('kategori')
    
    query = Sikayet.query
    
    if durum_filtre:
        query = query.filter_by(durum=durum_filtre)
    if kategori_filtre:
        query = query.filter_by(kategori_id=kategori_filtre)
    
    sikayetler = query.order_by(Sikayet.olusturma_tarihi.desc()).all()
    kategoriler = Kategori.query.all()
    
    return render_template('yonetici_panel.html', sikayetler=sikayetler, kategoriler=kategoriler)

# Şikayet oluşturma
@app.route('/sikayet-olustur', methods=['GET', 'POST'])
@login_required
def sikayet_olustur():
    if request.method == 'POST':
        baslik = request.form.get('baslik')
        aciklama = request.form.get('aciklama')
        kategori_id = request.form.get('kategori')
        anonim = request.form.get('anonim') == 'on'
        
        # Anonim şikayetlerde kullanici_id None olacak
        yeni_sikayet = Sikayet(
            kullanici_id=None if anonim else current_user.id,
            kategori_id=kategori_id,
            baslik=baslik,
            aciklama=aciklama,
            is_anonymous=anonim,
            durum='Yeni'
        )
        
        db.session.add(yeni_sikayet)
        db.session.commit()
        
        flash('Şikayetiniz başarıyla oluşturuldu!', 'success')
        return redirect(url_for('sakin_panel'))
    
    kategoriler = Kategori.query.all()
    return render_template('sikayet_olustur.html', kategoriler=kategoriler)

# Şikayet detayı
@app.route('/sikayet/<int:id>', methods=['GET', 'POST'])
@login_required
def sikayet_detay(id):
    sikayet = Sikayet.query.get_or_404(id)
    
    # Yetki kontrolü
    if current_user.rol == 'sakin':
        # Anonim şikayetleri sakin göremez
        if sikayet.is_anonymous:
            flash('Bu şikayeti görme yetkiniz yok!', 'danger')
            return redirect(url_for('sakin_panel'))
        # Kendi şikayeti değilse göremez
        if sikayet.kullanici_id != current_user.id:
            flash('Bu şikayeti görme yetkiniz yok!', 'danger')
            return redirect(url_for('sakin_panel'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        # Durum güncelleme (Sadece yönetici)
        if action == 'update_status' and current_user.rol == 'yonetici':
            yeni_durum = request.form.get('durum')
            sikayet.durum = yeni_durum
            sikayet.guncelleme_tarihi = datetime.utcnow()
            db.session.commit()
            flash('Şikayet durumu güncellendi!', 'success')
        
        # Not ekleme (Sadece yönetici)
        elif action == 'add_note' and current_user.rol == 'yonetici':
            not_icerigi = request.form.get('not_icerigi')
            gorunur = request.form.get('gorunur') == 'on'
            
            yeni_not = SikayetNotu(
                sikayet_id=sikayet.id,
                kullanici_id=current_user.id,
                not_icerigi=not_icerigi,
                rol='yonetici',
                is_visible_to_sakin=gorunur
            )
            
            db.session.add(yeni_not)
            db.session.commit()
            flash('Not eklendi!', 'success')
        
        return redirect(url_for('sikayet_detay', id=id))
    
    return render_template('sikayet_detay.html', sikayet=sikayet)

# Veritabanını başlat
def init_db():
    with app.app_context():
        db.create_all()
        
        # Demo veriler ekle
        if not Kullanici.query.filter_by(telefon_no='admin').first():
            admin = Kullanici(
                telefon_no='admin',
                sifre_hash=bcrypt.generate_password_hash('admin').decode('utf-8'),
                daire_no='YÖNETİM',
                rol='yonetici'
            )
            db.session.add(admin)
        
        if Kategori.query.count() == 0:
            kategoriler = ['Temizlik', 'Aidat', 'Güvenlik', 'Teknik Arıza', 'Diğer']
            for kat in kategoriler:
                db.session.add(Kategori(ad=kat))
        
        db.session.commit()
        print('✅ Veritabanı başlatıldı!')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
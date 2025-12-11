# app.py

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Uygulama ve Veritabanı Ayarları
app = Flask(__name__)
# Gizli Anahtar: Çevre değişkeni olarak ayarlanması önerilir. Basitlik için buraya yazıldı.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cok_guclu_gizli_anahtar_buraya_yazilmalidir_12345')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Kullanıcı Giriş Yönetimi
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Giriş yapılmamış kullanıcılar buraya yönlendirilir
login_manager.login_message_category = 'info'
login_manager.login_message = 'Bu sayfaya erişmek için lütfen giriş yapın.'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login için kullanıcı yükleyici fonksiyon."""
    return User.query.get(int(user_id))


# --- Veritabanı Modelleri ---

class User(db.Model, UserMixin):
    """Kullanıcı Bilgileri Modeli"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    # Goal modeli ile ilişki
    goals = db.relationship('Goal', backref='user', lazy='dynamic', cascade="all, delete-orphan")


class Goal(db.Model):
    """Hedef/Başarı Modeli"""
    id = db.Column(db.Integer, primary_key=True)
    # 'achieved' (başarılan/geçmiş yıl) veya 'future' (gelecek yıl hedefi)
    type = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# --- Yönlendirmeler (Routes) ---

@app.route('/')
def home():
    """Ana Geri Sayım Sayfası"""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Giriş Sayfası"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)  # Beni hatırla
            flash(f'Hoş geldiniz, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Kullanıcı adı veya şifre hatalı.', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Kayıt Sayfası"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Basit doğrulama
        if not username or not password or len(username) < 3 or len(password) < 6:
            flash('Kullanıcı adı en az 3, şifre en az 6 karakter olmalıdır.', 'error')
            return redirect(url_for('register'))

        # Kullanıcı adının benzersizliğini kontrol et
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Bu kullanıcı adı zaten alınmış. Lütfen başka bir tane deneyin.', 'error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Kayıt başarılı! Lütfen giriş yapın.', 'success')
            return redirect(url_for('login'))
        except Exception:
            db.session.rollback()
            flash('Kayıt sırasında bir hata oluştu.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    """Çıkış Yapma"""
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('home'))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """Kullanıcının Kişisel Hedef Sayfası"""
    if request.method == 'POST':
        goal_text = request.form.get('goal_text')
        goal_type = request.form.get('goal_type')

        if goal_text and goal_type in ['achieved', 'future']:
            new_goal = Goal(text=goal_text, type=goal_type, user_id=current_user.id)
            db.session.add(new_goal)
            db.session.commit()
            flash(f'Hedefiniz başarıyla kaydedildi!', 'success')
        else:
            flash('Lütfen geçerli bir hedef ve tip seçin.', 'error')

        return redirect(url_for('dashboard'))

    # Kullanıcının mevcut hedeflerini çek
    achieved_goals = Goal.query.filter_by(user_id=current_user.id, type='achieved').order_by(Goal.id.desc()).all()
    future_goals = Goal.query.filter_by(user_id=current_user.id, type='future').order_by(Goal.id.desc()).all()

    return render_template('dashboard.html', achieved_goals=achieved_goals, future_goals=future_goals)


@app.route('/delete_goal/<int:goal_id>', methods=['POST'])
@login_required
def delete_goal(goal_id):
    """Hedef Silme"""
    goal_to_delete = Goal.query.get_or_404(goal_id)

    # Yetki kontrolü
    if goal_to_delete.user_id != current_user.id:
        flash('Bu hedefi silme yetkiniz yok.', 'error')
        return redirect(url_for('dashboard'))

    db.session.delete(goal_to_delete)
    db.session.commit()
    flash('Hedef başarıyla silindi.', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    # İlk çalıştırmada (veya yeniden yapıda) veritabanını oluşturur
    with app.app_context():
        # Bu satır, veritabanı dosyasını ve tablolarını oluşturur.
        db.create_all()
    app.run(debug=True)
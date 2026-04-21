from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models.models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=bool(remember))
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('user.dashboard'))
        else:
            flash('Email ou senha inválidos.', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        full_name = request.form.get('full_name', '').strip()
        document = request.form.get('document', '').strip()
        address = request.form.get('address', '').strip()
        
        if not all([email, password, full_name, document, address]):
            flash('Preencha todos os campos obrigatórios.', 'error')
            return render_template('auth/register.html')
        
        if password != confirm:
            flash('As senhas não coincidem.', 'error')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Este email já está cadastrado.', 'error')
            return render_template('auth/register.html')
        
        user = User(
            email=email,
            full_name=full_name,
            document=document,
            address=address
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        
        # Handle pet registration
        from models.models import Pet
        pet_name = request.form.get('pet_name', '').strip()
        pet_breed = request.form.get('pet_breed', '').strip()
        
        if pet_name:
            pet = Pet(user_id=user.id, name=pet_name, breed=pet_breed)
            
            # Handle photo upload
            if 'pet_photo' in request.files:
                file = request.files['pet_photo']
                if file and file.filename:
                    import os
                    from werkzeug.utils import secure_filename
                    from flask import current_app
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    filename = f"pet_{user.id}_{pet_name.lower()}.{ext}"
                    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'pets')
                    os.makedirs(upload_path, exist_ok=True)
                    file.save(os.path.join(upload_path, filename))
                    pet.photo = f"uploads/pets/{filename}"
            
            db.session.add(pet)
        
        db.session.commit()
        login_user(user)
        flash('Cadastro realizado com sucesso! Complete seu perfil para continuar.', 'success')
        return redirect(url_for('user.complete_profile'))
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

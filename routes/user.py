from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.models import db, Pet, ServiceOrder, ServicePlan, WalkDuration, PetSize
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
@login_required
def dashboard():
    pet = Pet.query.filter_by(user_id=current_user.id).first()
    recent_orders = ServiceOrder.query.filter_by(user_id=current_user.id)\
        .order_by(ServiceOrder.created_at.desc()).limit(5).all()
    return render_template('user/dashboard.html', pet=pet, recent_orders=recent_orders)

@user_bp.route('/complete-profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    pet = Pet.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        # Update user info
        current_user.phone = request.form.get('phone', '').strip()
        current_user.city = request.form.get('city', '').strip()
        current_user.state = request.form.get('state', '').strip()
        current_user.zip_code = request.form.get('zip_code', '').strip()
        current_user.address_complement = request.form.get('address_complement', '').strip()
        
        if pet:
            size_val = request.form.get('pet_size')
            if size_val:
                pet.size = PetSize[size_val]
            pet.temperament_humans = request.form.get('temperament_humans', '')
            pet.temperament_animals = request.form.get('temperament_animals', '')
            
            if 'vaccine_card' in request.files:
                file = request.files['vaccine_card']
                if file and file.filename:
                    import os
                    from werkzeug.utils import secure_filename
                    from flask import current_app
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    filename = f"vaccine_{pet.id}.{ext}"
                    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'vaccines')
                    os.makedirs(upload_path, exist_ok=True)
                    file.save(os.path.join(upload_path, filename))
                    pet.vaccine_card = f"uploads/vaccines/{filename}"
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('user.dashboard'))
    
    return render_template('user/complete_profile.html', pet=pet)

@user_bp.route('/my-pet')
@login_required
def my_pet():
    pet = Pet.query.filter_by(user_id=current_user.id).first()
    orders = ServiceOrder.query.filter_by(user_id=current_user.id)\
        .order_by(ServiceOrder.created_at.desc()).all()
    return render_template('user/my_pet.html', pet=pet, orders=orders)

@user_bp.route('/walk-history')
@login_required
def walk_history():
    orders = ServiceOrder.query.filter_by(user_id=current_user.id)\
        .order_by(ServiceOrder.created_at.desc()).all()
    return render_template('user/walk_history.html', orders=orders)

@user_bp.route('/payment-data')
@login_required
def payment_data():
    return render_template('user/payment_data.html')

@user_bp.route('/contracted-services')
@login_required
def contracted_services():
    active_orders = ServiceOrder.query.filter_by(
        user_id=current_user.id
    ).filter(
        ServiceOrder.status.in_(['PENDING', 'CONFIRMED', 'IN_PROGRESS'])
    ).all()
    return render_template('user/contracted_services.html', orders=active_orders)

@user_bp.route('/change-plan')
@login_required
def change_plan():
    plans = ServicePlan.query.filter_by(is_active=True).all()
    return render_template('user/change_plan.html', plans=plans)

@user_bp.route('/cancel-service/<int:order_id>', methods=['POST'])
@login_required
def cancel_service(order_id):
    order = ServiceOrder.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    from datetime import timedelta, date
    
    can_refund = False
    if order.scheduled_date:
        days_until = (order.scheduled_date - date.today()).days
        can_refund = days_until >= 1
    
    order.status = 'CANCELLED'
    if can_refund and order.payment_status == 'APPROVED':
        order.payment_status = 'REFUNDED'
        # TODO: trigger MercadoPago refund API
    
    db.session.commit()
    msg = 'Serviço cancelado e reembolso iniciado.' if can_refund else 'Serviço cancelado (sem reembolso por cancelamento tardio).'
    flash(msg, 'info')
    return redirect(url_for('user.contracted_services'))

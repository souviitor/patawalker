from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.models import db, ServicePlan, WalkDuration, ServiceOrder, Pet
from datetime import datetime, date, timedelta

services_bp = Blueprint('services', __name__)

@services_bp.route('/plans')
@login_required
def plans():
    plans = ServicePlan.query.filter_by(is_active=True).all()
    return render_template('services/plans.html', plans=plans)

@services_bp.route('/plan/<int:plan_id>')
@login_required
def plan_detail(plan_id):
    plan = ServicePlan.query.get_or_404(plan_id)
    pets = Pet.query.filter_by(user_id=current_user.id).all()
    return render_template('services/plan_detail.html', plan=plan, pets=pets)

@services_bp.route('/plan/<int:plan_id>/subscribe', methods=['POST'])
@login_required
def subscribe_plan(plan_id):
    plan = ServicePlan.query.get_or_404(plan_id)
    pet_id = request.form.get('pet_id')
    selected_days = request.form.getlist('days[]')
    walk_time = request.form.get('walk_time')
    
    if not pet_id or not selected_days or not walk_time:
        flash('Selecione o pet, os dias e o horário do passeio.', 'error')
        return redirect(url_for('services.plan_detail', plan_id=plan_id))
    
    if len(selected_days) != plan.walks_per_week:
        flash(f'Selecione exatamente {plan.walks_per_week} dia(s) por semana.', 'error')
        return redirect(url_for('services.plan_detail', plan_id=plan_id))
    
    order = ServiceOrder(
        user_id=current_user.id,
        pet_id=int(pet_id),
        service_type='plan',
        plan_id=plan_id,
        scheduled_days={'days': selected_days, 'time': walk_time},
        amount=plan.price,
        status='PENDING',
        payment_status='PENDING'
    )
    db.session.add(order)
    db.session.commit()
    
    return render_template('services/confirm_order.html', order=order, plan=plan)

@services_bp.route('/avulso')
@login_required
def avulso():
    durations = WalkDuration.query.filter_by(is_active=True).all()
    pets = Pet.query.filter_by(user_id=current_user.id).all()
    
    # Generate available dates (next 30 days, Mon-Sat)
    available_dates = []
    today = date.today()
    for i in range(1, 31):
        d = today + timedelta(days=i)
        if d.weekday() < 6:  # Mon-Sat
            available_dates.append(d.isoformat())
    
    return render_template('services/avulso.html', 
        durations=durations, pets=pets, available_dates=available_dates)

@services_bp.route('/avulso/book', methods=['POST'])
@login_required
def book_avulso():
    pet_id = request.form.get('pet_id')
    duration_id = request.form.get('duration_id')
    walk_date = request.form.get('walk_date')
    walk_time = request.form.get('walk_time')
    
    if not all([pet_id, duration_id, walk_date, walk_time]):
        flash('Preencha todos os campos.', 'error')
        return redirect(url_for('services.avulso'))
    
    duration = WalkDuration.query.get_or_404(duration_id)
    
    order = ServiceOrder(
        user_id=current_user.id,
        pet_id=int(pet_id),
        service_type='avulso',
        walk_duration_id=int(duration_id),
        scheduled_date=datetime.strptime(walk_date, '%Y-%m-%d').date(),
        scheduled_time=datetime.strptime(walk_time, '%H:%M').time(),
        amount=duration.price,
        status='PENDING',
        payment_status='PENDING'
    )
    db.session.add(order)
    db.session.commit()
    
    return render_template('services/confirm_order.html', order=order, duration=duration)

@services_bp.route('/confirm/<int:order_id>/pay', methods=['POST'])
@login_required
def pay_order(order_id):
    order = ServiceOrder.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    # TODO: Integrate MercadoPago SDK
    # For now, simulate approval
    order.payment_status = 'APPROVED'
    order.status = 'CONFIRMED'
    db.session.commit()
    flash('Pagamento confirmado! Seu passeio foi agendado.', 'success')
    return redirect(url_for('user.my_pet'))

@services_bp.route('/vet')
@login_required
def vet():
    pets = Pet.query.filter_by(user_id=current_user.id).all()
    return render_template('services/vet.html', pets=pets)

@services_bp.route('/shopping')
@login_required
def shopping():
    pets = Pet.query.filter_by(user_id=current_user.id).all()
    return render_template('services/shopping.html', pets=pets)

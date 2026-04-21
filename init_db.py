#!/usr/bin/env python3
"""
Script para inicializar o banco de dados e criar usuário admin.
Execute: python init_db.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from models.models import User, UserRole, ServicePlan, WalkDuration, PlanType, AppSetting

def init_database():
    app = create_app()
    
    with app.app_context():
        print("🐾 Inicializando banco de dados PataWalker...")
        db.create_all()
        print("✅ Tabelas criadas!")

        # Create admin
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@patawalker.com.br')
        if not User.query.filter_by(email=admin_email).first():
            admin = User(
                email=admin_email,
                full_name='Administrador PataWalker',
                role=UserRole.ADMIN
            )
            admin.set_password('admin123')  # CHANGE IN PRODUCTION!
            db.session.add(admin)
            print(f"✅ Admin criado: {admin_email} / admin123")
        else:
            print(f"ℹ️  Admin já existe: {admin_email}")

        # Seed default plans
        if not ServicePlan.query.first():
            plans = [
                ServicePlan(
                    plan_type=PlanType.P,
                    name='Plano P — Iniciante',
                    description='Ideal para tutores que querem complementar o exercício do pet com passeios regulares. 2 passeios por semana com horário fixo e exclusivo.',
                    walks_per_week=2,
                    duration_minutes=30,
                    price=149.90,
                    is_active=True
                ),
                ServicePlan(
                    plan_type=PlanType.M,
                    name='Plano M — Regular',
                    description='O mais popular! 3 passeios por semana com horário fixo, fotos durante o passeio e relatório pós-passeio.',
                    walks_per_week=3,
                    duration_minutes=40,
                    price=199.90,
                    is_active=True
                ),
                ServicePlan(
                    plan_type=PlanType.G,
                    name='Plano G — Intensivo',
                    description='Para pets que adoram se movimentar! 5 passeios por semana com horário exclusivo, fotos, vídeos e relatório detalhado.',
                    walks_per_week=5,
                    duration_minutes=45,
                    price=299.90,
                    is_active=True
                ),
            ]
            db.session.add_all(plans)
            print("✅ Planos padrão criados!")

        # Seed walk durations
        if not WalkDuration.query.first():
            durations = [
                WalkDuration(name='Passeio Rápido', duration_minutes=20, price=35.00, is_active=True),
                WalkDuration(name='Passeio Padrão', duration_minutes=30, price=49.90, is_active=True),
                WalkDuration(name='Passeio Completo', duration_minutes=45, price=69.90, is_active=True),
                WalkDuration(name='Passeio Longo', duration_minutes=60, price=89.90, is_active=True),
            ]
            db.session.add_all(durations)
            print("✅ Durações padrão criadas!")

        db.session.commit()
        print("\n🎉 Banco de dados inicializado com sucesso!")
        print(f"\n📧 Admin: {admin_email}")
        print("🔑 Senha: admin123 (ALTERE IMEDIATAMENTE!)")
        print("\n🚀 Execute: python app.py")

if __name__ == '__main__':
    init_database()

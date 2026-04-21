from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import enum

class UserRole(enum.Enum):
    ADMIN = 'admin'
    TUTOR = 'tutor'

class PetSize(enum.Enum):
    SMALL = 'Pequeno'
    MEDIUM = 'Médio'
    LARGE = 'Grande'

class PlanType(enum.Enum):
    P = 'Plano P'
    M = 'Plano M'
    G = 'Plano G'

class ServiceStatus(enum.Enum):
    PENDING = 'Pendente'
    CONFIRMED = 'Confirmado'
    IN_PROGRESS = 'Em andamento'
    COMPLETED = 'Concluído'
    CANCELLED = 'Cancelado'
    REFUNDED = 'Reembolsado'

class PaymentStatus(enum.Enum):
    PENDING = 'Pendente'
    APPROVED = 'Aprovado'
    REJECTED = 'Rejeitado'
    REFUNDED = 'Reembolsado'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.TUTOR, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Tutor Info
    full_name = db.Column(db.String(200))
    document = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(300))
    address_complement = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(10))
    
    # Payment
    mp_customer_id = db.Column(db.String(100))
    
    # Relations
    pets = db.relationship('Pet', backref='tutor', lazy=True, cascade='all, delete-orphan')
    services = db.relationship('ServiceOrder', backref='tutor', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN
    
    @property
    def profile_complete(self):
        return all([self.full_name, self.document, self.address, self.phone])

class Pet(db.Model):
    __tablename__ = 'pets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100))
    size = db.Column(db.Enum(PetSize))
    temperament_humans = db.Column(db.String(50))
    temperament_animals = db.Column(db.String(50))
    photo = db.Column(db.String(300))
    vaccine_card = db.Column(db.String(300))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ServicePlan(db.Model):
    __tablename__ = 'service_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    plan_type = db.Column(db.Enum(PlanType), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    walks_per_week = db.Column(db.Integer, nullable=False)
    duration_minutes = db.Column(db.Integer, default=30)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class WalkDuration(db.Model):
    __tablename__ = 'walk_durations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

class ServiceOrder(db.Model):
    __tablename__ = 'service_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)  # plan, avulso, vet, shopping
    
    # Plan reference
    plan_id = db.Column(db.Integer, db.ForeignKey('service_plans.id'))
    walk_duration_id = db.Column(db.Integer, db.ForeignKey('walk_durations.id'))
    
    # Schedule
    scheduled_date = db.Column(db.Date)
    scheduled_time = db.Column(db.Time)
    scheduled_days = db.Column(db.JSON)  # For plans: list of weekdays
    
    # Status & Payment
    status = db.Column(db.Enum(ServiceStatus), default=ServiceStatus.PENDING)
    payment_status = db.Column(db.Enum(PaymentStatus), default=PaymentStatus.PENDING)
    amount = db.Column(db.Numeric(10, 2))
    mp_payment_id = db.Column(db.String(100))
    mp_preference_id = db.Column(db.String(100))
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    pet = db.relationship('Pet', backref='orders')
    plan = db.relationship('ServicePlan', backref='orders')
    walk_duration = db.relationship('WalkDuration', backref='orders')

class FinancialRecord(db.Model):
    __tablename__ = 'financial_records'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('service_orders.id'))
    type = db.Column(db.String(20))  # income, expense, refund
    amount = db.Column(db.Numeric(10, 2))
    description = db.Column(db.String(300))
    date = db.Column(db.Date, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AppSetting(db.Model):
    __tablename__ = 'app_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.String(300))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

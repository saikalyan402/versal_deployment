from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import PickleType, event
import secrets
import bcrypt
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship



from . import db

class BaseModel(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_deleted = db.Column(db.Boolean, default=False)

class RolePermission(BaseModel):
    __tablename__ = 'role_permissions'
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    permission_id = Column(Integer, ForeignKey('permissions.id'))


class Role(BaseModel):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    code = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255))
    
    user_roles = db.relationship('UserRole', back_populates='role', overlaps="user_roles")
    permissions = relationship('Permission', secondary='role_permissions')

class Permission(BaseModel):
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    

class UserRole(BaseModel):
    __tablename__ = 'user_roles'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    name= db.Column(db.String(255))
    user = db.relationship('User', back_populates='roles', overlaps="user_roles")
    role = db.relationship('Role', back_populates='user_roles', overlaps="user_roles")
    
    def get_permissions(self):
        return self.role.permissions if self.role else []


class User(BaseModel, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, default="User")
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # password should be hashed
    active = db.Column(db.Boolean, default=True, nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True)
    last_login_at = db.Column(db.DateTime)
    unactived_at = db.Column(db.DateTime)
    no_of_logins = db.Column(db.Integer, default=0)
    
    roles = db.relationship('UserRole', back_populates='user', overlaps="user_roles")
    
    
    def get_id(self):
        return str(self.fs_uniquifier)

    @property
    def is_authenticated(self):
        return True
    
class Company(BaseModel):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255))
    
class Category(BaseModel):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255))
    customised_risk_set = db.Column(MutableList.as_mutable(PickleType), default=[]) # these are list of scheme ids
    

class UserCategoryAccess(BaseModel):
    __tablename__ = 'user_category_access'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    db.UniqueConstraint('user_id', 'category_id', name='unique_user_category_access')
    
    user = db.relationship('User', backref=db.backref('user_category_access', lazy=True))
    category = db.relationship('Category')



class Scheme(BaseModel):
    __tablename__ = 'schemes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255))
    type = db.Column(db.String(255), nullable = False)
    subtype = db.Column(db.String(255), nullable = False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    db.UniqueConstraint('company_id', 'category_id', name='unique_scheme')
    
    
class DailySchemePerformanceParamenter(BaseModel):
    __tablename__ = 'daily_scheme_performance_parameters'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scheme_id = db.Column(db.Integer, db.ForeignKey('schemes.id'), nullable=False)
    performance_date = db.Column(db.Date, nullable = False)
    data = db.Column(db.JSON, nullable=False) # data validation
    
    db.UniqueConstraint('scheme_id', 'performance_date', name='unique_daily_scheme_performance_parameter')
    
class CategoryRiskSet(BaseModel):
    __tablename__ = 'category_risk_sets'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    subtype = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable = False)
    risk_set = db.Column(MutableList.as_mutable(PickleType), default=[]) # These are scheme id's of a category for multiple companies
    data = db.Column(db.JSON, nullable=False) # this true peer average, this is different from the above risk set

    db.UniqueConstraint('category_id',"type","subtype", 'date', name='unique_category_risk_set')
   

class Benchmark(BaseModel):
    __tablename__ = 'benchmarks'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255))

class BenchmarkData(BaseModel):
    __tablename__ = 'benchmark_data'
    
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    benchmark_id = db.Column(db.Integer, db.ForeignKey('benchmarks.id'), nullable = False)
    date = db.Column(db.Date, nullable = False)
    data = db.Column(db.JSON, nullable = False)


class BenchmarkConfig(BaseModel):
    __tablename__ = 'benchmark_configs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    benchmark_name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('benchmark_name', 'category_id', name='unique_benchmark_config'),
    )
    
    
class FundManagerCategoryConfig(BaseModel):
    __tablename__ = 'fundmanager_category_configs'
    
    id = db.Column(db.Integer, primary_key =  True, autoincrement = True)
    fund_manager = db.Column(db.String(255), nullable = False)
    deupty_fund_managers = db.Column(db.String(400))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)


def generate_fs_uniquifier(mapper, connection, target):
    target.fs_uniquifier = secrets.token_hex(16)

   
def set_default_active(mapper, connection, target):
    if target.active is None:
        target.active = True

event.listen(User, 'before_insert', generate_fs_uniquifier)
event.listen(User, 'before_update', generate_fs_uniquifier)
event.listen(User, 'before_update', set_default_active)
from application.initial_scripts.initial_data_helpers.populate_categories import (
    intially_populate_categories,
)
from application.initial_scripts.initial_data_helpers.populate_benchmark_master import (
    populate_benchmark_config,
)
from application.initial_scripts.initial_data_helpers.populate_company import (
    populate_company,
)
from application.initial_scripts.initial_data_helpers.populate_FundManagerConfig import (
    FM_names,
)

from werkzeug.security import generate_password_hash
 

from application.model.model import (
    db,
    FundManagerCategoryConfig,
    Category,
    Company,
    BenchmarkConfig,
    Permission,
    Role,
    UserRole,
    RolePermission,
    UserCategoryAccess,
)

import os


pages = [
    "Home",
    "Scheme Comparison",
    "AMC Overview",
    "Category Overview",
    "Edge",
    "Admin Dashboard",
]


def initial_data_loader():
    curr_dir = os.getcwd() + "/application/initial_scripts/initial_data_csv"
    # /home/shubham/adityaBirla/current_ABSL/backend/application/initial_scripts/initial_data_csv

    try:
        if Company.query.count() == 0:
            print("Populating Companies data")
            populate_company(curr_dir)
    except Exception as e:
        print("Error while adding Company initially", e)

    try:
        if Category.query.count() == 0:
            print("Populating Category data")

            intially_populate_categories(curr_dir)
    except Exception as e:
        print("Error while adding Categories initially", e)

    try:
        if BenchmarkConfig.query.count() == 0:
            print("Populating BenchmarkConfig data")

            populate_benchmark_config(curr_dir)
    except Exception as e:
        print("Error while adding Benchmark config", e)

    try:
        if FundManagerCategoryConfig.query.count() == 0:
            print("Populating FundManagerCategoryConfig data")
            FM_names(curr_dir)
    except Exception as e:
        print("Error while adding Fund Manager initially", e)

    try:
        if Permission.query.count() != len(pages):
            for page in pages:
                permission = Permission.query.filter_by(name=page).first()
                if permission is None:
                    new_permission = Permission(name=page)
                    try:
                        db.session.add(new_permission)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print("unable to add the permission: " + page)
    except Exception as e:
        print("Error while adding permissions", e)

    try:
        admin = Role.query.filter_by(code="ADMIN").first()
        if admin is None:
            admin = make_admin()

        if RolePermission.query.filter_by(role_id=admin.id).count() != len(pages):
            permissions = Permission.query.all()
            for permission in permissions:
                role_permission = RolePermission.query.filter_by(
                    role_id=admin.id, permission_id=permission.id
                ).first()
                if role_permission is None:
                    new_role_permission = RolePermission(
                        role_id=admin.id, permission_id=permission.id
                    )
                    try:
                        db.session.add(new_role_permission)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print("unable to add the role_permission: " + permission.name)
    except Exception as e:
        print("Error while adding admin role permissions", e)

    pass


def make_admin():
    new_role = Role(code="ADMIN", name="Admin")
    try:
        db.session.add(new_role)
        db.session.commit()
        return new_role
    except Exception as e:
        db.session.rollback()
        print("unable to add the role: ADMIN")
    return "failed"


def add_admin_user(admin_name,admin_email, admin_password):
    from application.model.model import User, Role, UserRole, db

    admin = User.query.filter_by(email=admin_email).first()
    if admin is None:
        hash_password = generate_password_hash(admin_password)

        admin = User(name = admin_name,email=admin_email, password=hash_password)
        try:
            db.session.add(admin)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("unable to add the admin user, error: ", e)
    admin_role = Role.query.filter_by(code="ADMIN").first()
    admin_role_ = UserRole.query.filter_by(
        user_id=admin.id, role_id=admin_role.id
    ).first()
    if admin_role_ is None:
        admin_role_ = UserRole(user_id=admin.id, role_id=admin_role.id)
        try:
            db.session.add(admin_role_)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("unable to add the admin role to the admin user, error: ", e)
    try:
        categories = Category.query.all()
        for category in categories:
            user_cat_access = UserCategoryAccess.query.filter_by(user_id=admin.id, category_id=category.id).first()
            if user_cat_access is None:
                new_user_cat_access = UserCategoryAccess(
                    user_id=admin.id, category_id=category.id
                )
                try:
                    db.session.add(new_user_cat_access)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print("unable to add the user_category_access: " + category.name)
    except Exception as e:
        print("Error while adding user category access", e)

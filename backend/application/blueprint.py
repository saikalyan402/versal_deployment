from flask import current_app as app

from application.apis.db_apis import db_api_bp
from application.apis.upload_apis import upload_api_bp
from application.apis.home_apis import home_api_bp
from application.apis.comp_amc_apis import amcOverview_api_bp
from application.apis.category_overview_apis import category_overview_api_bp
from application.apis.common_apis import common_api_bp
from application.apis.admin_apis import admin_api_bp
from application.apis.edge_apis import edge_api_bp
from application.apis.scheme_comparison_apis import scheme_comparison_api_bp

app.register_blueprint(db_api_bp)
app.register_blueprint(upload_api_bp)
app.register_blueprint(home_api_bp)
app.register_blueprint(amcOverview_api_bp)
app.register_blueprint(category_overview_api_bp)
app.register_blueprint(common_api_bp)
app.register_blueprint(admin_api_bp)
app.register_blueprint(edge_api_bp)
app.register_blueprint(scheme_comparison_api_bp)

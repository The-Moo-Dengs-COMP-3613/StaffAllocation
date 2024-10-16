# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .admin import setup_admin

from App.views.course_view import course_bp
from App.views.staff_view import staff_bp


views = [user_views, index_views, auth_views, course_bp, staff_bp]# blueprints must be added to this list


import os, sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.backend import DatabaseConfig, ResourcePlannerAPI

config = DatabaseConfig()
api = ResourcePlannerAPI(config)
api.init_database()
# mod_wsgi expects this name by default:
application = api.app

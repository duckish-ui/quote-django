import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotesite.settings')

application = get_wsgi_application()

# On Vercel the SQLite file lives in /tmp and starts empty on each cold start,
# so run migrations (which also seed the quotes) before serving requests.
if os.environ.get('VERCEL'):
    from django.core.management import call_command
    call_command('migrate', interactive=False, verbosity=0)

app = application  # Vercel needs this

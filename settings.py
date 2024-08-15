import os
import environ
from pathlib import Path
from django.urls import reverse_lazy
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from cryptography.fernet import Fernet


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()

DEBUG = False if env('DEBUG') == 'False' else True
SECRET_KEY = env('SECRET_KEY')
WWW = 'nps-feedback.bracbank.com'
ALLOWED_HOSTS = ['103.146.76.181','nps-feedback.bracbank.com','172.26.5.36','10.5.2.246','172.26.3.36']
SITE_URL = f'https://{WWW}'
#SITE_URL = 'http://172.20.10.14'

LOCAL_FOLDER = os.path.join(BASE_DIR, "local")

# Ensure the session cookies are secure and HttpOnly
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# Ensure the CSRF cookie is secure and HttpOnly
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Application definition
INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'csp',
    'access_management',
    'feedbacks',
    'log'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    'core.cspmiddleware.CSPNonceMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.restrict_access_middleware.RestrictAccessMiddleware',
    'access_management.middleware.PasswordChangeMiddleware',
]

AUTH_USER_MODEL ='access_management.User'

AUTHENTICATION_BACKENDS = [
    'access_management.backends.CustomAuthBackend',
    'django.contrib.auth.backends.ModelBackend',  # keep the default backend
]

ROOT_URLCONF = 'core.urls'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True     # opional, as this will log you out when browser is closed
SESSION_COOKIE_AGE = 1800                  # 0r 5 * 60, same thing
SESSION_SAVE_EVERY_REQUEST = True          # Will prrevent from logging you out after 300 seconds

#HSTS Settings
#SECURE_HSTS_SECONDS = 31536000
#SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#SECURE_HSTS_PRELOAD = True  # Optional for HSTS preload list
#SECURE_SSL_REDIRECT = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databasesBE

if DEBUG:
    DB_KEY = env("DB_KEY") 
    DB_TEXT = env("DB_TEXT") 
    DB_fernet = Fernet(DB_KEY)
    DB_PASS = DB_fernet.decrypt(DB_TEXT).decode('utf-8')
    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': env("DB_NAME"),
            'USER': env("DB_USER"),
            'PASSWORD': DB_PASS,
            'HOST': env("DB_HOST"),
            'PORT': env("DB_PORT"),
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
            },
        }
    }
else:
    DB_KEY = env("DB_KEY") 
    DB_TEXT = env("DB_TEXT") 
    DB_fernet = Fernet(DB_KEY)
    DB_PASS = DB_fernet.decrypt(DB_TEXT).decode('utf-8')
    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': env("DB_NAME"),
            'USER': env("DB_USER"),
            'PASSWORD': DB_PASS,
            'HOST': env("DB_HOST"),
            'PORT': env("DB_PORT"),
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
            },
        }
    }

#CSP Header Config
#CSP_SCRIPT_SRC = ("'self'", "'nonce-{{ request.csp_nonce }}'", "'unsafe-eval'")
#CSP_STYLE_SRC = ("'self'", "'nonce-{{ request.csp_nonce }}'")

CSP_SCRIPT_SRC = ("'self'", "'unsafe-eval'")
CSP_STYLE_SRC = ("'self'", "'nonce-{{ request.csp_nonce }}'")

#CSP_IMG_SRC = ("'self'")

#CSP_STYLE_SRC = ("'self'", "/static_files/unfold/css")

#CSP_SCRIPT_SRC = ("'self'", "/static_files/unfold/js")

# Content Security Policy

#CSP_INCLUDE_NONCE_IN = ['script-src', 'style-src']

#Logger Configuration
LOGGING = {
'version': 1,
'disable_existing_loggers': False,
'filters': {
    'require_debug_false': {
        '()': 'django.utils.log.RequireDebugFalse',
    },
    'require_debug_true': {
        '()': 'django.utils.log.RequireDebugTrue',
    },
},
'formatters': {
    'django.server': {
        '()': 'django.utils.log.ServerFormatter',
        'format': '[%(server_time)s] %(message)s',
    }
},
'handlers': {
    'console': {
        'level': 'INFO',
        'filters': ['require_debug_true'],
        'class': 'logging.StreamHandler',
    },
    # Custom handler which we will use with logger 'django'.
    # We want errors/warnings to be logged when DEBUG=False
    'console_on_not_debug': {
        'level': 'WARNING',
        'filters': ['require_debug_false'],
        'class': 'logging.StreamHandler',
    },
    'django.server': {
        'level': 'INFO',
        'class': 'logging.StreamHandler',
        'formatter': 'django.server',
    },
    'mail_admins': {
        'level': 'ERROR',
        'filters': ['require_debug_false'],
        'class': 'django.utils.log.AdminEmailHandler'
    }
},
'loggers': {
    'django': {
        'handlers': ['console', 'mail_admins', 'console_on_not_debug'],
        'level': 'INFO',
    },
    'django.server': {
        'handlers': ['django.server'],
        'level': 'INFO',
        'propagate': False,
    },
}
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,  # Set this value dynamically if required
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'access_management.validators.NotSameAsOldValidator',
    },
    {
        'NAME': 'access_management.validators.ComplexPasswordValidator',
    },
    
]


#SMTP Config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
MAIL_PORT = int(os.getenv("MAIL_PORT"))
MAIL_HOST = os.getenv("MAIL_HOST")
MAIL_HOST_USER = os.getenv("MAIL_HOST_USER")
MAIL_HOST_PASS = os.getenv("MAIL_HOST_PASS") or None
MAIL_SSL_CERT = f"{BASE_DIR}/{os.getenv('MAIL_SSL_CERT')}" if os.getenv('MAIL_SSL_CERT') else None
MAIL_SSL_KEY = f"{BASE_DIR}/{os.getenv('MAIL_SSL_KEY')}" if os.getenv('MAIL_SSL_KEY') else None


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True

LOGOUT_REDIRECT_URL = '/admin_access_VK!aAq/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static_files/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

#if not DEBUG:
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


UNFOLD = {
    "SITE_TITLE": "Customer Feedbacks",
    "SITE_HEADER": "Management Solution",
    "SITE_URL": "/",
    "STYLES": [
        lambda request: static("css/admin_style.css"),
    ],
    # "DASHBOARD_CALLBACK": "inventory.views.dashboard_callback",
    # "SCRIPTS": [
    #     lambda request: static("js/script.js"),
    # ],
    "SIDEBAR": { 
        "show_search": True,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Adminstration"),
                "separator": False,  # Top border
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:access_management_user_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Data Managements"),
                "separator": False,  # Top border
                "items": [
                    {
                        "title": _("Branch & ATM Data"),
                        "icon": "local_atm",
                        "link": reverse_lazy("admin:feedbacks_source_changelist"),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Data Upload"),
                        "icon": "upload",
                        "link": reverse_lazy("admin:feedbacks_dataupload_changelist"),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Customized Questions"),
                        "icon": "question_exchange",
                        "link": reverse_lazy("admin:feedbacks_question_changelist"),
                        "permission": lambda request: request.user.is_staff,
                    },
                ],
            },
            {
                "title": _("Feedbacks"),
                "separator": False,  # Top border
                "items": [
                    {
                        "title": _("Customer Feedbacks"),
                        "icon": "communication",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:feedbacks_customerresponses_changelist"),
                        "permission": lambda request: request.user.is_staff,
                    },
                ],
            },
            {
                "title": _("Logs"),
                "separator": False,  # Top border
                "items": [
                    {
                        "title": _("Job Logs"),
                        "icon": "work_alert",
                        "link": reverse_lazy("admin:log_joblog_changelist"),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Task Logs"),
                        "icon": "task",
                        "link": reverse_lazy("admin:log_tasklog_changelist"),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("User Login Logs"),
                        "icon": "passkey",
                        "link": reverse_lazy("admin:log_useractivitylogs_changelist"),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("User Activity Logs"),
                        "icon": "zone_person_alert",
                        "link": reverse_lazy("admin:admin_logentry_changelist"),
                        "permission": lambda request: request.user.is_staff,
                    },
                ],
            },
         ],
    },
}

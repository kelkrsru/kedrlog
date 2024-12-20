import os

from django.urls import reverse_lazy
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False if os.getenv('DEBUG') == 'False' else True

PRODUCTION = False if os.getenv('PRODUCTION') == 'False' else True

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', default='').split(' ')

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', default='').split(' ')

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'api',
    'mainpage',
    'core',
    'common',
    'staticpages',
    'ckeditor',
    'personal',
    'order',
    'bootstrap_modal_forms',
    'rest_framework',
    'analytical',
    # 'widget_tweaks',
    # 'admin_reorder',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'kedrlog.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'kedrlog.wsgi.application'

if not PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.sqlite3'),
            'NAME': os.getenv('DB_NAME', default=os.path.join(BASE_DIR, 'db.sqlite3')),
            'USER': os.getenv('DB_USER', default='test'),
            'PASSWORD': os.getenv('DB_PASSWORD', default='test'),
            'HOST': os.getenv('DB_HOST', default='localhost'),
            'PORT': os.getenv('DB_PORT', default='5432')
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer']
}

AUTH_USER_MODEL = 'users.User'
LOGIN_URL = reverse_lazy('accounts:login')
LOGOUT_URL = reverse_lazy('accounts:logout')

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Krasnoyarsk'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = 'media/'
if PRODUCTION:
    STATIC_ROOT = os.getenv('PATH_STATIC_ROOT')
    MEDIA_ROOT = os.getenv('PATH_MEDIA_ROOT')
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if not PRODUCTION:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = os.getenv('EMAIL_PORT')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    EMAIL_USE_SSL = False if os.getenv('EMAIL_USE_SSL') == 'False' else True
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

X_FRAME_OPTIONS = "SAMEORIGIN"

YANDEX_METRICA_COUNTER_ID = os.getenv('YANDEX_METRICA_COUNTER_ID')
YANDEX_METRICA_WEBVISOR = False if os.getenv('YANDEX_METRICA_WEBVISOR') == 'False' else True
YANDEX_METRICA_TRACKHASH = False if os.getenv('YANDEX_METRICA_TRACKHASH') == 'False' else True
YANDEX_METRICA_NOINDEX = False if os.getenv('YANDEX_METRICA_NOINDEX') == 'False' else True
YANDEX_METRICA_ECOMMERCE = False if os.getenv('YANDEX_METRICA_ECOMMERCE') == 'False' else True

ADMIN_REORDER = (
    {'label': 'Основные настройки сайта', 'app': 'core', 'models': [
        'core.Company',
        'core.SocialNetworks',
        'common.Badge',
    ]},
    {'label': 'Структура Главной страницы', 'app': 'mainpage', 'models': [
        'mainpage.ContentBlockMain',
        'mainpage.ContentBlockInfrastructure',
        'mainpage.ContentBlockService',
        'mainpage.ContentBlockYandexMap',
        'mainpage.ContentBlockBooking',
        'mainpage.ContentBlockRoundedMenuItem',
        'mainpage.ToastMain',
    ]},
    {'label': 'Статические страницы', 'app': 'staticpages', 'models': [
        'staticpages.GalleryHouses',
        'staticpages.GalleryTerritory',
        'staticpages.GalleryFood',
        'staticpages.TextContentRules',
        'staticpages.TextContentFz152',
        'staticpages.TextContentAccessories',
        'staticpages.ContentGiftCertificate',
        'staticpages.TextContentRulesGiftCert',
        'staticpages.TextContentCorporate',
        'staticpages.ContentPrice',
        'staticpages.ContentSpa',
        'common.GalleryItem',
    ]},
    {'label': 'Ресурсы', 'app': 'core', 'models': [
        'core.House',
        'core.AdditionalFeatures',
        'core.Weeks',
        'core.Price',
        'core.Rate',
        'core.AdditionalServices',
        'core.SpaServices',
        'core.PriceForSpaServices',
        'core.GiftCertificate',
        'core.GiftCertificateType',
        'core.WeekendDays',
        'core.SettingsSite',
        'core.SettingsBitrix24',
    ]},
    {'label': 'Бронирование', 'app': 'core', 'models': [
        'core.Reserve',
        'core.OrderGiftCertificate',
    ]},
    {'label': 'Пользователи', 'app': 'users', 'models': [
        'users.User',
        'auth.Group',
    ]},
)

CKEDITOR_CONFIGS = {
    'default': {
        'versionCheck': False
    }
}

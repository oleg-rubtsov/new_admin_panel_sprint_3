# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME'),
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
#         'PORT': os.environ.get('DB_PORT', 5432),
#         'OPTIONS': {
#            'options': '-c search_path=public,content'
#         }
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.environ.get('DB_NAME', default=None),
        'USER': os.environ.get('POSTGRES_USER', default=None),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', default=None),
        'HOST': os.environ.get('DB_HOST', default=None),
        'PORT': os.environ.get('DB_PORT', default=None)
    }
}
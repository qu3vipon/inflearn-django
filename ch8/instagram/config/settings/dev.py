from .base import *  # noqa

DEBUG = False

STATIC_ROOT = "staticfiles"

INSTALLED_APPS += [
    "ebhealthcheck.apps.EBHealthCheckConfig",
]

ALLOWED_HOSTS = [
    "develop.eba-d55a33tf.ap-northeast-2.elasticbeanstalk.com",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ebdb',
        'USER': 'ebroot',
        'PASSWORD': 'securepassword123!',
        'HOST': 'awseb-e-bikmxwxazr-stack-awsebrdsdatabase-ogdm7xmw1h67.c786iiw0sizb.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": "inflearn-django-instagram-s3",
            "region_name": "ap-northeast-2",
        }
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

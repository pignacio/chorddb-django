#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-wildcard-import,wildcard-import,line-too-long
from .base import *

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

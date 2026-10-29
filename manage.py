#!/usr/bin/env python3
import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)

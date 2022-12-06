# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SendAddress = os.environ.get("SEND_ADDRESS")
Mail_to = os.environ.get("MAIL_TO")
Pass = os.environ.get("PASS")
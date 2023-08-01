from flask import render_template,request,redirect, flash, url_for
from app import app, login_manager,db
from .models import LoginForm, User, is_safe_url, NewUserByAdmin, Registration
from config import Config




        
    


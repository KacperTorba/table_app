import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
source_dir = os.path.join(os.path.dirname(BASE_DIR) ,'source_excel','orders.xls')
database_sql = 'sqlite:///' + os.path.join(os.path.dirname(BASE_DIR) ,'database','source.db')
database_dir = os.path.join(os.path.dirname(BASE_DIR) ,'database','source.db')
source_folder= os.path.join(os.path.dirname(BASE_DIR) ,'source_excel')
logfile_dir = os.path.join(BASE_DIR ,'logfile','create_db_source.log')


class Config:
   SECRET_KEY = os.environ.get("SECRET_KEY") # CHANGE !!
   SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or database_sql)
   SECURITY_PASSWORD_SALT = (os.environ.get("SECURITY_PASSWORD_SALT"))
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   UPLOAD_FOLDER = source_folder

   

import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging
from config import source_dir,database_dir,logfile_dir


print(source_dir)
print(database_dir)

def remove_file(file_path):
    os.remove(file_path)
    


logging.basicConfig(level=logging.DEBUG, filename=logfile_dir, format='%(asctime)s %(message)s')

# Read data from the XLS file using pandas
xls_file = source_dir
df = pd.read_excel(xls_file, skiprows=1)

# Define the SQLAlchemy model
Base = declarative_base()

class Person(Base):
    __tablename__ = 'people'
    order_number = Column(String, primary_key=True)
    document_date = Column(Date)

# Create a database session
engine = create_engine(database_dir)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Insert data into the database
for index, row in df.iterrows():   
    order_number = row['Nr dok.']
    
    if type(order_number) is str and order_number[:2] == "ZL":
            
        document_date = row['Data dok.'] 
        new_row = Person(order_number=order_number, document_date=document_date)
        session.add(new_row)
        
    else:
        logging.info(f'Order number: {order_number}')
        break

  
    
# Commit changes and close the session
session.commit()
session.close()


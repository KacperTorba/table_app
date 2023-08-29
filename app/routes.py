from flask import render_template,request,redirect, flash, url_for
from config import Config,source_dir, database_dir
from os.path import exists
import os
from .models import Orders, Currency
from app import app, db
import pandas as pd
import requests
from werkzeug.utils import secure_filename
import datetime

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'xls'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
           
           
def get_exchange_rate(code,date_from_excel):        
    i = 0
    
    while True:
        one_day = datetime.timedelta(days=i)
        date = date_from_excel - one_day
        start_date = date.strftime("%Y-%m-%d")
        full_url = f"http://api.nbp.pl/api/exchangerates/rates/A/{code}/{start_date}/"
        response = requests.get(full_url)
        
        
        if response.status_code != 404 :
            response.raise_for_status()
            result = response.json()['rates'][0]['mid']
            
            if result == None:
                continue
            else:
                break        
       
        i += 1
        
    return result


@app.route('/init')
def init():
    path_exist = exists(database_dir)
    
    # Read data from the XLS file using pandas
    xls_file = source_dir
    df = pd.read_excel(xls_file, skiprows=1)
    
    if path_exist == False:
        db.create_all()
        
        # Insert data into the database
        for index, row in df.iterrows():
            
            order_number = row['Nr dok.']
            
            if type(order_number) is str and order_number[:2] == "ZL":
                    
                document_date = row['Data dok.']
                forwarder = row['Wystawił']
                client = row['Zleceniodawca']
                start = df.iloc[index,17]
                target = df.iloc[index,20]
                start_route_date = df.iloc[index,19]
                currency = df.iloc[index,23]
                
                if currency != 'PLN':
                                     
                    check = Currency.query.filter(Currency.date == start_route_date and Currency.currency == currency).first()
                    
                    if check == None:
                        exchange_rate = get_exchange_rate(currency,start_route_date)
                        new_exchange = Currency(currency = currency,date = start_route_date, exchange_rate = exchange_rate)
                        db.session.add(new_exchange)
                        db.session.commit()
                        
                    else:
                        exchange_rate = check.exchange_rate
                else:
                    exchange_rate = 1
                        
                customer_rate = df.iloc[index,24]
                our_rate = df.iloc[index,25]
                profit = df.iloc[index,26]
                
                if row['Plik'] == "Prawda":
                    is_row_edit = True
                else:
                    is_row_edit = False
                
                new_row = Orders(order_number=order_number, document_date=document_date,forwarder=forwarder,client=client,start=start,target=target,start_route_date=start_route_date,currency=currency,exchange_rate=exchange_rate,customer_rate=customer_rate,our_rate=our_rate,profit=profit,is_row_edit=is_row_edit)
                
                db.session.add(new_row)
                db.session.commit()
                
            else:
                #logging.info(f'Order number: {order_number}')
                break
            
        db.session.close()
        
        
    return redirect (url_for('home'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    
    path_exist = exists(database_dir)
    
    if path_exist == False:
        return redirect (url_for('init'))
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        
        if file.filename == '':
            
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Read data from the XLS file using pandas
            xls_file = file_path
            df = pd.read_excel(xls_file, skiprows=1)
            
            # Insert data into the database
        for index, row in df.iterrows():
            
            order_number_new = row['Nr dok.']
            check_order_number = Orders.query.filter(Orders.order_number == order_number_new).first()
            
            if type(order_number_new) is str and order_number_new[:2] == "ZL" and check_order_number == None:
                    
                document_date = row['Data dok.']
                forwarder = row['Wystawił']
                client = row['Zleceniodawca']
                start = df.iloc[index,17]
                target = df.iloc[index,20]
                start_route_date = df.iloc[index,19]
                currency = df.iloc[index,23]  
                
                if currency != 'PLN':
                                     
                    check = Currency.query.filter(Currency.date == start_route_date and Currency.currency == currency).first()
                    
                    if check == None:
                        exchange_rate = get_exchange_rate(currency,start_route_date)
                        new_exchange = Currency(currency = currency,date = start_route_date, exchange_rate = exchange_rate)
                        db.session.add(new_exchange)
                        db.session.commit()
                        
                    else:
                        exchange_rate = check.exchange_rate
                else:
                    exchange_rate = 1
                
                      
                customer_rate = df.iloc[index,24]
                our_rate = df.iloc[index,25]
                profit = df.iloc[index,26]
                
                if row['Plik'] == "Prawda":
                    is_row_edit = True
                else:
                    is_row_edit = False
                
                new_row = Orders(order_number=order_number_new, document_date=document_date,forwarder=forwarder,client=client,start=start,target=target,start_route_date=start_route_date,currency=currency,exchange_rate=exchange_rate, customer_rate=customer_rate,our_rate=our_rate,profit=profit,is_row_edit=is_row_edit)
                
                db.session.add(new_row)
                db.session.commit()
                
            else:
                #logging.info(f'Order number: {order_number}')
                break
            
    return redirect (url_for('home'))


        

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('base.html')

        
    


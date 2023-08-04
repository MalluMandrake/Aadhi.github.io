from flask import Flask, url_for,session,redirect,flash
from werkzeug.utils import secure_filename
from flask import render_template
from flask import request
import json 
import os
import sqlite3
import database
import pickle
import pandas as pd

database.databasecreation()




items={'Food':"""rice,
 cooking oil,
  snacks, 
  cookies, 
  sauces,
  canned food""",

'Fresh' : """fresh tuna,
fruits, 
frozen pizza, 
salads,
 meat""",

'Drinks' : """water,
 juices,
  wine,
   alcoholic drinks,
    milk, 
    soy drinks.""",

'Home' : """toilet paper to small appliances""",
'Beauty' : """shampoo, 
shaving foam,
 cosmetics.""",
'Health' : """diet pills,
 condoms,
  tooth paste.""",
'Baby' : """diapers,
 baby food,
  baby care.""",
'Pets' : """food, 
toys, 
sanitary sand"""
}

item_list={
    'health_concious':'Food',
    'grocery_regulars':'Food',
    'fresh_regulars':'Fresh',
    'home_decorators':'Home',
    'beauty_concious':'Beauty',
    'pet_lovers':'Pets',
    'loyals':'Fresh',
    'grocery_shoppers':'',
    'new_parents':'Baby' ,
    'drink_buyers': 'Drinks'
}



abcd= Flask(__name__)

abcd.secret_key= "wehgdvwehjdw"

abcd.config['UPLOAD_FOLDER']='depend_files'

@abcd.route('/')
def home():
    return render_template('home.html')
@abcd.route('/about')
def about():
    return render_template('about.html')
@abcd.route('/dash')
def dashboard():
    return render_template('dashboard.html')

@abcd.route('/login',methods=["GET","POST"])
def login():    
    if request.method=='POST':
        email= request.form['email']
        password=request.form['password']
        con=sqlite3.connect("database.sqlite3")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute(" select * from registration where email=? and password=? ",(email,password))
        data= cur.fetchone()
        if data:
            session['email']=data['email']
            session['password']=data['password']
            return redirect (url_for('dashboard'))
        else:
            flash("Credentials Error","danger")
            return redirect (url_for('home'))

@abcd.route('/register', methods= ['GET','POST'])
def signup():
    if (request.method =='POST'):
        Email=request.form['email']
        Phone=request.form['phone']
        Password=request.form['password']
        print(Email)
        print(Phone)
        print(Password)
        try:
            with sqlite3.connect("database.sqlite3") as con:
                cur = con.cursor()
                cur.execute("INSERT into registration (email,phone,password) values (?,?,?)",(Email,Phone,Password))
                con.commit()
                msg="Successfully Added"
        except:
            con.rollback()
            msg="Error in Creation"
        finally:
            return render_template('home.html', msg=msg)
    else:
        return render_template('registration.html')


def predicts(data_array):
    #Read model
    model = pickle.load(open('depend_files/'+'decisiontree'+'.pkl', 'rb'))#load early trained model
    predictions=model.predict(data_array)
    print("___"*10)
    prediction_lst=predictions.tolist()
    pred_json={}
    
    for uniuq in set(prediction_lst):
        pred_json[uniuq]=prediction_lst.count(uniuq)
   
    return pred_json


@abcd.route('/file_upload',methods=['GET','POST'])
def file_upload(): 
    if request.method == 'POST':        
        file = request.files['file']      
        if file.filename == '':
            print(request.files)
            return render_template('dashboard.html', message = "File Not Found")
        filename = secure_filename(file.filename)
        print("__"*10)
        print(filename)
        file.save(os.path.join(abcd.config['UPLOAD_FOLDER'], filename))
        message = "File uploaded successfully"
        data=pd.read_csv("depend_files/"+filename)#read file  
        pred_json=predicts(data.values)
        
        v = list(pred_json.values())
        k = list(pred_json.keys())
        most_occour_class=k[v.index(max(v))]  
        least_occour_class=k[v.index(min(v))]  
            
        itemslistss=items[item_list[most_occour_class]]
        item_least_occur=items[item_list[least_occour_class]]
        print("*"*10)
        print(least_occour_class)
        print(item_least_occur)
        
        json_data = json.dumps(pred_json)  

        data_output="""According to inputted dataset most visted customer comes under the category of {} so that 
           you can instock the following items it might increases your sales because those products have high demand on your shop {}
           and least visted customer comes under the category of {} so that you can reduce the spending on following items{}""".format(most_occour_class,itemslistss,least_occour_class,item_least_occur)
        return render_template('result.html', data=json_data,cls1=most_occour_class,item1=itemslistss,cls2=least_occour_class,item2=item_least_occur)
        """
           
        return render_template('result.html', data=json_data,cls=" Most visited Customer category is: {} ".format(most_occour_class),
                               cls2=' {}'.format(itemslistss),
                               cls3=" Least visited Customer category is: {} ".format(least_occour_class),
                               cls4=' {}'.format(item_least_occur)
                               
                               )
        """
    else:
        return render_template('home.html', message = "Method not allowed")
   



if __name__ == '__main__':
    abcd.run(debug=True)    
    
    
    
    
    

from datetime import datetime, date
import json#, arrow
import string, random
from flask import Flask, flash, Response, redirect, render_template, request, session, abort,send_from_directory
from flask import Flask, request, render_template, redirect, url_for
from flask_mongokit import MongoKit, Document
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import requests,time
from libs import utils as UT
from libs import dataToPDF as PDF
import pymongo
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate

app = Flask(__name__)
app.config["MONGODB_DATABASE"]="user"
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


class User(Document):
    __collection__ = 'customer'
    structure = {
        'firstName' : unicode,
        'lastName' : unicode,
        'email' : unicode, 'password' : unicode,
        'phonenumber' : unicode, 'address' : unicode, 
        'gender' : unicode, 'dob' : unicode, 'age' : unicode,  
        'device_id' : unicode,
        'creation': datetime
        #'name': unicode,
        #'username': unicode,
        #'password': unicode,
        #'age': unicode,
        #'device_id':unicode,
        #'creation': datetime
    }
    required_fields = ['firstName', 'lastName', 'email', 'password', 'phonenumber', 'address']
    default_values = {'creation': datetime.utcnow}
    use_dot_notation = True


    def getuser(self,params):
        #print "Getting customer: ", params
        try:
            users = self.find(params)
            if users == None:
                raise Exception("Customer not found")
            return {
                'status' : True,
                'users' : list(users)
            }
        except Exception, e:
            return UT.Exception(e)

    def getAllusers(self,params):
        try:
            users = self.find(params)
            if users == None:
                raise Exception("Customers not found")
            return {
                'status' : True,
                'users' : users
            }
        except Exception, e:
            return UT.Exception(e)

class empdata(Document):
    __collection__='employdata'
    structure = {
    'name':unicode,
    'email':unicode,
    'dept':unicode
    }
    required_fields = ['name','email','dept']
    #default_values = {'datetime': datetime.utcnow}
    use_dot_notation = True

    def getemployee(self,params):
        #print "Getting customer: ", params
        try:
            users = self.find(params)
            if users == None:
                raise Exception("Customer not found")
            return {
                'status' : True,
                'users' : list(users)
            }
        except Exception, e:
            return UT.Exception(e)




class Engdept(Document):
    __collection__='engdept'
    structure = {
        
        'name':unicode,
        'employ_id':unicode,
        'intime':unicode,
        'outtime':unicode,
        'rssi':unicode,
        'lat':float,
        'lon':float



    }
    required_fields = ['name','employ_id','intime','outtime','rssi','lat','lon']
    #default_values = {'datetime': datetime.utcnow}
    use_dot_notation = True

    def getengdept(self,params):
        #print "Getting customer: ", params
        try:
            users = self.find((params),sort=[("_id",pymongo.DESCENDING)])
            if users == None:
                raise Exception("Customer not found")
            return {
                'status' : True,
                'users' : list(users)
            }
        except Exception, e:
            return UT.Exception(e)


class Secdept(Document):
    __collection__='secdept'
    structure = {
        
        'name':unicode,
        'employ_id':unicode,
        'intime':unicode,
        'outtime':unicode,
        'rssi':unicode,
        'lat':float,
        'lon':float



    }
    required_fields = ['name','employ_id','intime','outtime','rssi','lat','lon']
    #default_values = {'datetime': datetime.utcnow}
    use_dot_notation = True

    def getsecdept(self,params):
        #print "Getting customer: ", params
        try:
            users = self.find((params),sort=[("_id",pymongo.DESCENDING)])
            if users == None:
                raise Exception("Customer not found")
            return {
                'status' : True,
                'users' : list(users)
            }
        except Exception, e:
            return UT.Exception(e)


class Admindept(Document):
    __collection__='admindept'
    structure = {
        
        'name':unicode,
        'employ_id':unicode,
        'intime':unicode,
        'outtime':unicode,
        'rssi':unicode,
        'lat':float,
        'lon':float



    }
    required_fields = ['name','employ_id','intime','outtime','rssi','lat','lon']
    #default_values = {'datetime': datetime.utcnow}
    use_dot_notation = True

    def getadmindept(self,params):
        #print "Getting customer: ", params
        try:
            users = self.find((params),sort=[("_id",pymongo.DESCENDING)])
            if users == None:
                raise Exception("Customer not found")
            return {
                'status' : True,
                'users' : list(users)
            }
        except Exception, e:
            return UT.Exception(e)


class Managdept(Document):
    __collection__='managdept'
    structure = {
        
        'name':unicode,
        'employ_id':unicode,
        'intime':unicode,
        'outtime':unicode,
        'rssi':unicode,
        'lat':float,
        'lon':float



    }
    required_fields = ['name','employ_id','intime','outtime','rssi','lat','lon']
    #default_values = {'datetime': datetime.utcnow}
    use_dot_notation = True

    def getmanagdept(self,params):
        #print "Getting customer: ", params
        try:
            users = self.find((params),sort=[("_id",pymongo.DESCENDING)])
            if users == None:
                raise Exception("Customer not found")
            return {
                'status' : True,
                'users' : list(users)
            }
        except Exception, e:
            return UT.Exception(e)

class Visitor(Document):
    __collection__='visitor'
    structure = {
        
        'name':unicode,
        'employ_id':unicode,
        'intime':unicode,
        'outtime':unicode,
        'rssi':unicode,
        'lat':float,
        'lon':float



    }
    required_fields = ['name','employ_id','intime','outtime','rssi','lat','lon']
    #default_values = {'datetime': datetime.utcnow}
    use_dot_notation = True

    def getvisitor(self,params):
        #print "Getting customer: ", params
        try:
            users = self.find((params),sort=[("_id",pymongo.DESCENDING)])
            if users == None:
                raise Exception("Customer not found")
            return {
                'status' : True,
                'users' : list(users)
            }
        except Exception, e:
            return UT.Exception(e)





class gps(Document):
    __collection__ = 'gpsdata'
    structure = {
        'Hum': int,
        'Temp': int,
        'Lum': int,
        'Lat': int,
        'Lon': int,
        'device_id':unicode,
        'date': unicode
    }
    required_fields = ['Hum','Temp', 'Lum','Lat','Lon','device_id','date']
    #default_values = {'datetime': datetime.utcnow}
    use_dot_notation = True




    def get_gpsdata(self,params):
            #print params
            try:
                temp= self.find(params)
                #print list(temp)
                if temp == None:
                    raise Exception("Customer not found")
                return{
                    'status' : True,
                    'temp' : temp
                }
            except Exception, e:
                return UT.Exception(e)

class temp_data(Document):
    __collection__ = 'tmpdata'
    structure = {
        'Hum': int,
        'Temp': int,
        'Lum': int,
        'device_id':unicode,
        'date': unicode
    }
    required_fields = ['Hum','Temp','Lum','device_id','date']
    #default_values = {'datetime': datetime.utcnow}
    use_dot_notation = True

    def get_tmpdata(self,params):
            #print params
            try:
                temp= self.find(params)
                #print list(temp)
                if temp == None:
                    raise Exception("Customer not found")
                return{
                    'status' : True,
                    'temp' : temp
                }
            except Exception, e:
                return UT.Exception(e)


db = MongoKit(app)

db.register([gps])
db.register([User])
db.register([Admindept])
db.register([Managdept])
db.register([Engdept])
db.register([Secdept])
db.register([Visitor])
db.register([empdata])
db.register([temp_data])



@app.route('/')
def home():
    if session.get('logged_in'):
       
        return render_template('graph.html')
        #return "Hello !  <a href='/logout'>Logout</a>"
    else:
        return render_template('index.html')



@app.route('/login', methods=['POST'])
def do_admin_login():
    '''url = 'https://zacprasad.data.thethingsnetwork.org/api/v2/query'
        #payload = open("request.json")
    headers = {'Authorization': 'key ttn-account-v2.UK4b-i_gjpvaq_FU6sGpDSl_-1aGhkV7_CqfP2_wbeI', 'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    newdata = json.loads(r.content)
    print newdata
    Hum =(newdata[0]['relative_humidity_2'])
    Temp =(newdata[0]['temperature_1'])
    Lum=(newdata[0]['luminosity_3'])
    date=(newdata['time'])

    user = db.iData()
    user.Hum = Hum
    user.Temp = Temp
    user.Lum = Lum

    user.datatime=date
    user.save()'''



    #if request.form['password'] == 'admin' and request.form['username'] == 'prasad':
    user =request.form['email']
    #print user
    #usera = db.User.find_one({"email":user})
    usera = db.User.getuser({"email":user})
    #usera = list(usera)
    #print usera
    usera = usera["users"]
    device_id=usera[0]['device_id']
    #print "------>>>>>>>"
    #print device_id
    if usera is None: 
        #abort(401)
        flash('Invalid Username or Password')


    elif (request.form['email'] == usera[0]['email']):
        #print "prasad"
        if(request.form['password'] == usera[0]['password']):
            #device_id = usera[0]['device_id']
            #print "------>>>>>>>"
            #print device_id
            session['logged_in'] =True
        return get_device(device_id)
            

        #return home()
          


    else:
        flash('Invalid Username or Password')
    return get_data()

@app.route('/register', methods=['GET','POST'])
def regist():
    if request.method == "GET":

#if not session.get('registered_in'):
        return render_template('register_temp.html')
    
    if request.method == "POST":
        user = request.form['email']
        userq = db.User.find_one({"email":user})
        #print userq
        if userq is None:
            user = db.User()
            user.firstName = request.form['firstName']
            user.lastName = request.form['lastName']
            user.email = request.form['email']
            user.password = generate_password_hash(request.form['password']).decode("utf-8")
            user.phonenumber = request.form['phonenumber']
            user.address = request.form['address']
            user.age = request.form['age']
            user.device_id = request.form['device_id']
            user.save()
            flash('Sucessfully registered')            
        else:
            flash('Already registered')
            session['registered_in'] = True


        return home()
    else:
        return home()



@app.route('/device_type')
def get_device(device_id,**kwargs):
    device_id = device_id
    #print ">>>>>><<<<<<<<<"
    #print device_id
    return render_template('device_type.html',device_id=device_id)


@app.route('/gpsdata/<device_id>')
def getgps(device_id,**kwargs):
    device_id = device_id
    temp=db.gps.get_gpsdata({"device_id":device_id})
    temp = temp["temp"]
    t=db.gps.find_one(sort=[("_id",pymongo.DESCENDING)])
    #print temp
    #temp = [{l,y},{l,y}]
    #rec = []
    dev= t["device_id"]
    if dev == device_id:

        hu = []
        te = []
        late = []
        lon = []
        for d in temp:
            #print d
            hu.append({'y':int(d['Hum'])})
            te.append({'y':int(d['Temp'])})

        #rec.append({'y':['Hum']})
            #rec+= "{'y':" + d['data']+"},"
    #lat.append({'lat':float(['Lat']),'lon':float(['Lon'])})
    
    
    
        ghum= t["Hum"]
    
        gtemp= t["Temp"]
        #print ghum ; print gtemp

        Lat = t["Lat"]
        Lon = t["Lon"]
    #{lat: -25.363, lng: 131.044};
        #print late
    #print t
    #print hu
    #print te// var lat1= {{lat | tojson}}
        return render_template("dashboard_test_map.html",hum=hu,tem=te,ghum=ghum,gtemp=gtemp,Lat=Lat,Lon=Lon)
    else:
        flash('Sorry The device is not registered')
        return get_device(device_id)




@app.route('/tmpdata/<device_id>', methods=['GET'])
def gettemp(device_id,**kwargs):
    device_id = device_id
    #print ">>>>>>><<<<<<<<"
   # print device_id

    #if request.method == 'GET': 

    temp=db.temp_data.get_tmpdata({"device_id":device_id})
    t=db.temp_data.find_one(sort=[("_id",pymongo.DESCENDING)])
    #print temp
    temp = temp["temp"]
    dev= t["device_id"]
    if dev == device_id:
        #print temp
        #temp = [{l,y},{l,y}]
        #rec = []
        hu = []
        te = []
        for d in temp:
            #print d
            hu.append({'y':int(d['Hum'])})
            te.append({'y':int(d['Temp'])})
            #rec.append({'y':['Hum']})
            #rec+= "{'y':" + d['data']+"},"
    
        thum= t["Hum"]
   
        htemp= t["Temp"]
        #print t
        #print hu
        #print te
        return render_template("dashboard_test.html",hum=hu,tem=te,thum=thum,htemp=htemp)
    else:
        flash('Sorry The device is not registered')
        return get_device(device_id)





    #if request.method == 'POST':
        
     #   return home()

    #  print r.status_code
    #print r.content
    #print r.json
    #print r.data
    #return home()

    

'''@app.route('/customer',methods=['GET','POST'])
def get_data(**kwargs):
    #print username'''

@app.route("/employ")
def dept():
    '''manag=db.empdata.getemployee({'dept':'managdept'})
    manag= manag["users"]


    admin=db.empdata.getemployee({'dept':'admindept'})
    admin= admin["users"]

    engin=db.empdata.getemployee({'dept':'engdept'})
    engin= engin["users"]

    secur=db.empdata.getemployee({'dept':'secdept'})
    secur= secur["users"]

    visit=db.empdata.getemployee({'dept':'visitor'})
    visit= visit["users"]

    return render_template("employee.html",manag=manag,admin=admin,secur=secur,engin=engin,visit=visit)'''

    engz=db.Engdept.find_one({'name':'zac'},sort=[("_id",pymongo.DESCENDING)])
    enga=db.Engdept.find_one({'name':'ali'},sort=[("_id",pymongo.DESCENDING)])
    engp=db.Engdept.find_one({'name':'prasad'},sort=[("_id",pymongo.DESCENDING)])
    engin =[]
    #a.append(engz)
    #a.append(enga)
    #a.append(engp)
    engin.extend([engp,engz,enga])
    

    mant=db.Managdept.find_one({'name':'Tom'},sort=[("_id",pymongo.DESCENDING)])
    mans=db.Managdept.find_one({'name':'shawn'},sort=[("_id",pymongo.DESCENDING)])
    manm=db.Managdept.find_one({'name':'manish'},sort=[("_id",pymongo.DESCENDING)])
    manag=[]
    manag.extend([mant,mans,manm])


    secse=db.Secdept.find_one({'name':'secu'},sort=[("_id",pymongo.DESCENDING)])
    secsu=db.Secdept.find_one({'name':'suzuki'},sort=[("_id",pymongo.DESCENDING)])
    seck=db.Secdept.find_one({'name':'kaustubh'},sort=[("_id",pymongo.DESCENDING)])
    secur=[]
    secur.extend([secse,secsu,seck])



    adms=db.Admindept.find_one({'name':'selena'},sort=[("_id",pymongo.DESCENDING)])
    admi=db.Admindept.find_one({'name':'ivory'},sort=[("_id",pymongo.DESCENDING)])
    adma=db.Admindept.find_one({'name':'alan'},sort=[("_id",pymongo.DESCENDING)])
    admin=[]
    admin.extend([adms,admi,adma])

    #t=db.Engdept.find().sort("name",pymongo.DESCENDING)
    


    '''manag=db.Managdept.getmanagdept({})
    manag = manag["users"]

    admin=db.Admindept.getadmindept({})
    #print admin
    #print "--->>>>>><<<<<<<<---"
    admin = admin ["users"]
    #print admin

    secur=db.Secdept.getsecdept({})
    secur=secur["users"]

    engin=db.Engdept.getengdept({})
    engin=engin["users"]'''
    visit=[]
    for t in db.Visitor.find().sort('_id',pymongo.DESCENDING).limit(3):
        visit.append(t)
        #print t
    #t=db.Engdept.find_one({'name':'zac'},sort=[("_id",pymongo.DESCENDING)])
    

    #visit=db.Visitor.getvisitor({})
    #visit=visit["users"]
    return render_template("employee.html",manag=manag,admin=admin,secur=secur,engin=engin,visit=visit)

    
@app.route("/managattendance/<name>")
def manag_att(name,**kwargs):
    manag=db.Managdept.getmanagdept({"name":name})
    manag=manag["users"]



    return render_template("employee_attendance.html",attend=manag,name=name)

@app.route("/engattendance/<name>")
def eng_att(name,**kwargs):
    eng=db.Engdept.getengdept({"name":name})
    eng=eng["users"]
    

    return render_template("employee_attendance.html",attend=eng,name=name)

@app.route("/adminattendance/<name>")
def ad_att(name,**kwargs):
    ad=db.Admindept.getadmindept({"name":name})
    ad=ad["users"]
    

    return render_template("employee_attendance.html",attend=ad,name=name)

@app.route("/secattendance/<name>")
def sec_att(name,**kwargs):
    sec=db.Secdept.getsecdept({"name":name})
    sec=sec["users"]
    

    return render_template("employee_attendance.html",attend=sec,name=name)


@app.route("/visitlist")
def visit_att():
    sec=db.Visitor.getvisitor({})
    sec=sec["users"]
    

    return render_template("visitorlist.html",attend=sec)



@app.route("/floor")
def floor_map():
    return render_template("floor_maps.html")


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()





@app.route('/report',methods=["POST"])
#@allowed_api_roles(['customer'])
def GenerateHBPDFHTML(**kwargs):
    doc = SimpleDocTemplate("/tmp/Health Report.pdf")

    name = request.form['employee_name']
    

    modelResponse = db.Managdept.getmanagdept({'name':name})
    customer = modelResponse['users']

    name = customer[0]['name']
    id = customer[0]['_id']
    intime = customer[0]['intime']
    outtime = customer[0]['outtime']
    '''customer_id = measurement['customer_id'];   subcustomer_id = measurement['subcustomer_id']
    modelResponse = db.Customer.getCustomer({'_id':ObjectId(customer_id)})
    customer = modelResponse['customer']
    modelResponse = db.subCustomer.getSubCustomer({'_id':ObjectId(subcustomer_id)})
    subcustomer = modelResponse['subcustomer']
    customerName = customer['firstName']+" "+customer['lastName']
    subcustomerName = subcustomer['firstName']+" "+subcustomer['lastName']

    sdatetime = datetime.strptime(request.form['stime'], "%Y-%m-%d %H:%M:%S")
    edatetime = request.form['etime']
    edatetime = datetime.strptime(edatetime, "%Y-%m-%d %H:%M:%S")
    edatetime = edatetime + timedelta(days=1)'''

    doc = PDF.hbpdfbuilder(name=name,id=id,intime=intime,outtime=outtime,modelResponse=customer, title='Attendance Report')

    doc.export('/tmp/Health Report.pdf')
    return send_from_directory('/tmp', 'Health Report.pdf', as_attachment=True)

    



if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5000',debug=True)


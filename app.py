from tkinter import scrolledtext
import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import LinearSVC
from xgboost import XGBClassifier
from flask import *
import mysql.connector
db=mysql.connector.connect(user="root",password="",port='3306',database='disease')
cur=db.cursor()

app=Flask(__name__)
app.secret_key="CBJcb786874wrf78chdchsdcv"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/userhome')
def userhome():
    return render_template('userhome.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        useremail=request.form['useremail']
        session['useremail']=useremail
        userpassword=request.form['userpassword']
        sql="select * from user where Email='%s' and Password='%s'"%(useremail,userpassword)
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()
        if data ==[]:
            msg="user Credentials Are not valid"
            return render_template("login.html",name=msg)
        else:
            return render_template('userhome.html')
    return render_template('login.html')

@app.route('/registration',methods=["POST","GET"])
def registration():
    if request.method=='POST':
        username=request.form['username']
        useremail = request.form['useremail']
        userpassword = request.form['userpassword']
        conpassword = request.form['conpassword']
        Age = request.form['Age']
        
        contact = request.form['contact']
        if userpassword == conpassword:
            sql="select * from user where Email='%s' and Password='%s'"%(useremail,userpassword)
            cur.execute(sql)
            data=cur.fetchall()
            db.commit()
            print(data)
            if data==[]:
                
                sql = "insert into user(Name,Email,Password,Age,Mob)values(%s,%s,%s,%s,%s)"
                val=(username,useremail,userpassword,Age,contact)
                cur.execute(sql,val)
                db.commit()
                flash("Registered successfully","success")
                return render_template("login.html")
            else:
                flash("Details are invalid","warning")
                return render_template("registration.html")
        else:
            flash("Password doesn't match", "warning")
            return render_template("registration.html")
    return render_template('registration.html')


# @app.route('/diabetes',methods=['POST','GET'])
# def diabetes():
#     global x_train,y_train
#     #input variables
#     if request.method == "POST":
#         Pregnancies = float(request.form['Pregnancies'])
#         Glucose = float(request.form['Glucose'])
#         BloodPressure = float(request.form['BloodPressure'])
#         SkinThickness = float(request.form['SkinThickness'])
#         Insulin = float(request.form['Insulin'])
#         BMI = float(request.form['BMI'])
#         DiabetesPedigreeFunction = float(request.form['DiabetesPedigreeFunction'])
#         Age = float(request.form['Age'])

#         lee = [Pregnancies,Glucose,BloodPressure, SkinThickness, Insulin,BMI,DiabetesPedigreeFunction,Age]
#         print(lee)
        
#         import pickle
#         with open("DecisionTreeClassifier(diabetes).pkl", 'rb') as fp:
#             model = pickle.load(fp) 
#         result=model.predict([lee])
#         result=result[0]
#         if result==0:
#             msg="The Person has NO-Diabetes"
#         elif result==1:
#             msg="The Person has Diabetes"
#         return render_template("diabetes.html",msg=msg)
#     return render_template("diabetes.html")

# # @app.route('/breastcancer',methods=['POST','GET'])
# # def breastcancer():
# #     global x_train,y_train,x_test,y_test,x,y,df1

# #     #input variables
# #     if request.method == "POST":
# #         radius_mean = float(request.form['radius_mean'])
# #         texture_mean = float(request.form['texture_mean'])
# #         smoothness_mean = float(request.form['smoothness_mean'])
# #         compactness_mean = float(request.form['compactness_mean'])
# #         symmetry_mean = float(request.form['symmetry_mean'])
# #         fractal_dimension_mean = float(request.form['fractal_dimension_mean'])
# #         texture_se = float(request.form['texture_se'])
# #         smoothness_se = float(request.form['smoothness_se'])
# #         symmetry_se = int(request.form['symmetry_se'])
# #         symmetry_worst = float(request.form['symmetry_worst'])

# #         lee = [radius_mean,texture_mean,smoothness_mean, compactness_mean, symmetry_mean,fractal_dimension_mean,texture_se,smoothness_se,symmetry_se,symmetry_worst]
# #         print(lee)
        
# #         import pickle
# #         filename = 'AdaBoostClassifier(breast).sav'
# #         model = pickle.load(open(filename, 'rb'))
# #         result=model.predict([lee])
# #         result=result[0]
# #         if result==0:
# #             msg="The patient is in benign(cancer-free)"
# #         elif result==1:
# #             msg="The patient is in Malignant(suffering with cancer)"
# #         return render_template("breastcancer.html",msg=msg)
# #     return render_template("breastcancer.html")

# @app.route('/breastcancer',methods=['POST','GET'])
# def breastcancer():
#     global x_train,y_train,x_test,y_test,x,y,df1

#     #input variables
   				
#     if request.method == "POST":
#         Age = float(request.form['Age'])
#         Sex = float(request.form['Sex'])
#         Chest_pain_type = float(request.form['Chest pain type'])
#         BP = float(request.form['BP'])
#         Cholesterol = float(request.form['Cholesterol'])
#         FBS_over_120 = float(request.form['FBS over 120'])
#         EKG_results = float(request.form['EKG results'])
#         Max_HR = float(request.form['Max HR'])
#         Exercise_angina = int(request.form['Exercise angina'])
#         ST_depression = float(request.form['ST depression'])
#         Slope_of_ST = float(request.form['Slope of ST'])
#         Number_of_vessels_fluro	 = int(request.form['Number of vessels fluro'])
#         Thallium = float(request.form['Thallium'])

#         lee = [Age, Sex, Chest_pain_type, BP, Cholesterol, FBS_over_120, EKG_results, Max_HR, 
#                Exercise_angina, ST_depression, Slope_of_ST, Number_of_vessels_fluro, Thallium]
#         print(lee)
        
#         import pickle
#         with open("CatBoostClassifier(herat).pkl", 'rb') as fp:
#             model = pickle.load(fp)
#         result=model.predict([lee])
#         result=result[0]
#         if result==0:
#             msg="The patient dont't have a Heart Diseas"
#         elif result==1:
#             msg="The patient has a Heart Diseas"
#         return render_template("breastcancer.html",msg=msg)
#     return render_template("breastcancer.html")

# @app.route('/liver',methods=['POST','GET'])
# def liver():
#     global X_train,y_train,X_test,y_test,x,y
    
#     #input variables
#     if request.method == "POST":
#         Age = float(request.form['Age'])
#         Gender = float(request.form['Gender'])
#         Total_Bilirubin = float(request.form['Total_Bilirubin'])
#         Direct_Bilirubin = float(request.form['Direct_Bilirubin'])
#         Alkaline_Phosphotase = float(request.form['Alkaline_Phosphotase'])
#         Alamine_Aminotransferase = float(request.form['Alamine_Aminotransferase'])
#         Aspartate_Aminotransferase = float(request.form['Aspartate_Aminotransferase'])
#         Total_Protiens = float(request.form['Total_Protiens'])
#         Albumin = int(request.form['Albumin'])
#         Albumin_and_Globulin_Ratio = float(request.form['Albumin_and_Globulin_Ratio'])

#         lee = [Age,Gender,Total_Bilirubin,Direct_Bilirubin,Alkaline_Phosphotase,Alamine_Aminotransferase,Aspartate_Aminotransferase,Total_Protiens,Albumin,Albumin_and_Globulin_Ratio]
#         print(lee)
        
#         import pickle
#         with open("XGBClassifier(liver).pkl", 'rb') as fp:
#             model = pickle.load(fp)
#         result=model.predict([lee])
#         result=result[0]
#         if result==0:
#             msg="The Person has No-Liver Disease"
#         elif result==1:
#             msg="The Person has Liver Disease"
#         return render_template("liver.html",msg=msg)
#     return render_template("liver.html")





@app.route('/graph')
def graph ():

    # pic = pd.DataFrame({'Models_diabetes':['Decision tree Classifier','XGBoostClassifier','AdaBoostClassifier','Catboost'],'Accuracy':[score1,score3,score2,score5,score4]})
    # pic = pd.DataFrame({'Models_breastcancer':['Decision tree Classifier','XGBoostClassifier','AdaBoostClassifier','Catboost'],'Accuracy':[score1,score3,score2,score5,score4]})
    # pic = pd.DataFrame({'Models_liver':['Decision tree Classifier','XGBoostClassifier','AdaBoostClassifier','Catboost'],'Accuracy':[score1,score3,score2,score5,score4]})
    # pic = pd.DataFrame({'Models_kidney':['Decision tree Classifier','XGBoostClassifier','AdaBoostClassifier','Catboost'],'Accuracy':[score1,score3,score2,score5,score4]})
    # pic


    # plt.figure(figsize = (10,6))
    # sns.barplot(y = pic.Accuracy,x = pic.Models_diabetes)
    # sns.barplot(y = pic.Accuracy,x = pic.Models_breastcancer)
    # sns.barplot(y = pic.Accuracy,x = pic.Models_liver)
    # sns.barplot(y = pic.Accuracy,x = pic.Models_kidney)

    # plt.xticks(rotation = 'vertical')
    # plt.show()

    return render_template('graph.html')




if __name__=='__main__':
    app.run(debug=True)
import ply.lex as lex
import ply.yacc as yacc
import sys
import re
import os
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
#Global variables
data1 =["Total cases","Active cases","Total Death","Total recovered","Total tests","Death/Million","Test/Million","New Cases","New Death","New Recovered"]
data2 = ["Change in active cases","Change in daily death","Change in new recovered","change in new cases","similar change in active cases","similar change in daily death","similar change in new recovered","similar change in new cases"]

month_list = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
month_name = list(month_list)
country_dict = {"World":None,'Asia':None,'North America':None,"South America":None,"Europe":None,"Africa":None,"Oceania":None,'India':'india','Turkey':'turkey','Iran':'iran','Indonesia':'indonesia','Philippines':'philippines','Japan':'japan','Israel':'israel','Malaysia':'malaysia','Thailand':'thailand','Vietnam':'viet-nam','Iraq':'iraq','Bangladesh':'bangladesh','Pakistan':'pakistan','France':'france','UK':'uk',"Russia":'russia',"Italy":'italy',"Germany":'germany',"Spain":'spain',"Poland":'poland',"Netherlands":'netherlands',"Ukraine":'ukraine',"Belgium":'belgium',"USA":'us',"Mexico":'mexico',"Canada":'canada',"Cuba":'cuba',"Costa Rica":'costa-rica',"Panama":'panama',"South Africa":'south-africa',"Morocco":'morocco',"Tunisia":'tunisia',"Ethiopia":'ethiopia',"Libya":'libya',"Egypt":'egypt',"Kenya":'kenya',"Zambia":"zambia","Algeria":'algeria',"Botswana":'botswana',"Nigeria":'nigeria',"Zimbabwe":'zimbabwe',"Australia":'australia',"Fiji":'fiji',"Papua New Guinea":'papua-new-guinea',"New Caledonia":'new-caledonia',"New Zealand":'new-zealand'}
country_name = list(country_dict)

#global variables to store intermediate data
date_currently_infected =""
date_daily_deaths =""
date_daily_cases_recoveries= '' 
data_currently_infected =''
data_daily_deaths =''
data_daily_cases =''
data_daily_recoveries='' 

#dictionary to store data of all country, continent and world and produced by all context free
# grammar rules
all_country_data = {}

#dictionary to store time range data of all country
all_country_range_data = {}


#base class of the GUI
class CovidApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(MainWindow)
    #This function switches between frames
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
    #Exiting from the gui    
    def close_frame(self):
        self.destroy()    

#main frame of the application
class MainWindow(tk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        top = ttk.Frame(self,style="T.TFrame")
        left = ttk.Frame(self,width=300,height=400,style="L.TFrame")
        right = ttk.Frame(self,width=300,height=400,style="R.TFrame")

        heading = ttk.Label(top,text="WELCOME",font=("Helvetica", 18))
        left_label = ttk.Label(left,text="Select country or Continent or World to get Yesterday's covid data",wraplength=150)
        right_label = ttk.Label(right,text="Select country and a range of date to get change in covid data",wraplength=150)
        left_button = ttk.Button(left,text="Go",command=lambda: master.switch_frame(PageOne))
        right_button = ttk.Button(right,text="Go",command=lambda: master.switch_frame(PageTwo))
        exit_button = ttk.Button(self,text="exit",command=lambda:master.close_frame())
        top.grid(row = 0,column=0,columnspan=2)
        left.grid(row=1,column=0)
        right.grid(row=1,column=1)
        heading.grid(row=0,column=0,padx=10,pady=(15,5))
        left_label.grid(row=0,column=0,padx=20,pady=(20,0))
        right_label.grid(row=0,column=0,padx=20,pady=(20,0))
        left_button.grid(row = 1, column=0,padx=20,pady=(0,20),sticky="EW")
        right_button.grid(row = 1, column=0,padx=20,pady=(0,20),sticky="EW")
        exit_button.grid(row=2,column=0,columnspan=2,padx=10,pady=10,sticky="EW")
        styles = ttk.Style()
        styles.configure("T.TFrame",bordercolor = "black",borderwidth=10)
        styles.configure("L.TFrame",background = "gray",bordercolor = "black",borderwidth=10)
        styles.configure("R.TFrame",background = "black",bordercolor = "black",borderwidth=10)
        styles.configure("TButton",background = "blue",foreground = "black")

#This page contains widgets for the first part of the program i.e. data of all country, continent and world
class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        top = ttk.Frame(self,style="T.TFrame")
        left = ttk.Frame(self,width=300,height=400,style="L.TFrame")
        right = ttk.Frame(self,width=300,height=400,style="R.TFrame")
        output_var = tk.StringVar()
        heading = ttk.Label(top,text="PAGE ONE",font=("Helvetica", 18))
        country_label = ttk.Label(left,text="Select Country",wraplength=150)
        data_label = ttk.Label(left,text="Select Option",wraplength=150)
        submit = ttk.Button(self,text="Go",command=lambda : output_var.set(self.submitHandler(country_combo.current(),data_combo.current())))
        output_label = ttk.Label(self,textvariable=output_var,text="output here",background="light green")
        country_combo = ttk.Combobox(right,values=country_name,state="readonly")
        data_combo = ttk.Combobox(right,values=data1,state="readonly")
        exit_button = ttk.Button(self,text="exit",command=lambda:master.close_frame())
        back_button = ttk.Button(self,text = "back",command=lambda: master.switch_frame(MainWindow))
        top.grid(row = 0,column=0,columnspan=2)
        left.grid(row=1,column=0)
        right.grid(row=1,column=1,sticky="N")
        heading.grid(row=0,column=0,padx=10,pady=(15,5))
        country_label.grid(row=0,column=0,padx=20,pady=(20,0),sticky="W")
        data_label.grid(row=1,column=0,padx=20,pady=(20,20),sticky="W")

        country_combo.grid(row = 0,column=0,padx=20,pady=(20,0))
        data_combo.grid(row=1,column=0,padx=20,pady=(20,20))
        #right_button.grid(row = 1, column=0,padx=20,pady=(0,20),sticky="W")
        output_label.grid(row=2,column=0,columnspan=2,sticky="EW",pady=(20,10),padx=10,ipadx=10,ipady=10)
        submit.grid(row = 3, column=0,columnspan=2,padx=10,pady=(10,0),sticky="EW")

        back_button.grid(row = 4,column=0,padx=10,pady=10,sticky="EW")
        exit_button.grid(row=4,column=1,padx=10,pady=10,sticky="EW")
        styles = ttk.Style()
        styles.configure("T.TFrame",bordercolor = "black",borderwidth=10)
        styles.configure("L.TFrame",background = "gray",bordercolor = "black",borderwidth=10)
        styles.configure("R.TFrame",background = "black",bordercolor = "black",borderwidth=10)
        styles.configure("TButton",background = "blue",foreground = "black")
    #This function sends data to the caller when we press the go button also update the log file    
    def submitHandler(self,country_index,query_index):
        logfile = open("log_23.txt","a")
        if(country_index==-1):
            return "Select Country"
        elif(query_index==-1):
            return "Select Option"
        query = ["total_cases","active_cases","total_deaths","total_recovered","total_tests","deaths_per_million","tests_per_million","new_cases","new_deaths","new_recovered"]
        country = country_name[country_index]
        query_result = all_country_data[country][query[query_index]]
        worldPercentage = percentageOfWorld(query_result,all_country_data["World"][query[query_index]])
        if worldPercentage !="N/A":
            worldPercentage=str(worldPercentage)+"%"
        query_result = str(query_result)+"\tWorld percentage: "+worldPercentage
        if query_index+1 == 1:
            logfile.write("<"+country+"> <Total cases> <"+str(all_country_data[country]["total_cases"])+">\n")
            logfile.close()
        elif query_index+1 == 2:
            logfile.write("<"+country+"> <Active cases> <"+str(all_country_data[country]["active_cases"])+">\n")
            logfile.close()
        elif query_index+1 == 3:
            logfile.write("<"+country+"> <Total death> <"+str(all_country_data[country]["total_deaths"])+">\n")
            logfile.close()
        elif query_index+1 == 4:
            logfile.write("<"+country+"> <Total recovered> <"+str(all_country_data[country]["total_recovered"])+">\n")
            logfile.close()
        elif query_index+1 == 5:
            logfile.write("<"+country+"> <Total test> <"+str(all_country_data[country]["total_tests"])+">\n")
            logfile.close()
        elif query_index+1 == 6:
            logfile.write("<"+country+"> <Death/Million> <"+str(all_country_data[country]["deaths_per_million"])+">\n")
            logfile.close()
        elif query_index+1 == 7:
            logfile.write("<"+country+"> <Test/Million> <"+str(all_country_data[country]["tests_per_million"])+">\n")
            logfile.close()
        elif query_index+1 == 8:
            logfile.write("<"+country+"> <New case> <"+str(all_country_data[country]["new_cases"])+">\n")
            logfile.close()
        elif query_index+1 == 9:
            logfile.write("<"+country+"> <New death> <"+str(all_country_data[country]["new_deaths"])+">\n")
            logfile.close()
        elif query_index+1 == 10:
            logfile.write("<"+country+"> <New recovered> <"+str(all_country_data[country]["new_recovered"])+">\n")
            logfile.close()
        return query_result
        
#This frame show time series widgets of the application        
class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)        
        top = ttk.Frame(self,style="T.TFrame")
        left = ttk.Frame(self,width=300,height=400,style="L.TFrame")
        right = ttk.Frame(self,width=300,height=400,style="R.TFrame")
        output_var = tk.StringVar()
        heading = ttk.Label(top,text="PAGE TWO",font=("Helvetica", 18))
        country_label = ttk.Label(left,text="Select Country",wraplength=150)
        data_label = ttk.Label(left,text="Select Option",wraplength=150)
        date1_label = ttk.Label(left,text="Start Date")
        date2_label = ttk.Label(left,text="End Date")
        submit = ttk.Button(self,text="Go",command=lambda : output_var.set(self.submitHandler(country_combo.current(),data_combo.current(),date1.get_date(),date2.get_date())))
        output_label = ttk.Label(self,textvariable=output_var,text="output here",background="light green")
        country_combo = ttk.Combobox(right,values=country_name[7:],state="readonly")
        data_combo = ttk.Combobox(right,values=data2,state="readonly")
        date1 = DateEntry(right,state="readonly")
        date2 = DateEntry(right,state="readonly")
        exit_button = ttk.Button(self,text="exit",command=lambda:master.close_frame())
        back_button = ttk.Button(self,text = "back",command=lambda: master.switch_frame(MainWindow))
        top.grid(row = 0,column=0,columnspan=2)
        left.grid(row=1,column=0)
        right.grid(row=1,column=1,sticky="N")

        heading.grid(row=0,column=0,padx=10,pady=(15,5))
        country_label.grid(row=0,column=0,padx=20,pady=(20,0),sticky="W")
        data_label.grid(row=1,column=0,padx=20,pady=(20,0),sticky="W")
        date1_label.grid(row = 2,column=0,padx=20,pady=(20,0),sticky="W")
        date2_label.grid(row = 3, column=0,padx=20,pady=(20,20),sticky="W")

        country_combo.grid(row = 0,column=0,padx=20,pady=(20,0),sticky="EW")
        data_combo.grid(row=1,column=0,padx=20,pady=(20,0),sticky="EW")
        date1.grid(row=2,column =0,padx=20,pady=(20,0),sticky = "EW")
        date2.grid(row = 3,column = 0,padx=20,pady=(20,20),sticky = "EW")
        output_label.grid(row=2,column=0,columnspan=2,sticky="EW",pady=(20,10),padx=10,ipadx=10,ipady=10)
        submit.grid(row = 3, column=0,columnspan=2,padx=10,pady=(10,0),sticky="EW")

        back_button.grid(row = 4,column=0,padx=10,pady=10,sticky="EW")
        exit_button.grid(row=4,column=1,padx=10,pady=10,sticky="EW")
        styles = ttk.Style()
        styles.configure("T.TFrame",bordercolor = "black",borderwidth=10)
        styles.configure("L.TFrame",background = "gray",bordercolor = "black",borderwidth=10)
        styles.configure("R.TFrame",background = "black",bordercolor = "black",borderwidth=10)
        styles.configure("TButton",background = "blue",foreground = "black")
        styles.configure(".",font=("", 11))

    def submitHandler(self,country_index,query_index,date1,date2):
        logfile = open("log_23.txt","a")
        if(country_index==-1):
            return "Select Country"
        elif(query_index==-1):
            return "Select Option"    
        elif(date1>date2):
            return "End date before Start date"
        date1 = date1.strftime("%b.%d.%Y")
        date2=date2.strftime("%b.%d.%Y")
        country = country_name[country_index+7]
        percentage = collectPercentage(date1,date2,all_country_range_data[country])
        if percentage == -1: 
            return "Date1 out of range"
        elif percentage==-2:
            return "Date2 out of range"    
        similar_case_country=""
        similar_case_data = 1000000
        similar_death_country = ""
        similar_death_data = 1000000
        similar_recovery_country = ""
        similar_recovery_data = 1000000
        similar_new_case_country = ""
        similar_new_case_data = 1000000
        for index in range(7,len(country_name)):
            name = country_name[index]
            if name != country:
                percentage1 = collectPercentage(date1,date2,all_country_range_data[name])
                if(percentage1==-1 or percentage1 == -2):
                    continue
                if percentage1[0] and percentage[0] and abs(percentage1[0]-percentage[0])<similar_case_data:
                    similar_case_country = name
                    similar_case_data = abs(percentage1[0]-percentage[0])
                if percentage1[1] and percentage[1] and abs(percentage1[1]-percentage[1])<similar_death_data:
                    similar_death_country = name
                    similar_death_data = abs(percentage1[1]-percentage[1])
                if percentage1[2] and percentage[2] and abs(percentage1[2]-percentage[2])<similar_recovery_data:
                    similar_recovery_country = name
                    similar_recovery_data = abs(percentage1[2]-percentage[2])
                if percentage1[3] and percentage[3] and abs(percentage1[3]-percentage[3])<similar_new_case_data:
                    similar_new_case_country = name  
                    similar_new_case_data = abs(percentage1[3]-percentage[3])
		    

        if query_index+1 ==1:
            perc = percentage[0] if percentage[0] else "N/A"
            logfile.write(f"<{country}> <change in active cases from {date1} to {date2}> <{perc}%>\n")
            logfile.close()
            return str(round(perc,2))+"%" if perc!="N/A" else perc
        elif query_index+1 ==2:
            perc = percentage[1] if percentage[1] else "N/A"
            logfile.write(f"<{country}> <change in daily death from {date1} to {date2}> <{perc}%>\n")
            logfile.close()
            return str(round(perc,2))+"%" if perc!="N/A" else perc
        elif query_index+1 == 3:
            perc = percentage[2] if percentage[2] else "N/A"
            logfile.write(f"<{country}> <change in new recovered from {date1} to {date2}> <{perc}%>\n")
            logfile.close()
            return str(round(perc,2))+"%" if perc!="N/A" else perc
        elif query_index+1 == 4:
            perc = percentage[3] if percentage[3] else "N/A"
            logfile.write(f"<{country}> <change in new cases from {date1} to {date2}> <{perc}%>\n")
            logfile.close()
            return str(round(perc,2))+"%" if perc!="N/A" else perc
        elif query_index+1==5:
            val = similar_case_country if similar_case_country!="" else "Not Found"
            logfile.write(f"<{country}> <country similar to change in active case from {date1} to {date2}> <{val}>\n")
            logfile.close()
            return val
        elif query_index+1 ==6:
            val = similar_death_country if similar_death_country!="" else "Not Found"
            logfile.write(f"<{country}> <country similar to change in daily deaths from {date1} to {date2}> <{val}>\n")
            logfile.close()
            return val
        elif query_index+1 == 7:
            val = similar_recovery_country if similar_recovery_country!="" else "Not Found"
            logfile.write(f"<{country}> <country similar to change in newly recovered from {date1} to {date2}> <{val}>\n")
            logfile.close()
            return val
        elif query_index+1 == 8:
            val = similar_new_case_country if similar_new_case_country!="" else "Not Found"
            logfile.write(f"<{country}> <country similar to change in new cases from {date1} to {date2}> <{val}>\n") 
            logfile.close()
            return val                    

#convert space separated string to integer
def sTOn(s):
    if(s==None or s=="N A"):
        return None
    r =s.replace(' ','')    
    if(r):
        return int(r)
    return 0  

#convert space separated strings to float
def sTOf(s):
    if(s==None or s=="N A"):
        return None
    r =s.replace(' ','')    
    if(r):
        return float(r)
    return 0 

#calculate the percentage of the world data(data one is the data of the country and data two is the data of the world)
def percentageOfWorld(data1,data2):
    if(data1 ==None or not data2):
        return "N/A"
    return round((data1/data2)*100,2)    

#calculate percentage change in data in the given range
def collectPercentage(date1,date2,country_data):
    currently_infected = country_data["currently_infected"]
    daily_deaths=country_data["daily_deaths"]
    daily_cases = country_data["daily_cases"]
    daily_recoveries=country_data["daily_recoveries"]
    if date1 not in currently_infected.keys():
        return -1
    if date2 not in currently_infected.keys():
        return -2
    ret = [(((currently_infected[date2]-currently_infected[date1])/currently_infected[date1]) *100) if currently_infected[date1] and currently_infected[date2]!=None else None,
           (((daily_deaths[date2]-daily_deaths[date1])/daily_deaths[date1]) *100) if daily_deaths[date1] and daily_deaths[date2]!=None else None,
           (((daily_recoveries[date2]-daily_recoveries[date1])/daily_recoveries[date1]) *100) if len(daily_recoveries)!=0 and  daily_recoveries[date1] and daily_recoveries[date2]!=None else None,
           (((daily_cases[date2]-daily_cases[date1])/daily_cases[date1]) *100) if daily_cases[date1] and daily_cases[date2]!=None else None] 
    return ret

#all tokens 
tokens = [
    'TABLESTART',
    'THEADSTART',
    'THEADEND',
    'TBODYSTART',
    'TBODYEND',
    'TRSTART',
    'TREND',
    'THSTART',
    'THEND',
    'TDSTART',
    'TDEND',
    'NOBRSTART',
    'NOBREND',
    'SPANSTART',
    'SPANEND',
    'ASTART',
    'AEND',
    'NAME',
    'BR',
    'NBSP',
    'CURRENTLYINFECTED',
    'CURRENTLYINFECTEDDATA',
    'OPENBRACE',
    'CLOSEBRACE',
    'OPENCBRACE',
    'CLOSECBRACE',
    'DAILYDEATHS',
    'DAILYDEATHSDATA',
    'NEWCASESRECOVERIES',
    'NEWCASESDATA',
    'NEWRECOVERIESDATA',
    'DAILYNEWCASES',
    'DAILYNEWCASESDATE'
]

#all tokens have intutive meaning
def t_TABLESTART(t):
    r'<table\sid="main_table_countries_yesterday"\sclass="table\stable-bordered\stable-hover\smain_table_countries"\sstyle="width:100%;margin-top:\s0px\s!important;display:none;">'
    return t


def t_THEADSTART(t):
    r'<thead>'
    return t

def t_THEADEND(t):
    r'</thead>'
    return t

def t_TBODYSTART(t):
    r'<tbody>'
    return t

def t_TBODYEND(t):
    r'</tbody>'
    return t


def t_TRSTART(t):
    r'<tr[^>]*>'
    return t   

def t_TREND(t):
    r'</tr>'
    return t

def t_TDSTART(t):
    r'<td[^>]*>'         
    return t

def t_TDEND(t):
    r'</td>'
    return t

def t_THSTART(t):
    r'<th[^>]*>'
    return t

def t_THEND(t):
    r'</th>'
    return t

def t_NOBRSTART(t):
    r'<nobr>'
    return t  

def t_NOBREND(t):
    r'</nobr>'
    return t

def t_SPANSTART(t):
    r'<span[^>]*>'
    return t

def t_SPANEND(t):
    r'</span>'
    return t        

def t_ASTART(t):
    r'<a[^>]*>'
    return t

def t_AEND(t):
    r'</a>'
    return t

def t_BR(t):
    r'<br\s/>'
    return t    

def t_NBSP(t):
    r'&nbsp;'
    return t

def t_DAILYNEWCASESDATE(t):
    r'text:\s\'Daily\sNew\sCases\''
    return t

def t_DAILYNEWCASES(t):
    r'name:\s\'Daily\sCases\''
    return t

def t_CURRENTLYINFECTED(t):
    r'text:\s\'Active\sCases\''
    return t

def t_CURRENTLYINFECTEDDATA(t):
    r'name:\s\'Currently\sInfected\''
    return t

def  t_DAILYDEATHS(t):
    r'text:\s\'Daily\sDeaths\'' 
    return t

def t_DAILYDEATHSDATA(t):
    r'name:\s\'Daily\sDeaths\''  
    return t 

def t_NEWCASESRECOVERIES(t):
    r'text:\s\'New\sCases\svs.\sNew\sRecoveries\''
    return t

def t_NEWCASESDATA(t):
    r'name:\s\'New\sCases\''
    return t

def t_NEWRECOVERIESDATA(t):
    r'name:\s\'New\sRecoveries\''  
    return t  

def t_OPENCBRACE(t):
    r'{'
    return t

def t_CLOSECBRACE(t):
    r'}'
    return t

def t_OPENBRACE(t):
    r'\['
    return t

def t_CLOSEBRACE(t):
    r'\]'
    return t


def t_NAME(t):
    r'[A-Za-z0-9.+-]+'
    return t   

t_ignore = " \t"

def t_error(t):
	t.lexer.skip(1)


# Parsing rules
# This production will collect data of all countries, continent and world
def p_allcovdata(t):
    '''allcovdata : TABLESTART  heading  covdata  TBODYEND'''

def p_heading(t):
    '''heading : THEADSTART  headingrow  THEADEND'''

#each row contains 22 beadings
def p_headingrow(t):
    '''headingrow : TRSTART hbr  hbr hbr hbr hbr hbr hbr hbr hbr hbr hbr hbr hbr hbr  hbr hbr hbr hbr hbr hbr hbr hbr TREND'''     
    
def p_hbr(t):
    '''hbr : THSTART name BR name THEND
           | THSTART name THEND
           | THSTART THEND
           | THSTART name BR NOBRSTART name NOBREND THEND
           | THSTART name NBSP name BR name THEND'''
               
def p_name(t):
    '''name : NAME
            | NAME name'''
    if len(t)==3:
        t[0] = ' '.join(t[1:])
    else:    
        t[0] = ''.join(t[1])               
           

def p_covdata(t):
    '''covdata : TBODYSTART datarow '''

#each row contains 32 table data
def p_datarow(t):
    '''datarow : TRSTART dt dt dt dt dt dt dt dt dt dt dt dt dt dt dt dt dt dt dt dt dt dt TREND
               | TRSTART dt dt dt dt dt dt dt dt dt dt dt dt dt dt dt dt dt dt dt dt dt dt TREND datarow'''
    one_country = {}
    one_country["serial_no"]=sTOn(t[2])
    one_country["country"] = t[3]
    one_country["total_cases"]= sTOn(t[4])
    one_country["new_cases"]=sTOn(t[5])
    one_country["total_deaths"]=sTOn(t[6])
    one_country["new_deaths"]=sTOn(t[7])
    one_country["total_recovered"]=sTOn(t[8])
    one_country["new_recovered"]=sTOn(t[9])
    one_country["active_cases"]=sTOn(t[10])
    one_country["deaths_per_million"]=sTOf(t[13])
    one_country["total_tests"]=sTOn(t[14])
    one_country["tests_per_million"]=sTOf(t[15])
    one_country["continent"]=t[17]
    one_country["population"]=sTOn(t[16])
    one_country["one_case_per_people"] = sTOn(t[18])
    one_country["one_death_per_people"] = sTOn(t[19])
    one_country["one_test_per_people"] = sTOn(t[20])
    one_country["new_cases_per_million"] = sTOf(t[21])
    one_country["new_deaths_per_million"] = sTOf(t[22])
    one_country["cases_per_million"] = sTOf(t[23])
    #inserting the data to a dictionary with key as the country/continent/world name for better query speed
    all_country_data[t[3]] = one_country

def p_tr(t):
    '''dt : TDSTART TDEND
          | TDSTART name TDEND
          | TDSTART NOBRSTART name NOBREND TDEND
          | TDSTART NOBRSTART NOBREND TDEND
          | TDSTART ASTART name AEND TDEND
          | TDSTART SPANSTART name SPANEND TDEND'''  
    if(len(t)==4):
        t[0] = t[2]
    elif len(t) == 6:
        t[0]=t[3]  

#This is the start production to collect time series data
def p_onecountry(t):
    '''onecountry : currentlyinfected
                | dailydeaths
                | currentlyinfecteddata
                | dailydeathsdata
                | newrecoveriesdata
                | dailynewcasesdata
                | dailynewcasesdate'''

def p_currentlyinfected(t):
    '''currentlyinfected : CURRENTLYINFECTED skip OPENBRACE alldates CLOSEBRACE'''
    global date_currently_infected
    date_currently_infected =t[4]
    #print("date infected ",t[4])

def p_dailynewcasesdata(t):
    '''dailynewcasesdata : DAILYNEWCASES skip OPENBRACE alldata CLOSEBRACE'''
    global data_daily_cases 
    data_daily_cases = t[4]
    #print('daily new cases data',t[4])    
    
def p_dailynewcasesdate(t):
    '''dailynewcasesdate : DAILYNEWCASESDATE skip OPENBRACE alldates CLOSEBRACE'''
    global date_daily_cases_recoveries
    date_daily_cases_recoveries = t[4]
    
def p_dailydeaths(t):
    '''dailydeaths : DAILYDEATHS skip OPENBRACE alldates CLOSEBRACE'''
    global date_daily_deaths
    date_daily_deaths = t[4]
    #print("date dailydeaths",t[4])
    
      

def p_currentlyinfecteddata(t):
    '''currentlyinfecteddata : CURRENTLYINFECTEDDATA skip OPENBRACE alldata CLOSEBRACE'''  
    global data_currently_infected
    data_currently_infected = t[4]
    #print("data infected",t[4]) 
           
    
def p_dailydeathsdata(t):
    '''dailydeathsdata : DAILYDEATHSDATA skip OPENBRACE alldata CLOSEBRACE'''
    global data_daily_deaths
    data_daily_deaths = t[4]
    #print("data death",t[4])
    

    
def p_newrecoveriesdata(t):
    '''newrecoveriesdata : NEWRECOVERIESDATA skip OPENBRACE alldata CLOSEBRACE'''
    global data_daily_recoveries
    data_daily_recoveries = t[4]
    #print("data recovered",t[4])
    

def p_alldates(t):
    '''alldates : NAME NAME NAME
                | NAME NAME NAME alldates'''
    temp = t[1]+'.'+t[2]+'.'+t[3]
    if len(t)==4:
        t[0]=temp
    else:
        t[0]=temp+' '+t[4]               

def p_alldata(t):
    '''alldata : NAME
               | NAME alldata'''    
    if len(t)==2:
        t[0]=t[1]
    elif len(t)==3:
        t[0] = ' '.join(t[1:])                          

#this production will skip some tokens
def p_skip(t):
    '''skip : NAME
            | NAME skip
            | OPENCBRACE
            | OPENCBRACE skip
            | CLOSECBRACE
            | CLOSECBRACE skip
            '''

def p_error(t):
    pass

if __name__ == "__main__":
    cwd = os.getcwd()
    filepath1 = os.path.join(cwd,'countries',"world.html")
    try:
        text = open(filepath1,"r").read()
    except:
        print("File not found. Try running task1 first")
        exit(0)    
    lexer = lex.lex()
    lexer.input(str(text))
    parser1 = yacc.yacc(start = 'allcovdata')
    parser1.parse(text)

    parser = yacc.yacc(start = "onecountry")
    #filling time range data of all countries
    for country in range(7,len(country_dict)):
        listglobals = globals()
        listglobals["date_currently_infected"] = ''
        listglobals["date_daily_deaths"]=''
        listglobals["date_daily_cases_recoveries"]=''
        listglobals["data_daily_deaths"]=''
        listglobals["data_currently_infected"]=''
        listglobals["data_daily_cases"]=''
        listglobals["data_daily_recoveries"]=''
        filepath = os.path.join(cwd,'countries',country_dict[country_name[country]]+'.html')
        try:
            txt = open(filepath,"r").read()
        except:
            print("File not found. Try running task1 first")
            exit(0)     
        lexer = lex.lex()
        lexer.input(str(txt))
        parser.parse(txt)
        currently_infected = {}
        daily_deaths = {}
        daily_cases = {}
        daily_recoveries = {}
        for date_i, data in zip(date_currently_infected.split(" "),data_currently_infected.split(' ')):
            currently_infected[date_i] = int(data) if data!='null' and data else None
        for date_i, data in zip(date_daily_deaths.split(" "),data_daily_deaths.split(' ')):
            daily_deaths[date_i] = int(data) if data!='null' and data else None
        for date_i, data in zip(date_daily_cases_recoveries.split(" "),data_daily_cases.split(' ')):
            daily_cases[date_i] = int(data) if data!='null' and data else None
        if(data_daily_recoveries):    
            for date_i, data in zip(date_daily_cases_recoveries.split(" "),data_daily_recoveries.split(' ')):
                daily_recoveries[date_i] = int(data) if data!='null' and data else None 
        all_country_range_data[country_name[country]] = {}
        #storing the data in a dictionary country name as key for better search
        all_country_range_data[country_name[country]]["currently_infected"]=currently_infected
        all_country_range_data[country_name[country]]["daily_deaths"]=daily_deaths
        all_country_range_data[country_name[country]]['daily_cases']=daily_cases
        all_country_range_data[country_name[country]]["daily_recoveries"]= daily_recoveries       
    print("Use the GUI to interact")
    #Just run the gui to interact with users
    app = CovidApp()
    app.title("covid info")
    app.mainloop()

    

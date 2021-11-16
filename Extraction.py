import json
"""
+----------------------+
+      Question 1      +
+----------------------+
"""

# 1. Number of URLH which are overlapping (Common) in two files.
def q1():
    urlh_tod={0} #empty sets to store urlh data from today file
    urlh_yest={1} #empty sets to store urlh data from yesterday file
    with open("today.json") as file:
        for obj in file: #read each json obj and store in a temp dict
            dic = json.loads(obj)
            urlh_tod.add(dic["urlh"])
    with open("yesterday.json") as file2:
        for obj in file2:
            dic = json.loads(obj)
            urlh_yest.add(dic["urlh"])
    y = urlh_tod.intersection(urlh_yest)# Built-in set function to find the intersection of 2 sets(toay,yesterday)
    print(len(y)) #The final common elements count


"""
+----------------------+
+      Question 2      +
+----------------------+
"""
# 2. For all the URLH which are overlapping, calculate the price difference (wrt available_price) if there is any between yesterday's and today's crawls (scraped data). There might be duplicate URLHs in which case you can choose the first valid (with http_status 200) record. (todo)
def q2():
    tod=[] #empty lists to store data from today file
    yest=[] #empty lists to store  data from yesterday file
    with open("today.json") as file:
        for obj in file: 
            dic = json.loads(obj)
            tod.append(dic)
    with open("yesterday.json") as file2:
        for obj in file2:
            dic = json.loads(obj)
            yest.append(dic)      
    #temperary dictionary to store the data and removing the duplication 
    main_yest = {}  #format like {urlh:[http_status,available_price]}
    main_tod = {}
    
    #iteratting in the yesterday's data 
    for i in yest:
        if i["urlh"] in main_yest.keys(): #considering the URLH as the key of the dictionary
            if (main_yest[i["urlh"]][0] != 200) and (i["http_status"]==200) and (i["available_price"] != None): #performing multi checks to avoid replication of records
                main_yest[i["urlh"]] = [i["http_status"],i["available_price"]] #if the check is satisfied the dictionary is updated
        elif i["available_price"] != None:
            temp={i["urlh"]:[i["http_status"],i["available_price"]]}
            main_yest.update(temp)
    #same way the today's data is also updated by removing the duplicate the data
    for i in tod:
        if i["urlh"] in main_tod.keys():
            if (main_tod[i["urlh"]][0] != 200) and (i["http_status"]==200) and (i["available_price"] != None):
                main_tod[i["urlh"]] = [i["http_status"],i["available_price"]]
        elif i["available_price"] != None:
            temp={i["urlh"]:[i["http_status"],i["available_price"]]}
            main_tod.update(temp)
    # a list of keys is made to travers in both the dictionary and find the difference using these keys        
    unlist = list(main_yest.keys())
    diff = {} #format {urlh:[http_status,diiference_value]}
    for i in unlist:
        if i in main_tod.keys():
            diffval = float(main_tod[i][1])-float(main_yest[i][1])
            temp = {i:[main_tod[i][0],diffval]}
            diff.update(temp)
    for i in diff.items():
        print(i)
    #Note: if the difference value is negative then we can say that yesterdays available_value is greater than today's value


"""
+----------------------+
+      Question 3      +
+----------------------+
"""
# 3. Number of Unique categories in both files.
def q3():
    cat_today={0} #empty sets to store category data from today file
    cat_yest={1} #empty sets to store category data from yesterday file
    with open("today.json") as file:
        for obj in file: 
            dic = json.loads(obj)
            cat_today.add(dic["category"])
    with open("yesterday.json") as file2:
        for obj in file2:
            dic = json.loads(obj)
            cat_yest.add(dic["category"])
    y = cat_today.union(cat_yest)#the built-in union function of set that concate the both sets and avoids the duplications
    y.remove(0) #as this was a junk value just to define a set 
    y.remove(1) #we will remove it
    print(len(y))


"""
+----------------------+
+      Question 4      +
+----------------------+
"""
# 4. Display List of categories which is not overlapping (Common) from two given files.
def q4():
    cat_today=[] #empty list to store category data from today file
    cat_yest=[]  #empty list to store category data from yesterday file
    with open("today.json") as file:
        for obj in file:
            dic = json.loads(obj)
            cat_today.append(dic["category"])
    with open("yesterday.json") as file2:
        for obj in file2:
            dic = json.loads(obj)
            cat_yest.append(dic["category"]) #extracting only the category names from the dictionary
    dicory={} # empty dictionary that will store the non common category 
    for i in cat_today:
        temp={i:0} 
        dicory.update(temp) #take the category from the first file and assign them as keys and value as 0
    for i in cat_yest:
        if i in dicory.keys():# check the category of yesterday file in dictionary keys
            dicory.pop(i) # pop the common category 
    print(dicory)


    #alternative way
    #c = set(cat_today)
    #d = set(cat_yest)
    #y = c.symmetric_difference(d)
    #print(y)

"""
+----------------------+
+      Question 5      +
+----------------------+
"""
# 5. Generate the stats with count of urlh for all taxonomies (taxonomy is concatenation of category and subcategory separated by " > ") for today's file.
"""Eg:
Cat1 > Subcat1: 3500
Cat1 > Subcat2: 2000
Cat2 > Subcat3: 8900"""
def q5():
    today_data = [] 
    cat_today  = []
    count=0
    with open("today.json") as file:
        for obj in file: 
            dic = json.loads(obj)
            cat_today.append(dic["category"]) #store the category in list
            today_data.append(dic) # store the entire object in list
    cat_today = list(set(cat_today)) #removes the duplication of a list
    for i in cat_today:
        sub_catlist = [] # stores the total subcategory
        for c_obj in today_data:
            if c_obj["category"] == i:
                sub_catlist.append(c_obj["subcategory"])
        uniq_list = list(set(sub_catlist))
        
        for j in uniq_list:
            count+=1
            print(f"{count} {i} > {j} ==> {sub_catlist.count(j)}")  

"""
+----------------------+
+      Question 6      +
+----------------------+
"""
# 6. Generate a new file where mrp is normalized. If there is a 0 or a non-float value or the key doesn't exist, make it "NA".
def q6():
    t_data=[]
    count=0
    with open("today.json") as file:
        for obj in file: 
            dic = json.loads(obj)
            t_data.append(dic)
    for i in t_data:
        if i["mrp"] == None or float(i["mrp"])<=0 or type(i['mrp'])==int : #finding the non float value and nonetype
            i["mrp"]="NA"
    with open("newdata.json","w") as nd:
        for i in t_data:
            json.dump(i,nd,indent=4)
        print("New Data file is Ready")


"""
+----------------------+
+      Question 7      +
+----------------------+
"""
# 7. Display the title and price of 10 items having least price.
"""
Eg:
Title1 --> its price
Title2 --> its price
upto 10
"""
def q7():
    data = []
    with open("today.json") as file:
        for obj in file: 
            dic = json.loads(obj)
            if dic['title'] != None or dic['available_price'] != None: #checking the title and price are non nonetype
                temp = [dic["available_price"],dic["title"]]  
                data.append(temp)
    data = sorted(data) #sorting the data in ascending order
    for i in range(10): #printing the  first 10 data
        print(f"{data[i][1]} --> {data[i][0]}")

"""
+----------------------+
+      Question 8      +
+----------------------+
"""
# 8. Display the top 5 subcategory having highest items.
def q8():
    subcat = []
    data=[]
    with open("today.json") as fo:
        for o in fo:
            dic = json.loads(o)
            subcat.append(dic["subcategory"]) #extract the subcategory from record
    unisub = list(set(subcat)) #removes the duplicates to use them as iterables to travers in the subcateg

    for i in unisub:
        temp = [subcat.count(i),i]
        data.append(temp)
    data = sorted(data,reverse=True)#sort the data in descending order to get the highest values
    for i in range(5):
        print(f"{data[i][1]}-->{data[i][0]}")#prints the sub cat and its item count

"""
+----------------------+
+      Question 9      +
+----------------------+
"""

# 9. Display stats of how many items have failed status (http_status other than 200 is to be considered as failure).
def q9():
    statusdata = []
    with open("today.json") as f:
        for i in f:
            d=json.loads(i)
            if d["http_status"] > "200":  #fetch all the http status greater than 200
                statusdata.append(d["http_status"])
    with open("yesterday.json") as f2:
        for i in f2:
            d = json.loads(i)
            if d["http_status"] > "200":
                statusdata.append(d["http_status"])
    #http status from both the file is appended into the list            
    uq = set(statusdata) #set is made to remove the duplicate values           
    print("Http_status --> count (it is the combination of both yesterdays and todays file)")
    for i in uq:
        print(f"{i} --> {statusdata.count(i)}")#using the list count() to get count of each http status

def driver():
    while True:
        ch = input("Enter the question number you want to search: ")
        if ch.isalpha():
            print("Please enter integer only")
        elif int(ch)==1:
            q1()
        elif int(ch)==2:
            q2()
        elif int(ch)==3:
            q3()
        elif int(ch)==4:
            q4()
        elif int(ch)==5:
            q5()
        elif int(ch)==6:
            q6()
        elif int(ch)==7:
            q7()
        elif int(ch)==8:
            q8()
        elif int(ch)==9:
            q9()
        else:
            print("Invalid question number")
            
driver()
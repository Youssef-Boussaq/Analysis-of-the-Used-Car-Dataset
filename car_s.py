import numpy as np 
import pandas as pd
from statistics import mode
import matplotlib.pyplot as plt
import seaborn as sns

data_care = pd.read_csv('used_cars_data.csv')

#print(data_care.head()) #print five five ligne 

#print(data_care.tail())# print five last ligne 

# data_care.info()
# print(data_care.describe().T)
data_care[data_care.duplicated(keep=False)]

print(data_care.isnull().sum()[data_care.isnull().sum()>0])


# print(data_care[data_care["Mileage"].isnull()])

print(data_care['Mileage'].describe())

data_care['Mileage']= data_care['Mileage'].fillna(mode(data_care['Mileage']))
print(data_care[data_care["Mileage"].isnull()])

print(data_care.isnull().sum()[data_care.isnull().sum()>0])

print("#"*30)
print(data_care["Engine"].value_counts())

data_care['Engine']= data_care['Engine'].fillna(mode(data_care['Engine']))
print(data_care[data_care['Engine'].isnull()])
print("#"*30)
print(data_care.isnull().sum()[data_care.isnull().sum()>0])
print("#"*30)
print(data_care['Power'].describe())
data_care['Power']= data_care['Power'].fillna(mode(data_care['Power']))
print("#"*30)
data_care.loc[data_care['Power'] == 'null bhp' , 'Power'] = mode(data_care['Power'])
print(data_care[data_care['Power']== 'null bhp'])
print("#"*30)
data_care.loc[data_care['Seats']==0 , 'Seats'] = 5
data_care['Seats'] = data_care['Seats'].fillna(mode(data_care['Seats']))
print("#"*30)
data_care[["Mileage_KMPL", "Cell_KMPL"]] = data_care.Mileage.str.split(" ", expand=True)
data_care['Mileage_KMPL'] = data_care['Mileage_KMPL'].astype("float")

print(data_care['Cell_KMPL'])
plt.hist(data_care['Mileage_KMPL'], bins=20)
plt.show()

def mileage_kmpl(data_care):
    if data_care.Mileage_KMPL > 20 :
        return "Performance greater than 20 KMPL"
    elif data_care.Mileage_KMPL > 10:
        return "Performance less than 10 KMPL"
    else : 
        return "Performance between 10 a 20 KMPL"
    
data_care['MileageKMPL'] = data_care.apply(mileage_kmpl, axis=1)
print(data_care)
fig, ax = plt.subplots(figsize=(10,5))
ax.bar(x = data_care["MileageKMPL"].unique(), height = data_care["MileageKMPL"].value_counts(), align = "center")
plt.show()

data_care[["Engine_CC", "Cell_CC"]] = data_care.Engine.str.split(" ", expand=True)
data_care["Engine_CC"] = data_care["Engine_CC"].astype('int64')

data_care[["Power_CC", "Cell_bhp"]] = data_care.Power.str.split(" ", expand=True)

data_care["Power_CC"] = data_care["Power_CC"].astype('float')
print("#"*40)
print(data_care['Engine_CC'])
plt.hist(data_care['Engine_CC'], bins=20)
plt.show()

 
def engine_cc(data_care):
    if data_care.Engine_CC > 2000:
        return "Cylindrara greater than 2000 CC"
    elif data_care.Engine_CC < 1200:
        return "Cilindrara less a 1200 CC"
    else:
        return "Cilindrara between 1200 a 2000 CC"
    
data_care['EngineCC'] = data_care.apply(engine_cc , axis=1)
print("#"*40)
print(data_care['EngineCC'])


fig , ax = plt.subplots(figsize=(10,5))
ax.bar(x=data_care['EngineCC'].unique(),  height = data_care['EngineCC'].value_counts(), align = 'center')
plt.show()




fig , ax = plt.subplots(figsize= (10,5))
ax.bar(x = data_care['Transmission'].unique() , height = data_care['Transmission'].value_counts() , align = 'center')
plt.show()
print("#"*40)
print(data_care['Year'].unique())


fig, ax = plt.subplots(figsize=(10,5))
ax.bar(x = data_care["Year"].unique(), height = data_care["Year"].value_counts(), align = "center")
plt.show()



fig, ax = plt.subplots(figsize=(10,5))
ax.bar(x = data_care["Fuel_Type"].unique(), height = data_care["Fuel_Type"].value_counts(), align = "center")
plt.show()

data_care = data_care.drop(["S.No.", "Mileage", "Engine"], axis=1)
print(data_care.columns)


def find_brand(qeury):
    # qeury = qeury.title()
    filter = data_care.Name.str.contains(qeury, case=False)
    return data_care[filter]
print("#"*30)
print(find_brand("Mahindra"))
data_care["Name"].str.split(" " , expand=True)[0].unique()
l= len(data_care["Name"].str.split(" " , expand=True)[0].unique())
print(l)
data_care["Name"]= data_care["Name"].str.replace("Land Rover", "Land-Rover")
data_care["Name"]= data_care["Name"].str.replace("ISUZU", "Isuzu")


split_names= data_care["Name"].str.split().str[:2]

data_care['Brand']= split_names.str[0]
data_care['Model']= split_names.str[1]

print(data_care['Brand'])
print(data_care['Model'])

data_care["Brand"].value_counts().sort_values(ascending=False)
print(data_care[data_care["Brand"]=='Hyundai'].T)

plt.figure(figsize=(6, 6))
data_care["Brand"].value_counts().plot(kind="bar", title='brand available in the dataset')
plt.show()
plt.figure(figsize=(6, 6))
data_care["MileageKMPL"].value_counts().plot(kind="pie", autopct="%.2f", title="Vehicle Fuel Economy (%)")

# Display the plot
plt.show()
import plotly.express as px
filter_brand = data_care.groupby(["Brand", "Model"])["Model"].count()
filter_brand = filter_brand.reset_index(name="counts").sort_values(by="counts", ascending=False)
fig = px.sunburst(data_frame=filter_brand[:30], path=["Brand", "Model"], values="counts", height=700, width=700,title="Top 30 Vehicle Brands and Models")
fig.show()

print(data_care.T)
cor = data_care.iloc[:, [2,3,8,10,11,14,16]].corr()

plt.figure(figsize=(8,5))
sns.heatmap(cor, annot=True, linewidths=0.4, linecolor="darkgreen",annot_kws={'size': 11, 'rotation': 45}, fmt='.3f', cmap="Greens")
plt.show() 


import matplotlib.pyplot as plt
from scipy import stats
data_care['Price'] = data_care["Price"].fillna(mode(data_care["Price"]))

x = data_care['Power_CC']
y = data_care['Price']
slope, intercept, r, p, std_err = stats.linregress(x, y)

def myfunc(x):
 return slope * x + intercept

mymodel = list(map(myfunc, x))

plt.scatter(x, y)
plt.plot(x,mymodel)
plt.xlabel("Power")
plt.ylabel ("Price")
plt.show()
t=max(data_care['Price'])
print(data_care[data_care['Price']==t].T)
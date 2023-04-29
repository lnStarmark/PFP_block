# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 00:34:11 2020

https://pandas.pydata.org/docs/getting_started/index.html

@author: ln.starmark@gmail.com
"""
#--- Изучаем pandas
#%matplotlib inline

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk 
from tkinter import ttk

plt.style.use('ggplot')                     # Красивые графики
plt.rcParams['figure.figsize'] = (15, 5)    # Размер картинок

'''
#--- variant 1
#--- Задаем вектор из 9 чисел
arr = np.arange(0,9)
print(arr, end='\n\n')

#--- переводим его в матрицу 3х3
arr = arr.reshape(3,3)
print(arr, end='\n\n')
'''

#--- variant 2
"""
arr = np.array([
    [1,2,3],
    [4,5,6],
    [7,8,9]
    ])
"""
'''
#--- печатаем матрицу с названиями строк и столбцов
df = pd.DataFrame(arr,['A','B','C'], ['X','Y','Z'])
print(df, end='\n\n')

#--- можно вывести столбец A и др.
print(df['X'], end='\n\n')
print(df['Y'], end='\n\n')
print(df['Z'], end='\n\n')

#--- можно вывести столбцы X,Z
print(df[['X','Z']], end='\n\n')

#--- вывести строку A (как вектор)
print(df.loc['A'], end='\n\n')

#--- вывести строки A,B
print(df.loc[['A','B']], end='\n\n')

#--- суммировать 2 столбца и создать новый столбец и вывести матрицу
df['sum_X_Y'] = df['X'] + df['Y']
print(df, end='\n\n')

#--- Еще способ создать dataframe
d = {'clmn_1': [4,3,2,1,0], 'clmn_2': ['x', 'z', 'y', 'x', 'z'], 'clmn_3': [2,3,4,1,0]}
df = pd.DataFrame(d)
print(df, end='\n\n')
#--- еще
data = [['tom', 10], ['nick', 15], ['juli', 14]]
df = pd.DataFrame(data, columns = ['Name', 'Age'])
print(df, end='\n\n')

df = pd.DataFrame(data, ['A','B','C'], columns = ['Name', 'Age'])
print(df, end='\n\n')

df = pd.DataFrame(data, ['A','B','C'], ['Name', 'Age'])
print(df, end='\n\n')

df = pd.DataFrame(data, index=['A','B','C'])
print(df, end='\n\n')

df = pd.DataFrame(data, index=['iA','iB','iC'], columns = ['cName', 'cAge'])
print(df, end='\n\n')

data = {'Name':['Tom', 'Jack', 'nick', 'juli'], 'marks':[99, 98, 95, 90]}
df = pd.DataFrame(data, index =['rank1', 'rank2', 'rank3', 'rank4'])
print(df, end='\n\n')

data = [{'a': 1, 'b': 2, 'c':3}, {'a':10, 'b': 20}]
df = pd.DataFrame(data)
print(df, end='\n\n')

#--- зачитать файл zoo.csv
df = pd.read_csv('nzoo.csv', delimiter=',')
print(df, end='\n\n')

#----------------------------------------------------------------------------

fixed_df = pd.read_csv('bikes.csv', 
                       sep=';', encoding='latin1',
                       parse_dates=['Date'], dayfirst=True,
                       index_col='Date')
#--- вывести таблицу
print(fixed_df,end='\n\n')

#--- взять из нее 7 строк в др таблицу и распечатать 2 столбца
df_el = fixed_df[:7]
print(df_el[['Ber1','Parc']],end='\n\n')

#--- тоже самое другим методом 
df_el = fixed_df[['Parc','Cath']][:37]
print(df_el,end='\n\n')

#--- график
#df_el['Parc'].plot()
fixed_df['Ber1'].plot()
fixed_df.plot(figsize=(15, 10))

asc = np.array(['a','b','c','d','e','f','g','h','i']).reshape(3,3)
print(asc)
Z = np.arange(9).reshape(3,3)
print(Z)
Y = np.array([el*el for el in np.arange(9)]).reshape(3,3)
print(Y*Z)

Z = np.ones((10,10))
Z[1:-1,1:-1] = 0
print(Z)

Z = np.zeros((8,8), dtype=int)
Z[1::2,::2] = 1
Z[::2,1::2] = 1
print(Z)

print(np.unravel_index(100, (6,7,8)))

Z = np.random.randint(0,10,50)
print(np.bincount(Z).argmax())

Z = np.arange(9).reshape(3,3)
print(Z)
Y = np.arange(9).reshape(3,3)
print(Y)
print(Z@Y)

dates = pd.date_range("20130101", periods=6)
print(dates)
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
print(df)
'''

def get_rgb(rgb):
    return "#%02x%02x%02x" % rgb 

def lb(mast,name,R,G,B):
    l = ttk.Label(master=mast,text=name,width=25) 
    l.config(background=get_rgb((R, G, B))) 
    l.pack(fill=tk.BOTH)
 
root = tk.Tk()
root.geometry("1300x970") 

excel_data_df = pd.read_excel('./colors.xlsx', sheet_name='Лист1')
dct = excel_data_df.to_dict('list')
N = dct['Name']
R = dct['Red']
G = dct['Green']
B = dct['Blue']
ln = len(R)

frm1 = ttk.Frame(root,borderwidth=3, relief=tk.SOLID, padding=[0, 0])
frm1.pack(side=tk.LEFT, expand=False, fill=tk.Y,  anchor="nw")
    
frm2 = ttk.Frame(root,borderwidth=3, relief=tk.SOLID, padding=[0, 0])
frm2.pack(side=tk.LEFT, expand=False, fill=tk.Y,  anchor="nw")
    
frm3 = ttk.Frame(root,borderwidth=3, relief=tk.SOLID, padding=[0, 0])
frm3.pack(side=tk.LEFT, expand=False, fill=tk.Y,  anchor="nw")
    
frm4 = ttk.Frame(root,borderwidth=3, relief=tk.SOLID, padding=[0, 0])
frm4.pack(side=tk.LEFT, expand=False, fill=tk.Y,  anchor="nw")
 
frm5 = ttk.Frame(root,borderwidth=3, relief=tk.SOLID, padding=[0, 0])
frm5.pack(side=tk.LEFT, expand=False, fill=tk.Y,  anchor="nw")
    
frm6 = ttk.Frame(root,borderwidth=3, relief=tk.SOLID, padding=[0, 0])
frm6.pack(side=tk.LEFT, expand=False, fill=tk.Y,  anchor="nw")

frm7 = ttk.Frame(root,borderwidth=3, relief=tk.SOLID, padding=[0, 0])
frm7.pack(side=tk.LEFT, expand=False, fill=tk.Y,  anchor="nw")
    
frm8 = ttk.Frame(root,borderwidth=3, relief=tk.SOLID, padding=[0, 0])
frm8.pack(side=tk.LEFT, expand=False, fill=tk.Y,  anchor="nw")

lab = []
for i in range(50):
    print( f'{N[i]} {R[i]} {G[i]} {B[i]}' )
    label = lb(frm1, N[i], R[i], G[i], B[i])
    lab.append(label)

lab2 = []    
for i in range(50,100):
    print( f'{N[i]} {R[i]} {G[i]} {B[i]}' )
    label2 = lb(frm2, N[i], R[i], G[i], B[i])
    lab2.append(label2)

lab3 = []
for i in range(100,150):
    print( f'{N[i]} {R[i]} {G[i]} {B[i]}' )
    label3 = lb(frm3, N[i], R[i], G[i], B[i])
    lab3.append(label3)

lab4 = []    
for i in range(150,200):
    print( f'{N[i]} {R[i]} {G[i]} {B[i]}' )
    label4 = lb(frm4, N[i], R[i], G[i], B[i])
    lab4.append(label4)  

lab5 = []
for i in range(200,250):
    print( f'{N[i]} {R[i]} {G[i]} {B[i]}' )
    label5 = lb(frm5, N[i], R[i], G[i], B[i])
    lab5.append(label5)

lab6 = []    
for i in range(250,300):
    print( f'{N[i]} {R[i]} {G[i]} {B[i]}' )
    label6 = lb(frm6, N[i], R[i], G[i], B[i])
    lab6.append(label6)      

lab7 = []
for i in range(300,350):
    print( f'{N[i]} {R[i]} {G[i]} {B[i]}' )
    label7 = lb(frm7, N[i], R[i], G[i], B[i])
    lab7.append(label7)

lab8 = []    
for i in range(350,400):
    print( f'{N[i]} {R[i]} {G[i]} {B[i]}' )
    label8 = lb(frm8, N[i], R[i], G[i], B[i])
    lab8.append(label8) 
    
root.mainloop()    


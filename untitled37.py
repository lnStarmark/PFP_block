# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 00:41:00 2023

@author: admin
"""


import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
 
plt.style.use('dark_background')
 
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
 

def create_file():
    with open('stock.txt', 'w' ) as f:
        for i in range(200):
            s1 = str(i)
            s2 = str(math.sin((i*i/7-12*i)*3.14/180))
            f.write(s1+':'+s2+'\n')
            
    

def animate(i):
    with open('stock.txt', 'r' ) as data:
        data = open('stock.txt', 'r').read()
        lines = data.split('\n')
        lines = lines[:-1]
    #print(lines)
    
 
    xs=[]
    ys=[]
    for line in lines:
       x, y = line.split(':')  # Отделяем дату от цены   
       xs.append(x)
       ys.append(float(y))  
    
       
    
    #print(xs)
    #print(ys)
    
    ax1.clear()
    ax1.plot(xs, ys)
 
    plt.xlabel('Дата')
    plt.ylabel('Цена')
    plt.title('Обновляемые графики в matplotlib')
 
 
create_file()
 
#animate(0) 
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

###
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()

x = np.arange(0, 2*np.pi, 0.01)
line, = ax.plot(x, np.sin(x))


def animate(i):
    line.set_ydata(np.sin(x + i/10.0))  # update the data
    return line,


# Init only required for blitting to give a clean slate.
def init():
    line.set_ydata(np.ma.array(x, mask=True))
    return line,

ani = animation.FuncAnimation(fig, animate, np.arange(1, 2000), init_func=init,
                              interval=25, blit=True)
plt.show()
'''
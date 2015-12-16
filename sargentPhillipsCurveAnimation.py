
# coding: utf-8

# In[1]:

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
import numpy as np
from fredpy import series,window_equalize
import subprocess


# In[2]:

# Dowload data from FRED
u = series('LNS14000028')
p = series('CPIAUCSL')

# Construct the inflation series
p.pc(annualized=True)
p.ma2side(length=6)
p.data = p.ma2data
p.datenumbers = p.ma2datenumbers
p.dates = p.ma2dates

window_equalize([p,u])
p.bpfilter(low=24,high=84,K=84)
u.bpfilter(low=24,high=84,K=84)

# Set data for animation
x = u.bpcycle
y = p.bpcycle
d=u.bpdates
n=len(x)


# In[3]:

# Plot setup
font = {'weight' : 'bold',
        'size'   : 15}
plt.rc('font', **font)
plt.rcParams['xtick.major.pad']='8'
plt.rcParams['ytick.major.pad']='8'

# colormap
color=cm.rainbow(np.linspace(0,1,n))

# Initialize figure
fig = plt.figure(figsize=(16,9))
ax = fig.add_subplot(1,1,1)
ax.grid()
xdata, ydata = [], []
ax.set_ylim(-4, 5)
ax.set_xlim(-2, 2)
ax.set_xlabel('Unemployment rate (%)',fontsize=20)
ax.set_ylabel('Inflation rate (%)',fontsize=20)
ax.set_title('US inflation and unemployment: BP-filtered data',fontsize=25)

scatter = ax.scatter([], [])
text = ax.text(1.95, 4.35, '',fontsize=18,horizontalalignment='right')
ax.text(1.125,-3.75, 'Created by Brian C Jenkins',fontsize=11, color='black',alpha=0.5)


# In[4]:

def update_plot(i):

    scatter = ax.plot(x[i],y[i],'o',fillstyle='none',alpha=0.9,markeredgecolor=color[i], markeredgewidth=2,markersize=13)
    text.set_text(d[i][0:4])

    return scatter, text


# In[5]:

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=10, metadata=dict(artist='Brian C Jenkins'), bitrate=5000)

# Make the animation
ani = animation.FuncAnimation(fig, update_plot, frames = n,fargs = (), blit=False,repeat=False,interval=20)

# Save the animation as .mp4
ani.save('US_Inflation_Unemployment_Monthly_BP_Filtered.mp4',writer=writer)

# Save the final image of the animation to use as the still image placeholder
plt.savefig('US_Inflation_Unemployment_Monthly_BP_Filtered.png',bbox_inches='tight',dpi=120)
# plt.show()


# In[6]:

# Convert the mp4 video to ogg format
makeOgg = 'ffmpeg -i US_Inflation_Unemployment_Monthly_BP_Filtered.mp4 -acodec libvorbis -ac 2 -ab 128k -ar 44100 -b:v 1800k  US_Inflation_Unemployment_Monthly_BP_Filtered.ogv'
subprocess.call(makeOgg,shell=True)


import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
from fredpy import series,window_equalize
import subprocess


# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=10, metadata=dict(artist='Brian C Jenkins'), bitrate=100000)


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


# Animation of the BP-filtered data
x = u.bpcycle
y = p.bpcycle
d=u.bpdates

font = {'weight' : 'bold',
        'size'   : 15}
plt.rc('font', **font)
plt.rcParams['xtick.major.pad']='8'
plt.rcParams['ytick.major.pad']='8'

def _update_plot(i, fig, scatter,text):

    scatter = ax.plot(x[i],y[i],'o',fillstyle='none',alpha=0.9,markeredgecolor=color[i], markeredgewidth=2,markersize=13)
    text.set_text(d[i][0:4])

    return scatter, text


n=len(x)
color=cm.rainbow(np.linspace(0,1,n))

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

ani = animation.FuncAnimation(fig, _update_plot, frames = n,fargs = (fig, scatter,text), blit=False,repeat=False,interval=75)
ani.save('US_Inflation_Unemployment_Monthly_BP_Filtered.mp4',writer=writer)
plt.savefig('US_Inflation_Unemployment_Monthly_BP_Filtered.png',bbox_inches='tight',dpi=120)
# plt.show()


# Convert the mp4 video to ogg format
makeOgg = 'ffmpeg -i US_Inflation_Unemployment_Monthly_BP_Filtered.mp4 -c:v libtheora -c:a libvorbis -q:v 6 -q:a 5 US_Inflation_Unemployment_Monthly_BP_Filtered.ogv'
subprocess.call(makeOgg,shell=True)
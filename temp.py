import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
import numpy as np
from fredpy import series,window_equalize
import subprocess


# Convert the mp4 video to ogg format
# makeOgg = 'ffmpeg -i US_Inflation_Unemployment_Monthly_BP_Filtered.mp4 -acodec libvorbis -ac 2 -ab 128k -ar 44100 -b:v 1800k  US_Inflation_Unemployment_Monthly_BP_Filtered.ogv'
makeOgg = 'ffmpeg -i US_Inflation_Unemployment_Monthly_BP_Filtered.mp4 -acodec libtheora -ac 2 -ab 128k -ar 44100 -b:v 1800k  US_Inflation_Unemployment_Monthly_BP_Filtered.ogv'
subprocess.call(makeOgg,shell=True)


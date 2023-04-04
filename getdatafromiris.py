# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 16:23:44 2020

@author: think
"""
import glob
import matplotlib.pyplot as plt
import numpy as np
import obspy.clients.iris
from obspy import Catalog, UTCDateTime, read
from obspy.clients.fdsn import Client
from obspy.core.event import read_events
from obspy import read_inventory

# Create a client instance connected to IRIS.
client = Client("IRIS")

# get events list
starttime = UTCDateTime("2020-12-01")
endtime = UTCDateTime("2020-12-30")
event_cat = client.get_events(starttime=starttime, endtime=endtime,
                              minlatitude=(20),maxlatitude=(45),
                              minlongitude=(122),maxlongitude=(153),
                              minmagnitude=4.9,maxmagnitude=(5.0))
#save catalog
event_cat.write('E:\obspy_examples\events.xml', format='QUAKEML') 
print(event_cat.__str__(print_all=True))
#%%
stainfo = client.get_stations(network="IC", station="*")
#print(stainfo)
nsta = len(stainfo[0].stations)
for ista in range(1,nsta):
    sta_name = stainfo[0].stations[ista].code
    if (sta_name == 'BJT'):
        sta_lat = stainfo[0].stations[ista].latitude
        sta_lon = stainfo[0].stations[ista].longitude
        print(sta_name,sta_lat,sta_lon)
        break   
#%%
#read catlog
evcat = read_events('E:\obspy_examples\events.xml', format='QUAKEML') 
for event in evcat[0:7]:
    #evlat = event.Event
    #print(event.origins[0].resource_id)
    #print(event.origins[0].time)
    ev_lat = event.origins[0].latitude
    ev_lon = event.origins[0].longitude
    evdep = event.origins[0].depth
    evtime = event.origins[0].time
    evmag = event.magnitudes[0].mag
    evmag_type = event.magnitudes[0].magnitude_type
    #print(evlat,evlon,evdep,evtime,evmag,evmag_type)
    client1 = obspy.clients.iris.Client()
    result = client1.distaz(stalat=sta_lat, stalon=sta_lon, evtlat=ev_lat, evtlon=ev_lon)
    # obtain epicenral distance between epicenter and Beijing station
    epicentral_dist = result['distance']
    st = client.get_waveforms('IC', 'BJT', '00', 'BHZ', evtime, evtime + 60 * 60, 
                          attach_response=True)
    ntr = len(st)
    for itr in range(ntr):
        tr = st[itr]
        tr_vel = tr.copy()
        tr_disp = tr.copy()
        # remove instrumental response
        fig = plt.figure(figsize=(12,12))   
        pre_filt = [0.001, 0.005, 8, 10]
        # remove instrument response to velocity
        #tr_vel.remove_response(output='VEL', zero_mean=True, pre_filt=pre_filt,
        #                     plot=False)         
        # save velocity waveform
        
        #sacname = 'G:\obspy_examples\sacdata1' + '\\' + figname1 + '.vel.SAC'
        #tr_vel.plot()
        #tr_vel.write(sacname, format='SAC') 
        # remove instrument response to displacement
        tr_disp.remove_response(output='DISP', zero_mean=True, pre_filt=pre_filt,
                                plot=True, fig=fig) 
        figname = tr.stats.network + '.' + tr.stats.station + '.' \
                          + tr.stats.channel + '.' + str(evtime.year) \
                          + '.' + str(evtime.month) + '.' + str(evtime.day)
        fig.savefig('E:\obspy_examples\sacdata1' + '\\' + figname + '.disp.pdf')
        # save displacement waveform
        sacname = 'E:\obspy_examples\sacdata1' + '\\' + figname + '.disp.SAC'
        tr_disp.plot()
        tr_disp.write(sacname, format='SAC') 
        #
        Fs = tr_disp.stats.sampling_rate
        dt = 1.0 / Fs
        npts = len(tr_disp.data)
        tt = np.arange(npts) * dt
        # applying bandpass filter
        tr_filt = tr_disp.copy()
        tr_filt.filter('bandpass', freqmin=0.04, freqmax=0.06, corners=2, zerophase=True)
        maxamp = max(tr_filt.data)
        # plot raw data，filtered data
        fig1,ax = plt.subplots(figsize=(10,5),nrows=3, ncols=1)
        Fs = tr.stats.sampling_rate
        npts = len(tr.data)
        tt = np.arange(npts) / Fs
        ax[0].plot(tt,tr.data,'r');
        ax[0].set_title(tr.stats.channel)
        ax[0].annotate(sacname + '_Raw Data', xy=(npts * 0.3 / Fs, 0.8*max(tr.data)))
        #
        ax[1].plot(tt,tr_disp.data,'b')
        ax[1].annotate(sacname + '_Displacement', xy=(npts * 0.3 / Fs, 0.8*max(tr_disp.data)))
        #
        ax[2].plot(tt,tr_filt.data,'g')
        ax[2].annotate(sacname + '_Filtered Disp', xy=(npts * 0.3 / Fs, 0.8*max(tr_filt.data)))
    
        fig1.savefig('E:\obspy_examples\sacdata1' + '\\' + figname + 'disp.filter.pdf')
        plt.close()

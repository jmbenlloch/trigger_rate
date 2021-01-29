import streamlit as st
import numpy as np
import matplotlib.pylab as plt


rate      = st.sidebar.slider('Trigger rate (Hz)' , min_value=  1, max_value= 150, value=  80)
window    = st.sidebar.slider('Buffer size (us)'  , min_value= 50, max_value=3500, value=3200, step=50)
max_time  = st.sidebar.slider('Maximum time (ms)' , min_value=  0, max_value= 500, value= 500)
max_drift = st.sidebar.slider('Maximum drift (us)', min_value=100, max_value=2000, value=1600, step=100)
st.sidebar.write('Trigger rate is', rate, " Hz")
st.sidebar.write('Buffer size is', window, " us")
st.sidebar.write('Max time difference is', max_time, " ms")
st.sidebar.write('Max drift time is', max_drift, " ms")

nevts = rate * 86400

evts_per_second = np.random.poisson(lam=rate     , size=nevts)
evt_times_ms    = np.random.exponential(1000/rate, size=nevts)
drifts          = np.random.uniform(max_drift, size=nevts)

waveform_s1 = evt_times_ms.cumsum()
waveform_s2 = waveform_s1 + drifts/1000.
pile_up     = ((waveform_s1[1:] - waveform_s2[:-1]) < 0)

pile_up_diff = np.diff(pile_up.astype(np.int))
pileup_mixed = (pile_up_diff > 0).sum() + pile_up.sum()
pileup_rate  = pileup_mixed / nevts * 100

total_pileup = evt_times_ms[evt_times_ms < (window/1000.)].shape[0] / nevts * 100

st.write(f"At a Kr rate of {rate} Hz the proportion of triggers with pile up in a pattern [s1, s1, s2, s2] is {pileup_rate:2.2f}%.")
st.write(f"The total number of events with pile up using a buffer of {window}us (some of them usable, like a [s1, s2, s1, s2] pattern) is {total_pileup:2.2f}%.")
st.write("Use the menu on the left to modify the parameters")

st.subheader('Events per second distribution')
upper_limit = int(rate * 1.7) + 1
fig, ax = plt.subplots()
ax.hist(evts_per_second    , bins=upper_limit, range=[0, upper_limit])
ax.set_xlabel("Evts/second [Hz]")
ax.set_ylabel("Counts")
st.pyplot(fig)

st.subheader('Time difference between consecutive events')
st.write('Maximum time to show: ', max_time, ' ms')
fig, ax = plt.subplots()
ax.hist(evt_times_ms    , bins=100, range=[0, max_time])
ax.set_xlabel("Time difference between events [ms]")
ax.set_ylabel("Counts")
st.pyplot(fig)

st.subheader('Z distribution (drift time)')
st.write('Maximum time to show: ', max_drift, ' ms')
fig, ax = plt.subplots()
ax.hist(drifts, bins=100, range=[0, max_time])
ax.set_xlabel("Drift time in [ms]")
ax.set_ylabel("Counts")
st.pyplot(fig)

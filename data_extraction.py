import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis
import os

directory_path=os.path.join('XLSX','240420_meditation data')
print('hello')

file_paths=[os.path.join(directory_path,f) for f in os.listdir(directory_path) if f.endswith('.xlsx')]
items=len(file_paths)
print('hello')

kk1=1
kk2=1

LH_all_pre=[]
RH_all_pre=[]
LL_all_pre=[]
RL_all_pre=[]
LH_all_post=[]
RH_all_post=[]
LL_all_post=[]
RL_all_post=[]

for i in range(items):
    filename=file_paths[i]
    name=os.path.basename(filename)
    if name[9]=='A':
        dataall=pd.read_excel(filename, header=None).values

        min_rows=min(dataall.shape[0],2403)
        dataall=dataall[:min_rows,:]
        LH=dataall[:, 1::5]
        RH=dataall[:, 2::5]
        LL=dataall[:, 3::5]
        RL=dataall[:, 4::5]

        if kk1==1:
            LH_all_pre=LH
            RH_all_pre=RH
            LL_all_pre=LL
            RL_all_pre=RL
        else:
            LH_all_pre=np.hstack((LH_all_pre[:min_rows,:], LH[:min_rows,:]))
            RH_all_pre=np.hstack((RH_all_pre[:min_rows,:], RH[:min_rows,:]))
            LL_all_pre=np.hstack((LL_all_pre[:min_rows,:], LL[:min_rows,:]))
            RL_all_pre=np.hstack((RH_all_pre[:min_rows,:], RL[:min_rows,:]))

        kk1+=1
print('hello')
for i in range(items):
    filename=file_paths[i]
    name=os.path.basename(filename)

    if name[9]=='2':
        dataall = pd.read_excel(filename, header=None).values
        LH = dataall[:, 1::5]
        RH = dataall[:, 2::5]
        LL = dataall[:, 3::5]
        RL = dataall[:, 4::5]

        if kk1 == 1:
            LH_all_post = LH
            RH_all_post = RH
            LL_all_post = LL
            RL_all_post = RL
        else:
            LH_all_post = np.hstack((LH_all_pre[:min_rows,:], LH[:min_rows,:]))
            RH_all_post = np.hstack((RH_all_pre[:min_rows,:], RH[:min_rows,:]))
            LL_all_post = np.hstack((LL_all_pre[:min_rows,:], LL[:min_rows,:]))
            RL_all_post = np.hstack((RH_all_pre[:min_rows,:], RL[:min_rows,:]))

        kk2 += 1
print('hello')
fs=20
number1=LL_all_pre.shape[1]

def ensure_2d(array):
    data=np.array(array)
    if data.ndim==1:
        return  data.reshape(-1,1)
    return data

total_signal =np.hstack((
    ensure_2d(LH_all_pre),
    ensure_2d(RH_all_pre),
    ensure_2d(LL_all_pre),
    ensure_2d(RL_all_pre),
    ensure_2d(LH_all_post),
    ensure_2d(RH_all_post),
    ensure_2d(LH_all_post),
    ensure_2d(RL_all_post)
))

print(total_signal)
statistics={
    "min": np.min(total_signal),
    'max': np.max(total_signal),
    'mean': np.mean(total_signal),
    'std_dev': np.std(total_signal),
    'skewness': skew(total_signal),
    'kurtosis': kurtosis(total_signal)

}

stats_df=pd.DataFrame(statistics)
print(stats_df)






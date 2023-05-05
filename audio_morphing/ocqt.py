from helper import remove_symmetry
from nmf_morph import NMFMorph
from numpy.linalg import norm
from untwist.untwist.data import Wave, Spectrogram
from untwist.untwist.hpss import MedianFilterHPSS
from rtpghi import pghi
import matlab.engine
import matplotlib.pyplot as plt
import numpy as np
import time

start = time.time()

######## Define source and target signals ########
# src = "../audio/samples/Tremblay-CF-ChurchBells_mono.wav"
tgt = "../audio_files/source_dist.wav"
src = "../audio_files/target_bass.wav"

######## Initialize Matlab Engine ########
eng = matlab.engine.start_matlab()
gen = eng.genpath('D:\Program Files\Matlab\ltfat-2.4.0-bin-win64-R2018a\ltfat')
gen2 = eng.genpath('../helpers')
eng.addpath(gen, nargout=0)
eng.addpath(gen2, nargout=0)
print(f"{'='*50}\nMATLAB Engine initialized.\n{'='*50}")

######## Initialize ltfat toolbox ########
eng.ltfatstart(nargout=0)

######## Load source and target signals ########
src_data, src_rate = eng.audioread(src, nargout=2)
src_Ls = eng.length(src_data,nargout=1)
tgt_data, tgt_rate = eng.audioread(tgt, nargout=2)
tgt_Ls = eng.length(tgt_data,nargout=1)

# Define constants
p = 0.8
fft_size = 2048
hop_size = 512
hLength = 17
pLength = 31
fmin = 200
bins = 48
fmax = 22050

# Compute source cqt
src_g,src_a,src_fc,src_L,src_info = eng.cqtfilters(src_rate,
                                                    matlab.double([fmin]),
                                                    matlab.double([fmax]),
                                                    matlab.double([bins]),
                                                    src_Ls,
                                                    "uniform",
                                                    nargout=5
                                                )
src_c0=eng.filterbank(src_data,src_g,src_a,nargout=1)
src_c2,src_row,src_col = eng.to_mat(src_c0,nargout=3)
src_c3 = np.array(src_c2)
src_c4 = src_c3.reshape((int(src_row),int(src_col)))

S = Spectrogram(src_c4, src_rate, hop_size)

# Compute target cqt
tgt_g,tgt_a,tgt_fc,tgt_L,tgt_info = eng.cqtfilters(tgt_rate,
                                                    matlab.double([fmin]),
                                                    matlab.double([fmax]),
                                                    matlab.double([bins]),
                                                    tgt_Ls,
                                                    "uniform",
                                                    nargout=5
                                                )
tgt_c0=eng.filterbank(tgt_data,tgt_g,tgt_a,nargout=1)
tgt_c2,tgt_row,tgt_col = eng.to_mat(tgt_c0,nargout=3)
tgt_c3 = np.array(tgt_c2)
tgt_c4 = tgt_c3.reshape((int(tgt_row),int(tgt_col)))

T = Spectrogram(tgt_c4, tgt_rate, hop_size)

######## Decompose source and target signals via HPSS ########
print(f"Applying HPSS...\n{'='*50}")
hpss = MedianFilterHPSS(hLength, pLength)
Hs, Ps = hpss.process(S)
Ht, Pt = hpss.process(T)
print(f"HPSS process applied.\n{'='*50}")

print(f"Morphing source and target...")
m_h = NMFMorph()
m_p = NMFMorph()
m_h.analyze(Hs.magnitude(), Ht.magnitude(), p)
m_p.analyze(Ps.magnitude(), Pt.magnitude(), p)

# for f in [0,0.5,1]:
# fig, axs = plt.subplots(1,3)
# for f in [0,0.5,0.75,1]:
for f in [1]:
    print(f"Interpolating with factor {f}...")
    Yh = m_h.interpolate(f)
    Yp = m_p.interpolate(f)
    print(f"Applying PGHI...")
    Yh2 = pghi(Yh, fft_size, hop_size)
    Yp2 = pghi(Yp, fft_size, hop_size)
    Y0 = np.array(Yh2 + Yp2)
    Y = Spectrogram(Y0, src_rate, hop_size)
    # S.plot(axes=axs[0])
    # T.plot(axes=axs[1])
    # Y.plot(axes=axs[2])
    y = matlab.double(Y0.tolist(), is_complex=True)
    y = eng.to_cell(y)
    r1 = eng.filterbankconstphase(y,
                            src_a,
                            src_info['fc'],
                            src_info['tfr'],
                            'wavelet',
                            nargout=1,
                            )
    gd = eng.filterbankrealdual(src_g,src_a,src_L,nargout=1)
    r2 = eng.ifilterbank(r1,gd,src_a,nargout=1)
    r3 = eng.real(r2[0:int(src_Ls)],nargout=1)
    r4 = 2*np.array(r3)
    r5 = r4.reshape(int(src_Ls),)
    x = range(1,r5.shape[0] + 1)
    r6 = matlab.double(r5.tolist())
    s = str(f).replace('.','')
    filename = f'../audio/slide2bass_{s}.wav'
    eng.audiowrite(filename,r6,src_rate,nargout=0)

eng.exit

end = time.time()
duration = end-start

print(f"Script run successful. Duration: {round(duration)} seconds.\n{'='*50}")

######## Checkpoint: Morphed Spectrogram ########

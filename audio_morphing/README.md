# Octave-wise Constant Q Transform (OCQT)

---

This application is a revised approach of a previous study on audio morphing. For more details on the previous study, visit [Flucoma](https://www.flucoma.org/DAFX-2020/). 
## Dependencies
- Python 3.8 (numpy, matlab)
- Matlab
- Untwist
- [LTFAT](https://ltfat.org/)

## Implementation
OCQT is run using the `filterbank` function from LTFAT.
```
% [S, Ss] = signal, sample rate
fs = Ss/2;
fmin = 100;
bins = 24;
fmax = Ss/2;
t = [100 400 1600 6400 20000];
dyn = 60;

% Source Spectrogram
figure(1)
Sl = length(S);
[Sg,Sa,Sfc] = cqtfilters(Ss, fmin, fmax, bins, Sl, 'fractional');
Sc=filterbank(S,{'realdual',Sg},Sa);
plotfilterbank(Sc,Sa,Sfc,Ss,dyn,'tick', t);
```
A helper function `try_cqtfilters` is provided in the helpers folder. This substitutes to the `cqtfilters` function from LTFAT.
User must work on Python 3.8 and install the Matlab engine to access LTFAT functions in Python.
The morphing script is run using the command
`py -3.8 ocqt.py`

## Results
User may refer to the `ocqt_morph.m` and `stft_morph.m` files to access and view the morphing spectrograms. Corresponding audio results are found in the `audio_files` folder.

---
This repository is a complementary work for a graduate thesis in Applied Mathematics - University of the Philippines, Diliman entitled *An Octave-wise Constant Q Transform via Nonstationary Gabor Frames and Some Applications*.

**Authors**: AJ Panganiban (arvinjaypanganiban24@gmail.com)

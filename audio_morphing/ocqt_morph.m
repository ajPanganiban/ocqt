% Parameters
[S, Ss] = audioread('../audio_files/source_dist.wav');
[T, Ts] = audioread('../audio_files/target_bass.wav');
[R, Rs] = audioread('../audio_files/morphed_dist_bass.wav');

% [S, Ss] = audioread('../audio_files/source_bell.wav');
% [T, Ts] = audioread('../audio_files/target_box.wav');
% [R, Rs] = audioread('../audio_files/morphed_bell_box.wav');

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
axis square;
colormap(jet);
colorbar off;

% Target Spectrogram
figure(2)
Tl = length(T);
[Tg,Ta,Tfc] = cqtfilters(Ts, fmin, fmax, bins, Tl, 'fractional');
Tc=filterbank(T,{'realdual',Tg},Ta);
plotfilterbank(Tc,Ta,Tfc,Ts,dyn,'tick', t);
axis square;
colormap(jet);
colorbar off;

% Morphed Spectrogram
figure(3)
Rl = length(R);
[Rg,Ra,Rfc] = cqtfilters(Rs, fmin, fmax, bins, Rl, 'fractional');
Rc=filterbank(R,{'realdual',Rg},Ra);
plotfilterbank(Rc,Ra,Rfc,Rs,dyn,'tick', t);
colormap(jet);
colorbar off;
axis square;


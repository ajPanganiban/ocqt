% Parameters
[S, Ss] = audioread('../audio_files/source_dist.wav');
[T, Ts] = audioread('../audio_files/target_bass.wav');
[R, Rs] = audioread('../audio_files/stft_morph.wav');

fs = Ss/2;
fmin = 100;
bins = 24;
fmax = Ss/2;
t = [100 400 1600 6400 20000];
dyn = 60;

% Source Spectrogram
figure(1)
Sc = dgtreal(S,'hann',100,1024);
plotdgt(Sc,100,Ss,'dynrange',dyn);
axis square
ylim([0, Ss/2])
yticks([0 Ss/6 Ss/3 Ss/2])
set(gca, 'YTickLabel',get(gca,'YTick'))
colormap(jet)

% Target Spectrogram
figure(2)
Tc = dgtreal(T,'hann',100,1024);
plotdgt(Tc,100,Ts,'dynrange',dyn);
axis square
ylim([0, Ss/2])
yticks([0 Ss/6 Ss/3 Ss/2])
set(gca, 'YTickLabel',get(gca,'YTick'))
colormap(jet)

% Morphed STFT
figure(3)
Rc = dgtreal(R,'hann',100,1024);
plotdgt(Rc,100,Rs,'dynrange',dyn);
axis square
ylim([0, Ss/2])
yticks([0 Ss/6 Ss/3 Ss/2])
set(gca, 'YTickLabel',get(gca,'YTick'))
colormap(jet)

% Morphed Spectrogram
figure(4)
Rl = length(R);
[Rg,Ra,Rfc] = cqtfilters(Rs, fmin, fmax, bins, Rl, 'fractional');
Rc=filterbank(R,{'realdual',Rg},Ra);
plotfilterbank(Rc,Ra,Rfc,Rs,dyn,'tick', t);
colormap(jet);
colorbar off;


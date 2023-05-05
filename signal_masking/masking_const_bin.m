% Givens
[f, fs] = gspi;
fmin = 200;
bins = 48;
fmax = fs/2;
Ls = length(f);

% Compute CQT
[g,a,fc] = cqtfilters(fs, fmin, fmax, bins, Ls, 'uniform');
c0=filterbank(f,{'realdual',g},a);
c1 = cellfun(@transpose,c0,'UniformOutput',false);
c2 = cell2mat(c1);

% Do something to c2
ax(1) = subplot(1,3,1);
t = [200 800 1600 3200 6400 12800 fmax];
t = [200 800 1000 1200 1400 1600 3200 12800 fmax];
plotfilterbank(c0,a,fc,fs,70,'tick', t);
title('Original Spectrogram')

% %%%% mask %%%%
m0 = zeros(size(c2));
m0(110:150,:) = 1;
m0(:,1:620) = 1;
m = to_array(m0);
ax(1) = subplot(1,3,2);
plotfilterbank(m,a,fc,fs,70,'tick', t);
title('Mask')


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

c3 = c2.*m0;
rc = to_array(c3);
ax(3) = subplot(1,3,3);
plotfilterbank(rc,a,fc,fs,70,'tick', t);
title('Masked Spectrogram')

r0 = ifilterbank(rc,g,a);
r = 2*real(r0(1:Ls));
audiowrite('masking_const_bin.wav', r, fs)

colormap(jet);

function c_array = to_array(coef)
    coef1 = num2cell(coef,2);
    coef2 = cellfun(@transpose,coef1,'UniformOutput',false);
    c_array = coef2;
end
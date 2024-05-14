% run this code to find the minimum order of your filter, providing the filter specs

Fs = 44100; % Sampling frequency (Hz)
F_Nyquist = Fs / 2; % Nyquist frequency

% Passband frequencies normalized to Nyquist frequency
Wp = [200 300] / F_Nyquist;

%  stopband frequencies normalized to Nyquist frequency
Ws = [150 350] / F_Nyquist;

Rp =0.5; % passband ripple (dB)
Rs = 40; % stopband ripple (dB)

% Use ellipord to calculate filter order and normalized cutoff frequency
[n, Wn] = ellipord(Wp, Ws, Rp, Rs);

disp(n);

%HIGH PASS FILTER
Fs = 44100; % Sampling frequency (Hz)
F_Nyquist = Fs / 2; % Nyquist frequency

% Passband frequencies normalized to Nyquist frequency
Wp = 6500 / F_Nyquist; % Passband starts from 6500 Hz (high-pass filter)

% Stopband frequencies normalized to Nyquist frequency
Ws = 6000 / F_Nyquist; % Stopband starts from 6000 Hz (below 6500 Hz)

Rp = 0.5; % passband ripple (dB)
Rs = 40; % stopband ripple (dB)

% Use ellipord to calculate filter order and normalized cutoff fre
[n, Wn] = ellipord(Wp, Ws, Rp, Rs);

disp(n);
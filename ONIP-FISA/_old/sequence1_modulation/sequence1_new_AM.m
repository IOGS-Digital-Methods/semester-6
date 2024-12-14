clear all;
close all;

%% Signaux sinus
sine4k = readmatrix('test_oscillo_sin_2k_2Vpp_4k.csv');

temps4k = sine4k(:,2);  % temps
signal4k = sine4k(:,3); % signal

% Affichage partiel
figure(1);
plot(temps4k(1:400), signal4k(1:400));

% FFT
Te4k = temps4k(2)-temps4k(1);
Fe4k = 1/Te4k
N4k = length(signal4k);
TA4k = N4k*Te4k;
pasF = Fe4k/N4k;
freq4k = linspace(-N4k/(2*TA4k),N4k/(2*TA4k)-pasF,N4k);

fft4k = abs(fft(signal4k))/N4k;
figure(2);
plot(freq4k, fftshift(fft4k));

%% Signaux AM
am4k = readmatrix('test_oscillo_AM_2k_400_50p_4k.csv');
temps_am4k = am4k(:,2);  % temps
signal_am4k = am4k(:,3); % signal

% Affichage partiel
figure(3);
plot(temps_am4k(1:400), signal_am4k(1:400));

% FFT
Te4k = temps_am4k(2)-temps_am4k(1);
N4k = length(signal_am4k);
TA4k = N4k*Te4k;
pasF = Fe4k/N4k;
freq4k = linspace(-N4k/(2*TA4k),N4k/(2*TA4k)-pasF,N4k);

fft4k = abs(fft(signal_am4k))/N4k;
figure(4);
plot(freq4k, fftshift(fft4k));


%% Demodulation
% creation signal porteuse
fp = 2000;
wp = 2 * pi * fp;
sine_p = sin(wp*temps_am4k);
demod = sine_p .* signal_am4k;

figure(5);
plot(temps_am4k, demod);

% FFT
fft_demod = abs(fft(demod))/N4k;
figure(6);
plot(freq4k, fftshift(fft_demod));
% "passe-bas"
np = floor(fp/pasF)
fft_demod_pb = fft_demod;
fft_demod_pb(np:N4k-np) = 0;
fft_demod_pb(1) = 0;

figure(7);
plot(freq4k, fftshift(fft_demod_pb));

% signal demodule
demod_signal = N4k*ifft(fft_demod_pb,'symmetric');
figure(8);
plot(temps4k, demod_signal);


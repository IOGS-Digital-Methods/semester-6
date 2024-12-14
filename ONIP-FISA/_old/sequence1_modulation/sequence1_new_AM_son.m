clear all;
close all;

%% Son
Fe = 44100;
signal_mus = audioread('test/musique-libre-de-droits-yuku-naghawo.mp3');
signal_mus = signal_mus(:,1);
% sound(signal_mus, Fe);
N = length(signal_mus);
fft_mus = abs(fft(signal_mus));
pasF = Fe/N;
freq = -Fe/2:pasF:Fe/2-pasF;
figure(1);
plot(freq, fftshift(fft_mus));

%% Modulation
temps = 0:1/Fe:N*1/Fe-1/Fe;
fp = 10000;
% creation signal porteuse
wp = 2 * pi * fp;
sine_p = sin(wp*temps);

signal_mod = sine_p' .* signal_mus;

figure(2);
plot(temps, signal_mod);
fft_mod_mus = abs(fft(signal_mod));
figure(3);
plot(freq, fft_mod_mus);

matrice_mus = [temps' signal_mod];
writematrix(matrice_mus, 'mus_mod.txt');


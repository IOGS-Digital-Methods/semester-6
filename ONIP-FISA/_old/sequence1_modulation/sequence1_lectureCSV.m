%% Traitement du signal / Modulation AM
%   Module : Init Calcul Scientifique / CFA-S6
%--------------------------------------------------------------
%   Autre
%--------------------------------------------------------------
%   Auteur : Julien VILLEMEJANE
%   Date : 22/09/2020
%--------------------------------------------------------------
clear all;
close all;
%% Lecture du fichier CSV / Te = 200 ns
data = csvread('AM_sinus.csv');
Te = 2e-7;
N = length(data);

%% Affichage
TA = N*Te;
t1 = (0 : Te : TA-Te);

figure(1);
subplot(2,1,1);
plot(t1, data);
xlabel('Temps (s)');
ylabel('Signal modulé (V)');
grid on;

%% FFT et affichage
freqa = linspace(-N/(2*TA),N/(2*TA),N);
tfT = fft(data);
tfT_s = fftshift(tfT)/N;

subplot(2,1,2);
plot(freqa,abs(tfT_s));
xlabel('Fréquence (Hz)')
ylabel('TF (V)')
grid on;


%% Rééchantillonnage
Fe_rs = 500000;
data_rs = resample(data, Fe_rs, 1/Te);
N_rs = length(data_rs);
t_rs = (0 : 1/Fe_rs : (N_rs-1)*1/Fe_rs);
figure(2);
subplot(2,1,1);
plot(t_rs, data_rs);
xlabel('Temps (s)');
ylabel('Signal modulé (V)');
grid on;
freq_rs = linspace(-Fe_rs/2,Fe_rs/2-Fe_rs/N_rs,N_rs);

tfT_rs = fft(data_rs);
tfT_s_rs = fftshift(tfT_rs)/N_rs;

subplot(2,1,2);
plot(freq_rs,abs(tfT_s_rs));
xlabel('Fréquence (Hz)')
ylabel('TF (V)')
grid on;

%% Suppression porteuse
[valMax,indMax] = max(tfT_s_rs);

% Suppression d'une partie du spectre (autour de fp)
MM=10;
tfT_s_rs(indMax) = 0;
tfT_s_rs(N_rs - indMax) = 0;
for indice = 1:MM
    tfT_s_rs(indMax-indice) = 0;
    tfT_s_rs(N_rs - indMax - indice) = 0;
    tfT_s_rs(indMax+indice) = 0;
    tfT_s_rs(N_rs - indMax + indice) = 0;
end;

figure(3);
subplot(2,1,1);
plot(freq_rs,abs(tfT_s_rs));
xlabel('Fréquence (Hz)')
ylabel('TF (V)')
grid on;

signal_sortie_rs = ifft(fftshift(tfT_s_rs),'symmetric');
subplot(2,1,2);
plot(t_rs,signal_sortie_rs);
xlabel('Temps (s)');
ylabel('Signal (V)');
grid on;

%% Décalage autour de 0
for indice = 1:N_rs/2
    tfT_s_rs(N_rs - indice) = 0;
end;
for indice = 1:N_rs/2-indMax
    tfT_s_rs(N_rs/2-indice) = tfT_s_rs(indMax-indice);
    tfT_s_rs(N_rs/2+indice) = tfT_s_rs(indMax+indice);
    %tfT_s_rs(N_rs/2 - indice) = ;
end;
for indice = 1:indMax/2
    tfT_s_rs(indMax-indice) = 0;
    tfT_s_rs(N_rs/2+indMax-indice) = 0;
    tfT_s_rs(indMax+indice) = 0;
    tfT_s_rs(N_rs/2+indMax+indice) = 0;
end;

signal_utile_rs = N_rs * ifft(fftshift(tfT_s_rs),'symmetric');
Fu = 1e4;   % frequence du signal modulant théorique
signal_reel_utile = sin(2*pi*t_rs*Fu);


figure(4);
subplot(2,1,1);
plot(freq_rs,abs(tfT_s_rs));
xlabel('Fréquence (Hz)')
ylabel('TF (V)')
legend('signal sans bruit');
grid on;
subplot(2,1,2);
plot(t_rs,signal_utile_rs,t_rs, signal_reel_utile);
xlabel('Temps (s)');
ylabel('Signal (V)');
grid on;

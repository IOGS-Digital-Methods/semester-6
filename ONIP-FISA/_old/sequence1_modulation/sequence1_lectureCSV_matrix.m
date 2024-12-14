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
data = readmatrix('WA000003_mod.CSV');
temps = data(:,4);
Te = data(2,4)-data(1,4);
N = length(data);
signal = data(:,5);

%% Affichage
TA = N*Te;
t1 = (0 : Te : TA-Te);

figure(1);
subplot(2,1,1);
plot(t1, signal);
xlabel('Temps (s)');
ylabel('Signal modulé (V)');
grid on;
%% FFT et affichage
freqa = linspace(-N/(2*TA),N/(2*TA),N);
tfT = fft(signal);
tfT_s = fftshift(tfT)/N;

subplot(2,1,2);
plot(freqa,abs(tfT_s));
xlabel('Fréquence (Hz)')
ylabel('TF (V)')
grid on;


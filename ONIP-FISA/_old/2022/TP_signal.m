%% Traitement du signal / Bases
%   Module : Electronique pour le traitement de l'Information
%--------------------------------------------------------------
%   Autre
%--------------------------------------------------------------
%   Auteur : Julien VILLEMEJANE
%   Date : 16/09/2020
%--------------------------------------------------------------
close all;
clear all;
%% from http://eleceng.dit.ie/dorran/matlab/resources/Matlab%20Signal%20Processing%20Examples.pdf
signal = load('_signaux/ecg.txt');   % file acquired @ 100 Hz
NP = max(size(signal));
TA = NP*0.01-0.01;
t = (0 : 0.01 : NP*0.01-0.01);
figure(1);
plot(t,signal);
xlabel('Temps (s)');
ylabel('Signal');

% FFT
freq = linspace(-NP/(2*TA),NP/(2*TA),NP);
tf1 = fft(signal);
tf1_s = fftshift(tf1)/NP;
figure(2);
plot(freq,abs(tf1_s));
xlabel('Fréquence (Hz)')
ylabel('TF (V)');

%% Filtre continu / from 
% https://fr.mathworks.com/help/control/ug/plotting-system-responses.html
% premier ordre - filtre passe-bas
R = 1e3; C = 1e-7;
w1 = 1/R * 1/C;
num1 = [1]; den1 = [1/w1 1];
sys1 = tf(num1, den1); 
% second ordre - filtre passe-bas
Q = 4; w2 = 1e5; K = 2;
num2 = [K];
den2 = [(1/w2)^2 1/Q*1/w2 1];

sys2 = tf(num2, den2);

figure(3);
subplot(2,1,1);
step(sys1,sys2);     % réponse indicielle
legend('Premier ordre','Deuxième ordre');
grid on;
subplot(2,1,2);
impulse(sys1,sys2);  % réponse impulsionnelle
grid on;

figure(4);
bode(sys1, sys2);
legend('Premier ordre','Deuxième ordre');
grid on;

% Réponse à un signal
t1 = (0 : 0.001 : 1);
f1 = 15;
ve1 = sin(2 * pi * f1 * t1);
figure(4);
lsim(sys1,ve1,t1);

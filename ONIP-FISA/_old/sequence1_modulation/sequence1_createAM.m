clear all;
close all;

%% Matrice
N = 1000;
M=ones(N,N);
x=pi*((1:N)-0.5)/N;
for j=2:N
M(:,j)=cos((j-1)*x); % remplissage de la colonne n°j d'un coup!
end
% Courbe paramétrique
theta = (0 : 0.01 : 2*pi);
x = 2 * cos(theta) + 5*sin(10*theta);
y = 2 * sin(theta) + 5*cos(10*theta);
figure(1);
plot(x,y);
set(gca,'DataAspectRatio',[1,1,1]);
grid on;

%% Temps de calcul
N = 10e6;
v = rand(N,1);
tic;
stf=fft(v);
toc
figure(2);
plot(abs(stf))

%% Signaux
Fe = 1e3;   % echantillonnage
Tt = 5e-1;     % temps d'observation
f1 = 10; f2 = 32; f3 = 22;  % fréquence des signaux utiles
A1 = 5; A2 = 3; A3 = 1;     % amplitude des signaux utiles
fp = 250;   % fréquence de la porteuse
Ap = 1;     % amplitude de la porteuse
% création du signal
Nt = Tt*Fe;
deltaT = 1/Fe;
deltaF = Fe/Nt;
t = (0:deltaT:Tt-deltaT);
modulante = A1*sin(2*pi*f1*t) + A2*sin(2*pi*f2*t) + A3*sin(2*pi*f3*t);
porteuse = Ap*sin(2*pi*fp*t);
ve = (modulante + 1).*porteuse;
% affichage du signal
figure(3);
subplot(3,1,1);
plot(t, modulante);
legend('modulante');
subplot(3,1,2);
plot(t, porteuse);
legend('porteuse');
subplot(3,1,3)
plot(t, ve);
legend('signal modulé');
xlabel('Temps (s)')
% calcul FFT
vetf = fftshift(fft(ve));
f=Fe/Nt*(-Nt/2:Nt/2-1);
f = f';
figure(4);
subplot(2,1,1);
plot(f,abs(vetf));
xlabel('Frequence (Hz)')
ylabel('TF')

% suppression porteuse
vetf_s = vetf;
vetf_s(Nt/2-fp/deltaF+1) = 0;
vetf_s(Nt/2+fp/deltaF+1) = 0;
subplot(2,1,2);
plot(f,abs(vetf_s));
xlabel('Frequence (Hz)')
ylabel('TF')

vetf_s = fftshift(vetf_s);
ve_s = ifft(vetf_s);

figure(5);
plot(t,ve_s);

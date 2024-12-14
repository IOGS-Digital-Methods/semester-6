close all;
clear all;
M=csvread('WA000002.CSV',2,0);
figure(1)
plot(M(:,1),M(:,2:end));                                                   %tracé

N=20480;                                                                   %nbr de points
Fe=250000;                                                                 %fréq d'échantillonage en Hz

Fx=fft(M(:,2));                                                            %transformée de fourier du signal
FX=fftshift(Fx);
Mod=abs(FX)*2;                                                             %module de la TF
Fn=Fe/2;                                                                   %fréd de Nyquist
V=linspace(-Fn,Fn,N);                                                      %échelle des fréquences

figure(1)
plot(V, Mod)                                                         
grid
title('Fourier Transform Of Original Signal ‘X’')
xlabel('Frequency (Hz)')
ylabel('Amplitude')

%%

[m,i]=max(Mod(10242:end));                                                 %recherche du maximum du spectre pour les fréq>0 (10241 est l'indice de fréq nulle)
iFp=10241+i;                                                               %indice de la fréq porteuse
[m,i]=max(Mod((iFp+1):end));                                               %recherche max du spectre pour f>Fp
iFm=iFp+i;                                                                     %indice de la fréq moduleuse
xFm=m;                                                                     %amplitude de Fm

%Filtrage: suppression de la porteuse
FX2=zeros(N,1);
FX2(10241)=Mod(10241);
FX2(10241+(iFm-iFp-1))=xFm;
FX2(10241-(iFm-iFp-1))=xFm;
%
figure(3)
plot(V, FX2)
grid
title('Filtered FFT ‘X’')
xlabel('Frequency (Hz)')
ylabel('Amplitude')



%Transformée inverse
FX2=fftshift(FX2);
X=ifft(FX2);
figure(4)
plot(M(:,1),X)
grid
title('Demodulated Signal')
xlabel('Time (s)')
ylabel('Amplitude')







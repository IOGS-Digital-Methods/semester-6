%%%%%%%on ferme les graphs ouverts précédemment 

close all;   

%%%%%%%on charge les données de la porteuse et les données du signal modulé

%fonction cvsread permet de lire des fichiers cvs  
si = csvread('JV2.CSV',3,3);
% on affiche la courbe 
plot(si(:,1),si(:,2),'g');

legend('signal modulé');

%%%%%%%Calcul et affichage des FFT

sy = fftshift(fft(si));%calcul fft du signal modulé
plot(v,abs(sy),'g'); % on affiche la fft 
legend('FFT du signal modulé');
xlabel('tps (s)');
ylabel('Amplitude');

%%%%% FFT en fréquence et démodulation 

%calcul du temps d'échantillonage et de la fréquence d'échantillonage
to =abs( si(1,1)-si(2,1)); 
Fe= 1/to;
N=4095;
% calcul de la fréquence par échantillon
Fe_ech = Fe/N ;
%on créer un axe à la bonne taille centré en 0 
F = (-N/2 : N/2 - 1)*Fe_ech; % on enlève 1 pour avoir F = 4095
% on trace le graph de la FFT en fréquence 
plot(F,abs(sy),'r');
title('fft en fréquence'); 
xlabel('fréquence (Hz)');
ylabel('Amplitude'); 

% On enlève la modulation qui est le pic central et maximal 

%/!\ il ne faut pas prendre les données du temps pour n'avoir
%que les valeurs de la modulation (il faut avoir un pic par une diagonale)

% %repérage modulation & indice modulation
donneesmod = sy(:,2);
[valmod, indmod]= max(abs(donneesmod)); 

% supp donnees
donneesmod(indmod) = 0;
donneesmod(indmod + 1) = 0;
donneesmod(indmod - 1) = 0;
donneesmod(indmod + 2) = 0;
donneesmod(indmod - 2) = 0;
if(indmod > N/2)
    for i = 1:(N-1)/2
        donneesmod(i) = 0;
    end
else
    for i = (N-1)/2:N
        donneesmod(i) = 0;
    end  
    for j = 3:2*indmod
        donneesmod((N-1)/2-j+1) = donneesmod(2*indmod - j+1);
        donneesmod(2*indmod - j+1) = 0;
    end
end

figure;
plot(v, abs(donneesmod));



%demodulation  (=TF inverse)
demod= ifft(donneesmod, 'symmetric'); 
figure;
plot(demod);


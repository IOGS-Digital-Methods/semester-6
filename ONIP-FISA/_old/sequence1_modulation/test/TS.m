%%%%%%%on ferme les graphs ouverts précédemment 
close all;   

%%%%%%%on charge les données de la porteuse et les données du signal modulé

%fonction cvsread permet de lire des fichiers cvs  
si = csvread('JV2.CSV',3,3);

% nombre de points
N = max(size(si(:,1)));
% Calcul du temps d'échantillonnage
to = abs( si(1,1)-si(2,1)); 
%calcul de la fréquence d'échantillonage
Fe= 1/to;
%on créer un axe à la bonne taille centré en 0 
% JV : vrai si fftshift :)
F = (-N/2 : N/2 - 1)*Fe/N; % on enlève 1 pour avoir size(F) = 4095

% on affiche la courbe 
figure;
plot(si(:,1),si(:,2));
legend('signal modulé');
xlabel('Temps (s)');
ylabel('Amplitude');

%%%%%%%Calcul et affichage des FFT
donneesmod = fftshift(fft(si(:,2)));%calcul fft du signal modulé
%car on veut avoir un axe des abscisses allant de 0 à Fe permettant d'avoir
%N points répartis de manière linéaire.N= 4095 car c'est est la taille de
%abs(sy)
% on trace le graph de la FFT en fréquence 
figure;
plot(F,abs(sy),'r');
title('fft en fréquence'); 
xlabel('fréquence (Hz)');
ylabel('Amplitude'); 

%%%%% FFT en fréquence et démodulation
% On enlève la modulation qui est le pic central et maximal 

%/!\ il ne faut pas prendre les données du temps pour n'avoir
%que les valeurs de la modulation (il faut avoir un pic par une diagonale)

% repérage modulation & indice modulation
[valmod ,indmod]= max(abs(donneesmod)); 
% creation d'une matrice pour pouvoir parcourir les pics
donnees = zeros(N,1);  %il faut créer remplie de zéros sinon reste vide pour toujours
matrice = zeros(N,1); 

% on enlève une partie de la FFT (la partie où il ne trouve pas le maximum) 
for i=(N-1)/2:N %indice tableau 1 à N
    donneesmod(i)= 0;
end 
% on remplace tous les maxs de donneesmod par 0 ( pour enlever la porteuse )
donneesmod(indmod)= 0; 
donneesmod(indmod-1) = 0; 
donneesmod(indmod+1) = 0; 
donneesmod(indmod-2) = 0; 
donneesmod(indmod+2) = 0; 
donneesmod(indmod-3) = 0; 
donneesmod(indmod+3) = 0; 
% on rempli le nouveau tableau sans le max
for i=4:N
     donnees(i) = donneesmod(i); 
end 

% % on a le spectre sans la modulation mais il n'est pas centré en 0, il faut
% % le centrée en 0 
% 
distance = abs(indmod-(N-1)/2)
for j = 1:2*distance
       donnees((N-1)/2+distance-j) = donnees((N-1)/2-j);
       donnees((N-1)/2-j) = 0; %on efface les donnees prisent dans indice
end

% on trace le graph de la FFT en fréquence modifiée
figure;
plot(F,abs(donnees),'r');
title('fft en fréquence'); 
xlabel('fréquence (Hz)');
ylabel('Amplitude');     

% %demodulation  (=TF inverse)
demod= ifft(fftshift(donnees(:)),'symmetric'); 
figure;
plot (si(:,1) ,demod,'b'); 
title('figure démodulée'), 
xlabel('temps');
ylabel('tension(V)'); 










clear all
close all

nom_fichier = 'trame3';
ext_fichier = '.jpg'

larg = 600;
haut = 400;

%% Tramage
x = linspace(1,larg,larg);
y = linspace(1,haut,haut);

[X,Y] = meshgrid(y,x);

% ----------------- tramage d'une image non tramée
pasX = 60; pasY = 80; amp = 1000;
trame = amp*round(0.5*(1 + cos(2.*pi./pasX.*X + 2.*pi./pasY.*Y)));
%trame = amp*(1 + cos(2.*pi./pasX.*X + 2.*pi./pasY.*Y));

% affichage trame
figure(2);
colormap(gray)
imagesc(trame)
% sauvegarde
nom_trame = strcat(nom_fichier,'_trame.png');
imwrite(trame,nom_trame)
nom_trame = strcat(nom_fichier,'_trame.jpg');
imwrite(trame,nom_trame)

%% Détramage
TF_trame = fftshift(fft2(trame));
TF_trame_aff = imcomplement(log(abs(TF_trame)));
figure(4);
colormap(gray)
imagesc(TF_trame_aff)
nom_trame = strcat(nom_fichier,'_TF.jpg');
imwrite(TF_trame_aff,nom_trame)
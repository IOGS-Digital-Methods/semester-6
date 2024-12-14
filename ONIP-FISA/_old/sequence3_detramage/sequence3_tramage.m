clear all
close all

%% Affichage image
image = imread('image/arbre.png'); % image non tramée
image = image(:,:,1);

figure();
imagesc(image);
colormap gray;

[hauteur, largeur] = size(image);

% TF
TFimage = fft2(image);

figure();
imagesc(log(abs(fftshift(TFimage))));
colormap gray;

%% Tramage via FFT
x1 = floor(5/11*hauteur);
x2 = floor(7/11*hauteur);
y1 = floor(4/9*largeur);
y2 = floor(5/9*largeur);

TFimage(x1,y1) = max(max(abs(TFimage)))/2;
TFimage(x2,y2) = max(max(abs(TFimage)))/2;

figure();
imagesc(log(abs(fftshift(TFimage))));
colormap gray;

%% Recréation de l'image tramée
image_trame = ifft2(TFimage);
figure();
imagesc(abs(image_trame));
colormap gray;

%% Trame
hauteurT = hauteur;
largeurT = largeur;
TFtrame = zeros(hauteurT,largeurT);

% Ajout de 2 points
K = 10;
pasH = 15;
pasL = 51;
NpasH = 7;
NpasL = 24;
TFtrame(floor(NpasH/pasH*hauteurT), floor(NpasL/pasL*largeurT)) = K*hauteurT*largeurT;
TFtrame(floor((pasH-NpasH)/pasH*hauteurT), floor((pasL-NpasL)/pasL*largeurT)) = K*hauteurT*largeurT;

figure();
imagesc(TFtrame);
colormap gray;

trame = ifft2(fftshift(TFtrame));
figure();
imagesc(abs(trame));
colormap gray;

% Ajout tramage
trame2 = uint8(abs(trame));
imageT2 = image + trame2;
figure();
imagesc(imageT2);
colormap gray;

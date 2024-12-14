clear all
close all

nom_fichier = 'chat_640';
ext_fichier = '.jpg'

%% Recup image
nom_image = strcat(nom_fichier,ext_fichier);
disp(nom_image)
image = imread(nom_image); % image non tramée
image1d = image(:,:,1);

%% Traitement
image_shift = fftshift(image1d);
figure(1);
colormap(gray)
imagesc(image_shift)
nom_trait = strcat(nom_fichier,'_traitement.png');
imwrite(image_shift,nom_trait)

%% Tramage
x = linspace(1,size(image,1),size(image,1));
y = linspace(1,size(image,2),size(image,2));

[X,Y] = meshgrid(y,x);

% ----------------- tramage d'une image non tramée
pasX = 10; pasY = 20; amp = 100;
trame = amp*round(0.5*(1 + cos(2.*pi./pasX.*X + 2.*pi./pasY.*Y)));
trame = amp*(1 + cos(2.*pi./pasX.*X + 2.*pi./pasY.*Y));

image1d = double(image1d) + trame;
image(:,:,1) = uint8(image1d);

% affichage trame
figure(2);
colormap(gray)
imagesc(trame)
% affichage image tramée
figure(3);
colormap(gray)
imagesc(image(:,:,1))
% sauvegarde
nom_trame = strcat(nom_fichier,'_2_trame.png');
imwrite(image,nom_trame)
nom_trame = strcat(nom_fichier,'_2_trame.jpg');
imwrite(image,nom_trame)

%% Détramage
TF_trame = fftshift(fft2(trame));
figure(4);
colormap(gray)
imagesc(log(abs(TF_trame)))

TF_image = fftshift(fft2(image1d));
figure(5);
colormap(gray)
imagesc(log(abs(TF_image)))
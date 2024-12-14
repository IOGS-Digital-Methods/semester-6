clear all
close all

nom_fichier = 'figure';
ext_fichier = '.png'

%% Recup image
nom_image = strcat(nom_fichier,ext_fichier);
disp(nom_image)
image = imread(nom_image); % image non tramée
image1d = imcomplement(image(:,:,1));

x_dim = size(image,1)
y_dim = size(image,2)
amp = 200;

%% Tramage
x = linspace(1,x_dim/2,x_dim/2);
y = linspace(1,y_dim/2,y_dim/2);
[X,Y] = meshgrid(y,x);

% ----------------- tramage d'une image non tramée
pasX = 6; pasY = 10; 
trame = amp*round(0.5*(1 + cos(2.*pi./pasX.*X + 2.*pi./pasY.*Y)));
trame = amp*(1 + cos(2.*pi./pasX.*X + 2.*pi./pasY.*Y));

image1d(1:x_dim/2,1:y_dim/2) = double(image1d(1:x_dim/2,1:y_dim/2)) + trame;
image(:,:,1) = uint8(image1d);

% ----------------- tramage d'une image non tramée
pasX = 12; pasY = -8; 
trame = amp*round(0.5*(1 + cos(2.*pi./pasX.*X + 2.*pi./pasY.*Y)));
trame = amp*(1 + cos(2.*pi./pasX.*X + 2.*pi./pasY.*Y));

image1d(x_dim/2:x_dim-1,1:y_dim/2) = double(image1d(x_dim/2:x_dim-1,1:y_dim/2)) + trame;
image(:,:,1) = uint8(image1d);

% ----------------- tramage d'une image non tramée
pasX = 8; pasY = 1000;
trame = amp*round(0.5*(1 + cos(2.*pi./pasX.*X + 2.*pi./pasY.*Y)));
trame = amp*(1 + cos(2.*pi./pasX.*X + 2.*pi./pasY.*Y));

image1d(x_dim/2:x_dim-1,y_dim/2:y_dim-1) = double(image1d(x_dim/2:x_dim-1,y_dim/2:y_dim-1)) + trame;
image(:,:,1) = uint8(image1d);

% ----------------- affichage image tramée
figure(3);
colormap(gray)
imagesc(image(:,:,1))
% ----------------- sauvegarde
nom_trame = strcat(nom_fichier,'_2_trame.png');
imwrite(image1d,nom_trame)
nom_trame = strcat(nom_fichier,'_2_trame.jpg');
imwrite(image1d,nom_trame)

%% Détramage
TF_image = fftshift(fft2(image1d));
figure(5);
colormap(gray)
imagesc(log(abs(TF_image)))
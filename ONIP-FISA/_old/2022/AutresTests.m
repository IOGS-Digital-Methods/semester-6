%% Essais
%   Module : Initiation au Calcul Scientifique
%--------------------------------------------------------------
%   Autre
%--------------------------------------------------------------
%   Auteur : Julien VILLEMEJANE
%   Date : 27/05/2021
%--------------------------------------------------------------
close all;
clear all;

%% Zonage
hauteur = 200;
largeur = 300;
pas = 20;
M = uint8(zeros(hauteur, largeur));

M(hauteur/2-2*pas:hauteur/2+2*pas, largeur/2-pas:largeur/2+pas) = 40;
M(hauteur/2-pas:hauteur/2+pas, largeur/2-pas:largeur/2+pas) = 100;

figure(1);
imshow(M); colormap(gray);

%% 
M1 = repmat(M,3,2);
figure(2);
imshow(M1); colormap(gray);
%%
M2 = kron(M,uint8(ones(2,3)));
figure(3);
imshow(M2); colormap(gray);
%%
M(M>50)=200;
figure(4);
imshow(M); colormap(gray);

%%
x = 1:largeur;
y = 1:hauteur;

[J,X]=meshgrid(x,y);
T=100*(1+sin(J/10));
figure(5);
imagesc(T); colormap(gray);

MT = M + uint8(T);
figure(6);
imagesc(MT); colormap(gray);

%% FFT 2D et filtrage
% Image brute
im_raw = imread('sequence3_detramage/arbre.png');
im_raw = im_raw(:,:,1);
hauteur = size(im_raw,1);
largeur = size(im_raw,2);
figure(10);
imagesc(im_raw);
colormap(gray);

% TF image
TF_img = fftshift(fft2(im_raw));
figure(11);
imagesc(log(abs(TF_img)));
colormap(gray);

% Masquage circulaire
[x0,y0] = ginput(1);
[x1,y1] = ginput(1);

[columnsInImage rowsInImage] = meshgrid(1:largeur, 1:hauteur);
rayon = sqrt((x0-x1)*(x0-x1)+(y1-y0)*(y1-y0));
circlePixels = (rowsInImage - y0).^2 + (columnsInImage - x0).^2 <= rayon.^2;

figure(12);
imagesc(circlePixels) ;
colormap(gray)

% Utilisation du masque sur la TF
TF_img_mask = TF_img .* double(circlePixels);
figure(13);
imagesc(log(abs(TF_img_mask))) ;
colormap(gray)

% Reconstruction de l'image
img_rec = ifft2(TF_img_mask);
figure(14);
imagesc(abs(img_rec)) ;
colormap(gray)

%% FFT 2D et filtrage / v2
% Image brute
im_raw = imread('sequence3_detramage/arbre.png');
im_raw = im_raw(:,:,1);
hauteur = size(im_raw,1);
largeur = size(im_raw,2);
figure(10);
imagesc(im_raw);
colormap(gray);

% Tramage
x = 1:largeur;
y = 1:hauteur;
[X,Y] = meshgrid(x,y);
% ----------------- tramage d'une image non tramée
pasX = 5; pasY = 10; amp = 10;
trame = amp*(1 + cos(2.*pi./pasX.*X + 2.*pi./pasY.*Y));
im_raw = double(im_raw) + trame;


% TF image
TF_img = fftshift(fft2(im_raw));
figure(11);
imagesc(log(abs(TF_img)));
colormap(gray);

% Masquage circulaire
[x0,y0] = ginput(1);

figure(12);

for k = 0:2
    [columnsInImage rowsInImage] = meshgrid(1:largeur, 1:hauteur);
    rayon = (k+1)*25;
    circlePixels = (rowsInImage - y0).^2 + (columnsInImage - x0).^2 <= rayon.^2;
    
    subplot(3,3,k*3+1)
    imagesc(circlePixels) ;
    colormap(gray)

    % Utilisation du masque sur la TF
    TF_img_mask = TF_img .* double(circlePixels);
    subplot(3,3,k*3+2)
    imagesc(log(abs(TF_img_mask))) ;
    colormap(gray)

    % Reconstruction de l'image
    img_rec = ifft2(TF_img_mask);
    subplot(3,3,k*3+3)
    imagesc(abs(img_rec)) ;
    colormap(gray)
end

%% Signaux et fft
Te = 1e-3;
N = 1e4;
t = 0:Te:N*Te;

y = 0.1 * t.^2;
figure;
subplot(2,1,1);
plot(t, y);
subplot(2,1,2);
plot(t, fftshift(y));
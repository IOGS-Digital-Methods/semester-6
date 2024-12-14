%% Traitement du signal / Images TP Diffraction
%   Module : Init Calcul Scientifique / CFA-S6
%--------------------------------------------------------------
%   Fonctions de Bessel
%--------------------------------------------------------------
%   Auteur : Julien VILLEMEJANE
%   Date : 09/11/2020
%--------------------------------------------------------------
clear all;
close all;
lambda = 632.8e-9;      % longueur d'onde en nm
Dcapt = 1;          % distance entre pupille et capteur en m
dpup = 1e-3;        % diametre pupille en m

k = dpup/(Dcapt*lambda);      % lien entre tache airy et diametre pupille

taille_pix = 5.3e-6;        % taille d'un pixel en m

z = linspace(-1280/2*taille_pix,1280/2*taille_pix, 1280);
J = besselj(1,k*z)./(k*z);
figure(1)
plot(z,J)
grid on
legend('J_1')
title('Bessel Functions of the First Kind for $\nu = 0$','interpreter','latex')
xlabel('z','interpreter','latex')
ylabel('$J_\nu(z)$','interpreter','latex')

%% Lecture image
% chemin et nom image
image_diametre1mm = 'airy_1mm.bmp';
image_diametre2mm = 'airy_2mm.bmp';
% ouverture image
img_1mm=double(imread(image_diametre1mm));
img_2mm=double(imread(image_diametre2mm));
% affichage de l'image
figure('name',image_diametre1mm)
colormap(gray)
imagesc(img_1mm),colorbar,axis image;
figure('name',image_diametre2mm)
colormap(gray)
imagesc(img_2mm),colorbar,axis image;

%% Recherche du max
% Image 1mm
[max_img1mm_x, I_1mm_x] = max(img_1mm);
[max_img1mm_y, I_1mm_y] = max(max_img1mm_x);
valeur_max_1mm = img_1mm(I_x(I_1mm_y), I_1mm_y);
ligne_x_1mm = img_1mm(I_1mm_x(I_1mm_y),:);
% Image 2mm
[max_img2mm_x, I_2mm_x] = max(img_2mm);
[max_img2mm_y, I_2mm_y] = max(max_img2mm_x);
valeur_max_2mm = img_2mm(I_x(I_2mm_y), I_2mm_y);
ligne_x_2mm = img_2mm(I_2mm_x(I_2mm_y),:);

% Bessel
kasintheha_1mm = 4000;
I0_1mm = 225;
J_1mm = I0_1mm * (2*besselj(1,kasintheha_1mm*z)./(kasintheha_1mm*z)).^2;
kasintheha_2mm = 8000;
I0_2mm = 225;
J_2mm = I0_2mm * (2*besselj(1,kasintheha_2mm*z)./(kasintheha_2mm*z)).^2;


figure;
plot(z, ligne_x_1mm, z, J_1mm, z, ligne_x_2mm, z, J_2mm);


%% Traitement du signal / Images TP Diffraction
%   Module : Init Calcul Scientifique / CFA-S6
%--------------------------------------------------------------
%   Autre
%--------------------------------------------------------------
%   Auteur : Julien VILLEMEJANE
%   Date : 09/11/2020
%--------------------------------------------------------------
clear all;
close all;

%% Lecture image
% chemin et nom image
%nom_image=input('Nom de l''image : ','s');
nom_image = 'airy_1mm.bmp';
% ouverture image
img=double(imread(nom_image));
% affichage de l'image
figure('name',nom_image)
colormap(gray)
imagesc(img),colorbar,axis image;

% Sélection dans l'image
disp('Recadrage de l''image - Créez une zone avec votre souris autour de la zone utile de l''image puis double-cliquez')
img_crop=imcrop;
imagesc(img_crop);
disp('Sélection du centre de la tache - Sélectionnez le centre de la tache à l''aide de la souris')
[x_centre, y_centre] = ginput(1);
x_centre = round(x_centre);
y_centre = round(y_centre);
% Profils horizontal et vertical
disp('Affichage du profil sans moyennage')
x_profil = (-size(img_crop,2)/2:size(img_crop,2)/2-1);
y_profil = (-size(img_crop,1)/2:size(img_crop,1)/2-1);

figure('name','Profil de la tache sans moyennage')
subplot(2,1,1); plot(x_profil,img_crop(y_centre,:)); title('Profil horizontal'); grid on;
xlabel('Position (x)');
subplot(2,1,2); plot(y_profil, img_crop(:,x_centre)); title('Profil vertical'); grid on;
xlabel('Position (y)');

% Profils moyennés
profil_2 = mean(img_crop(y_centre-2:y_centre+2,:));
profil_3 = mean(img_crop(y_centre-3:y_centre+3,:));
profil_5 = mean(img_crop(y_centre-5:y_centre+5,:));
profil_10 = mean(img_crop(y_centre-10:y_centre+10,:));
profil_50 = mean(img_crop(y_centre-50:y_centre+50,:));
figure('name','Profil de la tache avec moyennage')
plot(x_profil, profil_2, x_profil, profil_3, x_profil, profil_5, x_profil, profil_10, x_profil, profil_50)
legend('moy sur 5 lignes', 'moy sur 7 lignes', 'moy sur 11 lignes', 'moy sur 21 lignes', 'moy sur 101 lignes'); 
grid on

%% Modèle de Bessel / Fit


% non modifié
%% on calcule des "guess"
x0_ini = sum(x_profil.*profil_10)./sum(profil_10)   %% centre (barycentre)
decalage_ini = profil_10(1)     %% offset (valeur au bord)
Ampl_ini = max(profil_10)       % amplitude (maximum)
diametre_ini = 4*sqrt(sum((x_profil-x0_ini).^2.*(profil_10-decalage_ini))./sum(profil_10-decalage_ini)) % 4*rayon rms


options=optimset('Display','off','TolFun',1e-8,'TolX',1e-3);

param=[x0_ini diametre_ini Ampl_ini decalage_ini];
format long, param=lsqcurvefit('fonct_sinus_card_carre',param,x_profil,profil_10);
x0=param(1);
diametre=param(2)
Ampl=param(3);
decalage=param(4);


r=2.44*pi*abs(x_profil-x0)/diametre;
E_fit=ones(size(x_profil));
k=r~=0; % masque logique pour éviter les cas 0, précalculé à 1 par le ones(...)
E_fit(k)=(2*besselj(1,r(k))./r(k)).^2; % expression conditionnelle utilisant le masque
E_fit=E_fit*Ampl+decalage;

figure
plot(x_profil,profil_10,'g'),grid on,hold
 
plot(x_profil, E_fit,'r');
 
ylabel('Profil moyen horizontal et fit Airy')
xlabel(['Diamètre 1er anneau noir : ' num2str(diametre,4) ' pixels'])
 
 hold off

 
%% Fonction bessel
function E=fonct_tache_airy(param,x);
x0=param(1);
diametre=param(2);
ampl=param(3);
offset=param(4);

r=2.44*pi*abs(x-x0)/diametre; % le abs pour éviter les arguments réels négatifs
                      % on se servira de la parité de la tache d'Airy
E=ones(size(x));
k=r~=0; % masque logique pour éviter les cas 0, précalculé à 1 par le ones(...)
E(k)=(2*besselj(1,r(k))./r(k)).^2; % expression conditionnelle utilisant le masque

E=E*ampl+offset;
end
%% Fonction sinus cardinal
function y=fonct_sinus_card_carre(param,x);
x0=param(1);
largeur=param(2);
Ampl=param(3);
decalage=param(4);

u=(x-x0)/(0.5*largeur);
y=Ampl*sinc(u).^2+decalage;
end
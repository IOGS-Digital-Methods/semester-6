clear all
close all

%% Affichage image
image = imread('image/mire_siemens.jpg'); % image non tramée
%image = imread('chat.jpeg'); % image déjà tramée
%image = imread('univ.png'); % image déjà tramée à certain endroit

mire = image(:,:,1);
figure('color','w'),
colormap(gray(256))
imagesc(mire)

[hauteur, largeur] = size(mire);

%% TF image mire radiale
TFmire = fft2(mire);
figure('color','w'),
colormap(gray(256))
imagesc(log(abs(fftshift(TFmire))))

%% Suppression anneau sur image
R1 = 500;
R2 = 1200;

x0 = largeur/2;
y0 = hauteur/2;

for x=1:largeur
    for y = 1:hauteur
        rr = sqrt((x-x0)*(x-x0) + (y-y0)*(y-y0));
        if((rr > R1) && (rr < R2))
            mire(y,x) = 255;
        end;
    end;
end;

figure('color','w'),
colormap(gray(256))
imagesc(mire)

%% TF image mire radiale modifiée
TFmire = fft2(mire);
figure('color','w'),
colormap(gray(256))
imagesc(log(abs(fftshift(TFmire))))
clear all
close all

%%
hauteur = 200;
largeur = 300;
image = zeros(hauteur, largeur);

% tramage
A = 10;
wx = 1000;
wy = 100;
for i = 1:hauteur
    for j = 1:largeur
        image(i,j) = A*sin(2*pi*wx*(i/hauteur));
    end
end

figure();
imagesc(image);
colormap gray;

% TF
TF = fft2(image);

figure();
imagesc(log(abs(fftshift(TF))));
colormap gray;
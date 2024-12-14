clear all
close all

%% Affichage image
image = imread('image/figure_2_trame.jpg'); % image tramée
image = image(:,:,1);

figure();
imagesc(image);
colormap gray;

[hauteur, largeur] = size(image);

% TF
TFimage = fft2(image);
TFimage_shift = fftshift(TFimage);
figure();
imagesc(log(abs(TFimage_shift)));
colormap gray;

%% Masquage
display('Choix centre masque ');
[x0,y0] = ginput(1);
display('Choix fin masque ');
[x1,y1] = ginput(1);
x0 = ceil(x0);
y0 = ceil(y0);
x1 = ceil(x1);
y1 = ceil(y1);
r = ceil(sqrt((x1-x0)*(x1-x0)+(y1-y0)*(y1-y0)))

TFimage_new_shift = zeros(hauteur, largeur);

for x = x0-r:x0+r
    for y = y0-r:y0+r
        rr = sqrt((x-x0)*(x-x0) + (y-y0)*(y-y0));
        if((rr < r))
            TFimage_new_shift(y,x) = TFimage_shift(y,x);
        end;
    end;
end;
figure();
imagesc(log(abs(TFimage_new_shift)));
colormap gray;

%% reconstruction image
TFimage_new = fftshift(TFimage_new_shift);
image_new = abs(ifft2(TFimage_new));

figure();
imagesc(image_new);
colormap gray;
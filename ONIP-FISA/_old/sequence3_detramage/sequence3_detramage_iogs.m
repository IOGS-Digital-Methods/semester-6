clear all
close all

%% Affichage image
image = imread('arbre.png'); % image non tramée
%image = imread('chat.jpeg'); % image déjà tramée
%image = imread('univ.png'); % image déjà tramée à certain endroit

image = image(:,:,1);

x = linspace(1,size(image,1),size(image,1));
y = linspace(1,size(image,2),size(image,2));

[X,Y] = meshgrid(y,x);

% ----------------- tramage d'une image non tramée
pasX = 5; pasY = 1000; amp = 10;
trame = amp*(1 + cos(2.*pi./pasX.*X + 2.*pi./pasY.*Y));

image = double(image) + trame;
%------------------

figure('position',[100 100 1250 950],'color','w'),
colormap(gray(256))
subplot(2,2,1), imagesc(image)

%% TF image
TF_image = fftshift(fft2(image));
subplot(2,2,2), imagesc(20*log10(abs(TF_image)))
% VisudB(TF_image,-100)

%% Masquage à la souris (centre puis bord)

[Xcentre,Ycentre] = ginput(1);
[Xbord,Ybord] = ginput(1);

Rayon = sqrt((Xbord-Xcentre)^2+(Ybord-Ycentre)^2);

theta=linspace(0,2*pi,50)';
Tcercle=[Rayon*cos(theta)+Xcentre Rayon*sin(theta)+Ycentre];

hold on, plot(Tcercle(:,1),Tcercle(:,2),'r')

[thetas, rhos] = cart2pol(X-Xcentre,Y-Ycentre);

idx = (rhos <= Rayon) ; 
masque = zeros(size(X));
masque(idx) = 1 ;


TF_image_masque = TF_image.*masque;

subplot(2,2,3), VisudB(TF_image_masque,-100)


%% TF inverse

image_detram = (ifft2(TF_image_masque));

subplot(2,2,4), VisudB(image_detram,-30)

% ------------------




%% FFT 2D et filtrage / v2
% Image brute
im_raw = imread('images/mire_radiale.png');
im_raw = im_raw(:,:,1);
hauteur = size(im_raw,1);
largeur = size(im_raw,2);
figure(10);
imagesc(im_raw);
colormap(gray);

pasR = 20;

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
    rayon = (k+1)*pasR;
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





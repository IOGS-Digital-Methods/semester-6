%% Exemple de programme permettant d'ouvrir une image et d'afficher sa TF
%   LEnsE - 2025/01/24 - J. Villemejane

%% Lire l'image en niveaux de gris
image = imread('test_image.png');
if size(image, 3) == 3
    image = rgb2gray(image); % Convertir en niveaux de gris si l'image est en couleur
end
image = double(image); % Convertir en type double pour les calculs

% Affichage de l'image
figure('Name', 'Original Image');
imshow(uint8(image));
title('Original Image');
colormap(gca, 'gray');


%% Effectuer la FFT
fft_image = fft2(image);
fft_shifted = fftshift(fft_image);

magnitude_spectrum = log(abs(fft_shifted)+0.01);

% Afficher le spectre FFT
figure('Name', 'Spectre FFT');
imshow(magnitude_spectrum, [], 'InitialMagnification', 'fit');
title('FFT de l''image originale');
colormap(gca, 'gray');


%% Définir une fonction pour créer un masque circulaire
function masked_image = circular_mask(radius, image)
    [h, w] = size(image);
    center_y = floor(h / 2);
    center_x = floor(w / 2);
    [X, Y] = meshgrid(1:w, 1:h);
    % Distance au centre
    dist_from_center = sqrt((X - center_x).^2 + (Y - center_y).^2);
    % Créer un masque circulaire
    mask = dist_from_center <= radius;
    % Appliquer le masque
    masked_image = image .* mask;
end

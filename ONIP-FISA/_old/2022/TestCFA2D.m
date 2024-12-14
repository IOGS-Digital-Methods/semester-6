clear all;
close all;
% Image 1
X1 = imread('imageTestCercle.png');
figure(1);
subplot(1,2,1);
imagesc(X1);
set(gca,'DataAspectRatio',[1,1,1]);

Y1 = fft2(X1);
subplot(1,2,2);
imagesc(abs(fftshift(Y1)));
set(gca,'DataAspectRatio',[1,1,1]);

% Image 2
X2 = imread('imageTestCercle2.png');
figure(2);
subplot(1,2,1);
imagesc(X2);
set(gca,'DataAspectRatio',[1,1,1]);

Y2 = fft2(X2);
subplot(1,2,2);
imagesc(abs(fftshift(Y2)));
set(gca,'DataAspectRatio',[1,1,1]);

% Image 3
X3 = imread('imageTestCarre.png');
figure(3);
subplot(1,2,1);
imagesc(X3);
set(gca,'DataAspectRatio',[1,1,1]);

Y3 = fft2(X3);
subplot(1,2,2);
imagesc(abs(fftshift(Y3)));
set(gca,'DataAspectRatio',[1,1,1]);

% Image 4
X4 = imread('Franges.png');
figure(4);
subplot(1,2,1);
imagesc(X4);
set(gca,'DataAspectRatio',[1,1,1]);

Y4 = fft2(X4);
subplot(1,2,2);
imagesc(abs(fftshift(Y4)));
set(gca,'DataAspectRatio',[1,1,1]);

% Image 5
X5 = imread('franges-2.png');
figure(5);
subplot(1,2,1);
imagesc(X5);
set(gca,'DataAspectRatio',[1,1,1]);

Y5 = fft2(X5);
subplot(1,2,2);
imagesc(abs(fftshift(Y5)));
set(gca,'DataAspectRatio',[1,1,1]);
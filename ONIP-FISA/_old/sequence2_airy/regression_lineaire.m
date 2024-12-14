%% Traitement du signal / Moindres carres / Regression
%   Module : Init Calcul Scientifique / CFA-S6
%--------------------------------------------------------------
%   Autre
%--------------------------------------------------------------
%   Auteur : Julien VILLEMEJANE
%   Date : 22/09/2020
%--------------------------------------------------------------
clear all;
close all;
N = 51;     % nombre d'échantillon
K = 2;      % quantite de bruits
%% Données bruités
A = 10;
B = 20;
x2 = linspace(0,1,N)';
bruit = K*(rand([N 1])-0.5);
y2 = A * x2 + B;
y2b = y2 + bruit;
format long

figure;
subplot(1,3,1)
plot(x2, y2, x2, y2b, '+');
title('Données linéaires bruités');
legend('Lin','Bruit');
ylim([0 A+B+K])

%% Mauvaise Regression
M2_bad = x2\y2b;
y2_calc_bad = x2 * M2_bad;

subplot(1,3,2)
plot(x2, y2b, 'r+', x2, y2_calc_bad, 'b');
title('Regression (bad)');
legend('Data','Reg');
txt = {'Coeff:',['Reel : A = ',num2str(A)],['Calc : A = ',num2str(M2_bad)]};
text(0.5,(A+B)/3,txt);
ylim([0 A+B+K])

%% Meilleure Regression
X2 = [ones(length(x2),1) x2];
M2_good = X2\y2b;
y2_calc_good = X2*M2_good;

subplot(1,3,3)
plot(x2, y2b, 'r+', x2, y2_calc_good, 'b', x2, y2, 'g-');
title('Regression (better)');
legend('Data','Reg','No Bruit');
txt = {'Coeff:',strcat('Reel : A = ',num2str(A),' B = ',num2str(B)),strcat('Calc : A = ',num2str(M2_good(2)),' B = ',num2str(M2_good(1)))};
text(0.5,(A+B)/3,txt);
ylim([0 A+B+K])
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

z = -20:0.1:20;

J = zeros(5,length(z));
for i = 0:4
    J(i+1,:) = besselj(i,z);
end
figure(1)
plot(z,J)
grid on
legend('J_0','J_1','J_2','J_3','J_4','Location','Best')
title('Bessel Functions of the First Kind for $\nu \in [0, 4]$','interpreter','latex')
xlabel('z','interpreter','latex')
ylabel('$J_\nu(z)$','interpreter','latex')


%% Data
load census;
f=fit(cdate,pop,'poly2')
figure(2)
plot(f,'--',cdate,pop)
hold on

% Fit autre
ft = fittype('a*(x-b)^n','problem','n');
[curve2,gof2] = fit(cdate,pop,ft,'problem',2)
plot(curve2,'b')
[curve3,gof3] = fit(cdate,pop,ft,'problem',3)
plot(curve3,'g')
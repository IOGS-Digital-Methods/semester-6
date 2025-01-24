%% Exemple de programme permettant de générer un signal sinusoïdal à partir d'un vecteur temps
%   LEnsE - 2025/01/24 - J. Villemejane

%% Génération de signaux
% Définir les paramètres
frequence = 200;             % Fréquence en Hz
vecteurTemps = 0:0.0003:0.1;   % Vecteur temps de 0 à 1 seconde
amplitude = 2;              % Amplitude de 2

% Appeler la fonction
ySin1 = genererSinus(frequence, vecteurTemps, amplitude);

% Tracer le signal
figure;
hold on;
plot(vecteurTemps, ySin1);
xlabel('Temps (s)');
ylabel('Amplitude');
title('Signal Sinusoïdal');
grid on;


%% Calcul de ...
ySin1TF = fft(ySin1);
ySin1TFsh = fftshift(ySin1TF)
figure;
hold on;
plot(abs(ySin1TF));
plot(abs(ySin1TFsh));
xlabel('???');
ylabel('Amplitude');
title('???');
legend('FFT','FFT avec shift')
grid on;


%% Fonction de génération d'un signal sinusoïdal
function y = genererSinus(frequence, vecteurTemps, amplitude)
    % GENERERSINUS Génère un signal sinusoïdal
    % 
    % Syntaxe :
    %   y = genererSinus(frequence, vecteurTemps, amplitude)
    %
    % Entrées :
    %   - frequence : Fréquence du sinus en Hz
    %   - vecteurTemps : Vecteur temps (en secondes)
    %   - amplitude : Amplitude du sinus
    %
    % Sortie :
    %   - y : Signal sinusoïdal généré

    % Génération du signal sinusoïdal
    y = amplitude * sin(2 * pi * frequence * vecteurTemps);
end
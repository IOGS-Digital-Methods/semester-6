%% Exemple de programme permettant de générer un signal sinusoïdal à partir d'un vecteur temps
%   LEnsE - 2025/01/24 - J. Villemejane

%% Génération de signaux
% Définir les paramètres
frequence = 200;             % Fréquence en Hz
vecteurTemps = 0:0.0003:0.1;   % Vecteur temps de 0 à 1 seconde
amplitude = 2;              % Amplitude de 2

% Appeler la fonction
ySin1 = genererSinus(frequence, vecteurTemps, amplitude);
ySin2 = genererSinus(287, vecteurTemps, 3);
ySinSom = ySin1 + ySin2;

% Tracer le signal
figure;
hold on;
plot(vecteurTemps, ySin1);
plot(vecteurTemps, ySin2);
plot(vecteurTemps, ySinSom);
xlabel('Temps (s)');
ylabel('Amplitude');
title('Signal Sinusoïdal');
legend('200 Hz','287 Hz','Somme');
grid on;


%% Calcul de ...
ySinSomTF = fft(ySinSom);
ySinSomTFsh = fftshift(ySinSomTF)
figure;
hold on;
plot(abs(ySinSomTF));
plot(abs(ySinSomTFsh));
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
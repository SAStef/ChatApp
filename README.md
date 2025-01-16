# ChatApp
Cyberteknologi DTU opgave

This project was made as an exercise for the DTU subject, Cyberteknologi del 2. 

The project is basically a messaging app. In this project, a TCP server was coded and implemented, which acts as a midpoint and controller, 
along with a client-application which is a python file to be run by each client on each end of the connection. The whole project is singlehandedly coded with python, 
where the UI implementation was done with the library PyQt6 and multithreading was used along with a socket connection. 

\begin{enumerate}
    \item Åbn linket: {https://github.com/SAStef/ChatApp.git}.
    \item Klon koden fra repository.
    \item Åbn koden i VS-Code.
    \item Kontroller at IP-adressen i \texttt{Main.py} peger på chatserveren. Dette konfigureres på linje 21.
    \item Kør \texttt{server.py} i en dedikeret terminal.
    \item \texttt{main.py} køres i en dedikeret terminal af hver bruger.
    \item Cypher+ er nu åben og dens funktioner tilgængelige. Disse inkluderer:
    \begin{enumerate}
        \item Tekstfelt til beskeden der skal sendes.
        \item \texttt{Send Besked}-knappen der sender beskeden (Her kan der med fordel også benyttes \texttt{Enter}-knappen).
        \item \texttt{Vedhæft Fil(er)}-knappen (Crashes kan forekomme).
        \item \texttt{Set Theme}-knappen, der kræver at et tema vælges inden yderligere brug.
        \item \texttt{AutoScroll On/Off}-knapperne.
    \end{enumerate}
    \item Send beskeder til hinanden i chatrummet!
    
\end{enumerate}

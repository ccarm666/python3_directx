rem  launch operat.exe this is here because python can not keep from screwing up cmd strings with quotes
start C:\BCIHomeSystemFiles\VA_BCI2000\prog\operat.exe --OnConnect "-LOAD PARAMETERFILE %1;SETCONFIG" --OnSuspend "-QUIT" --OnSetConfig "-SET STATE Running 1"
start C:\BCIHomeSystemFiles\VA_BCI2000\prog\SignalGenerator.exe 127.0.0.1
start C:\BCIHomeSystemFiles\VA_BCI2000\prog\P3SignalProcessing.exe 127.0.0.1
start C:\BCIHomeSystemFiles\VA_BCI2000\prog\P3Speller.exe 127.0.0.1

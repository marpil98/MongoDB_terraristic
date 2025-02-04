# MongoDB_terraristic
Small application to menage db contaninig data about my breeding

# Disclaimer
I created this application for my own use, so all communications in this application are in Polish. Similarly, this document is written in Polish, but below is machine translation into English.

## PL
# Licencja
Poniższa aplikacja jest udostępniona na zasadach licencji Apache 2.0

# Działanie
Aplikacja służy do zarządzania danymi zebranymi w bazie MongoDB, które dotyczą mojej hodowli zwierząt terrarystycznych. Staram sie ją mimo to tworzyć w dość elastyczny sposób, który pozwoli w przyszłości
zarządzać innym NoSQL-owymi bazami.
Na ten moment zaimplementowane zostasły tworzenie nowej kolekcji, dodawanie dokumentów, oraz ich usuwanie. Aplikacja jest uruchamiana w terminalu. 
W najbliższym czasie mam również zamiar dodać inne funkcjonalności związane przede wszystkim z przeszukiwaniem bazy oraz potencjalnym wykorzystaniem jej do zagadnień związanych z ML.
Mimo tego, że aplikacja jest polskojęzyczna, to jej dokumentacja jest tworzona w języku angielskim.

Domyślnie aplikacja traktuje podawane wartości jako ciągi znaków, jednak jeśli zależy nam na jakimś konkretniejszym typie danych możemy go wpisać tak jakby to był kod w pythonie. Należy jednak upewnić się, czy pymongo potrafi przetworzyć dany typ danych (np. nie radzi sobie z typem date, ale datetime już obsługuje). W takim przypadku jeśli chcemy przekazać również ciąg znakó, należy jawnie go zapisać w cudzysłowiu, np. chcemy przekazać słownik, w którym klucze są ciągami znaków, a wartości mają różne typy: {"1":datetime(2023,1,1), "a":['abb', 1, 'aes', '2', datetime(1000,1,1)]}. Jeśli w podanym przykładzie napiszemy abb, zamiast 'abb' lub "abb", to kod będzie automatycznie szukał zmiennej abb wewnątrz kodu.

Aplikacja dalej jest w trakcie rozwoju. Planuję dodać do niej jeszcze możliwości przeszukiwania bazy oraz agregacji danych, a w przyszłości może rónież stworzyć na jej podstawie aplikację okienkową
## EN 
# License
The following application is released under the terms of the Apache 2.0 license

# Operation
The application is used to manage the data collected in the MongoDB database that pertains to my breeding of terrarium animals. Nevertheless, I try to create it in a rather flexible way, which will allow in the future to
manage other NoSQL databases.
At the moment, the creation of a new collection, adding documents, and deleting them have been implemented. The application is run in a terminal. 
In the near future I also intend to add other functionalities related primarily to searching the database and its potential use for ML issues.
Despite the fact that the application is Polish-language, its documentation is created in English.

By default, the application treats the given values as strings, but if you want a more specific data type, you can type it as if it were python code. However, you should make sure that pymongo can process the given data type (e.g. it cannot handle the date type, but datetime does). In that case, if you want to pass a string as well, you should explicitly enclose it in quotes, e.g. you want to pass a dictionary where the keys are strings and the values have different types: {‘1’:datetime(2023,1,1), ‘a’:[‘abb’, 1, ‘aes’, ‘2’, datetime(1000,1,1)]}. If we write abb in the example given, instead of ‘abb’ or ‘abb’, the code will automatically look for the variable abb inside the code.

The application is still under development. I plan to add database search and data aggregation capabilities to it, and in the future I may also create a window application based on it.

Translated with DeepL.com (free version)
Translated with DeepL.com (free version)

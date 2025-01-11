# Frontend API

## Uruchamianie

W głównym katalogu należy umieścić plik o nazwie '.github_token', który zawiera token autoryzacyjny do GitHub.
Jest to wymagane, aby wszystkie zmienne, które nie mogą być publiczne zostały odczytane z prywatnego repozytorium.

Zmienne środowiskowe dotyczące konfiguracji połączeń z innymi kontenerami znajdują się w pliku compose.yaml w sekcji 'Environments'

### Uruchomienie compose: 
W celu umożliwienia współpracy z bazami danych, warstwą prezentacji oraz usługą zajmującą się kontrolą cen aktywów, należy uruchomić następujące polecenia:

#### Budowanie compose

```commandline
    docker compose build
```

#### Uruchomienie compose

```commandline
    docker compose up -d
```

#### Zatrzymanie compose
Jeśli compose ma usunąć dane zawarte w bazach danych: 

```commandline
    docker compose down -v
```

W przypadku zachowywania danych pomijamy flagę -v.

## Dokumentacja API
[Dokumentacja](https://github.com/THD-C/Frontend_API/blob/main/THD(C)%20API.pdf)

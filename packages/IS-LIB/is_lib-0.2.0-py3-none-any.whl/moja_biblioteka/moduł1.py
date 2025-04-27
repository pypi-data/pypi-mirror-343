def login_req(func):
    def wrapper(*args, **kwargs):  # Obsługuje argumenty funkcji
        print("Chyba działa!")
        result = func(*args, **kwargs)  # Wywołanie oryginalnej funkcji
        print("Koniec")
        return result  # Zwróć wynik oryginalnej funkcji
    return wrapper
from random import randint

if __name__ == '__main__':
    # Générer le chiffre à trouver
    secret = randint(0, 100)
    print(secret)

    # Faire un boucle
    while True:
        # Demander un chiffre à l'utilisateur
        guess = int(input("Donnez un chiffre entre 0 et 100: "))
        print(guess)

        # Valider le chiffre
        # Afficher le résultat
        # Sortir ou Re commencer la bouche
        if guess > secret:
            print("C'est moins !")
        elif guess < secret:
            print("C'est plus !")
        else:
            print("C'est trouvé !")
            break

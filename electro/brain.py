def brain(cars1, cars2):
    a=max(cars1,cars2);
    tol=5
    if(a>tol):
        return min(a,10)*1000#entre deux valeurs
    else:
        return 2000
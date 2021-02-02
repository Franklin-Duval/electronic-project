def brain(P1,P2,P3,P4):
    #P1,P2,P3,P4 representent les pressions sur les differentes voies
    a=max(P1,P2)
    tol=5
    if(a>tol):
        return min(a,9)#entre deux valeurs
    else:
        return 4
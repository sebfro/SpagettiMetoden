module position




subroutine movefish

do l = 1, nfisn
  Xdir = x1-X(l)
  Ydir = Y1-X(l)
    # Swim against target, speed = 0.1 m/s
    Norm = sqrt(Xdir**2 + Ydir**2)
    Udir = 0.1 * mEW * Xdir / Norm
    Vdir = 0.1 * mNS * Ydir / Norm
    
    # Random component
    Urand = ...
    Vrand = ...

    # New position
    Xnew = X(l) + (Udir + Urand)*dt  
    Ynew = Y(l) + (Vdir + Vrand)*dt  





end subroutine movefish



end module position

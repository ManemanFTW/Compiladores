1 REM Este test si se puede hacer bien en BASIC
2 FOR A1 = 1 TO 5 STEP 1
3 IF A1 = 2 THEN 4
4 LET RES = 8
5 IF A1 = 3 THEN 6
6 LET RES = 10
7 NEXT A1
8 READ RES
9 PRINT "La variable res en este caso no esta en el scope correcto"
10 END
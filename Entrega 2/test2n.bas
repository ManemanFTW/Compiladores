1 REM El lenguaje BASIC no tiene clases, pero...
2 PRINT "Lo equivalente sseria hacer algun ciclo con una variable no declarada"
3 REM Asi que lo que hare sera lo siguiente
4 IF Y = 3 THEN 8
5 LET X = 2
6 PRINT "En este caso, se hace un for con una variable que no esta presente"
8 REM Tambien puede aplicar el mandar un goto a una linea que no existe
9 READ Q1
10 DATA 9
11 FOR Q2 = 1 TO 3 STEP 1
12 IF Q2 = 2 THEN 15
13 NEXT Q2
14 END
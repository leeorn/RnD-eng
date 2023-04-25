run: tests
	./Nehardea-Leeor

tests: test/tests.o
	g++ test/tests.o -o Nehardea-Leeor

test/tests.o: test/tests.cpp
	g++ -Iinclude -c test/tests.cpp -o test/tests.o
	
clean:
	rm -f *.o test/*.o Nehardea-Leeor
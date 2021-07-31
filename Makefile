metadata.so: metadata.c
	gcc -fPIC -shared -o ./Parser/metadata.so ./Parser/metadata.c

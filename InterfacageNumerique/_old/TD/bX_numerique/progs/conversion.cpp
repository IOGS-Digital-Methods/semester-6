#include <iostream>
#include <iomanip>

void intToBytes(int number) {
    const int numBytes = sizeof(int);

	printf("0x  ");
    for (int i = numBytes-1; i >= 0; --i) {
        unsigned char byte = (number >> (i * 8)) & 0xFF;
		if(byte < 10)	printf("0");
		printf("%x ", byte);
    }
	printf("\n");
}

void floatToBytes(float number) {
	unsigned char* bytePtr = reinterpret_cast<unsigned char*>(&number);

	printf("0x  ");
    for (size_t i = 0; i < sizeof(float); ++i) {
		unsigned char byte = static_cast<char>(bytePtr[i]);
		if(byte < 10)	printf("0");
		printf("%x ", byte);
    }
	
	printf("\n");
}

int main() {
    int iNumber = 128;
    float fNumber = 3.1418;
    printf("Integer : %d\n", iNumber);
    intToBytes(iNumber);
	
	printf("Float : %f\n", fNumber);
    floatToBytes(fNumber);
		
	char c = fNumber;
	printf("\t %x \n", c);
	
    return 0;
}
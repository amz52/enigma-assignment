Aaron Zehm
amz52
CS475
Assignment2

Design:
Breaking this assignment up was imperative due to the many sequential parts. There scrambling and arranging of the
message along with the encrypting and decrypting of the message. The shifting of the wheels was also made as a separate
function. I chose to use a text interface for simplicity and utilized error handling through out the text interface so
that the program wouldn't crash if incorrect characters were used. A significant change to the design of the offset was
to use the index rather than the value of the alphabet and numbers because it removed a step for converting and was
easier to understand. Code design abides by PEP8 and was coded in Python because that is the language I am most
experienced in.

Test Plan & Report:
This assignment took me many many hours due to not fully understanding the encryption and decryption process. I had
overlooked the offset of the wheels and had originally thought the offset only affected the character going into the
wheel. Once I understood fully how the encryption and decryption methods worked I verified the results of my processes
by hand on paper. Utilizing the example of CCI from the lecture acted as the baseline and with each successful step a
more complicated message was tested. Starting from a message of 10 characters or less, the wheels starting at the 0 0 0
indexes, and the config being sequential. This allowed for easier debugging and incrementing each function.

How To Use:
Choose one of the options to begin via correlated number. Following the prompts, the config string will only accept an
int of ten numbers with no duplicating digits. Then the wheel indexes will be prompted. Instead entering A you would
enter 0, for Z it would be 25, and for 5 it would 31. Lastly, enter your message with no spaces and only alphanumeric
characters otherwise you'll be prompted again. Depending on which option you chose your message will then be encrypted
or decrypted.
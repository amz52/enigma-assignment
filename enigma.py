# Created by Aaron Zehm for CS475 Drexel University
import sys


class Enigma:
    def __init__(self):
        """Declares variables to give value and appease PEP8. The exception being the options dictionary."""
        self.config = 0
        self.counter = None
        self.message = None
        self.wheel_config = []
        self.options = {
            "1": self.encryption,
            "2": self.decryption,
            "3": self.exit,
        }

    @staticmethod
    # The UI for the user
    def display_options():
        print("""
        Enigma V2 Options
        Are you encrypting or decrypting a message?
        Enter the number associated with the option.
        
        1. Encryption
        2. Decryption
        3. Exit        
        
        """)

    # The wiring of the rotors stored as a list of lists. 36 offsets with each offset being the transformed character.
    # So if offset 0 and encryption is selected then A would change to 3. If it was decryption then it would be 3 to A.
    @staticmethod
    def right_rotor():
        wiring = [['A', '3'], ['B', '5'], ['C', 'H'], ['D', 'E'], ['E', 'F'], ['F', 'G'], ['G', 'D'], ['H', 'Q'],
                  ['I', '8'], ['J', 'M'], ['K', '2'], ['L', 'K'], ['M', 'L'], ['N', 'J'], ['O', 'N'], ['P', 'S'],
                  ['Q', 'U'], ['R', 'W'], ['S', 'O'], ['T', 'V'], ['U', 'R'], ['V', 'X'], ['W', 'Z'], ['X', 'C'],
                  ['Y', 'I'], ['Z', '9'], ['0', 'T'], ['1', '7'], ['2', 'B'], ['3', 'P'], ['4', 'A'], ['5', '0'],
                  ['6', '1'], ['7', 'Y'], ['8', '6'], ['9', '4']]
        return wiring

    @staticmethod
    def mid_rotor():
        wiring = [['A', '0'], ['B', 'L'], ['C', 'X'], ['D', '1'], ['E', '2'], ['F', '8'], ['G', 'H'], ['H', 'B'],
                  ['I', '3'], ['J', 'N'], ['K', 'R'], ['L', 'O'], ['M', 'K'], ['N', 'D'], ['O', 'T'], ['P', '7'],
                  ['Q', 'C'], ['R', '6'], ['S', 'P'], ['T', 'I'], ['U', 'V'], ['V', 'J'], ['W', '4'], ['X', 'A'],
                  ['Y', 'U'], ['Z', 'W'], ['0', 'M'], ['1', 'E'], ['2', '9'], ['3', '5'], ['4', 'Q'], ['5', 'S'],
                  ['6', 'Z'], ['7', 'G'], ['8', 'Y'], ['9', 'F']]
        return wiring

    @staticmethod
    def left_rotor():
        wiring = [['A', '2'], ['B', 'Y'], ['C', 'Z'], ['D', '0'], ['E', '1'], ['F', 'A'], ['G', 'W'], ['H', 'I'],
                  ['I', 'P'], ['J', 'K'], ['K', 'S'], ['L', 'N'], ['M', '3'], ['N', 'T'], ['O', 'E'], ['P', 'R'],
                  ['Q', 'M'], ['R', 'U'], ['S', 'C'], ['T', '5'], ['U', 'V'], ['V', '6'], ['W', 'X'], ['X', '7'],
                  ['Y', 'F'], ['Z', 'Q'], ['0', 'O'], ['1', 'L'], ['2', '4'], ['3', '8'], ['4', 'G'], ['5', 'D'],
                  ['6', '9'], ['7', 'B'], ['8', 'J'], ['9', 'H']]
        return wiring

    # The starting function for running the menu.
    def run(self):
        print('Welcome to the Enigma V2 Program')
        while True:
            self.display_options()
            option = input('Enter an option: ')
            selection = self.options.get(option)
            if selection:
                selection()
            else:
                print('{0} is not a valid option'.format(selection))

    def settings(self):
        """
        Once encryption or decryption is selected this function takes in and records the settings of the Enigma
        machine. There simple error handling to allow for only acceptable answers otherwise the user is prompted
        again. The settings take in first the numeric config string that is 10 digits long and uses each digit once
        e.g. 0123456789 which scrambles or arranges the messages by blocks of 10 characters. Next is the wheel
        offsets which can only be 3 numbers between 0 and 35. Finally, you are prompted with a message to encrypt or
        decrypt with no spaces.
        """
        self.config = 0
        self.wheel_config = []
        while True:
            try:
                while len(str(self.config)) != 10:
                    self.config = input('Please enter a valid config string: ')
                    for n in list(str(self.config)):
                        if self.config.count(n) > 1:
                            self.config = 0
                            break
                break
            except ValueError:
                print('That\'s not a number, please try again.')
                continue

        while True:
            try:
                while len(self.wheel_config) < 3:
                    if len(self.wheel_config) == 0:
                        index = int(input('Please enter the wheel index for the left wheel: '))
                        if 0 <= index <= 35:
                            self.wheel_config.append(index)
                        else:
                            continue
                    if len(self.wheel_config) == 1:
                        index = int(input('Please enter the wheel index for the middle wheel: '))
                        if 0 <= index <= 35:
                            self.wheel_config.append(index)
                        else:
                            continue
                    if len(self.wheel_config) == 2:
                        index = int(input('Please enter the wheel index for the right wheel: '))
                        if 0 <= index <= 35:
                            self.wheel_config.append(index)
                        else:
                            continue
                break

            except ValueError:
                print('That\'s not a number, please try again.')
                continue

        self.message = input('Please enter your alphanumeric message: ')
        while self.message.isalnum() is False:
            self.message = input('Please enter your alphanumeric message: ')

    def scramble(self):
        """
        scramble() function occurs before the encryption method where the message is broken into blocks of 10
        characters and rearranged. If the numeric config string is set to 0123456789 then the message is not
        scrambled. If the string is 9876543210 then the message is reversed. Essentially, each digit represents the
        place the ordered character will be moved to.
        """
        transposed = []
        while len(self.message) % 10 != 0:
            self.message += 'x'
        blocks = [self.message[i:i + 10] for i in range(0, len(self.message), 10)]
        indices = [int(d) for d in str(self.config)]
        for block in blocks:
            bits = list(block)
            transposed.append([bits[i] for i in indices])
        transposed = [''.join(x) for x in transposed]
        self.message = list(''.join(transposed))

    def arrange(self):
        """
        arrange() does the opposite of scramble. It reorders the jumbled characters into their original order. This
        was a bit more tricky than scrambling because I wanted to iterate over both the indexes and bits without
        overwriting either so the zip() function allowed me to iterate over both simultaneously.
        """
        transposed = [None, None, None, None, None, None, None, None, None, None]
        transposed_message = []
        blocks = [self.message[i:i + 10] for i in range(0, len(self.message), 10)]
        indices = [int(d) for d in str(self.config)]
        for block in blocks:
            bits = list(block)
            for index, char in zip(indices, bits):
                transposed[index] = char
            transposed_message += transposed
        transposed_message = [''.join(x) for x in transposed_message]
        self.message = ''.join(transposed_message)

    def shift(self, char):
        """
        This shift() method changes the offset of the wheel with each character entered. The right wheel increases by
        one for each character. The middle wheel increases by one for 7 characters entered. the left wheel increases by
        one for 5 characters entered. Offset shifts before the character is entered into the machine. So if the offset
        set in the config is 0 0 35 then the first character will go in with the offset 0 0 0.
        """
        print('Entering {}'.format(char.upper()))
        previous = self.wheel_config[2]
        self.wheel_config[2] += 1
        if self.wheel_config[2] == 36:
            self.wheel_config[2] = 0
        print('\nRotating right rotor from {} to {}'.format(previous, self.wheel_config[2]))
        if self.counter % 7 == 0 and self.counter != 0:
            previous = self.wheel_config[1]
            self.wheel_config[1] += 1
            if self.wheel_config[1] == 36:
                self.wheel_config[1] = 0
            print('Rotating middle rotor from {} to {}'.format(previous, self.wheel_config[1]))
        if self.counter % 5 == 0 and self.counter != 0:
            previous = self.wheel_config[0]
            self.wheel_config[0] += 1
            if self.wheel_config[0] == 36:
                self.wheel_config[0] = 0
            print('Rotating left rotor from {} to {}'.format(previous, self.wheel_config[0]))
        self.counter += 1

    def encrypt(self):
        """
        The encrypt() method is one of the heavy lifting methods besides decrypt(). I realize it could be broken down
        into smaller functions but it was easier initially to iterate through each character(bit) and make the changes
        within the loop.
        """
        encrypted = ''
        self.counter = 0
        shifted_right_out = None
        shifted_mid_out = None
        shifted_left_out = None
        cipher = None

        # Begin looping through a block
        for character in self.message:
            # shift is called to increment the wheels
            self.shift(character)
            # Scroll through all of the characters in the right rotor
            for index in self.right_rotor():
                if character.upper() == index[0]:
                    # Calculates the offset for the character entered. Grabs the index of the matched character and adds
                    # the offset of mod 36.
                    shifted_right_in = (self.right_rotor().index(index) + self.wheel_config[2]) % 36
                    # The character selected on the wheel of the rotor.
                    right_in = self.right_rotor()[shifted_right_in][0]
                    # The character that has been transformed and comes out of the wheel
                    right_out = self.right_rotor()[shifted_right_in][1]
                    # Scroll through the other side of the rotor
                    for index_out in self.right_rotor():
                        if right_out == index_out[0]:
                            # Calculates the offset of the character leaving the rotor
                            shifted_right_out = (self.right_rotor().index(index_out) - self.wheel_config[2]) % 36
                            break
                    # The produced encrypted character from this rotor
                    cipher = self.right_rotor()[shifted_right_out][0]
                    # prints out the progression of the character entered and how each step altered it.
                    print('Right rotor: {} shifts by {} to {}, {} converts to {}, {} shifts by -{} and encrypts as {}'
                          .format(character.upper(), self.wheel_config[2], right_in, right_in, right_out, right_out,
                                  self.wheel_config[2], cipher))
                    break
            # As done previously with the right rotor computation is now completed with the middle rotor
            for index in self.mid_rotor():
                if cipher == index[0]:
                    previous_cipher = cipher
                    shifted_mid_in = (self.mid_rotor().index(index) + self.wheel_config[1]) % 36
                    mid_in = self.mid_rotor()[shifted_mid_in][0]
                    mid_out = self.mid_rotor()[shifted_mid_in][1]
                    for index_out in self.mid_rotor():
                        if mid_out == index_out[0]:
                            shifted_mid_out = (self.mid_rotor().index(index_out) - self.wheel_config[1]) % 36
                            break
                    cipher = self.mid_rotor()[shifted_mid_out][0]
                    print('Middle rotor: {} shifts by {} to {}, {} converts to {}, {} shifts by -{} and encrypts as {}'
                          .format(previous_cipher, self.wheel_config[1], mid_in, mid_in, mid_out, mid_out,
                                  self.wheel_config[1], cipher))
                    break
            # Finally, the left rotor encryption is computed.
            for index in self.left_rotor():
                if cipher == index[0]:
                    previous_cipher = cipher
                    shifted_left_in = (self.left_rotor().index(index) + self.wheel_config[0]) % 36
                    left_in = self.left_rotor()[shifted_left_in][0]
                    left_out = self.left_rotor()[shifted_left_in][1]
                    for index_out in self.left_rotor():
                        if left_out == index_out[0]:
                            shifted_left_out = (self.left_rotor().index(index_out) - self.wheel_config[0]) % 36
                            break
                    cipher = self.left_rotor()[shifted_left_out][0]
                    print('Left rotor: {} shifts by {} to {}, {} converts to {}, {} shifts by -{} and encrypts as {}'
                          .format(previous_cipher, self.wheel_config[0], left_in, left_in, left_out, left_out,
                                  self.wheel_config[0], cipher))
                    break
            encrypted = encrypted + cipher
            print('\nEncrypted message so far: {}'.format(encrypted))
        self.message = encrypted

    def decrypt(self):
        """
        Decrypts messages created from the encryption method. Works in the reverse order of encrypt(). Starting with the
        left rotor and working to middle then right rotor.
        """
        decrypted = ''
        self.counter = 0
        shifted_right_out = None
        shifted_mid_out = None
        shifted_left_out = None
        cipher = None

        for character in self.message:
            self.shift(character)
            for index in self.left_rotor():
                if character.upper() == index[0]:
                    shifted_left_in = (self.left_rotor().index(index) + self.wheel_config[0]) % 36
                    left_in = self.left_rotor()[shifted_left_in][0]
                    convert = [index for index in self.left_rotor() if left_in == index[1]]
                    left_out = convert[0][0]
                    for index_out in self.left_rotor():
                        if left_out == index_out[0]:
                            shifted_left_out = (self.left_rotor().index(index_out) - self.wheel_config[0]) % 36
                            break
                    cipher = self.left_rotor()[shifted_left_out][0]
                    print('Left rotor: {} shifts by {} to {}, {} converts to {}, {} shifts by -{} and decrypts as {}'
                          .format(character.upper(), self.wheel_config[0], left_in, left_in, left_out, left_out,
                                  self.wheel_config[0], cipher))
                    break

            for index in self.mid_rotor():
                if cipher == index[0]:
                    previous_cipher = cipher
                    shifted_mid_in = (self.mid_rotor().index(index) + self.wheel_config[1]) % 36
                    mid_in = self.mid_rotor()[shifted_mid_in][0]
                    convert = [index for index in self.mid_rotor() if mid_in == index[1]]
                    mid_out = convert[0][0]
                    for index_out in self.mid_rotor():
                        if mid_out == index_out[0]:
                            shifted_mid_out = (self.mid_rotor().index(index_out) - self.wheel_config[1]) % 36
                            break
                    cipher = self.mid_rotor()[shifted_mid_out][0]
                    print('Middle rotor: {} shifts by {} to {}, {} converts to {}, {} shifts by -{} and decrypts as {}'
                          .format(previous_cipher, self.wheel_config[1], mid_in, mid_in, mid_out, mid_out,
                                  self.wheel_config[1], cipher))
                    break

            for index in self.right_rotor():
                if cipher == index[0]:
                    previous_cipher = cipher
                    shifted_right_in = (self.right_rotor().index(index) + self.wheel_config[2]) % 36
                    right_in = self.right_rotor()[shifted_right_in][0]
                    convert = [index for index in self.right_rotor() if right_in == index[1]]
                    right_out = convert[0][0]
                    for index_out in self.right_rotor():
                        if right_out == index_out[0]:
                            shifted_right_out = (self.right_rotor().index(index_out) - self.wheel_config[2]) % 36
                            break
                    cipher = self.right_rotor()[shifted_right_out][0]
                    print('Right rotor: {} shifts by {} to {}, {} converts to {}, {} shifts by -{} and decrypts as {}'
                          .format(previous_cipher, self.wheel_config[2], right_in, right_in, right_out, right_out,
                                  self.wheel_config[2], cipher))
                    break
            decrypted = decrypted + cipher
            print('\nDecrypted message so far: {}'.format(decrypted))
        self.message = decrypted

    def encryption(self):
        """The method called in the options to initiate the encryption process"""
        print('\nEncryption Chosen')
        self.settings()
        self.scramble()
        self.encrypt()
        print('\nMessage encrypted to {}'.format(self.message))

    def decryption(self):
        """The method called in the options to initiate the decryption process"""
        print('\nDecryption Chosen')
        self.settings()
        self.decrypt()
        self.arrange()
        print('\nMessage decrypted to {}'.format(self.message))

    @staticmethod
    def exit():
        """Simple method to exit the program"""
        print('Good Bye!')
        sys.exit(0)


def main():
    Enigma().run()


if __name__ == "__main__":
    main()

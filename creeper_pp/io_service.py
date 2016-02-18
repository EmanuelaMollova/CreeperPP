import sys

class IoService(object):
    @classmethod
    def write_array_to_file(self, filename, array):
        with open(filename, 'w') as out:
            for word in array:
                if word.strip():                     #checks if word is not empty
                    out.write(word + '\n')

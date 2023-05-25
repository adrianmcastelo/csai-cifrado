import hashlib
import processing

def get_blocks(text, size):
    blocks = [text[i:i+size] for i in range(0, len(text)-size, size)]
    total_letters = len(text)
    total_got = len(blocks) * size
    value = total_letters-total_got
    last_block = text[-value:]
    return blocks,last_block


def get_columns(text_blocks):
    group_size = len(text_blocks[0])
    columns = []
    for letter_count in range(group_size):
        column = ''
        for group_count in range(len(text_blocks)):
            column += text_blocks[group_count][letter_count]
        columns.append(column)
    return columns

def get_columns_simple(text_block):
    return list(text_block)

def to_blocks(cols):
    col_size = len(cols[0])
    blocks = []
    for letter in range(col_size):
        block = ''
        for col in range(len(cols)):
            block += cols[col][letter]
        blocks.append(block)
    return blocks

def shift(text, amount, dictionary):
    shifted = ''
    for letter in text:
        shifted += dictionary[(dictionary.index(letter)-amount) % len(dictionary)]
    return shifted

# Simple text hashed based on sha256
def getHashFromText(text):
    h = hashlib.new("sha256",text.encode('utf-8'))
    return h.hexdigest()

def getFileContent(fileName):
    with open (fileName, "r") as file:
         text=file.read().replace('\n','')
         return text

def checkHash(originalHash, gotHash):
    return originalHash == gotHash

# decypher func, used on several methods of the app.
def decypher(cyphertext, key, dictionary):
    shifts = [dictionary.index(letter) for letter in key]
    blocks, last_block = processing.get_blocks(text=cyphertext,size=len(key))
    cols = processing.get_columns(blocks)
    decyphered_blocks = processing.to_blocks([processing.shift(col, shift, dictionary) for col, shift in zip(cols, shifts)])
    cols = processing.get_columns_simple(last_block)
    last_letter = processing.to_blocks([processing.shift(col, shift, dictionary) for col, shift in zip(cols, shifts)])
    decyphered = ''.join(decyphered_blocks)
    return decyphered + ''.join(last_letter)
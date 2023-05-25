import processing
import kasiski
from const import MAX_KEY_GUESS, spanish_dictionary, englise_french_dictionary

checkedES = []
checkedEN = []

def attackKasiski(ciphered, max_guess, hash):
    # Will guess best key length on range 0-max_guess
    key_len_es = kasiski.get_key_length(ciphered, spanish_dictionary, max_guess)
    key_len_en_fr = kasiski.get_key_length(ciphered, englise_french_dictionary, max_guess)

    if (key_len_es == 0 or key_len_en_fr == 0):
        return "",""
    # If the key_len returned was already tried to decrypt, skip
    if (key_len_es in checkedES or key_len_en_fr in checkedEN):
        return "",""
    checkedES.append(key_len_es)
    checkedEN.append(key_len_en_fr)

    keyEn = kasiski.get_key(ciphered.lower(),key_len_en_fr, englise_french_dictionary, "en")
    keyEn = keyEn.upper()
    decipheredEn = processing.decypher(ciphered, keyEn, englise_french_dictionary)
    if hash == processing.getHashFromText(decipheredEn):
        return keyEn, decipheredEn

    keyEs = kasiski.get_key(ciphered.lower(),key_len_es, spanish_dictionary, "es")
    keyEs = keyEs.upper()
    decipheredEs = processing.decypher(ciphered, keyEs, spanish_dictionary)
    if hash == processing.getHashFromText(decipheredEs):
        return keyEs, decipheredEs

    keyFr = kasiski.get_key(ciphered.lower(),key_len_en_fr, englise_french_dictionary, "fr")
    keyFr = keyFr.upper()
    decipheredFr = processing.decypher(ciphered, keyFr, englise_french_dictionary)
 
    return keyFr, decipheredFr

        
def crackText(ciphered, hash):
    key = ""
    decyphered = ""

    # Trying different key measures from 1 to MAX_KEY_GUESS
    for i in range(MAX_KEY_GUESS+1):
        key, decyphered = attackKasiski(ciphered, i+1, hash)
        if hash == processing.getHashFromText(decyphered):
            return key,decyphered

    # If no confirmed, return last key tried
    return key, decyphered
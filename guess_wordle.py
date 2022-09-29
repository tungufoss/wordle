# importing the collections module
import collections
from itertools import chain, combinations

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def all_subsets(ss):
    return list(chain(*map(lambda x: combinations(ss, x), range(0, len(ss)+1))))

def all_subsets_of_length(ss, length):
    return list([list(ss) for ss in all_subsets(ss) if len(ss)==length])

def intersect(lst1, lst2):
    return set([value for value in lst1 if value in lst2])

def contains_all(lst1,lst2):    
    return len(intersect(lst1,lst2))==len(set(lst2))

def contains_any(lst1,lst2):
    return len(intersect(lst1,lst2))>0

def letters_available(words):
    return set([letter for word in words for letter in word])

def letter_frequency(words, word_length):
    # intializing the arr
    arr = [letter for word in words for letter in word]
    # getting the elements frequencies using Counter class
    elements_count = collections.Counter(arr)
    
    freq_at_pos = []    
    for i in range(word_length):
        arr = [word[i] for word in words]
        freq_at_pos.append(collections.Counter(arr))
        
    return elements_count, freq_at_pos

def glance(d,length=3):
    return dict(list(d.items())[:length])

def order_dict(d):
    return dict(reversed(sorted(d.items(), key=lambda item: item[1])))

def read_language(language, word_length = 5):
    filename = f'data/{language.lower()}-len{word_length}.txt'    
    myfile = open(filename, 'r')
    words = [ list(str.strip(line)) for line in myfile.readlines() ]
    myfile.close() 
   
    letters = letters_available(words)
    print(f'\n{language}:')
    print(f'Total of {len(words)} with {len(letters)} letters available')        

    return words

def color_word(word, letter_at_pos, contains_letters):
    return "".join([(color.GREEN if letter == letter_at_pos[i] else color.YELLOW if letter in contains_letters else color.UNDERLINE) + letter + color.END for i,letter in enumerate(word) ])
 
def process(word_length, words, not_contains_letters = list(), letter_at_pos = [None,None,None,None,None], letters_not_at_pos = [[],[],[],[],[]], max_show = 20, print_out=True, must_contain = []):
    not_contains_letters = [letter.upper() for letter in not_contains_letters]
    letter_at_pos = [letter.upper() if letter is not None else None for letter in letter_at_pos ]
    letters_not_at_pos = [[letter.upper() for letter in letters] for letters in letters_not_at_pos ]
    assert len(letter_at_pos)==word_length
    assert len(letters_not_at_pos)==word_length
    assert type(must_contain)==list
    contains_letters = list(set([letter for letter in letter_at_pos if letter is not None] + [ letter for letters in letters_not_at_pos for letter in letters ] + must_contain))

    def print_info(words):
        all_letters = letters_available(words)
        letters = [ color_word(letter,letter_at_pos, contains_letters) for letter in sorted(all_letters)]    
        print(f'Eliminated down to {len(words)} words with {len(letters)} letters: {",".join(letters)}')    

    words = [word for word in words if not contains_any(word,not_contains_letters) and contains_all(word,contains_letters) ]
    
    if print_out: 
        print_info(words)
        
    for i in range(word_length):
        if letter_at_pos[i] is not None : 
            words = [word for word in words if word[i] == letter_at_pos[i]]
        elif len(letters_not_at_pos[i]) > 0 :
            words = [word for word in words if word[i] not in letters_not_at_pos[i]]           
            
    if print_out:
        print_info(words)
            
    overall_freq, positional_freq  = letter_frequency(words,word_length)
    def freq_word(word):
        overall = sum([overall_freq[letter] for letter in set(word)])
        positional = sum([positional_freq[ix][letter] for ix,letter in enumerate(list(word))])
        required = sum([overall_freq[letter] for letter in set(word) if letter in must_contain])
        return (overall, positional, required)
    values = order_dict({ "".join(word): freq_word(word) for word in words })
        
    if print_out:
        print("\n".join([f'{color_word(key, letter_at_pos, contains_letters)}\t{value}' for key,value in glance(values, max_show).items()]))    
        if(len(values)>max_show):
            print(f'\ttruncated {len(values)-max_show} values')
    
    return values, overall_freq, positional_freq

def candidate_words(letters, word_length, words):
    complement = dict()
    for i in reversed(range(1,min(word_length,len(letters))+1)):
        subsets = all_subsets_of_length(set(letters),i)        
        for subset in subsets:            
            aux, aux_freq_overall, aux_freq_pos = process(word_length, words, max_show=1, print_out=False, must_contain=subset)            
            if len(aux)>0:                
                aux_word = list(aux.keys())[0]
                complement[aux_word] = aux[aux_word]                
        
        if len(complement) > 0:            
            break     
    complement = order_dict(complement)    
    return complement

def complement_words(word_length, words, not_contains_letters, letter_at_pos, letters_not_at_pos):
    candidates = dict()
    complement = dict()
    for word, value in words.items():
        for i in reversed(range(1,word_length+1)):
            subsets = all_subsets_of_length(set(list(word)),i)
            for subset in subsets:                
                aux, aux_freq_overall, aux_freq_pos = process(word_length, words, set(not_contains_letters+subset), letter_at_pos, letters_not_at_pos, 1, print_out=False)
                if len(aux)>0:                
                    aux_word = list(aux.keys())[0]
                    complement[aux_word] = aux[aux_word]
            if len(complement) > 0:
                complement = order_dict(complement)
                break 
        if len(complement)>0:
            complement_word = list(complement.keys())[0]
            value = (value[0]+complement[complement_word][0] , value[1]+complement[complement_word][1])
            candidates[word] = (value, complement_word)
    return order_dict(candidates)

def wordle():
    # https://www.powerlanguage.co.uk/wordle/
    process('EN', 5,
        not_contains_letters=[],
        letter_at_pos = [None,None,None,None,None],
        letters_not_at_pos = [[],[],[],[],[]]
    )

def ordla(lang='IS',word_length=5): 
    # https://torfbaer.itch.io/ordla?secret=tAAEeMtlFSHv4FJo8eTn6cfyd2M
    process(lang,word_length,
        not_contains_letters=[],
        letter_at_pos = [None,None,None,None,None],
        letters_not_at_pos = [[],[],[],[],[]]
    )

def absurdle(lang='EN', word_length=5, max_show=25):
    # https://qntm.org/files/wordle/index.html
    not_contains_letters=['A','R','O','S','U','T','N','C']
    letter_at_pos = ['W',None,'I','L','E']
    letters_not_at_pos = [[],['E'],[],[],['H']]
    all_words = read_language(lang, word_length)
    words, freq_overall, freq_positional = process(word_length, all_words, not_contains_letters, letter_at_pos, letters_not_at_pos, max_show, print_out=True)
    candidates = complement_words(word_length, glance(words,15), not_contains_letters, letter_at_pos, letters_not_at_pos)
    print("\n".join([ f'{key}+{value[1]}={value[0]}' for key,value in candidates.items()]))
    
    
    print('Illegal words with additional information:')
    unknowns = dict()
    for i in range(word_length):
        possibilities_at_pos = freq_positional[i].keys()        
        if len(possibilities_at_pos)==1:            
            letter_at_pos[i]=list(possibilities_at_pos)[0]
        else : 
            for key in freq_positional[i].keys():
                if key not in unknowns:
                    unknowns[key]=freq_overall[key]
    unknowns = order_dict(unknowns)
    print(unknowns,len(unknowns))
    unknowns = list(unknowns.keys())[0:10]
    words = candidate_words(unknowns, word_length, all_words)
    words = glance(words,10)
    print('\n'.join([f'{color_word(word, letter_at_pos, unknowns)}: {value}' for word,value in words.items()]))
            
absurdle()
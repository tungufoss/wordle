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

def letter_frequency(words):
    # intializing the arr
    arr = [letter for word in words for letter in word]
    # getting the elements frequencies using Counter class
    elements_count = collections.Counter(arr)    
    return elements_count

def glance(d,length=3):
    return dict(list(d.items())[:length])

def order_dict(d):
    return dict(reversed(sorted(d.items(), key=lambda item: item[1])))

def process(language, word_length = 5,  not_contains_letters = list(), letter_at_pos = [None,None,None,None,None], letters_not_at_pos = [[],[],[],[],[]], max_show = 20, print_out=True, must_contain = []):
    not_contains_letters = [letter.upper() for letter in not_contains_letters]
    letter_at_pos = [letter.upper() if letter is not None else None for letter in letter_at_pos ]
    letters_not_at_pos = [[letter.upper() for letter in letters] for letters in letters_not_at_pos ]
    assert len(letter_at_pos)==word_length
    assert len(letters_not_at_pos)==word_length
    assert type(must_contain)==list
    contains_letters = list(set([letter for letter in letter_at_pos if letter is not None] + [ letter for letters in letters_not_at_pos for letter in letters ] + must_contain))

    def color_word(word):
        return "".join([(color.GREEN if letter in letter_at_pos else color.YELLOW if letter in contains_letters else color.UNDERLINE) + letter + color.END for letter in word ])

    def print_info(words):
        all_letters = letters_available(words)
        letters = [ color_word(letter) for letter in sorted(all_letters)]    
        print(f'Eliminated down to {len(words)} words with {len(letters)} letters: {",".join(letters)}')
                
    filename = f'data/{language.lower()}-len{word_length}.txt'    
    myfile = open(filename, 'r')
    all_words = [ list(str.strip(line)) for line in myfile.readlines() ]
    myfile.close() 
    letters = letters_available(all_words)
    words = [word for word in all_words if not contains_any(word,not_contains_letters) and contains_all(word,contains_letters) ]
    
    if print_out: 
        print(f'\n{language}:')
        print(f'Total of {len(all_words)} with {len(letters)} letters available')        
        print_info(words)
        
    for i in range(word_length):
        if letter_at_pos[i] is not None : 
            words = [word for word in words if word[i] == letter_at_pos[i]]
        elif len(letters_not_at_pos[i]) > 0 :
            words = [word for word in words if word[i] not in letters_not_at_pos[i]]           
            
    if print_out:
        print_info(words)
            
    freq = letter_frequency(words)
    def freq_word(word):
        return sum([freq[letter] for letter in set(word)])
    values = order_dict({ "".join(word): freq_word(word) for word in words })
    
    if print_out:
        print("\n".join([f'{color_word(key)}\t{value}' for key,value in glance(values, max_show).items()]))    
        if(len(values)>max_show):
            print(f'\ttruncated {len(values)-max_show} values')
    
    return glance(values,max_show)

def wordle():
    # https://www.powerlanguage.co.uk/wordle/
    process('EN', 5,
        not_contains_letters=[],
        letter_at_pos = [None,None,None,None,None],
        letters_not_at_pos = [[],[],[],[],[]]
    )

def ordla(): 
    # https://torfbaer.itch.io/ordla?secret=tAAEeMtlFSHv4FJo8eTn6cfyd2M
    process('IS', 5,
        not_contains_letters=[],
        letter_at_pos = [None,None,None,None,None],
        letters_not_at_pos = [[],[],[],[],[]]
    )

def absurdle(lang='EN', word_length=5, max_show=15):
    # https://qntm.org/files/wordle/index.html
    not_contains_letters=[]
    letter_at_pos = [None,None,None,None,None]
    letters_not_at_pos = [[],[],[],[],[]]
    words = process(lang, word_length,not_contains_letters, letter_at_pos, letters_not_at_pos, max_show, print_out=True)
    candidates = dict()
    complement = dict()
    for word, value in words.items():
        for i in reversed(range(1,word_length+1)):            
            subsets = all_subsets_of_length(set(list(word)),i)            
            for subset in subsets:
                aux = process(lang, word_length,set(not_contains_letters+subset), letter_at_pos, letters_not_at_pos, 1, print_out=False)
                if len(aux)>0:
                    aux_word = list(aux.keys())[0]
                    complement[aux_word] = aux[aux_word]                    
            if len(complement) > 0:
                complement = order_dict(complement)
                break 
        
        complement_word = list(complement.keys())[0]
        value += complement[complement_word]
        candidates[word] = (value, complement_word)    
    candidates = order_dict(candidates)
    print("\n".join([ f'{key}+{value[1]}={value[0]}' for key,value in candidates.items()]))
    
    #x = process(lang, word_length, max_show=10, print_out=False, must_contain=['C','D','F'])
    #print(x)
    
    
        
absurdle()
# importing the collections module
import collections
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


def process(language, word_length = 5,  not_contains_letters = list(), letter_at_pos = [None,None,None,None,None], letters_not_at_pos = [[],[],[],[],[]], max_show = 20):  
    not_contains_letters = [letter.upper() for letter in not_contains_letters]
    letter_at_pos = [letter.upper() if letter is not None else None for letter in letter_at_pos ]
    letters_not_at_pos = [[letter.upper() for letter in letters] for letters in letters_not_at_pos ]
    assert len(letter_at_pos)==word_length
    assert len(letters_not_at_pos)==word_length
    contains_letters = [letter for letter in letter_at_pos if letter is not None] + [ letter for letters in letters_not_at_pos for letter in letters ]

    def color_word(word):
        return "".join([(color.GREEN if letter in letter_at_pos else color.YELLOW if letter in contains_letters else color.UNDERLINE) + letter + color.END for letter in word ])

    def print_info(words):
        all_letters = letters_available(words)
        letters = [ color_word(letter) for letter in sorted(all_letters)]    
        print(f'Eliminated down to {len(words)} words with {len(letters)} letters: {",".join(letters)}')
                
    filename = f'data/{language.lower()}-len{word_length}.txt'
    print(f'\n{language}:')
    myfile = open(filename, 'r')
    all_words = [ list(str.strip(line)) for line in myfile.readlines() ]
    myfile.close() 
    letters = letters_available(all_words)
    print(f'Total of {len(all_words)} with {len(letters)} letters available')        
    
    words = [word for word in all_words if not contains_any(word,not_contains_letters) and contains_all(word,contains_letters) ]
    print_info(words)
        
    for i in range(word_length):
        if letter_at_pos[i] is not None : 
            words = [word for word in words if word[i] == letter_at_pos[i]]
        elif len(letters_not_at_pos[i]) > 0 :
            words = [word for word in words if word[i] not in letters_not_at_pos[i]]           
            
    print_info(words)
            
    freq = letter_frequency(words)
    def freq_word(word):
        return sum([freq[letter] for letter in set(word)])
    values = { "".join(word): freq_word(word) for word in words }    
    values = dict(reversed(sorted(values.items(), key=lambda item: item[1])))    
    print("\n".join([f'{color_word(key)}\t{value}' for key,value in glance(values, max_show).items()]))    
    if(len(values)>max_show):
        print(f'\ttruncated {len(values)-max_show} values')

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

def absurdle():
    # https://qntm.org/files/wordle/index.html
    process('EN', 7,
        not_contains_letters=[],
        letter_at_pos = [None,None,None,None,None,None,None],
        letters_not_at_pos = [[],[],[],[],[],[],[]]
    )
    
wordle()
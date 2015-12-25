#Ethan Sterling
#Python 3.3
#2/11/2015

from string import ascii_lowercase;
import random;
import urllib.request;

#def randomLetter():
#    return randomFrom(ascii_lowercase);
scrabble_letters = ('a'*9 + 'b'*2 + 'c'*2 + 'd'*4 + 'e'*12 + 'f'*2 +
                    'g'*3 + 'h'*2 + 'i'*9 + 'j'*1 + 'k'*1  + 'l'*4 +
                    'm'*2 + 'n'*6 + 'o'*8 + 'p'*2 + 'q'*1  + 'r'*6 +
                    's'*4 + 't'*6 + 'u'*4 + 'v'*2 + 'w'*2  + 'x'*1 +
                    'y'*2 + 'z'*1);
def randomScrabbleFrequencyLetter(): #For building random Boggle boards.
    return randomFrom(scrabble_letters);
def randomFrom(L):
    return L[random.randrange(0,len(L))];

class Boggle():
    "A Boggle set which treats q and u as separate letters."
    def __init__(self, board = None):
        if board == None:
            self.setRandomBoard(4, 4, randomScrabbleFrequencyLetter);
        else:
            self.board = board;
            self.wrapBoard();
        
    def setRandomBoard(self, x, y, Rletter = randomScrabbleFrequencyLetter):
        self.board = [[Rletter() for i in range(x)]
                                 for j in range(y)];
        self.wrapBoard();
    def wrapBoard(self):
        "Bounds the board in empty strings."
        x,y = len(self.board), len(self.board[0]);
        wrapped_board = [['']*(y+2)]
        wrapped_board.extend([[''] + row + [''] for row in self.board]);
        wrapped_board.append(['']*(y+2));  #Wraps board
        self.board = wrapped_board;
        
    def show(self):
        print("\n".join(" ".join(row) for row in self.board));

    def adj(self, tile):
        "Returns the (x,y) coordinates of all tiles adjacent to tile."
        x,y = tile;
        return ((x-1,y-1), (x-1,y), (x-1,y+1),
                (x,  y-1),          (x,  y+1),
                (x+1,y-1), (x+1,y), (x+1,y+1));
        
    def allwords(self, dictroot): #Give it a default dictionary?
        "Returns a set of all dictionary words on the board."
        #Start from every non-border tile
        return {letter + word
                for r,row in enumerate(self.board[1:-1])
                for c,letter in enumerate(row[1:-1])
                if letter in dictroot
                for word in self.search(dictroot[letter],
                                    (r+1, c+1), {letter})};

    def allBoggleWords(self, dictroot, minimum_length = 3):
        "Returns a list of all long-enough dictionary words on the board."
        return list(filter(lambda w: len(w) >= minimum_length,
                           self.allwords(dictroot)));
                     
    def search(self, node, tile, frontier):
        "Generates all word endings from a given state."
        if node.ends_word:  yield ""
        for other in self.adj(tile):
            letter = self.board[other[0]][other[1]];
            #print(tile, other, letter);
            if letter in node and other not in frontier:
                #print("   ", letter);
                frontier.add(other);
                for ending in self.search(node[letter], other, frontier):
                    yield letter + ending;
                frontier.remove(other);
                
                
                
class Dictionary(dict): 
    "A case-sensitive dict-based trie.  Case-sensitive."
    def __init__(self, source = None, type = None):
        self.ends_word = False;
        if source: #Load the dictionary from the source.
            if type and type.lower() == "file": self.addfile(source);
            elif type and type.lower() == "url": self.addurl(source);
            else: self.addwords(source.split());
        #else our dictionary starts out empty.
    def addword(self, word):
        if word:
            if word[0] not in self: self[word[0]] = Dictionary();
            self[word[0]].addword(word[1:]);
        else: self.ends_word = True;
        
    #A few convenient functions to add words in bulk.
    def addwords(self, words):
        for word in words: self.addword(word);
    def addfile(self, filename): #Load all words from a file.
        self.addwords(open(filename,'r').read().split());
    def addurl(self, url):
        raw_text = urllib.request.urlopen(url).read().decode("utf-8");
        self.addwords(raw_text.split());
                
#Has Boggle make a generic Boggle.
#Searches it with a dictionary built from an online list.
#Note: the word list is >100K words, so the dictionary takes a little to build.
if __name__ == "__main__":
    b = Boggle();
    b.setRandomBoard(5,4);
    b.show();
    wordlistURL = "http://www.puzzlers.org/pub/wordlists/wlist1.txt"
    d = Dictionary(wordlistURL, type = "url");
    print("Dictionary compiled.\n");
    print(b.allBoggleWords(d));

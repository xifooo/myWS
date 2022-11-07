# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random,string
from pathlib import Path

# f"{Path.cwd()}/words.txt"
# WORDLIST_FILENAME = "./words.txt"
WORDLIST_FILENAME = f"{Path.cwd()}/words.txt"


def load_words():
  """
  Returns a list of valid words. Words are strings of lowercase letters.
  Depending on the size of the word list, this function may
  take a while to finish.
  """
  print("Loading word list from file...")
  # inFile: file
  with open(WORDLIST_FILENAME,'r') as inFile:
  # inFile = open(WORDLIST_FILENAME, 'r')
  # line: string
    line = inFile.readline()
  # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
  """
  wordlist (list): list of words (strings)
  Returns a word from wordlist at random
  """
  return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program


def is_word_guessed(secret_word, letters_guessed):
  '''
  secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
  letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
  returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
      
  secretword:string, 用户猜测的单词; 
  假设所有字母都是小写字母
  letters_guessed: （字母）列表, 到目前为止已经猜到了哪些字母; 
  假设所有字母都是小写的
  returns:boolean, 如果secret_word的所有字母都是letters_guided, 则为True; 
  否则为False
  '''
  return secret_word == letters_guessed


def get_guessed_word(secret_word, letters_guessed):
  '''
  secret_word: string, the word the user is guessing
  letters_guessed: list (of letters), which letters have been guessed so far
  returns: string, comprised of letters, underscores (_), and spaces that represents
    which letters in secret_word have been guessed so far.

  secretword:string, 用户正在猜测的单词
  letters_guided: (字母)列表, 到目前为止已经猜到了哪些字母
  returns: 字符串, 由字母、下划线(_)和空格组成, 表示到目前为止, secretword中的哪些字母已经被猜到了。
  '''
  # str_guessed = list("_ "*len(secret_word))
  str_guessed = ['_ ' for h in range(len(secret_word))]
  for i,j in enumerate(secret_word):
    if j in letters_guessed:
      str_guessed[i] = f'{j} '
  return "".join(str_guessed)


def get_available_letters(letters_guessed:list):
  '''
  letters_guessed: list (of letters), which letters have been guessed so far
  returns: string (of letters), comprised of letters that represents which letters have not
    yet been guessed.

  letters_guided: （字母）列表, 到目前为止已经猜到了哪些字母
  returns: 字符串（由字母组成）, 由表示哪些字母没有还没猜到。
  '''
  s = "abcdefghijklmnopqrstuvwxyz"
  if not letters_guessed:
    return s

  uni_letter_guessed = set(letters_guessed)

  lst = [x for x in s if x not in uni_letter_guessed]
  return "".join(lst)
    
    
def hangman(secret_word):
  '''
  secret_word: string, the secret word to guess.

  Starts up an interactive game of Hangman.
  * At the start of the game, let the user know how many 
    letters the secret_word contains and how many guesses s/he starts with.
  * The user should start with 6 guesses
  * Before each round, you should display to the user how many guesses
    s/he has left and the letters that the user has not yet guessed.
  * Ask the user to supply one guess per round. Remember to make
    sure that the user puts in a letter!
  * The user should receive feedback immediately after each guess 
    about whether their guess appears in the computer's word.
  * After each guess, you should display to the user the 
    partially guessed word so far.
  Follows the other limitations detailed in the problem write-up.

  secretword:string, 要猜的秘密单词。
  启动Hangman互动游戏。
  * 在游戏开始时, 让用户知道有多少secretword包含的字母以及他/她以多少个猜测开头。
  * 用户应该从6次猜测开始
  * 在每一轮之前, 您应该向用户显示猜测的次数 他/他已经离开了, 用户还没有猜到的字母。
  * 要求用户每轮提供一个猜测。记住要确保用户填写了一封信！
  * 用户应在每次猜测后立即收到反馈他们的猜测是否出现在计算机的单词中。
  * 在每次猜测之后, 您应该向用户显示到目前为止, 部分猜测的单词。
  
  遵循问题总结中详述的其他限制。
  '''
  print("Welcome to the game Hangman! ")
  print(f"I am thinking of a word that is {len(secret_word)} letters long.")
  while True:
    if is_word_guessed():
      break
  ...


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)

# -----------------------------------

def match_with_gaps(my_word, other_word):
  '''
  my_word: string with _ characters, current guess of secret word
  other_word: string, regular English word
  returns: boolean, True if all the actual letters of my_word match the 
  corresponding letters of other_word, or the letter is the special symbol
  _ , and my_word and other_word are of the same length;
  False otherwise: 
  myword: 包含_个字符的字符串, 当前猜测的秘密单词
  other_word:string, 普通英语单词
  returns:boolean, 如果my_word的所有实际字母都与
  其他单词的对应字母, 或者该字母是特殊符号
  _以及my_word和other_word具有相同的长度:
  否则为假: 
  '''
  
  ...



def show_possible_matches(my_word):
  '''
  my_word: string with _ characters, current guess of secret word
  returns: nothing, but should print out every word in wordlist that matches my_word
  Keep in mind that in hangman when a letter is guessed, all the positions
  at which that letter occurs in the secret word are revealed.
  Therefore, the hidden letter(_ ) cannot be one of the letters in the word
  that has already been revealed.
  myword: 包含_个字符的字符串, 当前猜测的秘密单词
  returns: 没有, 但应该打印出单词列表中与myword匹配的每个单词
  请记住, 在绞刑中, 当一封信被猜中时, 所有的位置
  该字母出现在密语中的时间被揭示。
  因此, 隐藏的字母（_）不能是单词中的一个字母
  这已经被揭露了。
  '''
  
  ...



def hangman_with_hints(secret_word):
  '''
  secret_word: string, the secret word to guess.
  Starts up an interactive game of Hangman.
  * At the start of the game, let the user know how many 
    letters the secret_word contains and how many guesses s/he starts with.
  * The user should start with 6 guesses
  * Before each round, you should display to the user how many guesses
    s/he has left and the letters that the user has not yet guessed.
  * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
  * The user should receive feedback immediately after each guess 
    about whether their guess appears in the computer's word.
  * After each guess, you should display to the user the 
    partially guessed word so far.
  * If the guess is the symbol *, print out all words in wordlist that
    matches the current guessed word. 
  Follows the other limitations detailed in the problem write-up.
  
  secretword:string, 要猜的秘密单词。
  启动Hangman互动游戏。
  *在游戏开始时, 让用户知道有多少secretword包含的字母以及他/她以多少个猜测开头。
  *用户应该从6次猜测开始
  *在每一轮之前, 您应该向用户显示猜测的次数
  他/他已经离开了, 用户还没有猜到的字母。
  *要求用户每轮提供一个猜测。确保检查用户是否猜到了字母
  *用户应在每次猜测后立即收到反馈
  他们的猜测是否出现在计算机的单词中。
  *在每次猜测之后, 您应该向用户显示
  到目前为止, 部分猜测的单词。
  *如果猜测是符号*, 打印出单词列表中的所有单词
  匹配当前猜测的单词。
  遵循问题总结中详述的其他限制。
  '''
    
  ...

def main():
  ...

"""完成hangman_with_hint函数后, 将两个类似的
上面用于运行hangman函数的行, 然后取消注释
这两行并运行此文件进行测试！
提示: 您可能需要在测试时选择自己的secret_word。"""

if __name__ == "__main__":
  # To test part 2, comment out the ... line above and
  # uncomment the following two lines.
  wordlist = load_words()
  secret_word = choose_word(wordlist)
  hangman(secret_word)

###############
    
  # To test part 3 re-comment out the above lines and 
  # uncomment the following two lines. 
  
  #secret_word = choose_word(wordlist)
  #hangman_with_hints(secret_word)

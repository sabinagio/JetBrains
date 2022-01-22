import random

print('HANGMAN')

list = ['python', 'java', 'kotlin', 'javascript']
correct_word = random.choice(list)
n = len(correct_word)
new_word = '-' * n
index = 0
tries = 8
used_letters = ''
choice = input('Type "play" to play the game, "exit" to quit:')
while choice != 'exit':
    if choice == 'play':
        while new_word != correct_word and tries != 0: 
            print('''
            {}'''.format(new_word))
            letter = input('Input a letter:')
            if len(letter) != 1:
                print('You should input a single letter')
            elif letter.islower() != True:
                print('Please enter a lowercase English letter')
            else:
                if letter in used_letters:
                    print("You've already guessed this letter")
                elif letter in correct_word:
                    for j in range (0, n):
                        index = correct_word.find(letter, j, n)
                        if index != -1:
                            new_word = new_word[0:index] + letter + new_word[(index + 1):n]
                        else:
                            new_word = new_word
                else:
                    tries = tries - 1
                    print("That letter doesn't appear in the word")
                used_letters = used_letters + letter       
        if new_word != correct_word:
            print('You lost!')
        else:
            print('''You guessed the word!
        You survived!''')
        choice = input('Type "play" to play the game, "exit" to quit:')
    else: 
        choice = input('Type "play" to play the game, "exit" to quit:')       
print('exit')

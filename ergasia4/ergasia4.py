import random
import re
from sys import exit

#Global variables

words=[] #Contains each word from the given file.
words_trinities=[] #Contains all the possible continuous trinities from the words of given file.
finaltxt=[] #Contains the words that will be finally printed based on a random triad of words,picked from words_trinities.


#Functions

def split_into_words(line): #Split a given line into words.
    line=re.sub(r'http\S+','',line) #Getting rid of links.
    line=re.sub(r'@\S+','',line)    #Getting rid of words starting with '@'.
    line=re.sub(r'#\S+','',line)    #Getting rid of words starting with '#'.
    line=re.sub(r' \d+','',line)
    line=re.sub(r"['’]",'',line)    #Getting rid of " ' " characters and converting them to "" in order to convert words such as "it's" to "its".
    line=re.sub(r'[^\w\s]',' ',line) #Getting rid of commas,periods etc and converting them to ' ' in order to have every word split by a space characters.

    return line.split()


def result(current_double):
    """
    Gets a double set of words and matches them with the first 2 words of a triad from words_trinities and appends the third word from the
    particular triad into finaltxt list.This is a recursive function,calling itself whenever a match is made in order to start checking for
    a new triad,searching from the beggining of the text once again.
    """
    global finaltxt,words_trinities
    i=0
    for triad in words_trinities:
        if len(finaltxt)>=200: #Max length of the resulting text is 200 words,return stops the recursive function.
            return
        i+=1
        if current_double[0]==triad[0] and current_double[1]==triad[1]: #A match is found.
            if triad[2]==finaltxt[-1]: #If the word we are going to append to finaltxt is same with finaltxt last word.
                del words_trinities[i]
                continue
            finaltxt.append(triad[2]) #Appending the last word of the certain triad.
            del words_trinities[i]    #Deleting the triad we were using.
            del words_trinities[i]    #Deleting the next triad because it's first two words are the same with the last 2 words in finaltxt.

            temp=[finaltxt[-2],finaltxt[-1]] #Picking the last 2 words from the final text.
            result(temp) #Calling the function with a new set of 2 words.


def file_to_words(filepath='two_cities.txt'):
    file=open(filepath,'r',encoding='utf-8')
    global words,words_trinities,finaltxt

    for line in file:
        temp=split_into_words(line.lower())
        if temp==[]:
            continue
        for word in temp:
            words.append(word)

    for i in range(0,len(words)-2): #Getting every single continous triad of words.
        temp=[words[i],words[i+1],words[i+2]]
        words_trinities.append(temp)

    random_num=random.randrange(len(words_trinities)) #Picking a random number to pick a random triad.
    random_triad=words_trinities[random_num]
    del words_trinities[random_num] #Deleting the random triad picked
    del words_trinities[random_num] #Deleting the following triad

    for word in random_triad:
        finaltxt.append(word)

    file.close()


#Main program

file_path=input("Give the filepath (if filepath is not entered,it is initially set to the example file two_cities.txt): ")
if file_path=='':
    try:
        print("Run the program a couple of times,sometimes a match isn't found with some triads.\n")
        file_to_words()
    except:
        print("Example file 'two_cities.txt' must have been deleted.")
        exit()
else:
    try:
        print("Run the program a couple of times,sometimes a match isn't found with some triads.\n")
        file_to_words(file_path)
    except:
        print("File doesnt exist.")
        exit()

result(finaltxt[1:])
result_text=''

for word in finaltxt:
    result_text+=word+' '
print(f"Length: {len(finaltxt)}\n")
print(result_text)

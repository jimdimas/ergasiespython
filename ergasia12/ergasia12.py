#Function set

def text_change(filepath='text.txt'):
    """
    Gets the filepath,opens the file and for each character in each line,it converts it into its specular,
    and finally prints out the reversed text.
    """
    file=open(filepath,'r',encoding='utf-8')
    char_list=[]
    text=''
    for line in file:
        for char in line:
            char=chr(128-ord(char))
            char_list.append(char)

    char_list.reverse()
    for char in char_list:
        text+=char
    print(text)
    file.close()


#Main program

file_path=input('Give the filepath (if filepath is not entered,it is initially set to the example file text.txt):')

if file_path=='':
    try:
        text_change()
    except:
        print("Example file 'text.txt' must have been deleted.")
else:
    try:
        text_change(file_path)
    except:
        print("File doesnt exist.")

import sys

#This will be my scanner that will be built later
def run(source):
    
    print("Scanner Not Implemented Yet")

#Takes the file path as an argument and runs the file
def open_file(path):
    with open(path, 'r') as file:
        source = file.read()

    run(source)

#Takes user file input and runs the input
def print_prompt():
    try:
        while True:
            source = input('> ') # This made it easier to follow with a '>'  vs having it blank
            print(f'{source}')
            run(source)
    except KeyboardInterrupt:
        print()
        
def main():
    if len(sys.argv) == 1:   #If there is only one argument in the command line
        print_prompt()

    elif len(sys.argv) == 2:   #If there are two arguments in the command line, the second argument is the file path
        open_file(sys.argv[1])

    else:
        print('Usage: python src/yuck.py [script]')


if __name__ == "__main__":
    main()
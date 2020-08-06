# stolen from https://www.tutorialspoint.com/rename-multiple-files-using-python#:~:text=rename()%20method%20is%20used,part%20of%20the%20os%20module.

import os
# Function to rename multiple files
def main():
    i = 0
    # path="C:/Users/TP/Desktop/sample/Travel/west bengal/bishnupur/"
    for i in range(1,8):
        my_source = "./" + "idle" + str(i) + ".png"
        my_dest = "./" + str(i) + ".png"
        # rename() function will
        # rename all the files
        os.rename(my_source, my_dest)
        i += 1
# Driver Code
if __name__ == '__main__':
    # Calling main() function
    main()
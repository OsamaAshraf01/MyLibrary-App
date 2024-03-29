from Config import *
from Style import *



def get_books_from(PATH):
    """Get books' details list from database.txt file OR default.txt file

    Args:
        PATH (string): path of file

    Returns:
        list: list of books' details
    """
    books_details = []
    database = advanced_open(PATH, "r")  # Opening input file
    lines = database.readlines()
    for line in lines:
        line = [element.strip('\t \n') for element in line.split("|")]    # Clearing line
        line = removeAll(line, "")

        if len(line) > 1:
            books_details.append(line)

    database.close()
    books_details = reorder_books(books_details[1:], PATH)    # Reorder books according to global parameters & remove table header
    return books_details


def output(string):
    """Printing Values in both terminal and output.txt file

    Args:
        string (string): string to be printed
    """
    output_file = open(OUTPUT_PATH, "a")
    print(string, end="")
    output_file.write(string)
    output_file.close()


def check_found(title):
    """Check if book is in database or not

    Args:
        title (string): book title

    Returns:
        bool: True if book is in database, False otherwise
    """
    books = get_books_from(DATABASE_PATH)

    for i in range(len(books)):
        if books[i][TITLE].title() == title:
            return True

    return False


def removeAll(list, value):
    """Remove all occurences of value from list

    Args:
        list (list): list to be modified
        value (any): value to be removed

    Returns:
        list: list after removing all occurences of value
    """
    for e in list.copy():
        if e == value:
            list.remove(value)

    return list


def update_database(library):
    """Update Database after any modification

    Args:
        library (list): list of books after any modification
    """
    database = open(DATABASE_PATH, "w")        # Clearing Database
    database.write(TABLE_HEADER)               # Appending table Header
    database.close()
    database = open(DATABASE_PATH, "a")

    for book in library:  # Formatting lines to be printed in terminal and output.txt file
        book[ID] = str(library.index(book) + 1)
        database.write(formatting(book))
        database.write("\n" + SEPARATING_LINE)  # Printing Separating Line

    database.close()

    
    # Updating Sorted Database

    default = open(SORTED_PATH, "w")  # Clearing Database
    default.write(TABLE_HEADER)  # Appending table Header
    default.close()
    default = open(SORTED_PATH, "a")

    library = apply_sort(library)

    for book in library:  # Formatting lines to be printed in terminal and output.txt file
        book[ID] = str(library.index(book) + 1)
        default.write(formatting(book))
        default.write("\n" + SEPARATING_LINE)  # Printing Separating Line

    default.close()


def integer_only(instructions, Error_Massage): 
    """Making sure that user entered an integer value

    Args:
        instructions (string): Message to enter integer
        Error_Massage (string): Meassage when invalid integer detected

    Returns:
        int: Correct integer
    """
    while True:
        try:
            variable = int(input(instructions))
            break
        except:
            print(Error_Massage)
    return variable


def calc_percentage(choose):
    """Calculate percentage of book read

    Args:
        choose (int): book index
    """
    library = get_books_from(DATABASE_PATH)
    read_pages = int(library[choose - 1][PAGES].split("/")[0])
    total_pages = int(library[choose - 1][PAGES].split("/")[1])

    library[choose - 1][PERCENT] = f"{int((read_pages / total_pages) * 100)}%"  # Update Percentage

    update_database(library)

    full_percentage(library, choose)


def full_percentage(library, choose):
    """Check if book is finished or not

    Args:
        library (list): list of books
        choose (int): book index
    """
    read_pages = int(library[choose - 1][PAGES].split("/")[0])
    total_pages = int(library[choose - 1][PAGES].split("/")[1])

    if read_pages == total_pages:  # If book is finished
        print("Congratiolatins!! You have finished the book")
        library[choose - 1][STATUS] = "Finished"
        rating_after_finishing(library,choose)

    update_database(library)


def choose_book():  
    """Choose book from library after showing all books

    Returns:
        int: book index
    """
    library = get_books_from(DATABASE_PATH)
    # library = sort_library_by(TITLE, False)

    books_list = []
    for book in library:  # Getting books list
        books_list.append(book[TITLE])

    for book in range(len(books_list)):
        print(f"{book + 1}. {books_list[book]}")
    while True:  # Asking user to shoose and amking sure that he entered integer value
        try:
            choose = integer_only("Choose book: ", "INVALID! Integers only")
            if 0 < choose <= len(books_list):
                break
        except:
            print("OUT OF RANGE! Choose one of the above options")
    return choose


def get_correct_date_format(instructions, Error_Massage, start_date = True):  # Making sure that user entered a valid date
    """Making sure that user entered a valid date

    Args:
        instructions (string): Message to enter date
        Error_Massage (string): Meassage when invalid date detected

    Returns:
        string: Correct Date
    """
    import time
    Current_day = time.strftime("%d", time.localtime())
    Current_month = time.strftime("%m", time.localtime())
    Current_year = time.strftime("%Y", time.localtime())
    Current_date_value = Current_year + Current_month + Current_day

    while True:
        try:
            date = input(instructions)
            date_components = date.split("/")
            if len(date_components) == 3:
                
                day = date_components[0]
                month = date_components[1]
                year = date_components[2]
                regular_months = [4, 6, 8, 11]
                if int(month) == 0 or int(day) == 0 or int(year) < 1000:
                    print(Error_Massage)
                    continue
                if int(month) > 12 or int(day) > 31 or len(year) != 4:
                    print(Error_Massage)
                    continue
                if int(month) in regular_months and int(day) > 30:
                    print(Error_Massage)
                    continue
                if int(month) == 2 and int(year) % 4 == 0:
                    if int(day) > 29:
                        print(Error_Massage)
                        continue
                elif int(month) == 2 and int(year) % 4 != 0:
                    if int(day) > 28:
                        print(Error_Massage)
                        continue
                if int(day) < 10:
                    day = "0" + day
                if int(month) < 10:
                    month = "0" + month
                date_value = year + month + day
                if start_date == True:
                    if int(date_value) > int(Current_date_value):
                        print(Error_Massage)
                        continue
                    else:
                        break
                else:
                    break
            else:
                print(Error_Massage)
        except:
            print(Error_Massage)
    return date


def sort_by_pages(book):
    """Sort books by pages

    Args:
        book (list): book details

    Returns:
        tuple: total pages, read pages
    """
    read_pages, total_pages = map(int, book[PAGES].split("/"))
    return total_pages, read_pages


def sort_by_percentage(book):
    """Sort books by percentage

    Args:
        book (list): book details

    Returns:
        int: book percentage
    """
    percentage = int(book[PERCENT].rstrip("%"))
    return percentage


def sort_by_date(book):
    """Sort books by date

    Args:
        book (list): book details

    Returns:
        tuple: date in year, month, day format
    """

    day, month, year = map(int, (book[DATE] if book[DATE] != "N/A" else "0/0/0").split("/"))     # If date is N/A, set it to 0/0/0 to be sorted at the end
    return year, month, day


def reorder_books(library, PATH):
    """Reorder books according to global parameters

    Args:
        library (list): list of books
        PATH (string): path of file

    Returns:
        list: list of books after reordering
    """
    database = advanced_open(PATH, "r")
    lines = database.readlines()

    # Getting old order of parameters
    old_order = lines[2].split("|")
    old_order = [element.strip('\t \n') for element in old_order]  # Getting old order of parameters
    removeAll(old_order, "")
    
    # Reorder box according to new order
    new_indicies = [old_order.index(element) for element in PARAMETERS]   # Getting new order of parameters
    ordered_library = []

    for book in library:
        ordered_library.append([book[i] for i in (new_indicies)])

    return ordered_library


def advanced_open(path, mode="r"):
    """Open file for read and create it if not found to avoid errors

    Args:
        path (string): file path to be opened
        mode (_type_): file mode

    Returns:
        file: opened file
    """
    try:
        file = open(path, mode)
    
    except FileNotFoundError:
        file = open(path, 'w')   # Creating database.txt file in required place

        if path == DATABASE_PATH: # Adding appropriate header based on file
            file.write(TABLE_HEADER)
        elif path == SORTED_PATH :
            file.write(TABLE_HEADER)
        elif path == RATINGS_PATH:
            file.write(RATINGS_HEADER)
        elif path == MARKS_PATH:
            file.write(MARKS_HEADER)
        elif path == SORT_MODE_PATH:
            file.write("off")

        file.close()
        file = open(path, mode)
    
    return file


def get_book_order(title):
    """Get book index in database

    Args:
        title (string): book title

    Returns:
        int: book index
    """
    library = get_books_from(DATABASE_PATH)
    for i in range(len(library)):
        if library[i][TITLE] == title:
            return i


def divide_string(string, segment_length):
    """Divide string to segments with length less than or equal to segment_length according to spaces

    Args:
        string (string): string to be divided
        segment_length (int): maximum length of each segment

    Returns:
        list: list of segments
    """
    segments = []
    while len(string) > segment_length:                                 # If string is larger than column width, divide it to more than one line
        segment = string[:segment_length]                   # Forming segment
        last_space = segment_length-segment[::-1].find(' ')             # Inverse segment --> get first space index --> negative of that index is the index from the end --> adding segment_length will result in index from start
        segment = segment[:last_space]   
        segments.append(segment)
        string = string[last_space:]

    segments.append(string)

    return segments


def rating_after_finishing(library, choose):
    """Ask user to rate book after finishing it

    Args:
        library (list): list of books
        choose (int): book index
    """
    advanced_open(RATINGS_PATH, 'r').close()     # Making sure that Ratings file is found and appending header
    file = open(RATINGS_PATH, 'a')
    title = library[choose - 1][TITLE]

    while True:
        rating = integer_only("Enter your rating for this book from 1 to 10: ", "INVALID! Integers only")
        if 0 < rating <= 10:
            break
        else:
            print("OUT OF RANGE! Enter Correct rating")

    file.write(f"\n|{cell_format(title, WIDTHS['Title'])}|{cell_format(f"{rating}/10", 2)}|")
    file.write("\n+-------------------------------+---------------+")

    file.close()


def apply_sort(library):
    mode = advanced_open(SORT_MODE_PATH)
    values= mode.readlines()
    values = [value.strip("\n") for value in values]
    mode.close()
    if values[0] == "on":
        library = sort_library_by(SORTING_PARAMETERS[values[1]], SORT_TYPE[values[2]])
        return library
    
    elif values[0] == "off":
        return library
    

def sort_library_by(Parameter, Type):
    """Sorting the library by any parameter

    Args:
        Parameter (string): Parameter to sort by
        Type (string): Type of sorting [Ascending, Descending]

    Returns:
        list: sorted library
    """
    books = get_books_from(DATABASE_PATH)
    if Parameter == PAGES:
        sorted_books = sorted(books, key= sort_by_pages, reverse= Type)
    elif Parameter == PERCENT:
        sorted_books = sorted(books, key= sort_by_percentage, reverse= Type)
    elif Parameter == DATE:
        sorted_books = sorted(books, key= sort_by_date, reverse= Type)
    else:
        sorted_books = sorted(books, key= lambda book: book[Parameter], reverse= Type)
    return sorted_books

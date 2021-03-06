
###################################################################
#
#   CSSE1001 - Assignment 1
#
#   Student Number: 42094353
#
#   Student Name: Justin Mancinelli
#
###################################################################

"""
Comments for each function have been copied from the assignment description
for the sake of accuracy of implementation.
"""

parts_file = 'parts.txt'
products_file = 'products.txt'

def load_parts(filename):
    """ Takes the name of a file containing parts information and returns
    a dictionary that associates each part ID with a pair consisting of the
    part and the cost of the part in cents.

    precondition: the file referenced by the filename must exist
        and be non-empty containing three pieces of information
        separated by commas.
        The first and second parts must be alphanumeric,
        The third part must be numeric.

    load_parts(str) -> dict(str, tuple(str, int))
    """
    parts = open(filename, 'U')
    parts_list = {}
    for part in parts:
        part_details = [el.strip() for el in part.split(',')]
        # We only care about lists which are of the correct format
        if len(part_details) == 3:
            key = part_details.pop(0)
            price = int(part_details.pop(-1))
            name = part_details.pop(0)
            parts_list[key] = (name, price)
    parts.close()
    return parts_list

def get_components(parts):
    """ Takes a list of strings representing pairs of part IDs and number of
    this part (colon separated) and returns a list of pairs consisting of a
    part ID and a number representing the number of parts in the list.

    Precondition: Each element in the parts list must be a string representing
        a pair separated by a colon. The first element must be alphanumeric and
        the second element must be numeric.

    get_components(list(string:string)) -> list(tuple(str, int))
    """
    component_list = []
    for component in parts:
        formatted_component = component.split(':')
        part_id = formatted_component[0].strip()
        part_quantity = int(formatted_component[1].strip())
        component_tuple = (part_id,part_quantity)
        component_list.append(component_tuple)
    return component_list

def load_products(filename):
    """ Takes the name of a file containing product information
    and returns a dictionary that associates each part ID with a pair
    consisting of the name of the product and a list of pairs, each consisting
    of the name of the part and the number of this part required to build the
    product.

    Precondition: the file referenced by the filename must exist
        and be non-empty containing information
        separated by commas.
        The first and second parts must be alphanumeric,
        The remaining parts must consist of pairs of values separated by colons.
        The first value in a pair must be alphanumeric
        and the second value in the pair must be numeric.

    load_products(str) -> dict(str, tuple(str,list(tuple(str, int))))
    """
    products = open(filename, 'U')
    products_list = {}
    for product in products:
        product_details = [el.strip() for el in product.split(',')]
        # We only care about lists which are the correct format
        if len(product_details) >= 2:
            key = product_details.pop(0)
            product_name = product_details.pop(0)
            
            part_info = []
            for el in product_details:
                formatted_el = el.split(':')
                #el_tuple -> (part_name, number of this part required)
                el_tuple = (formatted_el[0].strip(),
                            int(formatted_el[1].strip()))
                part_info.append(el_tuple)
            products_list[key] = (product_name, part_info)
    products.close()
    return products_list

def get_product_id(product_dict, name):
    """ Takes, as arguments, a product dictionary, as produced by
    load_products, and a string, name, and returns the ID of the product
    with the given name from the dictionary, if it exists, and
    returns None otherwise.

    Precondition: The product_dict must be of the same form as produced by
        the load_products function. name must be a string.

    get_product_id(dict, str) -> str
    """
    product_id = None
    for key in product_dict:
        if product_dict[key][0] == name:
            product_id = key
    return product_id

def get_product_name(product_dict, pid):
    """ Takes, as arguments, a product dictionary, as produced by
    load_products, and a string, pid, and returns the name of the product
    with the given ID from the dictionary, if it exists, and
    returns None otherwise.

    Precondition: The product_dict must be of the same form as produced by
        the load_products function. pid must be a string.

    get_product_name(dict, str) -> str
    """

    product_name = None
    if product_dict.has_key(pid):
        product_name = product_dict[pid][0]
    return product_name
    
def get_parts(product_dict, pid):
    """ Takes, as argumnets, a product dictionary, as produced by
    load_products, and a string, pid, and returns the parts list of the product
    with the given ID from the dictionary, if it exists, and
    returns None otherwise.

    Precondition: The product_dict must be of the same form as produced by
        the load_products function. pid must be a string.

    get_parts(dict, str) -> list(tuple(str, int))
    """
    
    parts_list = None
    if product_dict.has_key(pid):
        parts_list = product_dict[pid][1]
    return parts_list

def compute_cost(product_dict, parts_dict, pid):
    """ Takes, as arguments, a product dictionary, as produced by load_products,
    a parts dictionary as produced by load_parts, and a string, pid, and
    returns the cost (in cents) of all the parts of the product with the given
    ID, if it exists, and returns None otherwise.

    Precondition: The product_dict must be of the same form as produced by
        the load_products function. The product_dict must be of the same form
        as produced by the load_parts function. pid must be a string. 

    compute_cost(dict, dict, str) -> int
    """
    total_cost = None
    running_total = 0
    parts_list = get_parts(product_dict, pid)
    if parts_list:
        for part in parts_list:
            part_id, part_quantity = part[0], part[1]
            running_total += parts_dict[part_id][1] * part_quantity
        total_cost = running_total
    return total_cost

def interact():
    """ The interaction interface repeatedly asks the user for a command,
    processes the command and prints out the results.

    Precondition: If the command is a valid command,
        then the command is followed by the correct number of arguments.

    interact()-> None (the output will be printed rather than returned
    """
    valid_commands = ('e','i','n','c','p')
    products = load_products(products_file)
    parts = load_parts(parts_file)
    command = None

    while(1):
        user_input = raw_input("Command: ").split(' ', 1)
        command = user_input[0]
        if command in valid_commands:
            if command == 'e':
                # exit the program
                break
            elif command == 'i':
                result = get_product_id(products, user_input[1])
            elif command == 'n':
                result = get_product_name(products, user_input[1])
            elif command == 'c':
                result = compute_cost(products, parts, user_input[1])
                if result:
                    #convert to dollars
                    result = "%.2f" % (result/100.0)
            elif command == 'p':
                result = get_parts(products, user_input[1])

            if result:
                print result
            else:
                print "Unknown Item"
        else:
            print "Unknown Command"

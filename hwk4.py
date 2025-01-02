# Name:  - Nida Chacar-Palubinskas <br>
# Peers:  - N/A <br>
# References:  - https://www.cs.hmc.edu/~geoff/classes/hmc.cs070.200101/homework10/hashfuncs.html
#https://www.geeksforgeeks.org/what-are-hash-functions-and-how-to-choose-a-good-hash-function/
#https://www.geeksforgeeks.org/python-linked-list/
#https://www.geeksforgeeks.org/implementation-of-hash-table-in-python-using-separate-chaining/<br>
import math
import time
import csv          # Used to read a .csv file.

### DO NOT EDIT ###
def new_array(size: int):
    """ Creates a new array of a given size.
    :param size: (int) the number of 0s you want in the array
    :return : (list) the array with zeros 
    >>> new_array(3)
    [0,0,0]
    """
    L = [0] * size
    return L

class HashNode:
    """Class to instantiate linked list node objects, with both a key and a value.
    >>> node = HashNode(7, "Matt Damon")
    >>> print(node)
    {key:7, value:Matt Damon}
    """

    def __init__(self, key:int, value:str) -> object:
        """ Constructor of new node with a key and value. Initially nodes do not have a next value.
        :param key: (int) the key that will be added to the node
        :param value: (str) the value that will be added to the node
        :return : (HashNode) a pointer to the object
        """
        self.key = key
        self.value = value
        self.next = None

    def __str__(self) -> str:
        """ Returns a string representation of the object.
        :return : (str) a string description of the HashNode object.
        """
        return "{key:" + str(self.key) + ", value:" + self.value + "}"     
### END OF DO NOT EDIT###




# Hint: create a linked list class here...
class LinkedList:
    """Class to instantiate linked lists, with a head and connected nodes.

    Attributes:
        head (HashNode): the first node in the list        
    """
    #TODO: add comments explaining what everything is doing
    def __init__(self, head:HashNode|None):
        """ Initializes the LinkedList
        :param head: (HashNode) the first node in the LinkedList
        """
        self.head=head

    def firstInsert(self, key:int, data:int):
        """ inserts a 
        :param head: (HashNode) the first node in the LinkedList
        """
        newest = HashNode(key, data)
        if self.head is None:
            self.head = newest
            return
        else:
            newest.next = self.head
            self.head = newest

#     def lastInsert(self, key:int, data:int):
#         newest = HashNode(key, data)
#         if self.head is None:
#             self.head = newest
#             return
# 
#         #looking for the end of the list. loop ends when current points to the end of the list
#         current = self.head
#         while(current.next):
#             current = current.next
# 
#         current.next = newest
# 
#     def midInsert(self, key:int, data:int, position:int):
#         if(position == 0):
#             self.firstInsert(key, data)
# 
#         temp_pos = 0
#         current = self.head
#         while(current != None and temp_pos < position - 1):
#             temp_pos += 1
#             current = current.next
# 
#         if(current != None):
#             newest = HashNode(key, data)
#             newest.next = current.next
#             current.next = newest
#         else:
#             raise Exception("Position out of range")

#     def update(self, key:int, data:int, position:int):
#         if(position == 0):
#             self.firstInsert(key, data)
# 
#         temp_pos = 0
#         current = self.head
#         while(current != None and temp_pos < position):
#             temp_pos += 1
#             current = current.next
# 
#         if(current != None):
#             current.data = data
#         else:
#             raise Exception("Position out of range")

    def delete(self, position:int):
        """ Removes a node from the LinkedList.
        :param position: (int) index of the node that should be removed
        :throws IndexError: when the position inputted is less than 0 or greater than the size of the list
        """
        if self.head == None:
            return
        
        if position==0:
            self.head = self.head.next
            return

        current = self.head
        temp_pos = 0
        while current != None and temp_pos < position - 1:
            temp_pos += 1
            current = current.next

        if current != None and current.next != None:
            current.next = current.next.next
        else:
            raise IndexError("Position ", position, " out of range for length ", self.size_of())


    def size_of(self)->int:
        """ Adds up the size of the LinkedList
        return : (int) the size of the list, i.e. the number of nodes
        """
        size = 0
        if(self.head):
            current = self.head
            while(current):
                size += 1
                current = current.next
            return size
        return 0

    #Other methods I could implement: delete a node based on data parameter, delete the last node

class HashTable:
    """ Class to instantiate HashTable objects, with an array of linked lists.
    Attributes:
        table (array): an array that will hold all of the linked lists of HashNodes
        size (int): the size of the table array
        hash_choice (int): the hash function that will be used (0,4)
    """

    def __init__(self, size:int, hash_choice:int) -> object:
        """ Constructs a HashTable object with an array of the inputted size filled with empty LinkedLists.
        param size: (int) the size of the table array
        param hash_choice: (int) the function that the nodes will be hashed with, between 0 and 4
        """
        self.size = size
        self.hash_choice = hash_choice                  # Which hash function you will use.
        self.table = new_array(size)
        
        for i in range(0,self.size):
            self.table[i] = LinkedList(None)
        

    def __str__(self) -> str:
        """ Expresses the table as a string of format {Index 0: list[0],...list[size-1]}\n ... {Index n: list[0],...list[size-1]}
        return : (str) all the linked lists in the table array printed in order preceded by their index, with a new line between them
        """
        ret = ""
        for i in range(0, self.size):
            ret+="Index "
            ret+=str(i)
            ret+= ": "
            temp_node = self.table[i].head
            ret+="{"
            if temp_node != None:
                while temp_node.next != None:
                    ret+=str(temp_node)
                    ret+=", "
                    temp_node = temp_node.next
                ret+=str(temp_node)
            ret+="}\n"
        return ret

    def hashFunc(self, key:int) -> int:
        """ Returns an index for a node based on key value and the HashTable's hash function.
        param key: (int) the key value of a HashNode. The same key value will always return the same index
        return : (int) an index for the node that will always be within the bounds of the HashTable's size
        """
        if type(key) != int:
            raise Exception("Key must be an integer.")
        if self.hash_choice == 0:
            return hash(key) % self.size    #Embedded Python hash function.
        elif self.hash_choice == 1:
            return 0    #Everything in the hash is stored in a single linked list.
        elif self.hash_choice == 2:
            #Returns the mod of the key by the HashTable size. Simple but not stellar distribution
            return key%self.size
        elif self.hash_choice == 3:
            #Similar to hash function #2, but with a prime number added
            #Returns the mod of the sum of the key+3 by the HashTable size
            return (key+3)%self.size
        elif self.hash_choice == 4:
            #chosen  because I wanted to do something other than +,-,*,/ with the key and then involve a prime number.
            #Returns the square root of the key multiplied by 257
            return (int)(math.sqrt(key)*257)%self.size
        raise Exception("Key must be between 0 and 4.")

    def insert(self, key:int, val:str) -> bool:
        """Inserts a new node into the HashTable
        param key: (int) the key of the inserted HashNode. Indicates where the node should be placed after running the key through a hash function
        param val: (str) the value attached to the inserted HashNode
        return : (bool) true if there has been a successful insertion, false if the insertion failed
        """
        try:
            position = self.hashFunc(key)
            self.table[position].firstInsert(key, val)
            return True
        except:
            return False

    def getValue(self, key:int) -> str:
        """Finds the value associated with the inputted key
        param key: (int) the key of the HashNode we're looking for
        return : (str) value of the HashNode with the inputted key. If the key doesn't exist, returns None
        """
        position = self.hashFunc(key)
        temp_node = self.table[position].head
        while temp_node != None:
            if temp_node.key == key:
                return temp_node.value
            temp_node = temp_node.next
        return None

    def remove(self, key:int) -> bool:
        """Removes the HashNode
        param key: (int) the key of the HashNode that has to be removed
        return : (bool) true if there has been a successful deletion, false if the insertion failed
        """
        position = self.hashFunc(key)
        
        temp_node = self.table[position].head
        prev_node = None
        
        while temp_node:
            if temp_node.key == key:
                if prev_node:
                    prev_node.next = temp_node.next
                else:
                    self.table[position] = LinkedList(None)
                return True
            prev_node = temp_node
            temp_node = temp_node.next
            
        return False
            

    def isOverLoadFactor(self) -> bool:
        """Calculates overload factor, the porportion of filled slots in the table, and checks if it's above 0.7.
        return : (bool) true if the overload factor is greater than or equal to 0.7, false it's below
        """
        full_slots = 0.0
        
        for i in range(0, self.size):
            if self.table[i].head!=None:
                full_slots+=1.0
        
        return (full_slots/self.size)>=0.7

    def reHash(self) -> bool:
        """Triples the size of the HashTable and copies over the HashNodes, re-hashing them to find their new positions
        return : (bool) true if the rehash has been successful, false if it failed
        """
        try:
            temp_table = HashTable(self.size*3, self.hash_choice)
            for i in range(0, self.size):
                if self.table[i].head!=None:
                    temp_node = self.table[i].head
                    for j in range(0, self.table[i].size_of()):
                        new_pos = temp_table.hashFunc(temp_node.key)

                        temp_table.table[new_pos].firstInsert(temp_node.key, temp_node.value)
                        temp_node = temp_node.next
            
            self.table = temp_table.table
            self.size = temp_table.size
            return True
        except:
            return False


def main():
    """
    Creates a HashTable with nodes from hwk4-people.csv
    Takes user input to run insert(), getValue(), remove(), print(), isOverLoadFactor(), reHash(), or quit
    """
    # You should update these three values as you test your implementation.
    hash_to_test = 4    
    initial_bucket_size = 89 
    initial_num_to_add = 50

    hash_table = HashTable(initial_bucket_size, hash_to_test)
    # Users/nida/smithassignments/csc252/hwk4/
    with open('hwk4-people.csv') as csv_file:    
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = csv_reader.__next__()
        for row_iterator in range(initial_num_to_add):
            row = csv_reader.__next__()
            hash_table.insert(int(row[0]),row[1])
        print("Hash Map Initialized")

        option = ""
        while option != "QUIT":
            option = input("Select an option (ADD, GET, REMOVE, PRINT, CHECK, REHASH, QUIT): ").upper()        

            if option == "ADD":
                row = csv_reader.__next__()
                hash_table.insert(int(row[0]),row[1])
                print("Added - Key:", int(row[0]), "\tValue:", row[1])
            elif option == "GET":
                key = int(input("Which # would you like to get the value of? "))
                val = hash_table.getValue(key)
                if val is None:
                    print("Error,", key, "not found.")
                else:
                    print(val)
            elif option == "REMOVE":
                key = int(input("Which # would you like to remove? "))
                suc = hash_table.remove(key)
                if suc:
                    print(key, "was removed.")
                else:
                    print("Error,", key, "was not removed.")                    
            elif option == "PRINT":
                print(hash_table)   # calls the __str__ method.  
            elif option == "CHECK":
                isOver = hash_table.isOverLoadFactor()
                if isOver:
                    print("Your load factor is over 0.7, it's time to rehash.")
                else:
                    print("Load factor is ok.")
            elif option == "REHASH":
                suc = hash_table.reHash()
                if suc:
                    print("Rehash was successful.")
                else:
                    print("ERROR: rehash failed.")
            elif option == "QUIT" or option == "Q":
                break 
            else:
                print("Error: invalid input, please try again.")

        print("Goodbye!")


def profilerMain():
    """
    Creates a HashTable with nodes from hwk4-people.csv
    Loops through the HashTable and times how long different functions take to run
    """
    # You should update these three values as you profile your implementation.
    num_hash_implemented = 2    
    initial_bucket_size = 999 
    initial_num_to_add = 100

    for i in range(0,5):
        for i in range(0, num_hash_implemented):        
            hash_table = HashTable(initial_bucket_size, i)
            #Users/nida/smithassignments/csc252/hwk4/hwk4-people.csv
            with open('hwk4-people.csv') as csv_file:    
                csv_reader = csv.reader(csv_file, delimiter=',')
                header = csv_reader.__next__()
                for row_iterator in range(initial_num_to_add):
                    row = csv_reader.__next__()
                    hash_table.insert(int(row[0]),row[1])
                print("Hash Map", i, "Initialized")
                start_time_create = time.time()    # Get start Time.
                #### Start of code you want to profile ####

                # Add/Edit code to profile
                
                row = csv_reader.__next__()
                #hash_table.reHash()
                #hash_table.remove(138)
                #hash_table.getValue(138)
                hash_table.isOverLoadFactor()
                #hash_table.insert(int(row[0]),row[1])

                #### End of code you want to profile ####
                end_time_create = time.time()      # Get end Time. 
                calc = end_time_create - start_time_create  
                print("Hash Map", i, "Test \tTime:", calc, "seconds.")



if __name__ == "__main__":
    # Swap these options to profile or test your code.
    #profilerMain()     
    main()
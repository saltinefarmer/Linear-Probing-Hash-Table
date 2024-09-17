class HashTable:
    """
    This program implements linear probing to create a hashtable.
    It accepts a Key / Value pair and stores them in a list.    
    """

    __author__ = "Silver Lippert"
    __version__ = "23.10.9"
    table = []
    mod = 0
    size = 0

    def __init__ (self, initial_size = 11):
        """
        Constructor sets the list size to 11 unless specified otherwise
        """
        self.mod = initial_size
        self.table = [None] * self.mod

    # inserts a new key / value pair to table
    def put (self, key, value):
        """
        Method Put accepts a key and value, hashes and mods it, and places
        it into the list. If key already exists, it will instead replace 
        the old value with the specified new one
        """

        location = self.__hash_and_mod(key)
        end = location - 1
        self.size += 1

        # if the hash & mod matches exactly to a formerly occupied spot
        if self.table[location] == (None, None):
            self.table[location] = (key, value)
            return

        while True: # go through whole table
            
            if location == self.mod: # loop table to beginning if it gets to far
                location = 0
            
            if self.table[location] == None: # if slot is empty
                self.table[location] = (key, value)
                break
                
            if self.table[location][0] == key: # if key already exists in table
                self.table[location] = (key, value)
                self.size -= 1
                break

            if location == end: # if somehow the table is full, rehash and add. This should't be possible but I don't want to risk it
                self.__rehash((self.mod * 2) + 1)
                self.put(key, value)
                break
            location += 1

        
        if self.get_load_factor() > .75: # if table gets to full, rehash to a larger one
            self.__rehash((self.mod * 2) + 1)

    # deletes a key / value pair, returns value, or null if
    # key is not present
    def delete (self, key):
        """
        Method Delete searches for the input key and removes it from
        the list. It will then return the value. Will return None if
        key does not exist within the hashtable
        """

        location = self.__hash_and_mod(key)
        value = None

        while not self.table[location] == None: # until end of cluster is reached
            
            if location == self.mod: # if location reaches end of table, loop back around
                location = 0

            if self.table[location][0] == key: # if key matches
                self.size -= 1
                value = self.table[location][1]
                self.table[location] = (None, None) # reset k / v pair
                break

            else: # continue iterating until end of cluster
                location += 1
        
        
        if self.get_load_factor() < .125 and self.mod > 11: # if list is too small, also make sure it wont shrink too much
            self.__rehash(int(self.mod / 2))
        
        return value
        
    # returns value at given key or null if not present
    def get(self, key):
        """
        Method Get accepts a key as input and searches for it within
        the list. It will return the value associated with the key,
        or None if the key is not found
        """
        location = self.__hash_and_mod(key)
        value = None

        while self.table[location] != None: # iterate through cluster
            
            if self.table[location][0] == key: # if key matches
                value = self.table[location][1]
                break
            else:
                location += 1 # else keep moving forward

                if location == self.mod: # if end of list is reached
                    location = 0

        return value


    # searches for key, returns true if present
    def contains_key(self, key) -> bool:
        """
        Method Contains Key searches for the input key, and
        returns a boolean indicating whether it is in the list
        """
        location = self.__hash_and_mod(key)

        while self.table[location] != None: # iterate through cluster
            
            if self.table[location][0] == key: # if key matches
                return True
            else:
                location += 1 # else keep moving forward

                if location == self.mod: # if end of list is reached
                    location = 0

        return False

    # searches for value, returns true if found
    def contains_value (self, value) -> bool:
        """
        Method Contains Value searches through the hashtable for
        the input value, and returns a boolean indicating
        whether it is in the list.
        """

        for item in self.table: # iterate through whole table
            if item == None:
                continue
            if item[1] == value:
                return True
            
        return False


    # returns true if table is empty
    def is_empty (self) -> bool:
        """
        Method Is Empty returns true if there are no Key / Value
        pairs in the table, or false otherwise
        """
        return self.size == 0

    # returns number of key / value pairs in the table
    def __len__ (self) -> int:
        """
        Method len (length) returns the number of key / value
        pairs in the table
        """
        return self.size

    # finds a key that maps to the value, or returns None
    # if not present
    def reverse_lookup (self, value):
        """
        Method Reverse Lookup takes a value as input, and searches
        for it. If found, it returns the associated key. Returns
        None otherwise
        """

        for item in self.table: # iterate through whole table
            if item == None:
                continue
            if item[1] == value:
                return item[0]
                    
        return None

    # returns size of array, including unoccupied spaces
    # this will be the number the hash is being modded by
    def get_table_size (self) -> int:
        """
        Method Get Table Size returns the length of the 
        table, unoccupied spaces included.
        """

        return self.mod

    # returns alpha, which is n / m (number of entries / list length)
    def get_load_factor (self) -> float:
        """
        Method Get Load Factor calculates the number of items
        in the table divided by the total size of the table to
        return alpha, the representation of what % of the table
        is being used.
        """
        return float(self.size) / float(self.mod)

    # counts number of entries with no value key / value pairs
    def count_empty_slots (self) -> int:
        """
        Method Count Empty Slots calculates the number of None or
        (None, None) in the list.
        """

        # getTableSize - len
        return self.get_table_size() - self.size
    
    # find largest cluster
    def find_longest_run (self) -> int:
        """
        Method Find longest Run determines how long the largest
        cluster is.
        """        

        largest_cluster = 0
        current_cluster = 0

        for item in self.table:
            if not (item == None or item == (None, None)):
                current_cluster += 1

            if current_cluster > largest_cluster:
                    largest_cluster = current_cluster

            if item == None or item == (None, None):
                current_cluster = 0

        return largest_cluster


    # rehash list when it gets above the load factor
    def __rehash (self, mod):
        temp_table = self.table

        self.table = [None] * mod
        self.size = 0
        self.mod = mod

        for item in temp_table:
            if item == (None, None) or item == None:
                continue
            
            self.put(item[0], item[1])

    # hashes and mods key to place in list
    def __hash_and_mod(self, key) -> int:
        return hash(key) % self.mod

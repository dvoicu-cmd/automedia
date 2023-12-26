import pickle

class Queue:
    """
    Queue class made to be serialized with pickle lib
    """

    q = None

    def __init__(self):
        """
        Constructor
        """
        # Init as list
        self.q = []

    # --- Manipulation --- #

    def put(self, item):
        """
        puts an item into the queue
        """
        self.q.append(item)

    def get(self):
        """
        removes and returns an item from the queue
        """
        if self.is_empty():
            return # Return nothing if queue is empty
        else:
            return self.q.pop(0)

    # --- View Properties --- #

    def size(self):
        """
        gets the number of elements in the queue
        """
        return self.q.__len__()

    def contains(self, item):
        """
        states if a value is in the queue
        """
        if self.q.__contains__(item):
            return True
        else:
            return False

    def is_empty(self):
        """
        states if the queue is empty
        """
        if self.size() <= 0:
            return True
        else:
            return False

    def __str__(self):
        """
        toString representation of tuple
        """
        return self.q.__str__()

    # --- Saving the file --- #

    def save(self, name):
        """
        Save a pickle file of the queue data structure
        Save the tuple component
        """
        file_name = name+".pickle"
        try:
            with open(file_name, "wb") as f:
                pickle.dump(self.q, f)
            f.close()
        except FileExistsError:
            with open(file_name, "xb") as f:
                pickle.dump(self.q, f)
            f.close()
        return 0

    def load(self, name):
        """
        Loads the saved pickle file found in the dir of where the obj exists
        """
        file_name = name+".pickle"
        load_value = None
        try:
            with open(file_name, "rb") as f:
                load_value = pickle.load(f)
            f.close()
        except FileNotFoundError:
            print(file_name + " does not exits in object directory")
        self.q = load_value


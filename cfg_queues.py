class Queue:
    def __init__(self):
        self.list = []

    def put(self, value):
        self.list.append(value)

    def take(self):
        value = self.list.pop(0)
        return value

    def empty(self):
        return len(self.list) == 0


class SetQueue:
    """Queue that just enqueues if the item isn't already
    on the Queue"""
    def __init__(self, set_instance):
        self.list = []
        self.set = set_instance

    def put(self, value):
        if value not in self.set:
            self.list.append(value)
            self.set.add(value)

    def take(self):
        value = self.list.pop(0)
        self.set.remove(value)
        return value

    def empty(self):
        return len(self.list) == 0


class AdditiveDictQueue:
    """When enqueueing items with keys already in the Queue, adds both values"""
    def __init__(self):
        self.list = []
        self.dict = {}

    def put(self, value):
        if value[0] in self.dict:
            self.dict[value[0]].extend(value[1])
        else:
            self.list.append(value[0])
            self.dict[value[0]] = value[1]

    def take(self):
        string = self.list.pop(0)
        derivations = self.dict.pop(string)
        return string, derivations

    def empty(self):
        return len(self.list) == 0


class ConservativeDictQueue:
    """When enqueueing items with keys already in the Queue, maintains the old value"""
    def __init__(self):
        self.list = []
        self.dict = {}

    def put(self, value):
        if value[0] not in self.dict:
            self.list.append(value[0])
            self.dict[value[0]] = value[1]

    def take(self):
        string = self.list.pop(0)
        derivations = self.dict.pop(string)
        return string, derivations

    def empty(self):
        return len(self.list) == 0


class CountSet:
    """a set_instance that count the number of occurrences of an item.
    made to be used with cfg_string_gen.
    Since the string generation is a Queue, to generate new strings,
    one has to be removed. This one is stored in last_removed and it's
    used to preserve the number of occurrences of a string when generating
    while still returning a string from take()"""
    last_removed = ('', 1)

    def __init__(self):
        self.dict = {}

    def add(self, value):
        try:
            self.dict[value] += self.last_removed[1]
        except KeyError:
            self.dict[value] = self.last_removed[1]

    def remove(self, value):
        CountSet.last_removed = (value, self.dict.pop(value))
    
    def insert(self, value):
        """This method is called only by cfg_string_gen, never by SetQueue"""
        self.dict[value] = self.last_removed[1]

    def __contains__(self, value):
        # an add() has been called on SetQueue
        # increase count if item already on the set_instance
        if value in self.dict:
            self.add(value)
            return True
        return False

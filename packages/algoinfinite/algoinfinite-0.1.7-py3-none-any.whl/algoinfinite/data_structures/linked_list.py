class Node:
    """A node in a linked list."""
    
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """Simple implementation of a singly linked list."""
    
    def __init__(self):
        self.head = None
        self.size = 0
        
    def append(self, data):
        """Add a node to the end of the list."""
        new_node = Node(data)
        
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
            
        self.size += 1

    def display(self):
        """Display the linked list."""
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")

    def remove(self, data):
        """Remove a node from the list."""
        current = self.head
        previous = None
        
        while current and current.data != data:
            previous = current
            current = current.next
        
        if not current:
            return
        if previous:
            previous.next = current.next
        else:
            self.head = current.next
        self.size -= 1

    def find(self, data):
        """Find a node in the list."""
        current = self.head
        
        while current:
            if current.data == data:
                return current
            current = current.next
        
        return None
    
    def insert_after(self, prev_node_data, data):
        """Insert a node after a given node."""
        current = self.head
        
        while current and current.data != prev_node_data:
            current = current.next
        
        if not current:
            return
        
        new_node = Node(data)
        new_node.next = current.next
        current.next = new_node
        self.size += 1

    def insert_before(self, next_node_data, data):
        """Insert a node before a given node."""
        current = self.head
        previous = None
        
        while current and current.data != next_node_data:
            previous = current
            current = current.next
        
        if not current:
            return
        
        new_node = Node(data)
        
        if previous:
            previous.next = new_node
        else:
            self.head = new_node
        
        new_node.next = current
        self.size += 1

    def pop(self):
        """Remove the last node from the list."""
        if not self.head:
            return None
        
        current = self.head
        previous = None
        
        while current.next:
            previous = current
            current = current.next
        
        if previous:
            previous.next = None
        else:
            self.head = None
        
        self.size -= 1
        return current.data
    
    def pop_first(self):
        """Remove the first node from the list."""
        if not self.head:
            return None
        
        popped_data = self.head.data
        self.head = self.head.next
        self.size -= 1
        return popped_data
    
    def pop_at(self, index):
        """Remove a node at a specific index."""
        if index < 0 or index >= self.size:
            return None
        
        current = self.head
        previous = None
        
        for _ in range(index):
            previous = current
            current = current.next
        
        if previous:
            previous.next = current.next
        else:
            self.head = current.next
        
        self.size -= 1
        return current.data
    
    def clear(self):
        """Clear the linked list."""
        self.head = None
        self.size = 0
        
    def prepend(self, data):
        """Add a node to the beginning of the list."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
        
    def __len__(self):
        return self.size
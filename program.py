import os

class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def heapify(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self.queue) and self.queue[left] < self.queue[smallest]:
            smallest = left
        if right < len(self.queue) and self.queue[right] < self.queue[smallest]:
            smallest = right

        if smallest != index:
            self.queue[index], self.queue[smallest] = self.queue[smallest], self.queue[index]
            self.heapify(smallest)

    def push(self, node):
        self.queue.append(node)
        current = len(self.queue) - 1
        parent = (current - 1) // 2

        while current > 0 and self.queue[current] < self.queue[parent]:
            self.queue[current], self.queue[parent] = self.queue[parent], self.queue[current]
            current = parent
            parent = (current - 1) // 2

    def pop(self):
        if len(self.queue) == 1:
            return self.queue.pop()

        root = self.queue[0]
        self.queue[0] = self.queue.pop()
        self.heapify(0)
        return root

    def __len__(self):
        return len(self.queue)

def calculate_frequencies(text):
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    return frequency

def build_huffman_tree(text):
    frequency = calculate_frequencies(text)
    priority_queue = PriorityQueue()

    for char, freq in frequency.items():
        priority_queue.push(Node(char, freq))

    while len(priority_queue) > 1:
        x = priority_queue.pop()
        y = priority_queue.pop()
        z = Node(freq=x.freq + y.freq)
        z.left = x
        z.right = y
        priority_queue.push(z)

    return priority_queue.pop()

def build_codes(node, prefix="", codes=None):
    if codes is None:
        codes = {}

    if node.char is not None:
        codes[node.char] = prefix
    else:
        if node.left:
            build_codes(node.left, prefix + "0", codes)
        if node.right:
            build_codes(node.right, prefix + "1", codes)

    return codes

def encode_text(text, codes):
    return ''.join(codes[char] for char in text)

def save_to_file(encoded_text, codes, output_file):
    try:
        with open(output_file, "wb") as f:
            encoded_data = int(encoded_text, 2).to_bytes((len(encoded_text) + 7) // 8, byteorder='big')
            f.write(encoded_data)

        with open(output_file + ".dict", "w") as f:
            f.write(str({"codes": codes, "length": len(encoded_text)}))
    except IOError as e:
        print(f"Error saving files: {e}")

def decode_file(encoded_file, codes_file, output_file):
    try:
        with open(encoded_file, "rb") as f:
            encoded_data = f.read()

        with open(codes_file, "r") as f:
            data = eval(f.read())
            codes = data["codes"]
            length = data["length"]

        encoded_text = bin(int.from_bytes(encoded_data, byteorder='big'))[2:].zfill(length)

        reversed_codes = {v: k for k, v in codes.items()}
        decoded_text = ""
        buffer = ""

        for bit in encoded_text:
            buffer += bit
            if buffer in reversed_codes:
                decoded_text += reversed_codes[buffer]
                buffer = ""

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(decoded_text)
    except (IOError, ValueError, KeyError) as e:
        print(f"Error decoding files: {e}")

def main():
    input_file = input("Enter the input file name: ")
    encoded_file = "encoded.bin"
    decoded_file = "decoded.txt"

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()

        huffman_tree = build_huffman_tree(text)
        codes = build_codes(huffman_tree)
        encoded_text = encode_text(text, codes)
        save_to_file(encoded_text, codes, encoded_file)

        decode_file(encoded_file, encoded_file + ".dict", decoded_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except IOError as e:
        print(f"Error reading/writing files: {e}")

if __name__ == "__main__":
    main()

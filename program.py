import os

class TreeNode:
    def __init__(self, symbol=None, frequency=0):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

class MinHeap:
    def __init__(self):
        self.heap = []

    def heapify(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self.heapify(smallest)

    def push(self, node):
        self.heap.append(node)
        current = len(self.heap) - 1
        parent = (current - 1) // 2

        while current > 0 and self.heap[current] < self.heap[parent]:
            self.heap[current], self.heap[parent] = self.heap[parent], self.heap[current]
            current = parent
            parent = (current - 1) // 2

    def pop(self):
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify(0)
        return root

    def __len__(self):
        return len(self.heap)

def count_frequencies(text):
    frequency_map = {}
    for char in text:
        if char in frequency_map:
            frequency_map[char] += 1
        else:
            frequency_map[char] = 1
    return frequency_map

def create_huffman_tree(text):
    frequency_map = count_frequencies(text)
    min_heap = MinHeap()

    for char, freq in frequency_map.items():
        min_heap.push(TreeNode(char, freq))

    while len(min_heap) > 1:
        left = min_heap.pop()
        right = min_heap.pop()
        merged_node = TreeNode(frequency=left.frequency + right.frequency)
        merged_node.left = left
        merged_node.right = right
        min_heap.push(merged_node)

    return min_heap.pop()

def generate_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}

    if node.symbol is not None:
        code_map[node.symbol] = prefix
    else:
        if node.left:
            generate_codes(node.left, prefix + "0", code_map)
        if node.right:
            generate_codes(node.right, prefix + "1", code_map)

    return code_map

def encode(text, code_map):
    return ''.join(code_map[char] for char in text)

def save_encoded_data(encoded_text, code_map, file_name):
    try:
        with open(file_name, "wb") as f:
            encoded_data = int(encoded_text, 2).to_bytes((len(encoded_text) + 7) // 8, byteorder='big')
            f.write(encoded_data)

        with open(file_name + ".dictionary", "w") as f:
            f.write(str({"code_map": code_map, "length": len(encoded_text)}))
    except IOError as e:
        print(f"Problem with saving files: {e}")

def decode_from_file(encoded_file, dictionary_file, output_file):
    try:
        with open(encoded_file, "rb") as f:
            encoded_data = f.read()

        with open(dictionary_file, "r") as f:
            data = eval(f.read())
            code_map = data["code_map"]
            length = data["length"]

        encoded_text = bin(int.from_bytes(encoded_data, byteorder='big'))[2:].zfill(length)

        reversed_map = {v: k for k, v in code_map.items()}
        decoded_text = ""
        buffer = ""

        for bit in encoded_text:
            buffer += bit
            if buffer in reversed_map:
                decoded_text += reversed_map[buffer]
                buffer = ""

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(decoded_text)
    except (IOError, ValueError, KeyError) as e:
        print(f"Error while decoding files: {e}")

def main():
    input_file = input("Please provide the name of the input file: ")
    encoded_file = "encoded_output.bin"
    decoded_file = "decoded_output.txt"

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()

        huffman_tree = create_huffman_tree(text)
        code_map = generate_codes(huffman_tree)
        encoded_text = encode(text, code_map)
        save_encoded_data(encoded_text, code_map, encoded_file)

        decode_from_file(encoded_file, encoded_file + ".dictionary", decoded_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except IOError as e:
        print(f"Problem with reading or writing files: {e}")

if __name__ == "__main__":
    main()

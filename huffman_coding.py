"""Huffman Puffman."""
import heapq
from graphviz import Digraph
from collections import Counter

def encode_message(message):
    """
    Convert the String to a Fixed 8 bit binary
    ord(character) -> Unicode -> 08b binary
    """
    return ("".join(f"{ord(i):08b}" for i in message))

def decode_message(binary):
    """
    Convert 8 bit binary stream to string
    int(08 Binary, 2) -> chr(Unicode) -> String
    """
    binary_stream = [binary[bit:bit+8] for bit in range(0, len(binary), 8)]
    return str(''.join([chr(int(byte, 2)) for byte in binary_stream]))

"""
Since high frequency characters are more important
A perfect implementation candidate is a priority queue 
https://docs.python.org/3/library/heapq.html
"""

class HuffmanCode(object):
    """
    Generate Huffman Code
    """
    def __init__(self, message):
        self.message = message
        self.characters = [char for char in message]
        self.symbols = Counter(self.characters)
        dot = Digraph(comment='Huffman Tree')
        char_count = Counter(self.characters)
        mapping = dict.fromkeys(char_count.keys(),'')
        hq = []
        for key, value in char_count.items():
            heapq.heappush(hq, (value, key))
        while len(hq) > 1:
            freq_left, character_left = heapq.heappop(hq)
            freq_right, character_right = heapq.heappop(hq)

            for left in character_left:
                mapping[left] = '0' + mapping[left]

            for right in character_right:
                mapping[right] = '1' + mapping[right]

            
            dot.node(f'{character_left}', f'{freq_left}-{character_left}')
            dot.node(f'{character_right}', f'{freq_right}-{character_right}')

            freq_sum =freq_left + freq_right
            character_sum = f'{character_left}{character_right}'
            dot.node(character_sum, f'{freq_sum}-{character_sum}')

            dot.edge(character_sum, f'{character_right}')
            dot.edge(character_sum, f'{character_left}')
            heapq.heappush(hq, (freq_sum, character_sum))
        self.mapping = mapping
        self.graph = dot 

    @property
    def tree(self):
        return self.graph

    @property
    def binary_map(self):
        return self.mapping

    def encode(self):
        encoded_binary = ''
        binary_map = self.mapping
        for symbol in self.characters:
            encoded_binary+=binary_map[symbol]
        return encoded_binary

    def decode(self, bits):
        _mapping = {v: k for k, v in self.mapping.items()}
        decoded_string = ''
        index = 0
        while index < 20:
            part = bits[:index]
            if part in _mapping:
                bits = bits[index:]
                index = 0
                decoded_string+=_mapping[part]
            else:
                index+=1
        return decoded_string


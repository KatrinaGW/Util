CONTENTS OF THIS FILE

* Introduction

* Requirements

* Running Instructions


INTRODUCTION

util.py will use Huffman compression to compress and decompress a file. This will be accomplished by using a Huffman Tree specifically generated for the file that needs to be decoded/encoded. Note that this program will not generate the Huffman Tree. 

REQUIREMENTS

The following files/modules must be imported to run util.py:

* bitio.py : A program containing a BitReader class and a BitWriter class. 

* huffman.py : A program that can generate a huffman tree object which has the encoding for a given file

* pickle : The standard Python Pickle module to serialize and deserialize Python objects. 

Note that the bitio.py and huffman.py files are not included in this repository because I did not make them and I do not have permission to upload them. 


RUNNING INSTRUCTIONS

* Ensure that util.py, bitio.py, and huffman.py are in the same directory. 

* To compress a file using its Huffman Tree the compress function in util.py must be called. The function paramenters are the Huffman Tree, the uncompressed file stream, and the file stream which the compressed data will be written to. All of the mentioned files must be in the same directory as util.py. Note that the program will not check that the Huffman Tree contains the correct encoding for the uncompressed file stream. 

* To decompress a pickle file, the decompress function in util.py must be called. The function paramenters are the compressed file stream, containing the encoded data and Pickled Huffman tree, and the uncompressed file stream which the decoded data will be written to. All of the mentioned files must be in the same directory as util.py.

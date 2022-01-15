# ---------------------------------------------------
# GitHub username : KatrinaGW
#
# Consultations: None
# ---------------------------------------------------

from bitio import*
from huffman import*
import pickle


def read_tree(tree_stream):
    '''Read a description of a Huffman tree from the given compressed
    tree stream, and use the pickle module to construct the tree object.
    Then, return the root node of the tree itself.

    Args:
      tree_stream (file object handle): The compressed stream to read the tree
                                         from, assumed to have been opened 
                                         with the "rb" permission

    Returns:
      A Huffman tree root constructed according to the given description.
    '''

    #Construct the root node of the tree object in the compressed file
    tree = pickle.load(tree_stream)

    return tree


def decode_byte(tree, bitreader): 
    """
    Continuously read bits from the bit reader as left or right directions to
    take in a tree. Once a tree leaf has been reached, cease reading bits
    and return the value of the leaf. 

    Args:
      bitreader (BitReader): An instance of bitio.BitReader with the tree 
      to read from tree (Huffman Tree): A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.
    """

    #Instantiate the value to hold the next byte of the compressed bit stream
    value = None

    continueLooping = True

    #Read the next bit from the bit reader
    nextBit = bitreader.readbit()

    #If the current tree is a branch, use the next bit as a direction
    #to take in the tree, True is right, False is left
    if(isinstance(tree, TreeBranch)):
      node = tree
      #Continue looping through the bitreader's compressed
      #bit stream until a tree leaf is reached
      while(continueLooping):
        if(nextBit):
          nextValue = node.getRight()
        else:
          nextValue = node.getLeft()
        #Once the tree leaf has been located, get its value because it is the
        #next byte of the bit stream
        if(isinstance(nextValue, TreeLeaf)):
          value = nextValue.getValue()
          #Terminate the loop because the next byte has been found
          continueLooping=False
        else:
          #If a leaf hasn't been found yet, move the current node to the next
          #node that was confirmed to be a branch, and then read the next bit
          node = nextValue
          nextBit = bitreader.readbit()
    else:
      #If the first tree was a leaf, get its value because it is the next byte
      #of the compressed bit stream
      value = tree.getValue()

    return value


def decompress(compressed, uncompressed):
    ''' Decompress a given file to get a Huffman tree and a compressed
    bit stream, whose encoding corresponds to the one in the Huffman tree.
    Then write the decoded bit stream to the uncompressed file stream

    Args:
      compressed (file object): A file stream from which compressed input,
                                the Huffman tree and encoded bit stream,
                                is read.
      uncompressed: A writable file stream to which the uncompressed
                    output is written.
    '''
    
    #Construct the tree object from the compressed file 
    tree = read_tree(compressed)
    
    #Instantiate the BitReader to read from the compressed file, 
    #and the BitWriter to write to the uncompressed file
    reader = BitReader(compressed)
    writer = BitWriter(uncompressed)

    #Assume that the next byte of the stream is None, and 
    #set the while loop to continue decoding the BitReader's
    # next byte  until the end of the file is reached, or a None 
    #sentinel value is decoded
    nextByte = None
    continueLooping=True
    while continueLooping:
      try:
        nextByte = decode_byte(tree, reader)
        if(nextByte is not None):
          #Write the decoded byte value to the uncompressed file
          writer.writebits(nextByte, 8)
        else:
          continueLooping=False
      except EOFError:
        continueLooping=False

    #Make sure to flush the writer to get it to finish 
    #writing any bits it had been storing
    writer.flush()


def write_tree(tree, tree_stream):
    '''Write the specified Huffman tree to the given tree_stream
    using the pickle module. 

    Args:
      tree (A Huffman Tree): A Huffman tree to write to the file
      tree_stream (Binary File): The binary file to write the tree to.
    '''

    #Write the given tree to the given binary file
    pickle.dump(tree, tree_stream) 

def writeEnd(writer, count, table):
  """ Encode a None value at the end of a a compressed
  binary file

  Arguments:
    writer (BitWriter): The writer with the compressed binary file
    count (int): The current number of bits written to the file
    table (Dictionary): An encoding table for the data, the keys
                          are the data, and their values are their
                          encoding
    Returns:
      None
  """

  #Encode a None value at the end of the 
  #compressed file's bits using its encoding, made up of 1's and
  #0's, from the encoding table
  path = table[None]
  for choice in path:
    writer.writebit(choice)
    #Continue keeping track of how many bits are in the file
    count+=1


  #Check if all the bytes in the file
  #are complete, if not, write False
  #bits after the None value's bits, 
  #until no fractional bytes remain
  if((count%8)>0):
    for extra in range(8-(count%8)):
      writer.writebit(False)
    writer.flush()

def encodeStream(reader, writer, table):
  """ Encode a bit stream from a bit reader using a given
  encoding table and a bit writer

  Arguments:
    reader (BitReader) : An instance of class BitReader to read the
                          file stream from
    writer (BitWriter) : An instance of class BitWriter to write the 
                          encoded file data and Huffman tree to
    table (Dictionary) : A table to use for encryption, the
                          values are the encoding to use for
                          the objects to which they're keyed
  Returns:
    None
  """

  #Initiate a counter for the number of bits written
  count = 0

  #Write the values of the bytes of the bitreader's file stream to
  #the bitwriters file stream using the value's encoding, until there
  #are no bytes left in the bitreader. 
  continueLooping=True
  while continueLooping:
    #Try to read the next byte from the bit reader
    try:
      #Using the encoding table, get the encoding of 
      #the value stored in the next byte
      value = reader.readbits(8)
      path = table[value]
      #Write the encoding, made of 1's and 0's, to the bitwriter
      #file stream
      for choice in path:
        writer.writebit(choice)
        count+=1

    #At the end of the file, encode a None value
    #and add enough False bits to ensure that all
    #bytes in the file are fully written
    except EOFError:
      writeEnd(writer, count, table) 
      continueLooping=False
      writer.flush()
  writer.flush()


def compress(tree, uncompressed, compressed):
    '''Write the given tree to the compressed stream
    and encode the uncompressed data to the same 
    compressed stream in a complete number of 
    bytes. 

    Args:
      tree (Huffman Tree): A Huffman tree to use for encoding the 
                            uncompressed file
      uncompressed (file object stream): A file stream from which which
                                          to read the data from, assumed
                                          to have been opened in binary mode
      compressed (file object stream): A file stream to write the tree
                                        description and coded input data,
                                        assumed to have been opened in
                                        binary mode
    '''

    #Write the given tree to the compressed file
    write_tree(tree, compressed)

    #Create a new BitWriter to write to the binary compressed file
    writer = BitWriter(compressed)
    #Create a new BitReader to read from the binary uncompressed file
    reader = BitReader(uncompressed)

    #Get the tree's encoding table to use to encode the uncompressed 
    #file stream
    table = make_encoding_table(tree)
    encodeStream(reader, writer, table)

    #Flush the writer to ensure that all the bits were fully written. 
    writer.flush()


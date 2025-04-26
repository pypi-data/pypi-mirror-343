from .services.compression_core.encoding_and_decoding import EncodeDecode
from .services.compression_core.padding import Padding

class Decompress:
    """
    A class to handle file decompression using Huffman coding.
    """

    def __init__(self, file_content: str) -> None:
        """
        Initializes the Decompress class with the binary string.

        Args:
            file_content (str): The binary string to be decompressed.
        """
        self.file_content = file_content

    def decompress(self) -> str:
        """
        Decompresses the binary string back to its original content.

        Returns:
            str: The decompressed file content.
        """
        file_content, encoded_dictionary = Padding(self.file_content).remove_padding()
        decoded_dictionary = EncodeDecode(file_content, encoded_dictionary).decode_dictionary()
        decoded_data = EncodeDecode(file_content, decoded_dictionary).decode()
        return decoded_data
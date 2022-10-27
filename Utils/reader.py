from collections import Iterable


class Reader:

    @staticmethod
    def read_in_chunks(file_object, chunk_size: int = 1024) -> Iterable:
        """ Yields data line by line """
        while True:
            data = file_object.readline(chunk_size)
            if not data:
                break
            yield data

    def read_contents(self, path: str, chunk_size: int = 1024) -> Iterable:
        """ Yields lines """
        with open(path, 'r', encoding='utf-8') as reader:
            yield from self.read_in_chunks(reader, chunk_size)

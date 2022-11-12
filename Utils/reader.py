from dataclasses import dataclass
from typing import Iterable


@dataclass
class Reader:
    path: str
    chunk_size: int = 1024

    def read_in_chunks(self, file_object) -> Iterable:
        """
        Yields data line by line

        :concern: 1024 might not cover a function fully.
        """
        while True:
            data = file_object.readline(self.chunk_size)
            if not data:
                break
            yield data

    def read_contents(self) -> Iterable:
        """Yields lines"""
        with open(self.path, "r", encoding="utf-8") as reader:
            yield from self.read_in_chunks(reader)

    def read_in_string(self) -> str:
        """
        Returns string version of the file contents

        :returns file_content_as_string: string version of the file contents
        """
        with open(self.path, "r", encoding="utf-8") as reader:
            file_content_as_string = reader.read()
        return file_content_as_string

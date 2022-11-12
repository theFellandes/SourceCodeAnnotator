from dataclasses import dataclass, field


@dataclass
class Writer:
    path: str
    buffer: list = field(init=False, default_factory=list)

    def write_append(self, write_context: str) -> None:
        """Appends data line by line"""
        with open(self.path, "a") as sink:
            sink.write(write_context)

    def write_overwrite(self, write_context: str) -> None:
        """Overwrites data and writes line by line"""
        with open(self.path, "w") as sink:
            sink.write(write_context)

    def clear_content(self) -> None:
        """Clears the file data"""
        with open(self.path, "w") as clear:
            clear.write("")

    def buffered_writer(self) -> None:
        """Writes from buffer"""
        with open(self.path, "w") as sink:
            sink.writelines(self.buffer)

    def append_buffer(self, buffer_context: str) -> None:
        """Appends to the buffer object list"""
        self.buffer.append(str(buffer_context))

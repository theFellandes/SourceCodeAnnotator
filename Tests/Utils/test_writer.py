import pytest

from conf import settings
from Utils.writer import Writer


@pytest.fixture
def mock_report():
    mock_report = [
        "Main.java Report\n",
        "\n",
        "Source Code Annotator took: 0.012 seconds\n",
        "There are:\n",
        "\n",
        "* 1234 Single Line Comments\n",
        "* 1234 Multi Line Comments\n",
        "* 1234 Javadoc Comments\n",
        "* 1234 Total Lines of Comments\n",
        "\n",
        "** The Most Used Comment Type: Javadoc **\n",
        "** The Least Used Comment Type: Single Line **\n",
        "* Average Single Line Comment Usage is Lower than project > Suggestion: Add some comments\n",
        "* Average Multi Line Comment Usage is on par with project\n",
        "* Average Javadoc Comment Usage is Lower than project > Suggestion: Remove some comments\n",
        "* Average Total Lines is Lower than project > Suggestion: Create some classes",
    ]
    return mock_report


@pytest.fixture
def writer():
    return Writer(settings.REPORT_PATH)


def test_buffered_writer(writer, mock_report):
    writer.buffer = mock_report
    writer.buffered_writer()


def test_writer(writer, mock_report):
    writer.clear_content()
    for line in mock_report:
        writer.write_append(line)


def test_buffered_writer_with_numbers(writer):
    buffer = [1, 2, 3, 4, 5]
    for item in buffer:
        writer.append_buffer(item)
    writer.buffered_writer()

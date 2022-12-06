import stanza
from stanza.pipeline.core import DownloadMethod
from re import finditer

from conf import settings



class NameAnalyzer:
    def __init__(self):
        if settings.is_path_empty(settings.STANZA_RESOURCES_PATH):
            stanza.download()
        self.nlp = stanza.Pipeline('en',
                                   verbose=False,
                                   download_method=DownloadMethod.REUSE_RESOURCES,
                                   model_dir='.\\Stanza')

    def parse_function_name(self, function_name: str):
        splunk_function_name = self.split_function_name(function_name)
        doc = self.nlp(splunk_function_name)
        print(doc)


    def split_function_name(self, function_name: str) -> str:
        if '_' in function_name:
            function_word_list = function_name.split('_')
        else:
            function_word_list = self.camel_case_split(function_name)
        return ' '.join(function_word_list)

    @staticmethod
    def camel_case_split(identifier) -> list[str]:
        matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
        return [m.group(0) for m in matches]


if __name__ == '__main__':
    na = NameAnalyzer()
    na.parse_function_name('getUserId')
    na.parse_function_name('getAnotherUserId')
    na.parse_function_name('nameAnalyser')

import stanza
from stanza.pipeline.core import DownloadMethod
from re import finditer

from conf import settings


class NameAnalyzer:
    def __init__(self):
        if not settings.does_path_exists(settings.STANZA_RESOURCES_PATH) or settings.is_path_empty(
                settings.STANZA_RESOURCES_PATH):
            stanza.download(model_dir='.\\Stanza')
        self.nlp = stanza.Pipeline('en',
                                   verbose=False,
                                   download_method=DownloadMethod.REUSE_RESOURCES,
                                   model_dir='.\\Stanza')

    def get_generated_comment(self, name: str) -> str:
        splunk_name = self.split_function_name(name)
        doc = self.nlp(splunk_name)
        return self.generate_comment(doc.sentences)

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

    @staticmethod
    def generate_comment(sentences: list) -> str:
        string_builder = ''
        for sentence in sentences:
            for word in sentence.words:
                if word.pos == 'VERB':
                    string_builder += f'{word.text.capitalize()}s '
                else:
                    string_builder += f'{word.text.capitalize()} '
        return string_builder


if __name__ == '__main__':
    na = NameAnalyzer()
    # na.parse_function_name('getUserId')
    # print(na.parse_function_name('getAnotherUserId'))
    # print(na.parse_function_name('nameAnalyser'))
    # print(na.get_generated_comment('getUserId'))
    print(na.get_generated_comment('setUserId'))
    print(na.get_generated_comment('userIdSetter'))

    # Beyni yanan kısımlar
    # print(na.get_generated_comment('userIdSet'))
    # print(na.get_generated_comment('generateUserId'))
    print(na.get_generated_comment('increment_number_by_one'))

    # Boss fight #
    # print(na.get_generated_comment('nameAnalyser')) # Analyses the name?
    # print(na.get_generated_comment('quickSort')) # Performs quick sort algorithm?
    # We could store generic algorithm names in a list, so that program flow
    # can be bypassed and adds that comment static.

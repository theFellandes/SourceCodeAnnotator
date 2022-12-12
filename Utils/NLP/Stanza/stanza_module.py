import itertools

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

    def get_generated_comments_list(self, class_name: str, function_name: str) -> list[str]:
        splunk_name_list = self.split_function_name(function_name)
        permutations_of_name_list = self.get_permutations_list(splunk_name_list)

        list_of_comments = []
        for permutation in permutations_of_name_list:
            doc = self.nlp(permutation)
            list_of_comments.append(self.generate_comment(class_name, doc.sentences))
        return list_of_comments

    def split_function_name(self, function_name: str) -> list[str]:
        if '_' in function_name:
            function_word_list = function_name.split('_')
        else:
            function_word_list = self.camel_case_split(function_name)
        return function_word_list

    @staticmethod
    def camel_case_split(identifier) -> list[str]:
        matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
        return [m.group(0) for m in matches]

    @staticmethod
    def get_permutations_list(list_of_words: list[str]) -> list[str]:
        return [' '.join(permutation) for permutation in itertools.permutations(list_of_words, len(list_of_words))]

    @staticmethod
    def generate_comment(class_name: str, sentences: list) -> str:
        coherent_sentence = {
            'CLASS': class_name,
            'REST': ''
        }
        for sentence in sentences:
            for word in sentence.words:
                if word.pos == 'VERB':
                    coherent_sentence[word.pos] = f'{word.text.capitalize()}'
                else:
                    coherent_sentence['REST'] = coherent_sentence.get('REST') + f'{word.text.capitalize()} '

        if coherent_sentence.get('VERB') is not None:
            return f"{coherent_sentence.get('VERB')}s {coherent_sentence.get('REST')}" \
                   f"in {coherent_sentence.get('CLASS')} class"
        return f"{coherent_sentence.get('REST').rstrip()} in {coherent_sentence.get('CLASS')} class"

if __name__ == '__main__':
    na = NameAnalyzer()
    # print(na.get_generated_comments_list('Employee', 'getUserId')) # Returns userId of Employee Class
    print(na.get_generated_comments_list('Employee', 'getUserSet'))


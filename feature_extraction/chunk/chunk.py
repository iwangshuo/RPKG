import nltk
from nltk.tag import pos_tag
from nltk import RegexpParser

class SentenceAnalyzer:
    def __init__(self, sentence):
        self.sentence = sentence
        self.tagged_sent = pos_tag(sentence.split())
        self.grammar = r"""
            Function: {<VB.*>+<CD>*<DT>?<CD>*<JJ>*<CD>*<VBD|VBG>*<NN.*>*<POS>*<CD>*<VBD|VBG>*<NN.*>*<VBD|VBG>*<NN.*>*<POS>*<CD>*<NN.*>+}
            Characteristics: {<CD>*<DT>?<CD>*<JJ>*<CD>*<VBD|VBG>*<NN.*>*<POS>*<CD>*<VBD|VBG>*<NN.*>*<VBD|VBG>*<NN.*>*<POS>*<CD>*<NN.*>+} 
            """
        self.parser = RegexpParser(self.grammar)
        self.sentence_tree = self.parser.parse(self.tagged_sent)

    def extract_function(self):
        for subtree in self.sentence_tree.subtrees():
            if subtree.label() == 'Function':
                yield ' '.join(word for word, tag in subtree.leaves())

    def function_list(self):
        return list(self.extract_function())

    def extract_characteristics(self):
        for subtree in self.sentence_tree.subtrees():
            if subtree.label() == 'Characteristics':
                yield ' '.join(word for word, tag in subtree.leaves())

    def characteristics_list(self):
        return list(self.extract_characteristics())

    def draw_tree(self):
        self.sentence_tree.draw()


if __name__ == "__main__":
    # a descriptive sentence for ros package hector_quadrotor_gazebo
    sentence = "It provides a quadrotor model for the gazebo simulator"
    analyzer = SentenceAnalyzer(sentence)

    func_list = analyzer.function_list()
    print(func_list)

    char_list = analyzer.characteristics_list()
    print(char_list)

    analyzer.draw_tree()

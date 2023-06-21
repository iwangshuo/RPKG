import nltk
from nltk.tag import pos_tag


# 提取function
def Phrase(sentence):
    # Tag sentence for part of speech
    tagged_sent = pos_tag(sentence.split())  # List of tuples with [(Word,PartOfSpeech)]
    # Define several tag patterns
    # grammar = r"""
    #         VP: {<MD>*<VB.*>+<CD>*<JJ>*<RB>*<JJ>*<VB.*>?<DT>?<IN*|TO*>+}
    #             {<MD>*<VB.*>+<JJ>*<RB>*<JJ>*<VB.*>?<DT>?<IN*|TO*>+}
    #             {<MD>*<VB.*>+<JJ>*<RB>*<JJ>*<VB.*>+}
    #             {<MD>*<VB.*>+}
    #         NP: {<CD>*<DT>?<CD>*<JJ>*<CD>*<VBD|VBG>*<NN.*>*<POS>*<CD>*<VBD|VBG>*<NN.*>*<VBD|VBG>*<NN.*>*<POS>*<CD>*<NN.*>+}
    #         VVP: {<MD>*<VB.*>+<JJ>*<RB>*<JJ>*<VB.*>?<DT>?<TO*>+<VB>+}
    #             {<MD>*<VB.*>+<JJ>*<RB>*<JJ>*<VB.*>?<DT>?<IN*>+<VBG>+}
    #         """
    grammar = r"""
            Function: {<VB.*>+<CD>*<DT>?<CD>*<JJ>*<CD>*<VBD|VBG>*<NN.*>*<POS>*<CD>*<VBD|VBG>*<NN.*>*<VBD|VBG>*<NN.*>*<POS>*<CD>*<NN.*>+}
            Category: {<CD>*<DT>?<CD>*<JJ>*<CD>*<VBD|VBG>*<NN.*>*<POS>*<CD>*<VBD|VBG>*<NN.*>*<VBD|VBG>*<NN.*>*<POS>*<CD>*<NN.*>+} 
            """
    # Function指的是动词短语，但有的动词短语不对，这是个问题，可以放进实验验证里面
    # Category指的是名词短语，除去设计Function中的动词短语中的名词短语
    # Function: {<MD>*<VB.*>+<CD>*<DT>?<CD>*<JJ>*<CD>*<VBD|VBG>*<NN.*>*<POS>*<CD>*<VBD|VBG>*<NN.*>*<VBD|VBG>*<NN.*>*<POS>*<CD>*<NN.*>+}

    cp = nltk.RegexpParser(grammar)  # Define Parser
    SentenceTree = cp.parse(tagged_sent)
    # NounPhrases = traverse(SentenceTree)  # collect Noun Phrase

    return SentenceTree
    # return (NounPhrases)


def extract_function(sentencetree):
    for subtree in sentencetree.subtrees():
        if subtree.label() == 'Function': # 这里就不是NP了。而是自己定义的名字
            yield ' '.join(word for word, tag in subtree.leaves())


def function_list(sentence):
    func_list = []
    for funcstr in extract_function(Phrase(sentence)):
        func_list.append(funcstr)
    return func_list

def extract_category(sentencetree):
    for subtree in sentencetree.subtrees():
        if subtree.label() == 'Category': # 这里就不是NP了。而是自己定义的名字
            yield ' '.join(word for word, tag in subtree.leaves())

def category_list(sentence):
    cate_list = []
    for catestr in extract_category(Phrase(sentence)):
            cate_list.append(catestr)
    return cate_list


if __name__ == "__main__":
    sentence = "PyTables is built on top of the HDF5 library, using the Python language and the NumPy package."
    sentence1 = "RealSense Camera description package for Intel 3D D400 cameras"
    sentence2 = "The turtlebot3_navigation provides roslaunch scripts for starting the navigation"
    sentence3 = "Outputs audio to a speaker from a source node."
    sentence4 = "Test package for khi_robot"


    # func_list = function_list(sentence2)
    # print(func_list)
    # cate_list = category_list(sentence2)
    # print(cate_list)
    # Function = Phrase(sentence2)
    # Function.draw()  # draw()函数要放在最后，draw()函数执行之后就执行完了，放在前面可能导致之后的函数无法执行到

    sentence_rpldiar = "The rplidar ros package, support rplidar A2/A1 and A3/S1"
    func_list = function_list(sentence_rpldiar)
    print(func_list)
    cate_list = category_list(sentence_rpldiar)
    print(cate_list)
    Function = Phrase(sentence_rpldiar)
    Function.draw()  # draw()函数要放在最后，draw()函数执行之后就执行完了，放在前面可能导致之后的函数无法执行到

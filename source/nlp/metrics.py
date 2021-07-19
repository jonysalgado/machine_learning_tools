#-------------------------------------------------------------------------------
# Importations
.nlp import NLP_base
import language_tool_python
from collections import Counter
from nltk.translate.bleu_score import sentence_bleu 

#-------------------------------------------------------------------------------
# Class Metrics

class Metrics(NLP_base):
    def __init__(self, language):
        super().__init__(language)
        #TODO: check if the language exists on language_tool_python
        self.tool = language_tool_python.LanguageTool(language)

    def analyse_errors(self, text, except_words):
        self.analyse_errors = Analyse_errors(self.tool, text, except_words)
        return self.analyse_errors

    def errors_score(self, query, except_words, only_speel_error=True,
                mean="only"):

        self.errors_metric = Errors_metric(self.tool)
        return self.errors_metric.score(query, except_words, only_speel_error, mean)

    def mapper_errors(self, matches):
        self._mapper_errors = Mapper_errors()
        self._mapper_errors.update(matches)

        return self._mapper_errors.counter_matches

    def MBR_score(self, query):
        self.mbr = MBR()
        return self.mbr.score(query)
    




#-------------------------------------------------------------------------------
# Class Analyse_errors

class Analyse_errors:
  def __init__(self, tool, text, except_words):
    self.tool = tool
    self.text = text
    self.except_words = except_words
    self.errors = []
    self.speel_errors = []
  
    self.check_speel_text()

  def get_errors(self, only_speel_errors=True):
    if only_speel_errors:
      return self.speel_errors
    else:
      return self.errors
    
  def check_speel_text(self):
    self.errors = self.tool.check(self.text)
    errors = []
    for error in self.errors:
      offset = error.offset
      errorLength = error.errorLength
      word = self.text[offset:offset+errorLength]
      if word not in self.except_words and error.ruleId == 'HUNSPELL_RULE':
        errors.append(error)
    self.speel_errors = errors  

  def score(self, only_speel_error=True, mean="both"):
    if only_speel_error:
      e = len(self.speel_errors)
    else:
      e = len(self.errors)
    if mean == "only":
      return e/len(self.text.split(" "))
    elif mean == "not":
      return e
    else:
      return e/len(self.text.split(" ")), e

  def corrections(self):
    dict_corrections = {}
    for error in self.speel_errors:
      offset = error.offset
      errorLength = error.errorLength
      replacements = error.replacements
      word = self.text[offset:offset+errorLength]
      dict_corrections[word] = replacements  
    return dict_corrections


#-------------------------------------------------------------------------------
# Class Errors_metric

class Errors_metric:
  def __init__(self, tool):
    self.scores = None
    self. tool = tool

  def score(self, query, except_words=[], only_speel_error=True, mean="only"):
    scores = np.zeros(len(query))
    for i in range(len(query)):
      scores[i] = self._score(query[i], except_words, only_speel_error, mean)

    self.score = scores
    return scores

  def _score(self, text, except_words, only_speel_error, mean):
    analyser = Analyse_errors(self.tool, text, except_words)
    return analyser.score(only_speel_error, mean)


class mapper_errors:
  def __init__(self):
    self.counter_matches = Counter()
    self.list_matches = []

  def update(self, matches):
    for match in matches:
      if match.ruleId not in sorted(self.counter_matches.elements()):
        self.list_matches.append(match)
      self.counter_matches.update([match.ruleId])

#-------------------------------------------------------------------------------
# MBR

class MBR:
  def __init__(self):
    self.scores = None

  def score(self, query):
    scores = np.zeros(len(query))
    for i in range(len(query)):
      compared = query[i]
      query_without_compared = query.copy()
      query_without_compared.remove(compared)
      scores[i] = self._score(compared, query_without_compared)

    self.scores = scores
    return scores
      
  def _score(self, compared, query_without_compared):
    similarity = 0
    for i in range(len(query_without_compared)):
      reference = query_without_compared[i]
      similarity += sentence_bleu(reference, compared)

    return similarity/len(query_without_compared)
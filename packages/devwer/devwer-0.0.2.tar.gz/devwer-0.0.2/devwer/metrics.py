from difflib import SequenceMatcher
from devwer.normalizer import Normalizer
import numpy as np
import Levenshtein as lev

class Metrics:
    def __init__(self,type='wer'):
        self.normalizer = Normalizer()

    def cer(self, reference, hypothesis):
        """
        Calculate the Character Error Rate (CER) for Devanagari text.
        :param reference: The correct reference text.
        :param hypothesis: The text to evaluate.
        :return: The CER as a float.
        """
        # Convert texts to character lists (strings are iterable, so no need to tokenize further)
        ref_chars = self.normalizer.tokenize_for_cer(reference)
        hyp_chars = self.normalizer.tokenize_for_cer(hypothesis)

        # Calculate the edit distance between reference and hypothesis
        edits = lev.distance(''.join(ref_chars), ''.join(hyp_chars))
        return edits / len(ref_chars) if len(ref_chars) > 0 else 0.0

    def wer(self, reference, hypothesis):
        """
        Calculate the Word Error Rate (WER) for Devanagari text.
        :param reference: The correct reference text.
        :param hypothesis: The text to evaluate.
        :return: The WER as a float.
        """
        # Tokenize texts by splitting on spaces
        # ref_tokens = reference.split()
        # hyp_tokens = hypothesis.split()
        ref_tokens = self.normalizer.tokenize_for_wer(reference)
        hyp_tokens = self.normalizer.tokenize_for_wer(hypothesis)

        
        # Use SequenceMatcher to calculate WER
        matcher = SequenceMatcher(None, ref_tokens, hyp_tokens)
        edits = sum(tag != 'equal' for tag, _, _, _, _ in matcher.get_opcodes())
        return edits / len(ref_tokens) if len(ref_tokens) > 0 else 0.0

    def wer_legacy(self, reference, hypothesis):
            ref_tokens = self.normalizer.tokenize_for_wer(reference)
            hyp_tokens = self.normalizer.tokenize_for_wer(hypothesis)
            d = np.zeros((len(ref_tokens) + 1, len(hyp_tokens) + 1), dtype=np.uint8)

            for i in range(len(ref_tokens) + 1):
                d[i][0] = i
            for j in range(len(hyp_tokens) + 1):
                d[0][j] = j

            for i in range(1, len(ref_tokens) + 1):
                for j in range(1, len(hyp_tokens) + 1):
                    if ref_tokens[i - 1] == hyp_tokens[j - 1]:
                        substitution_cost = 0
                    else:
                        substitution_cost = 1
                    
                    d[i][j] = min(
                        d[i - 1][j] + 1,
                        d[i][j - 1] + 1,
                        d[i - 1][j - 1] + substitution_cost
                    )

            wer_value = d[len(ref_tokens)][len(hyp_tokens)] / float(len(ref_tokens))
            wer_value = wer_value.item()
            return wer_value if wer_value > 0 else 0.0
    
    def tokenize(self,type,sentence):
        if(type == 'wer'):
            return self.normalizer.tokenize_for_wer(sentence)
        elif(type == 'cer'):
            return self.normalizer.tokenize_for_cer(sentence)
        else:
            return ['SELECT','CER','OR','WER']
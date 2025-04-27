import re
import unicodedata

class Normalizer:
    def __init__(self):
        self.halant = '्'
        self.vowel_signs = {'ि', 'ी', 'ु', 'ू', 'ृ', 'े', 'ै', 'ो', 'ौ', 'ं'}
        self.pre_base_vowels = {'ि'}
        self.nasal_consonants = "ङञणनम"
        self.valid_devanagari = re.compile(r'[\u0900-\u097F]+')
        self.number_map = str.maketrans({
            '0': '०',
            '1': '१',
            '2': '२',
            '3': '३',
            '4': '४',
            '5': '५',
            '6': '६',
            '7': '७',
            '8': '८',
            '9': '९',
        })

    def normalize_unicode(self, sentence):
        """Apply NFC normalization and remove zero-width characters."""
        sentence = unicodedata.normalize('NFC', sentence)
        sentence = re.sub(r'[\u200B-\u200D\uFEFF]', '', sentence)
        return sentence

    def normalize_numbers(self, sentence):
        """Convert English digits to Nepali digits."""
        return sentence.translate(self.number_map)

    def remove_non_devanagari(self, sentence):
        """Remove all non-Devanagari characters except spaces and Nepali digits."""
        return ''.join(ch for ch in sentence if self.valid_devanagari.match(ch) or ch.isspace() or '०' <= ch <= '९')

    def normalize_spaces(self, sentence):
        """Normalize spaces."""
        return re.sub(r'\s+', ' ', sentence).strip()

    def normalize_diacritics(self, sentence):
        """Standardize vowel diacritics."""
        sentence = re.sub(r'[िी]', 'ि', sentence)
        sentence = re.sub(r'[ुू]', 'ु', sentence)
        return sentence

    def normalize_vowel_positions(self, sentence):
        """Fix wrong vowel positioning: क्ि → कि"""
        chars = list(sentence)
        output = []
        i = 0
        while i < len(chars):
            if chars[i] == self.halant:
                if (i+1 < len(chars)) and (chars[i+1] in self.pre_base_vowels):
                    output.append(chars[i+1])
                    output.append(chars[i])
                    i += 2
                else:
                    output.append(chars[i])
                    i += 1
            else:
                output.append(chars[i])
                i += 1
        return ''.join(output)

    def normalize_consonant_clusters(self, sentence):
        """Fix broken consonant clusters (no halant-space-halant)."""
        sentence = re.sub(r'(\w)्\s+(\w)', r'\1्\2', sentence)
        return sentence

    def normalize_anusvara(self, sentence):
        """Convert nasal consonants + halant into anusvara."""
        pattern = f"([{self.nasal_consonants}]){self.halant}"
        sentence = re.sub(pattern, 'ं', sentence)
        return sentence

    def normalize_punctuation(self, sentence):
        """Remove all punctuation."""
        return re.sub(r'[।॥.?!,:;\'"“”‘’()\[\]{}]', '', sentence)

    def normalize_sentence(self, sentence):
        """Full ASR normalization pipeline."""
        sentence = self.normalize_unicode(sentence)
        sentence = self.normalize_numbers(sentence)
        sentence = self.remove_non_devanagari(sentence)
        sentence = self.normalize_spaces(sentence)
        sentence = self.normalize_diacritics(sentence)
        sentence = self.normalize_vowel_positions(sentence)
        sentence = self.normalize_consonant_clusters(sentence)
        sentence = self.normalize_anusvara(sentence)
        sentence = self.normalize_punctuation(sentence)
        sentence = self.normalize_spaces(sentence)  # after punctuation removal
        return sentence

    def tokenize_for_cer(self, sentence):
        """Normalize and split into characters."""
        sentence = self.normalize_sentence(sentence)
        return list(sentence)

    def tokenize_for_wer(self, sentence):
        """Normalize and split into words."""
        sentence = self.normalize_sentence(sentence)
        return sentence.split()

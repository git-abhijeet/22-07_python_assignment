from collections import Counter
import re
import string
from math import sqrt

class TextAnalyzer:
    """
    A comprehensive text analysis tool using Counter for various text statistics
    Useful for content writers and SEO analysis
    """
    
    def __init__(self, text):
        """
        Initialize with text to analyze
        Args:
            text (str): Text to analyze
        """
        print("📝 TEXT ANALYSIS TOOL")
        print("=" * 50)
        print()
        
        self.original_text = text
        self.text = text.lower()  # For case-insensitive analysis
        
        # Pre-process text for different analysis types
        self.words = self._extract_words()
        self.sentences = self._extract_sentences()
        
        print(f"✅ Text loaded for analysis:")
        print(f"   📄 Length: {len(self.original_text)} characters")
        print(f"   📝 Preview: \"{self.original_text[:100]}{'...' if len(self.original_text) > 100 else ''}\"")
        print()
    
    def _extract_words(self):
        """Extract words from text, removing punctuation"""
        # Remove punctuation and split into words
        words = re.findall(r'\b[a-zA-Z]+\b', self.text)
        return words
    
    def _extract_sentences(self):
        """Extract sentences from text"""
        # Split by sentence endings, filter out empty strings
        sentences = re.split(r'[.!?]+', self.original_text.strip())
        return [s.strip() for s in sentences if s.strip()]
    
    def get_character_frequency(self, include_spaces=False):
        """
        Get frequency of each character
        Args:
            include_spaces (bool): Whether to include spaces in count
        Returns:
            Counter: Character frequencies
        """
        print("🔤 CHARACTER FREQUENCY ANALYSIS:")
        print("-" * 30)
        
        text_to_analyze = self.text
        if not include_spaces:
            text_to_analyze = text_to_analyze.replace(' ', '')
        
        char_counter = Counter(text_to_analyze)
        
        print(f"   Total characters analyzed: {len(text_to_analyze)}")
        print(f"   Unique characters: {len(char_counter)}")
        print(f"   Include spaces: {include_spaces}")
        print()
        
        print("   🔥 Most frequent characters:")
        for i, (char, count) in enumerate(char_counter.most_common(10), 1):
            percentage = (count / len(text_to_analyze)) * 100
            char_display = repr(char) if char in string.whitespace else char
            bar = "█" * int(count / 10) if count >= 10 else "▪" * (count // 2)
            print(f"      {i:2d}. {char_display}: {count:3d} ({percentage:4.1f}%) {bar}")
        print()
        
        return char_counter
    
    def get_word_frequency(self, min_length=1):
        """
        Get frequency of each word (minimum length filter)
        Args:
            min_length (int): Minimum word length to include
        Returns:
            Counter: Word frequencies
        """
        print(f"📚 WORD FREQUENCY ANALYSIS (min length: {min_length}):")
        print("-" * 30)
        
        # Filter words by minimum length
        filtered_words = [word for word in self.words if len(word) >= min_length]
        word_counter = Counter(filtered_words)
        
        print(f"   Total words: {len(self.words)}")
        print(f"   After length filter: {len(filtered_words)}")
        print(f"   Unique words: {len(word_counter)}")
        print()
        
        print("   🔥 Most frequent words:")
        for i, (word, count) in enumerate(word_counter.most_common(10), 1):
            percentage = (count / len(filtered_words)) * 100
            bar = "█" * count if count <= 10 else "█" * 10 + "+"
            print(f"      {i:2d}. {word:12s}: {count:3d} ({percentage:4.1f}%) {bar}")
        print()
        
        return word_counter
    
    def get_sentence_length_distribution(self):
        """
        Analyze sentence lengths (in words)
        Returns:
            dict: Contains 'lengths' (Counter), 'average', 'longest', 'shortest'
        """
        print("📏 SENTENCE LENGTH ANALYSIS:")
        print("-" * 30)
        
        sentence_lengths = []
        sentence_details = []
        
        for i, sentence in enumerate(self.sentences, 1):
            words_in_sentence = len(re.findall(r'\b[a-zA-Z]+\b', sentence))
            sentence_lengths.append(words_in_sentence)
            sentence_details.append({
                'number': i,
                'length': words_in_sentence,
                'text': sentence[:50] + "..." if len(sentence) > 50 else sentence
            })
        
        if not sentence_lengths:
            return {
                'lengths': Counter(),
                'average': 0,
                'longest': 0,
                'shortest': 0,
                'sentence_details': []
            }
        
        lengths_counter = Counter(sentence_lengths)
        average_length = sum(sentence_lengths) / len(sentence_lengths)
        longest = max(sentence_lengths)
        shortest = min(sentence_lengths)
        
        print(f"   Total sentences: {len(self.sentences)}")
        print(f"   Average length: {average_length:.1f} words")
        print(f"   Longest sentence: {longest} words")
        print(f"   Shortest sentence: {shortest} words")
        print()
        
        print("   📊 Length distribution:")
        for length in sorted(lengths_counter.keys()):
            count = lengths_counter[length]
            percentage = (count / len(sentence_lengths)) * 100
            bar = "█" * count if count <= 10 else "█" * 10 + "+"
            print(f"      {length:2d} words: {count:2d} sentences ({percentage:4.1f}%) {bar}")
        print()
        
        print("   📝 Sentence details:")
        for detail in sentence_details[:5]:  # Show first 5 sentences
            print(f"      Sentence {detail['number']}: {detail['length']} words - \"{detail['text']}\"")
        if len(sentence_details) > 5:
            print(f"      ... and {len(sentence_details) - 5} more sentences")
        print()
        
        return {
            'lengths': lengths_counter,
            'average': round(average_length, 2),
            'longest': longest,
            'shortest': shortest,
            'sentence_details': sentence_details
        }
    
    def find_common_words(self, n=10, exclude_common=True):
        """
        Find most common words, optionally excluding very common English words
        Args:
            n (int): Number of words to return
            exclude_common (bool): Exclude common words like 'the', 'and', etc.
        Returns:
            list: List of tuples (word, count)
        """
        print(f"🎯 MOST COMMON WORDS (top {n}, exclude common: {exclude_common}):")
        print("-" * 30)
        
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 
            'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'is', 
            'are', 'was', 'were', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 
            'her', 'us', 'them'
        }
        
        word_counter = Counter(self.words)
        
        if exclude_common:
            # Remove common words
            filtered_counter = Counter({word: count for word, count in word_counter.items() 
                                      if word not in common_words})
            analysis_counter = filtered_counter
            print(f"   ❌ Excluded {len(word_counter) - len(filtered_counter)} common word types")
        else:
            analysis_counter = word_counter
        
        most_common = analysis_counter.most_common(n)
        
        print(f"   📊 Analysis results:")
        print(f"      Total word instances: {sum(word_counter.values())}")
        print(f"      Unique words analyzed: {len(analysis_counter)}")
        print()
        
        print(f"   🏆 Top {n} words:")
        for i, (word, count) in enumerate(most_common, 1):
            percentage = (count / sum(analysis_counter.values())) * 100
            bar = "█" * min(count, 15)
            print(f"      {i:2d}. {word:15s}: {count:3d} ({percentage:4.1f}%) {bar}")
        print()
        
        return most_common
    
    def get_reading_statistics(self):
        """
        Get comprehensive reading statistics
        Returns:
            dict: Contains character_count, word_count, sentence_count,
                 average_word_length, reading_time_minutes (assume 200 WPM)
        """
        print("📊 COMPREHENSIVE READING STATISTICS:")
        print("-" * 30)
        
        character_count = len(self.original_text)
        character_count_no_spaces = len(self.original_text.replace(' ', ''))
        word_count = len(self.words)
        sentence_count = len(self.sentences)
        
        # Calculate average word length
        total_word_length = sum(len(word) for word in self.words)
        average_word_length = total_word_length / word_count if word_count > 0 else 0
        
        # Calculate reading time (assuming 200 WPM average reading speed)
        reading_time_minutes = word_count / 200
        
        # Calculate additional metrics
        words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        characters_per_word = character_count_no_spaces / word_count if word_count > 0 else 0
        
        # Text complexity estimation (Flesch Reading Ease approximation)
        if sentence_count > 0 and word_count > 0:
            avg_sentence_length = word_count / sentence_count
            avg_syllables_per_word = average_word_length * 0.5  # Rough approximation
            flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
            flesch_score = max(0, min(100, flesch_score))  # Clamp between 0-100
        else:
            flesch_score = 0
        
        # Determine reading level
        if flesch_score >= 90:
            reading_level = "Very Easy"
        elif flesch_score >= 80:
            reading_level = "Easy"
        elif flesch_score >= 70:
            reading_level = "Fairly Easy"
        elif flesch_score >= 60:
            reading_level = "Standard"
        elif flesch_score >= 50:
            reading_level = "Fairly Difficult"
        elif flesch_score >= 30:
            reading_level = "Difficult"
        else:
            reading_level = "Very Difficult"
        
        stats = {
            'character_count': character_count,
            'character_count_no_spaces': character_count_no_spaces,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'average_word_length': round(average_word_length, 2),
            'reading_time_minutes': round(reading_time_minutes, 2),
            'words_per_sentence': round(words_per_sentence, 2),
            'characters_per_word': round(characters_per_word, 2),
            'flesch_reading_score': round(flesch_score, 1),
            'reading_level': reading_level
        }
        
        print("   📏 Basic Counts:")
        print(f"      Characters (with spaces): {character_count:,}")
        print(f"      Characters (no spaces): {character_count_no_spaces:,}")
        print(f"      Words: {word_count:,}")
        print(f"      Sentences: {sentence_count:,}")
        print()
        
        print("   📐 Averages:")
        print(f"      Average word length: {average_word_length:.2f} characters")
        print(f"      Words per sentence: {words_per_sentence:.2f}")
        print(f"      Characters per word: {characters_per_word:.2f}")
        print()
        
        print("   ⏰ Reading Time:")
        print(f"      Estimated reading time: {reading_time_minutes:.2f} minutes")
        print(f"      Reading speed assumed: 200 WPM")
        print()
        
        print("   🎓 Readability:")
        print(f"      Flesch Reading Score: {flesch_score:.1f}")
        print(f"      Reading Level: {reading_level}")
        print()
        
        return stats
    
    def compare_with_text(self, other_text):
        """
        Compare this text with another text
        Args:
            other_text (str): Text to compare with
        Returns:
            dict: Contains 'common_words', 'similarity_score', 'unique_to_first', 'unique_to_second'
        """
        print("🔄 TEXT COMPARISON ANALYSIS:")
        print("-" * 30)
        
        # Create analyzer for other text
        other_analyzer = TextAnalyzer.__new__(TextAnalyzer)
        other_analyzer.original_text = other_text
        other_analyzer.text = other_text.lower()
        other_analyzer.words = other_analyzer._extract_words()
        other_analyzer.sentences = other_analyzer._extract_sentences()
        
        # Get word sets
        words1 = set(self.words)
        words2 = set(other_analyzer.words)
        
        # Find common and unique words
        common_words = words1 & words2
        unique_to_first = words1 - words2
        unique_to_second = words2 - words1
        
        # Calculate similarity score (Jaccard similarity)
        union_words = words1 | words2
        similarity_score = len(common_words) / len(union_words) if union_words else 0
        
        # Calculate word frequency similarity
        counter1 = Counter(self.words)
        counter2 = Counter(other_analyzer.words)
        
        # Cosine similarity for word frequencies
        common_vocab = common_words
        if common_vocab:
            vec1 = [counter1[word] for word in common_vocab]
            vec2 = [counter2[word] for word in common_vocab]
            
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            magnitude1 = sqrt(sum(a * a for a in vec1))
            magnitude2 = sqrt(sum(b * b for b in vec2))
            
            cosine_similarity = dot_product / (magnitude1 * magnitude2) if magnitude1 * magnitude2 > 0 else 0
        else:
            cosine_similarity = 0
        
        # Get most common words in each text
        common_word_frequencies = []
        for word in sorted(common_words):
            freq1 = counter1[word]
            freq2 = counter2[word]
            common_word_frequencies.append((word, freq1, freq2))
        
        # Sort by combined frequency
        common_word_frequencies.sort(key=lambda x: x[1] + x[2], reverse=True)
        
        comparison_result = {
            'common_words': list(common_words),
            'common_word_count': len(common_words),
            'similarity_score': round(similarity_score, 3),
            'cosine_similarity': round(cosine_similarity, 3),
            'unique_to_first': list(unique_to_first),
            'unique_to_second': list(unique_to_second),
            'common_word_frequencies': common_word_frequencies[:10]
        }
        
        print(f"   📊 Comparison Results:")
        print(f"      Text 1 unique words: {len(words1)}")
        print(f"      Text 2 unique words: {len(words2)}")
        print(f"      Common words: {len(common_words)}")
        print(f"      Jaccard similarity: {similarity_score:.3f}")
        print(f"      Cosine similarity: {cosine_similarity:.3f}")
        print()
        
        print(f"   🤝 Common Words (top 10 by frequency):")
        for i, (word, freq1, freq2) in enumerate(common_word_frequencies[:10], 1):
            total_freq = freq1 + freq2
            print(f"      {i:2d}. {word:12s}: {freq1:2d} + {freq2:2d} = {total_freq:2d}")
        print()
        
        print(f"   🔹 Unique to Text 1 ({len(unique_to_first)} words):")
        unique1_sample = sorted(unique_to_first)[:10]
        print(f"      {', '.join(unique1_sample)}")
        if len(unique_to_first) > 10:
            print(f"      ... and {len(unique_to_first) - 10} more")
        print()
        
        print(f"   🔸 Unique to Text 2 ({len(unique_to_second)} words):")
        unique2_sample = sorted(unique_to_second)[:10]
        print(f"      {', '.join(unique2_sample)}")
        if len(unique_to_second) > 10:
            print(f"      ... and {len(unique_to_second) - 10} more")
        print()
        
        return comparison_result
    
    def get_advanced_analytics(self):
        """Get advanced text analytics"""
        print("🚀 ADVANCED TEXT ANALYTICS:")
        print("-" * 30)
        
        # Vocabulary richness (Type-Token Ratio)
        unique_words = len(set(self.words))
        total_words = len(self.words)
        vocabulary_richness = unique_words / total_words if total_words > 0 else 0
        
        # Most and least common word lengths
        word_lengths = [len(word) for word in self.words]
        length_counter = Counter(word_lengths)
        
        # Letter frequency analysis
        letters_only = re.sub(r'[^a-zA-Z]', '', self.text)
        letter_counter = Counter(letters_only.lower())
        
        # Punctuation analysis
        punctuation_chars = [char for char in self.original_text if char in string.punctuation]
        punctuation_counter = Counter(punctuation_chars)
        
        print(f"   📚 Vocabulary Analysis:")
        print(f"      Vocabulary richness (TTR): {vocabulary_richness:.3f}")
        print(f"      Unique words: {unique_words}")
        print(f"      Total words: {total_words}")
        print()
        
        print(f"   📏 Word Length Distribution:")
        for length in sorted(length_counter.keys())[:10]:
            count = length_counter[length]
            percentage = (count / len(word_lengths)) * 100
            bar = "█" * min(count, 20)
            print(f"      {length:2d} letters: {count:3d} words ({percentage:4.1f}%) {bar}")
        print()
        
        print(f"   🔤 Letter Frequency (top 10):")
        for i, (letter, count) in enumerate(letter_counter.most_common(10), 1):
            percentage = (count / len(letters_only)) * 100
            bar = "█" * min(count // 5, 20)
            print(f"      {i:2d}. {letter}: {count:4d} ({percentage:4.1f}%) {bar}")
        print()
        
        if punctuation_counter:
            print(f"   ❗ Punctuation Usage:")
            for punct, count in punctuation_counter.most_common(5):
                percentage = (count / len(self.original_text)) * 100
                print(f"      '{punct}': {count:3d} ({percentage:4.1f}%)")
        print()
        
        return {
            'vocabulary_richness': vocabulary_richness,
            'word_length_distribution': dict(length_counter),
            'letter_frequency': dict(letter_counter),
            'punctuation_frequency': dict(punctuation_counter)
        }


def demonstrate_counter_features():
    """Demonstrate Counter-specific features"""
    print("🔧 COUNTER FEATURES DEMONSTRATION")
    print("=" * 50)
    print()
    
    # Counter creation and operations
    sample_words = ['python', 'java', 'python', 'c++', 'python', 'java', 'go']
    word_counter = Counter(sample_words)
    
    print("📊 Counter Creation and Operations:")
    print(f"   Original list: {sample_words}")
    print(f"   Counter result: {word_counter}")
    print()
    
    print("🔥 Counter Methods:")
    print(f"   most_common(3): {word_counter.most_common(3)}")
    print(f"   most_common(): {word_counter.most_common()}")
    print(f"   total(): {sum(word_counter.values())}")
    print()
    
    # Counter arithmetic
    other_counter = Counter(['python', 'rust', 'go', 'go'])
    print("➕ Counter Arithmetic:")
    print(f"   Counter 1: {word_counter}")
    print(f"   Counter 2: {other_counter}")
    print(f"   Addition: {word_counter + other_counter}")
    print(f"   Subtraction: {word_counter - other_counter}")
    print(f"   Intersection: {word_counter & other_counter}")
    print(f"   Union: {word_counter | other_counter}")
    print()


def main():
    """Main function to test the TextAnalyzer implementation"""
    print("🎯 TESTING TEXT ANALYZER SYSTEM")
    print("=" * 60)
    print()
    
    # Sample text for analysis
    sample_text = """
    Python is a high-level, interpreted programming language with dynamic semantics.
    Its high-level built-in data structures, combined with dynamic typing and dynamic binding,
    make it very attractive for Rapid Application Development. Python is simple, easy to learn
    syntax emphasizes readability and therefore reduces the cost of program maintenance.
    Python supports modules and packages, which encourages program modularity and code reuse.
    The Python interpreter and the extensive standard library are available in source or binary
    form without charge for all major platforms, and can be freely distributed.
    """
    
    # Create analyzer
    analyzer = TextAnalyzer(sample_text.strip())
    
    # Test all methods
    print("🧪 RUNNING ALL ANALYSIS METHODS:")
    print("=" * 50)
    print()
    
    # Character frequency analysis
    char_freq = analyzer.get_character_frequency(include_spaces=False)
    
    # Word frequency analysis
    word_freq = analyzer.get_word_frequency(min_length=3)
    
    # Sentence length analysis
    sentence_analysis = analyzer.get_sentence_length_distribution()
    
    # Common words analysis
    common_words = analyzer.find_common_words(5, exclude_common=True)
    
    # Reading statistics
    reading_stats = analyzer.get_reading_statistics()
    
    # Advanced analytics
    advanced_stats = analyzer.get_advanced_analytics()
    
    # Text comparison
    other_text = "Java is a programming language. Java is object-oriented and platform independent. Java provides robust memory management and security features."
    comparison_result = analyzer.compare_with_text(other_text)
    
    # Summary of results
    print("📋 ANALYSIS SUMMARY:")
    print("=" * 50)
    print(f"Character frequency (top 5): {char_freq.most_common(5)}")
    print(f"Word frequency (top 5): {word_freq.most_common(5)}")
    print(f"Common words: {common_words}")
    print(f"Reading statistics: Word count = {reading_stats['word_count']}, Reading time = {reading_stats['reading_time_minutes']} min")
    print(f"Comparison similarity: {comparison_result['similarity_score']}")
    print()
    
    # Demonstrate Counter features
    demonstrate_counter_features()
    
    print("🎉 TEXT ANALYSIS COMPLETE!")
    print("=" * 60)
    print()
    print("✅ All features tested successfully:")
    print("   • Character frequency analysis with Counter")
    print("   • Word frequency with filtering options")
    print("   • Sentence length distribution")
    print("   • Common word identification with stop word filtering")
    print("   • Comprehensive reading statistics")
    print("   • Text comparison and similarity analysis")
    print("   • Advanced analytics including vocabulary richness")
    print("   • Counter arithmetic operations demonstration")
    print()


if __name__ == "__main__":
    main()

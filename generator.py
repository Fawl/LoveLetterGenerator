from random import choice, seed, getrandbits
import configparser

class LoveLetterGenerator():
    '''
    Generates love letters
    '''
    def __init__(self, name: str, rand_seed: int = 0x69, ) -> None:
        seed(rand_seed)
        self.name = name

        config = configparser.ConfigParser()
        config.read("config.ini")

        self.__wordlists = dict(config["LoveLetterGenerator"])
        del config

        for key in self.__wordlists.keys():
            self.__wordlists[key] = self.__wordlists[key].split(",")

        self.__used_words = {
            "ADJECTIVES": set(),
            "NOUNS": set(),
            "ADVERBS": set(),
            "VERBS": set()
        }


    def _generate_unique_word(self, category: str):
        '''
        Generates a unique random word for category selected.
        '''
        wordlist = self.__wordlists.get(category.lower())
        used_words = self.__used_words.get(category)

        if wordlist:
            # Valid category
            rand_word = choice(self.__wordlists.get(category.lower()))

            while rand_word in used_words:
                rand_word = choice(self.__wordlists.get(category.lower()))

            self.__used_words[category].add(rand_word)

            return rand_word.strip()

        else:
            # Invalid category
            return False

    
    def _get_random_bool(self) -> bool:
        '''
        Decides if love letter starts with long expression or short expression
        '''
        return bool(getrandbits(1))

    
    def get_loveletter(self):
        last = None

        sal_1 = choice(self.__wordlists.get("SALUTATION_1".lower()))
        sal_2 = choice(self.__wordlists.get("SALUTATION_2".lower()))

        salutation = f"{sal_1} {sal_2},\n\t"

        body = ""
        concat = ""

        for _ in range(5):
            if self._get_random_bool():
                opt_adj_1 = self._generate_unique_word("ADJECTIVES") if self._get_random_bool() else ""
                noun_1 = self._generate_unique_word("NOUNS")
                opt_adv = self._generate_unique_word("ADVERBS") if self._get_random_bool() else ""
                verb = self._generate_unique_word("VERBS")
                opt_adj_2 = self._generate_unique_word("ADJECTIVES") if self._get_random_bool() else ""
                noun_2 = self._generate_unique_word("NOUNS")

                if last is not None or last == "LONG":
                    concat = ". "

                body += f"{concat} My {opt_adj_1} {noun_1} {opt_adv} {verb} {opt_adj_2} {noun_2}"
                last = "LONG"

            else:
                adj = self._generate_unique_word("ADJECTIVES")
                noun = self._generate_unique_word("NOUNS")

                if last == "SHORT":
                    concat = ", "
                elif last == "LONG":
                    concat = ". You are"
                elif last is None:
                    concat = "You are "

                body += f"{concat} my {adj} {noun}"
                last = "SHORT"
        
        ending_adj = self._generate_unique_word("ADVERBS")
        signature = f".\n\tYours {ending_adj},\n\t{self.name}\n"

        love_letter = salutation + body + signature

        return love_letter.replace("  ", " ").upper()
    


def main():
    gen = LoveLetterGenerator("Sam", rand_seed=69)
    print(gen.get_loveletter())


if __name__ == '__main__':
    main()
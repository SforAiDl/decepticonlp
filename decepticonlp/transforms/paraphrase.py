_author_ = "Abheesht Sharma"

import re
import random
import abc

class Paraphrases(metaclass=abc.ABCMeta):
	"""
		An abstract class used to represent paraphrases. SubClass should implement the apply method.
		Methods
        -------
        apply(self, text: str, **kwargs)
            - applies the paraphrasing on the text and returns it.
            """


	@abc.abstractmethod
	def apply(self, text:str, **kwargs):
		"""Applies paraphrasing and returns the text."""
		raise NotImplementedError


	def get_ignore_default_value(self):
		return True

	def get_reverse_default_value(self):
		return False

class ContractParaphrases(Paraphrases):
	"""
	    A class used to apply contract paraphrasing.
	    Methods
	    -------
	    apply(self, text: str, **kwargs)
	        - applies the contract paraphrase on the word and returns it.
	""" 

	def get_length_less_than_two_error_message(self):
		return "given string's length is less than two"

	def get_not_a_contraction_error_message(self):
		return "given string is not a contraction"


	def apply(self, text: str, **kwargs):
		"""
		Contract words in the text (if reverse=False (default))

		text=I would
		output=contract(text=text, reverse=False)
		print(output)
		I'd

		text=He'll
		output=contract(text=text, reverse=True)
		print(output)
		He will

		Note: For reverse=True, this function does NOT disambiguate the output (eg: 's can be is/has). 
			  For that, I would need to implement PoS Tagging (https://www.zora.uzh.ch/id/eprint/47923/4/Volk_Sennrich_Contraction_ResolutionV.pdf),
			  take context into account and input a whole sentence/document rather than just a few words.

		:param
		:text: (str) if reverse is False, two or more words that are to be edited. If reverse is True, one word (the contraction)
		:reverse: (boolean) default (False), word-->contraction. If True, contraction-->word
		:ignore: (boolean) default (True), boolean if assertions should be ignored
		"""

		if(kwargs.get("reverse",self.get_reverse_default_value())):
			if(kwargs.get("ignore", self.get_ignore_default_value()) and '\'' not in text):
				return text
			
			assert '\'' in text, self.get_not_a_contraction_error_message()
			text=re.sub(r"\blet's\b", "let us", text, flags=re.IGNORECASE)
			text=re.sub(r"\bwon't\b", "will not",text, flags=re.IGNORECASE)
			text=re.sub(r"n't", " not", text, flags=re.IGNORECASE)
			text=re.sub(r"'ve", " have", text, flags=re.IGNORECASE)
			text=re.sub(r"'m", " am", text, flags=re.IGNORECASE)

			#For contractions with multiple choices, choose the expansion arbitrarily
			list_for_s=[r" is", r" has"]
			list_for_d=[r" had", r" would"]
			list_for_ll=[r" will", r" shall"]
			list_for_re=[r" are", r" were"]
			
			choice=random.randint(0,1)
			text=re.sub(r"'s", list_for_s[choice],text,flags=re.IGNORECASE)
			text=re.sub(r"'d", list_for_d[choice],text,flags=re.IGNORECASE)
			text=re.sub(r"'ll", list_for_ll[choice],text,flags=re.IGNORECASE)
			text=re.sub(r"'re", list_for_re[choice],text,flags=re.IGNORECASE)
			return text
			


		if (kwargs.get("ignore", self.get_ignore_default_value()) and len(text.split(" ")) < 2):
			return text
		
		assert not len(text.split())<2, self.get_length_less_than_two_error_message()
		
		#Define text:contraction dictionary
		text_to_contraction={
		r"\blet us\b":r"let's",
		r" not":r"n't",
		r" have":r"'ve",
		r" is":r"'s",
		r" would":r"'d",
		r" had":r"'d",
		r" has":r"'s",
		r" will":r"'ll",
		r" shall":r"'ll",
		r" are":r"'re",
		r" were":r"'re",
		r" am":r"'m"
		}

		
		text=re.sub(r"\bwill not\b", "won't", text, flags=re.IGNORECASE)
		#Iterate over the keys of the dictionary and replace by contraction if found
		for substring in text_to_contraction:
			text=re.sub(substring,text_to_contraction[substring],text,flags=re.IGNORECASE)

		return text

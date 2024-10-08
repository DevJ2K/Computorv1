# What's a valid polynomial ?
# - Pas d'autres characteres hormis '0->9', ' ', '*+-','^ =', 'xX'
# - len 3 min
# - 1 equal (=) avec 2 blocs et min 1 de len

from ErrorManager import *
from Monomial import Monomial
from MyRegex import MyRegex
import re

def is_an_equation(polynomial: str) -> bool:
	# polynomial = re.sub(r"\s*", "", polynomial)
	side_regex = MyRegex['side']
	regex = side_regex + r"\s*=\s*" + side_regex + r"$"
	match = re.match(regex, polynomial)
	if match:
		return True
	return False


def is_polynomial_form(polynomial: str) -> bool:
	if (len(polynomial) < 3):
		return False
	if (is_an_equation(polynomial) == False):
		return False

	regex_duplicates = r"(?:\d+\s+\d+)|(?:[xX]\s*[xX])"
	match_duplicates = re.search(regex_duplicates, polynomial)
	# print(match_duplicates)
	if match_duplicates:
		# print(match_duplicates)
		return False
	regex_follow_x = r"\^\d+\s*[xX]"
	match_follow_x = re.search(regex_follow_x, polynomial)
	if match_follow_x:
		return False
	# regex = r"(\s*[-+]?\s*\d+(?:\.\d+)?\s*(?:\*\s*X\^\d+)?)"
	regex = MyRegex['monomial']
	# polynomial = re.sub(r"\s*", "", polynomial)
	match = re.findall(regex, polynomial)
	if match:
		rm_equal_polynomial = polynomial.replace('=', '')
		rm_whitespace_polynomial = re.sub(r"\s", "", rm_equal_polynomial)

		# print(rm_whitespace_polynomial)
		# print(re.sub(r"\s", "",''.join(match)))
		# print(match)


		# formatted_match = [re.sub(r"\s", "", item) for item in match]
		# print(formatted_match)

		if len(rm_whitespace_polynomial) == len(re.sub(r"\s", "",''.join(match))):
			return True
		else:
			return False

	return False


def convertToMonomialList(polynomial: str) -> list[Monomial]:
	regex = MyRegex['monomial']
	# polynomial = re.sub(r"\s*", "", polynomial)
	match = re.findall(regex, polynomial)
	monomial_list = []
	if match:
		# print(match)
		rm_equal_polynomial = polynomial.replace('=', '')
		rm_whitespace_polynomial = re.sub(r"\s", "", rm_equal_polynomial)
		if len(rm_whitespace_polynomial) != len(re.sub(r"\s", "",''.join(match))):
			raise InvalidPolynomialError
		for monomial_str in match:
			monomial = Monomial(monomial_str)
			monomial_list.append(monomial)
		return monomial_list
	else:
		raise InvalidPolynomialError


def simplifiedPolynomialSide(side: list[Monomial]) -> list[Monomial]:
	existing_degree: list[int] = []
	simplified_list: list[Monomial] = []
	for monomial in side:
		if monomial.degree not in existing_degree:
			existing_degree.append(monomial.degree)

	for degree in existing_degree:
		coefficient = 0
		for monomial in side:
			if monomial.degree == degree:
				coefficient += monomial.coefficient
		if coefficient != 0:
			simplified_list.append(Monomial(f"{coefficient} * X^{degree}"))

	# print(simplified_list)
	return simplified_list

def needToReduce(number: float) -> bool:
	number_str = str(number)
	# print(f"{number_str} | ", end="")
	match = re.search(r"\.\d+", number_str)
	if match:
		if len(match.group()) > 4:
			# print("Display irreducible fraction")
			return True
		else:
			# print("Display full decimal")
			return False
	else:
		# print("No match")
		return False


if (__name__ == "__main__"):
	print(convertToMonomialList("0+ 2x + 7 "))
	# print(is_polynomial_form("5 5 5 5 = 0"))
	# print(is_polynomial_form("5 * XXXXXXXXXXXXxX^0 + 4 * X^1 - 9.3 * X^2 = 0"))
	# print(is_polynomial_form("X^3 + X^2 - X^1 = x^3"))
	# temp_list = convertToMonomialList("2 * X^2 - 2 * X^2 - 2 * X^2 + 4 * X^1 + 4 * X^1")
	# print(temp_list)
	# print(simplifiedPolynomialSide(temp_list))
	# print(convertToMonomialList("5.00 * 	X^015	"))
	# print(convertToMonomialList("5 * X^0 + 4 * X^1 - 9.3 * X^2"))
	# is_an_equation("0 = 3 = 4")
	# is_polynomial_form("5 * X^0")
	# is_polynomial_form("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 0")
	# is_polynomial_form("X^0")
	# is_polynomial_form("5 * X^0 + 4 * X^1 - 9.3 * X^2 - 5 * X^0")
	# is_polynomial_form("5 * X^0 + 4 * X^ - 9.3 * X^2 - 5 * X^0")
	# l1str = convertToMonomialStrList("5 * X^0 + 4 * X^1 - 9.3 * X^2")
	# l1 = convertToMonomialList(l1str)
	# print(l1)
	# print("==================")
	# convertToMonomialStrList("+ 4 * X^1 - 9.3 * X^2")
	# print("==================")
	# convertToMonomialStrList("+5 * X^0 + 4 * X^1 - 9.3 * X^2 - 3 * X^3")
	# print("==================")
	# convertToMonomialStrList("-5 * X^0 + 4 * X^1 - 9.3 * X^2")
	pass

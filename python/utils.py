from flask import jsonify
from fractions import Fraction
#Fraction percent convert
def float_to_fraction_percent(value, suffix, usepercent, purefrac, accuracy=1e-8):
  fraction = Fraction(value).limit_denominator()
  pure_fraction = f"{fraction.numerator}/{fraction.denominator}"

  if fraction.denominator == 1:
      fraction_result = f"{fraction.numerator}/1"
  else:
      whole_number = fraction.numerator // fraction.denominator
      remainder = fraction.numerator % fraction.denominator

      if whole_number == 0:
          fraction_result = f"{remainder}/{fraction.denominator}"
      else:
          fraction_result = f"{whole_number} {remainder}/{fraction.denominator}"

  percentage_result = round(value * 100, 2)

  if usepercent:
      if purefrac:
          return f"{value:.3f}{suffix} | {fraction_result}{suffix} | {percentage_result}{suffix}%", pure_fraction
      else:
          return f"{value:.3f} | {pure_fraction}{suffix} | {percentage_result}%"
  else:
      if purefrac:
          return f"{value:.3f}{suffix} | {fraction_result}{suffix}"
      else:
          return f"{value:.3f}{suffix} | {pure_fraction}{suffix}"
from fractions import Fraction
from recipebox.models import MeasurementUnit
from recipebox.conversions import convert


def test_teaspoon_to_tablespoon():
    result = convert(1, MeasurementUnit.TEASPOON, MeasurementUnit.TABLESPOON)
    result == Fraction('3')

def test_tablespoon_to_teaspoon():
    result = convert(1, MeasurementUnit.TABLESPOON, MeasurementUnit.TEASPOON)
    result == Fraction('1/3')

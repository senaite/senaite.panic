
from bika.lims.interfaces import ISubmitted
from bika.lims import api


def has_analyses_in_panic(sample):
    """Returns whether the sample passed in have at least one analysis for which
    the result is in panic in accordance with the specifications. Only analyses
    in "to_be_verified" status and beyond are considered
    """
    analyses = sample.getAnalyses(full_objects=True)
    for analysis in analyses:
        if ISubmitted.providedBy(analysis) and is_in_panic(analysis):
            return True
    return False


def is_in_panic(brain_or_object):
    """Returns whether if the result of the analysis is below the min panic or
    above the max panic
    """
    result = api.safe_getattr(brain_or_object, "getResult", None)
    if not api.is_floatable(result):
        return False

    result_range = api.safe_getattr(brain_or_object, "getResultsRange", None)
    if not result_range:
        return False

    result = api.to_float(result)

    # Below the min panic?
    panic_min = result_range.get("min_panic", "")
    panic_min = api.is_floatable(panic_min) and api.to_float(panic_min) or None
    if panic_min is not None and result <= panic_min:
        # The result is a detection limit?
        obj = api.get_object(brain_or_object)
        if obj.isUpperDetectionLimit() and result == panic_min:
            # The result is above the panic min
            return False
        return True

    # Above the max panic
    panic_max = result_range.get("max_panic", "")
    panic_max = api.is_floatable(panic_max) and api.to_float(panic_max) or None
    if panic_max is not None and result >= panic_max:
        # The result is a detection limit?
        obj = api.get_object(brain_or_object)
        if obj.isLowerDetectionLimit() and result == panic_max:
            # The result is below the panic max
            return False
        return True

    # Not in panic
    return False


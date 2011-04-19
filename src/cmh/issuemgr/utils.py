from datetime import datetime

def get_complaint_sequence (complaint_base, location, logdate):

    return "C.#.%s.%s.%s.%s" % (location.parent.parent.parent.value,
                                location.id,
                                logdate.strftime ("%Y%m%d"),
                                datetime.now ().strftime ("%Y%m%d"))


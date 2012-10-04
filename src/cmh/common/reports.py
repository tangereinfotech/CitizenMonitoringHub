from issuemgr.models import Complaint
from django.utils.encoding import smart_str

class Report():
    START_DATE = None
    END_DATE = None
    FILE = None

    def __init__(self,sdate, edate, file_handle):
        self.START_DATE = sdate
        self.END_DATE = edate
        self.FILE     = file_handle

    def export_data(self):

        column_headers = ['Complaint Number:','Filed by [name]','Filed by [mobile number]','Filed on','complaint summary','Location','Complaint type','Department','Gender','SC/ST','Status',    'start date','end date','description of specific status']

        complaints = Complaint.objects.filter(logdate__gte = self.START_DATE).filter(logdate__lte = self.END_DATE)
        complaint_nos = set()
        for c in complaints:
            complaint_nos.add(c.complaintno)

        all_complaints = []
        for cno in complaint_nos:
            same_complaint = complaints.filter(complaintno = cno).order_by('created')
            base   = same_complaint.filter(original = None)[0]
            i = 0
            for c in same_complaint:
                try:
                    end_date = same_complaint[i+1].created
                except IndexError:
                    end_date = None
                i = i + 1
                try:
                    row = [ smart_str(base.complaintno),
                            smart_str(base.filedby.name),
                            smart_str(base.filedby.mobile),
                            smart_str(base.logdate),
                            smart_str(base.description),
                            smart_str(c.get_location_name()),
                            smart_str(c.complainttype.summary),
                            smart_str(c.complainttype.department.name),
                            smart_str(c.gender),
                            smart_str(c.community),
                            smart_str(c.curstate.name),
                            smart_str(c.created),
                            smart_str(end_date),
                            smart_str(c.description)]
                    all_complaints.append(row)
                except AttributeError:
                    pass

        import csv
        with self.FILE as csvfile:
            export_file = csv.writer(csvfile, delimiter = '$', quoting = csv.QUOTE_MINIMAL)
            export_file.writerow(column_headers)
            for row in all_complaints:
                export_file.writerow(row)
        self.FILE.close()

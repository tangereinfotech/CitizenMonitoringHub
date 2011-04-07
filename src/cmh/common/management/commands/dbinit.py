import xlrd
import sys
import os

from optparse import make_option, OptionParser
from django.core.management.base import BaseCommand, CommandError
from cmh.common.models import Category, Attribute
from cmh.issuemgr.models import Department, ComplaintItem


class ExcelFormatError (Exception):
    pass

class Command (BaseCommand):
    help = """This utility parses an Excel file for issue types and location information
and updates the database models as expected by the rest of the CMH application.

The specified path must be to a valid Excel file that complies the template
provided at:
  https://spreadsheets.google.com/ccc?key=0AtZDy1RF3WCsdF9ST205Y2JxZkY5TS1kbngzYWR1eEE&hl=en&authkey=CKaOwrEH#gid=0
"""

    option_list = BaseCommand.option_list + (
        make_option ('-f', '--file', action='store', dest='file', type='string',
                    help='Spreadsheet file complying to the template at https://spreadsheets.google.com/ccc?key=0AtZDy1RF3WCsdF9ST205Y2JxZkY5TS1kbngzYWR1eEE&hl=en&authkey=CKaOwrEH#gid=0'
                     ),
        )

    def handle (self, *args, **options):
        workbook = options ['file']
        if workbook == None:
            print self.help
            sys.exit (0)
        if os.path.exists (workbook) == False:
            print self.help
            sys.exit (0)
        self.parse_update_db (workbook)

    def parse_update_db (self, filename):
        try:
            workbook = xlrd.open_workbook (filename)
            self.confirm_worksheets (workbook)

            for sheet in self.sheets:
                self.update_sheet_models (workbook.sheet_by_name (sheet ['name']))

        except xlrd.XLRDError, e:
            print "Excel read error - " + str (e) + "\n"
            print "HELP:"
            print self.help
        except ExcelFormatError, e:
            print "Excel read error - " + str (e) + "\n"
            print "HELP:"
            print self.help
        except Exception, e:
            import traceback
            traceback.print_exc ()


    def update_sheet_models (self, worksheet):
        if worksheet.name == self.CCAT_SHEET_NAME:
            self.update_complaint_models (worksheet)
        elif worksheet.name == self.LMAP_SHEET_NAME:
            self.update_location_models (worksheet)
        else:
            raise ExcelFormatError ("Incorrect worksheet specified")


    def update_complaint_models (self, worksheet):
        for row  in range (1, worksheet.nrows):
            dept_name = worksheet.cell_value (row, 0).strip ()
            dept_code = worksheet.cell_value (row, 1).strip ()
            issue_code = worksheet.cell_value (row, 2).strip ()
            issue_sum  = worksheet.cell_value (row, 3).strip ()
            issue_desc = worksheet.cell_value (row, 4).strip ()

            try:
                dept = Department.objects.get (code = dept_code, name = dept_name)
                print "Found department : %s, %s" % (dept_code, dept_name)
            except Department.DoesNotExist:
                dept = Department.objects.create (code = dept_code, name = dept_name)
                print "Created department: %s, %s" % (dept_code, dept_name)

            try:
                issue = ComplaintItem.objects.get (code = issue_code,
                                                   name = issue_sum,
                                                   desc = issue_desc)
                issue.department = dept
                issue.save ()
                print "Found issue type: %s, %s" % (issue_code, issue_sum)
            except ComplaintItem.DoesNotExist:
                issue = ComplaintItem.objects.create (code = issue_code,
                                                      name = issue_sum,
                                                      desc = issue_desc,
                                                      department = dept)
                print "Created issue type: %s, %s" % (issue_code, issue_sum)


    def update_location_models (self, worksheet):
        for row in range (1, worksheet.nrows):
            state_name = worksheet.cell_value (row, 0).strip ()
            state_code = worksheet.cell_value (row, 1).strip ()
            distt_name = worksheet.cell_value (row, 2).strip ()
            distt_code = worksheet.cell_value (row, 3).strip ()
            block_name = worksheet.cell_value (row, 4).strip ()
            block_code = worksheet.cell_value (row, 5).strip ()
            gp_name    = worksheet.cell_value (row, 6).strip ()
            gp_code    = worksheet.cell_value (row, 7).strip ()
            vill_name  = worksheet.cell_value (row, 8).strip ()
            vill_code  = worksheet.cell_value (row, 9).strip ()
            latitude   = worksheet.cell_value (row, 10)
            longitude  = worksheet.cell_value (row, 11)

            try:
                state = State.objects.get (name = state_name, code = state_code)
            except State.DoesNotExist:
                state = State.objects.create (name = state_name, code = state_code)

            try:
                distt = District.objects.get (name = distt_name, code = distt_code, state = state)
            except District.DoesNotExist:
                distt = District.objects.create (name = distt_name,
                                                 code = distt_code,
                                                 state = state)

            try:
                block = Block.objects.get (name = block_name, code = block_code, distt = distt)
            except Block.DoesNotExist:
                block = Block.objects.create (name = block_name,
                                              code = block_code,
                                              distt = distt)

            try:
                gp = GramPanchayat.objects.get (name = gp_name, code = gp_code, block = block)
            except Gp.DoesNotExist:
                gp = GramPanchayat.objects.create (name = gp_name,
                                                   code = gp_code,
                                                   block = block)

            try:
                vill = Village.objects.get (name = vill_name, code = vill_code, block = block)
            except Village.DoesNotExist:
                vill = Village.objects.create (name = vill_name,
                                               code = vill_code,
                                               block = block,
                                               latitude = latitude,
                                               longitude = longitude)




    def confirm_worksheets (self, workbook):
        sheetnames = workbook.sheet_names ()

        for sheet_info in self.sheets:
            if not sheet_info ['name'] in sheetnames:
                raise ExcelFormatError ("Workbook does not have '%s' worksheet" %
                                        sheet_info ['name'])

            worksheet = workbook.sheet_by_name (sheet_info ['name'])
            exp_num_cols = len (sheet_info ['columns'])

            if worksheet.ncols != exp_num_cols:
                raise ExcelFormatError ("'%s': incorrect column count. Expected [%d], Actual: [%d]"
                                        % (sheet_info ['name'], exp_num_cols, worksheet.ncols))

            exp_cols = sheet_info ['columns']
            for exp_col in exp_cols:
                if worksheet.cell_value (0, exp_col ['id']) != exp_col ['name']:
                    raise ExcelFormatError ("Worksheet [%s] template error: %s not found at %d" %
                                            (sheet_info ['name'],
                                             exp_col ['name'],
                                             (exp_col ['id'] + 1)))

            self.confirm_rows (worksheet, exp_num_cols)

    def confirm_rows (self, sheet, num_cols):
        for row in range (sheet.nrows):
            for col in range (num_cols):
                t = sheet.cell_type (row, col)
                if t == xlrd.XL_CELL_EMPTY or t == xlrd.XL_CELL_BLANK:
                    raise ExcelFormatError (("Empty cells are not allowed." +
                                             " First empty cell at [%d, %d] in" +
                                             " worksheet [%s]") %
                                            ((row + 1), (col + 1), sheet.name))


    CCAT_SHEET_NAME = 'Issue Categorization'
    LMAP_SHEET_NAME = 'Location Map'
    sheets = [{'name' : CCAT_SHEET_NAME,
               'columns' : [{'id' : 0,  'name' : 'Department'},
                            {'id' : 1,  'name' : 'Department Code'},
                            {'id' : 2,  'name' : 'Issue Code'},
                            {'id' : 3,  'name' : 'Issue Summary'},
                            {'id' : 4,  'name' : 'Issue Description'}]},
              {'name' : LMAP_SHEET_NAME,
               'columns' : [{'id' : 0,  'name' : 'State Name'},
                            {'id' : 1,  'name' : 'State Code'},
                            {'id' : 2,  'name' : 'District Name'},
                            {'id' : 3,  'name' : 'District Code'},
                            {'id' : 4,  'name' : 'Block Name'},
                            {'id' : 5,  'name' : 'Block Code'},
                            {'id' : 6,  'name' : 'Gram Panchayat Name'},
                            {'id' : 7,  'name' : 'Gram Panchayat Code'},
                            {'id' : 8,  'name' : 'Village Name'},
                            {'id' : 9,  'name' : 'Village Code'},
                            {'id' : 10, 'name' : 'Latitude'},
                            {'id' : 11, 'name' : 'Longitude'},]}]



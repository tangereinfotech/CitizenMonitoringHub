import xlrd
import sys
import os

from optparse import make_option, OptionParser
from django.core.management.base import BaseCommand, CommandError
from cmh.common.models import Category, Attribute, LatLong, CodeName
from cmh.issuemgr.models import ComplaintItem


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
        self.populate_complaint_status ()

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
        categories = ['Complaint Department', 'Complaint Type']
        try:
            cat_cpldepartment = Category.objects.get (key = 'Complaint Department')
        except Category.DoesNotExist:
            cat_cpldepartment = Category.objects.create (key = 'Complaint Department')

        try:
            cat_cpltype = Category.objects.get (key = 'Complaint Type')
        except Category.DoesNotExist:
            cat_cpltype = Category.objects.create (key = 'Complaint Type',
                                                   parent = cat_cpldepartment)


        for row  in range (1, worksheet.nrows):
            dept_name = worksheet.cell_value (row, 0).strip ()
            dept_code = worksheet.cell_value (row, 1).strip ()
            issue_code = worksheet.cell_value (row, 2).strip ()
            issue_sum  = worksheet.cell_value (row, 3).strip ()
            issue_desc = worksheet.cell_value (row, 4).strip ()

            dept_code  = '.'.join (['Complaint', dept_code])
            issue_code = '.'.join ([dept_code, issue_code])

            try:
                attr_dept = Attribute.objects.get (value = dept_code,
                                                   category = cat_cpldepartment)
            except Attribute.DoesNotExist:
                attr_dept = Attribute.objects.create (value = dept_code,
                                                      category = cat_cpldepartment)

            try:
                attr_cplitem = Attribute.objects.get (value = issue_code,
                                                      category = cat_cpltype)
            except Attribute.DoesNotExist:
                attr_cplitem = Attribute.objects.create (value = issue_code,
                                                      category = cat_cpltype)
            attr_cplitem.parents.add (attr_dept)

            try:
                codename = CodeName.objects.get (code = dept_code)
                codename.name = dept_name
                codename.save ()
            except CodeName.DoesNotExist:
                codename = CodeName.objects.create (code = dept_code, name = dept_name)

            try:
                ci = ComplaintItem.objects.get (code = issue_code)
                ci.name = issue_sum
                ci.desc = issue_desc
                ci.save ()
            except CodeName.DoesNotExist:
                ci = ComplaintItem.objects.create (code = issue_code,
                                                   name = issue_sum,
                                                   desc = issue_desc)



    def update_location_models (self, worksheet):
        try:
            cat_country = Category.objects.get (key = 'Country')
        except Category.DoesNotExist:
            cat_country = Category.objects.create (key = 'Country')

        try:
            cat_state = Category.objects.get (key = 'State')
        except Category.DoesNotExist:
            cat_state = Category.objects.create (key = 'State', parent = cat_country)

        try:
            cat_district = Category.objects.get (key = 'District')
        except Category.DoesNotExist:
            cat_district = Category.objects.create (key = 'District', parent = cat_state)

        try:
            cat_block = Category.objects.get (key = 'Block')
        except Category.DoesNotExist:
            cat_block = Category.objects.create (key = 'Block', parent = cat_district)

        try:
            cat_grampanchayat = Category.objects.get (key = 'Gram Panchayat')
        except Category.DoesNotExist:
            cat_grampanchayat = Category.objects.create (key = 'Gram Panchayat', parent = cat_block)

        try:
            cat_village = Category.objects.get (key = 'Village')
        except Category.DoesNotExist:
            cat_village = Category.objects.create (key = 'Village', parent = cat_grampanchayat)

        try:
            attr_india = Attribute.objects.get (value = 'IN', category = cat_country)
        except Attribute.DoesNotExist:
            attr_india = Attribute.objects.create (value = 'IN', category = cat_country)

        try:
            codename = CodeName.objects.get (code = 'IN')
            codename.name = 'India'
            codename.save ()
        except CodeName.DoesNotExist:
            codename = CodeName.objects.create (code = 'IN', name = 'India')


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

            state_code = '.'.join (['IN', state_code])
            distt_code = '.'.join ([state_code, distt_code])
            block_code = '.'.join ([distt_code, block_code])
            gp_code    = '.'.join ([block_code, gp_code])
            vill_code  = '.'.join ([gp_code, vill_code])

            try:
                attr_state = Attribute.objects.get (value = state_code, category = cat_state)
            except Attribute.DoesNotExist:
                attr_state = Attribute.objects.create (value = state_code, category = cat_state)
            attr_state.parents.add (attr_india)

            try:
                attr_distt = Attribute.objects.get (value = distt_code, category = cat_district)
            except Attribute.DoesNotExist:
                attr_distt = Attribute.objects.create (value = distt_code, category = cat_district)
            attr_distt.parents.add (attr_state)

            try:
                attr_block = Attribute.objects.get (value = block_code, category = cat_block)
            except Attribute.DoesNotExist:
                attr_block = Attribute.objects.create (value = block_code, category = cat_block)
            attr_block.parents.add (attr_distt)

            try:
                attr_grampanchayat = Attribute.objects.get (value = gp_code,
                                                            category = cat_grampanchayat)
            except Attribute.DoesNotExist:
                attr_grampanchayat = Attribute.objects.create (value = gp_code,
                                                               category = cat_grampanchayat)
            attr_grampanchayat.parents.add (attr_block)

            try:
                attr_village = Attribute.objects.get (value = vill_code, category = cat_village)
            except Attribute.DoesNotExist:
                attr_village = Attribute.objects.create (value = vill_code, category = cat_village)
            attr_village.parents.add (attr_grampanchayat)

            try:
                codename = CodeName.objects.get (code = state_code)
                codename.name = state_name
                codename.save ()
            except CodeName.DoesNotExist:
                codename = CodeName.objects.create (code = state_code, name = state_name)

            try:
                codename = CodeName.objects.get (code = distt_code)
                codename.name = distt_name
                codename.save ()
            except CodeName.DoesNotExist:
                codename = CodeName.objects.create (code = distt_code, name = distt_name)

            try:
                codename = CodeName.objects.get (code = block_code)
                codename.name = block_name
                codename.save ()
            except CodeName.DoesNotExist:
                codename = CodeName.objects.create (code = block_code, name = block_name)

            try:
                codename = CodeName.objects.get (code = gp_code)
                codename.name = gp_name
                codename.save ()
            except CodeName.DoesNotExist:
                codename = CodeName.objects.create (code = gp_code, name = gp_name)

            try:
                codename = CodeName.objects.get (code = vill_code)
                codename.name = vill_name
                codename.save ()
            except CodeName.DoesNotExist:
                codename = CodeName.objects.create (code = vill_code, name = vill_name)

            try:
                latlong = LatLong.objects.get (location = attr_village)
                latlong.latitude = latitude
                latlong.langitude = longitude
                latlong.save ()
            except LatLong.DoesNotExist:
                latlong = LatLong.objects.create (location = attr_village,
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



    def populate_complaint_status (self):
        try:
            cat_complaintstatus = Category.objects.get (key = 'Status')
        except Category.DoesNotExist:
            cat_complaintstatus = Category.objects.create (key = 'Status')

        statuses = ['New', 'Reopened', 'Acknowledged', 'Open', 'Resolved', 'Closed']
        for status in statuses:
            try:
                s = Attribute.objects.get (value = status)
            except Attribute.DoesNotExist:
                s = Attribute.objects.create (value = status, category = cat_complaintstatus)

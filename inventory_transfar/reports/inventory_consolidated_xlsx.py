from odoo import models

class INvConsolidatedEXcel(models.AbstractModel):
    _name='report.inventory_transfar.report_inventory_xls'
    _inherit='report.report_xlsx.abstract'

    def generate_xlsx_report(self,workbook,data,vals):

        result_data=self.env['report.inventory_transfar.report_inventory'].retrive_data(data['from_date'],data['to_date'],data['picking_type'])

        sheet=workbook.add_worksheet('Inventory Consolidated Report')
        bold=workbook.add_format({'bold':True})

        row=3
        col=3

        sheet.write(row,col,'Reference',bold)
        sheet.write(row,col+1,'From',bold)
        sheet.write(row,col+2,'To',bold)

        r=1
        c=1
        for i in result_data:

            print(i['state'])
            state=i['state']
            sheet.write(row+r,col+c-1,state,bold)
            inner_row=row+r+1
            for rec in i['data']:
                print('::::::data::::::::',rec['reference'])
                ref=rec['reference']
                from_location=rec['from_location']
                to_location=rec['to_location']
                sheet.write(inner_row,)
            r=r+1    


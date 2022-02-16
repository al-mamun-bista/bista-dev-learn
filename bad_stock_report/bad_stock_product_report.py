from odoo import models,fields,api
from datetime import datetime,timedelta

class BadStockReport(models.TransientModel):
    _name='bad.stock.report'



    def bad_stock_data(self):
        date=datetime.now().date()
        new_date = date + timedelta(days=-30)

        black_data=self.env['stock.production.lot'].search([('create_date', '>=', new_date),('create_date', '<=', date)])


        result = []
        dict = {}

        if black_data:
            dict={'color':'black'}
            list_of_data = []
            for i in black_data:
                inner_dict = {}
                inner_dict['name'] = i.product_id.product_tmpl_id.name
                inner_dict['lot'] = i.name
                inner_dict['qty'] = i.product_qty
                list_of_data.append(inner_dict)
            dict['data'] = list_of_data
            result.append(dict)



        new_date_2=new_date+timedelta(days=-30)

        orange_data=self.env['stock.production.lot'].search([('create_date', '>=', new_date_2),('create_date', '<', new_date)])

        if orange_data:
            dict={'color':'orange'}
            list_of_data = []
            for i in orange_data:
                inner_dict = {}
                inner_dict['name'] = i.product_id.product_tmpl_id.name
                inner_dict['lot'] = i.name
                inner_dict['qty'] = i.product_qty
                list_of_data.append(inner_dict)
            dict['data'] = list_of_data
            result.append(dict)
        new_date_3=new_date_2+timedelta(days=-30)


        yellow_data=self.env['stock.production.lot'].search([('create_date', '>=', new_date_3),('create_date', '<', new_date_2)])


        if yellow_data:
            dict={'color':'yellow'}
            list_of_data = []
            for i in yellow_data:
                inner_dict = {}
                inner_dict['name'] = i.product_id.product_tmpl_id.name
                inner_dict['lot'] = i.name
                inner_dict['qty'] = i.product_qty
                list_of_data.append(inner_dict)
            dict['data'] = list_of_data
            result.append(dict)
        new_date_4=new_date_3+timedelta(days=-30)
        

        red_data = self.env['stock.production.lot'].search([('create_date', '<', new_date_4)])
        if red_data:
            dict={'color':'red'}
            list_of_data = []
            for i in red_data:
                inner_dict = {}
                inner_dict['name'] = i.product_id.product_tmpl_id.name
                inner_dict['lot'] = i.name
                inner_dict['qty'] = i.product_qty
                list_of_data.append(inner_dict)
            dict['data'] = list_of_data
            result.append(dict)


        data={
            'from_data':'Empty String',
            'data':result
        }
        return self.env.ref('bad_stock_report.action_report_bad_stock').report_action(self,data=data)    









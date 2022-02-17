from odoo import fields, models, api
import datetime


class BadDueReport(models.Model):
    _name = 'bad.due.report'

    def bad_due_report(self):
        today = datetime.datetime.now().date()

        thirty_days_prev_start = datetime.datetime.strptime(str(today - datetime.timedelta(days=30)), '%Y-%m-%d')
        thirty_days_prev_end = datetime.datetime.strptime(str(datetime.datetime.now().date()), '%Y-%m-%d').replace(hour=23, minute=59, second=59)

        sixty_days_prev_start = datetime.datetime.strptime(str(today - datetime.timedelta(days=60)), '%Y-%m-%d')
        sixty_days_prev_end = datetime.datetime.strptime(str(today - datetime.timedelta(days=31)), '%Y-%m-%d').replace(hour=23, minute=59, second=59)

        ninety_days_prev_start = datetime.datetime.strptime(str(today - datetime.timedelta(days=90)), '%Y-%m-%d')
        ninety_days_prev_end = datetime.datetime.strptime(str(today - datetime.timedelta(days=61)), '%Y-%m-%d').replace(hour=23, minute=59, second=59)

        more_than_ninety_end = datetime.datetime.strptime(str(today - datetime.timedelta(days=91)), '%Y-%m-%d').replace(hour=23, minute=59, second=59)

        so_invoice_datas_thirty = self.env['account.move'].search([('invoice_date', '>=', thirty_days_prev_start), ('invoice_date', '<=', thirty_days_prev_end), ('payment_state', '!=', 'paid'), ('state', '=', 'posted'), ('move_type', '=', 'out_invoice')])

        so_invoice_datas_sixty = self.env['account.move'].search([('invoice_date', '>=', sixty_days_prev_start), ('invoice_date', '<=', sixty_days_prev_end), ('payment_state', '!=', 'paid'), ('move_type', '=', 'out_invoice')])

        so_invoice_datas_ninety = self.env['account.move'].search([('invoice_date', '>=', ninety_days_prev_start), ('invoice_date', '<=', ninety_days_prev_end), ('payment_state', '!=', 'paid'), ('move_type', '=', 'out_invoice')])

        so_invoice_datas_ninety_more = self.env['account.move'].search([('invoice_date', '<=', more_than_ninety_end), ('payment_state', '!=', 'paid'), ('move_type', '=', 'out_invoice')])

        data_list = []

        if len(so_invoice_datas_thirty)>0:
            for data in so_invoice_datas_thirty:
                so_dict = {
                    'invoice_num': data.payment_reference,
                    'invoice_date': data.invoice_date,
                    'invoice_amount': data.amount_total,
                    'customer': data.partner_id.name,
                    'color': 'black',
                }
                data_list.append(so_dict)


        if len(so_invoice_datas_sixty)>0:
            for data in so_invoice_datas_sixty:
                so_dict = {
                    'invoice_num': data.payment_reference,
                    'invoice_date': data.invoice_date,
                    'invoice_amount': data.amount_total,
                    'customer': data.partner_id.name,
                    'color': 'orange',
                }
                data_list.append(so_dict)

        if len(so_invoice_datas_ninety)>0:
            for data in so_invoice_datas_ninety:
                so_dict = {
                    'invoice_num': data.payment_reference,
                    'invoice_date': data.invoice_date,
                    'invoice_amount': data.amount_total,
                    'customer': data.partner_id.name,
                    'color': 'yellow',
                }
                data_list.append(so_dict)

        if len(so_invoice_datas_ninety_more)>0:
            for data in so_invoice_datas_ninety_more:
                so_dict = {
                    'invoice_num': data.payment_reference,
                    'invoice_date': data.invoice_date,
                    'invoice_amount': data.amount_total,
                    'customer': data.partner_id.name,
                    'color': 'red',
                }
                data_list.append(so_dict)

        datas = {
            'data': data_list
        }
        return self.env.ref('bad_due_report.action_bad_due_report_generate').report_action(self, data=datas)







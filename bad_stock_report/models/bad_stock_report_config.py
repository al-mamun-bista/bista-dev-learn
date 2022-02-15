from odoo import fields, models, api
import datetime


class ProductWisePurchaseReportWizard(models.Model):
    _name = 'bad.stock.report.config'
    _description = 'bad.stock.report.config'

    days_duration = fields.Integer(string='Stock Config Days')
    user_id = fields.Many2many('res.users', string='Salesperson')

    def get_stock_production_lot_data(self):
        message_list = []
        today = datetime.datetime.now().date()
        bad_stock_ids = self.env['bad.stock.report.config'].sudo().search([])
        for day in bad_stock_ids:
            diff = datetime.timedelta(days=day.days_duration)
            prev_day = today - diff
            from_date = datetime.datetime.strptime(str(prev_day), '%Y-%m-%d')
            to_date = from_date.replace(hour=23, minute=59, second=59)
            spl = self.env['stock.production.lot'].sudo().search([('create_date', '<=', to_date)])
            for data in spl:
                product_name = data.product_id.display_name
                lot_no = data.name
                qty = self.env['stock.move.line'].search([('lot_id', '=', data.id), ('lot_name', '=', data.name)]).qty_done

                if day.days_duration<30:
                    color = 'black'
                if day.days_duration>=30 and day.days_duration<60:
                    color = 'orange'
                if day.days_duration>=60 and day.days_duration<90:
                    color = 'yellow'
                if day.days_duration>=90:
                    color = 'red'
                message_list.append({'product': product_name, 'lot_no': lot_no, 'qty':qty, 'color': color})


        user_ids = self.env['bad.stock.report.config'].search([]).user_id
        for user in user_ids:
            message_body = "<p>Dear sir,&nbsp;</p><p>Product lots data are given below:</p><ul>"
            lot_list_flag = []
            partner_id = user.partner_id
            for data in message_list:
                if data['lot_no'] not in lot_list_flag:
                    if data['color'] == 'black':
                        message_body += "<li><p style='color:black'>%s - %s - %s</p></li>" % (data['product'], data['lot_no'], data['qty'])
                    if data['color'] == 'yellow':
                        message_body += "<li><p style='color:yellow'>%s - %s - %s</p></li>"%(data['product'], data['lot_no'], data['qty'])
                    if data['color'] == 'red':
                        message_body += "<li><p style='color:red'>%s - %s - %s</p></li>"%(data['product'], data['lot_no'], data['qty'])
                    if data['color'] == 'orange':
                        message_body += "<li><p style='color:orange'>%s - %s - %s</p></li>"%(data['product'], data['lot_no'], data['qty'])

                    lot_list_flag.append(data['lot_no'])
            message_body += "</ul>"
            self.notification_to_user('Stock Lot Notification', message_body, partner_id)

    def notification_to_user(self, name, msg, partner_id):
        body = msg
        values = {
            'subject': name,
            'body_html': body,
            'record_name': "Due Notification",
            'email_from': self.env.user.email_formatted,
            'reply_to': self.env.user.email_formatted,
            'email_to': partner_id.email,
            'model': 'account.move',
            'res_id': self.id,
            'message_type': 'user_notification',
        }
        message = self.env['mail.mail'].sudo().create(values)

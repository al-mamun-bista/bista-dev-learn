from odoo import fields, models, api
import datetime


class ProductWisePurchaseReportWizard(models.Model):
    _name = 'due.days.mail.config'
    _description = 'due.days.mail.config'

    days_duration = fields.Integer(string='Mail Schedule Days')

    def get_cust_and_salesman_data(self):
        today = datetime.datetime.now().date()
        durations = self.env['due.days.mail.config'].search([])
        dict_for_cust = {}
        dict_for_sp = {}

        for day in durations:
            day = day.days_duration
            diff = datetime.timedelta(days=day)
            prev_day = today - diff
            from_date = datetime.datetime.strptime(str(prev_day), '%Y-%m-%d')
            to_date = from_date.replace(hour=23, minute=59, second=59)
            so_invoice_datas = self.env['account.move'].search([('invoice_date', '>=', prev_day), ('invoice_date', '<=', prev_day), ('payment_state', '!=', 'paid')])
            if len(so_invoice_datas)>0:
                for i in so_invoice_datas:
                    so_dict = {
                        'invoice_num': i.payment_reference,
                        'invoice_date': i.invoice_date,
                        'so_num': i.invoice_origin,
                        'invoice_amount': i.amount_total,
                        'due_amount': i.amount_residual_signed,
                        'sales_person_id': i.invoice_user_id.id,
                        'sales_person': i.invoice_user_id.name,
                        'sales_person_email': i.invoice_user_id.email if i.invoice_user_id.email else '',

                        'customer_id': i.partner_id.id,
                        'customer': i.partner_id.name,
                        'customer_email': i.partner_id.email if i.partner_id.email else '',
                    }
                    if so_dict['customer'] not in dict_for_cust:
                        dict_for_cust[so_dict['customer']] = [so_dict]
                    else:
                        dict_for_cust[so_dict['customer']].append(so_dict)

                    if so_dict['sales_person'] not in dict_for_sp:
                        dict_for_sp[so_dict['sales_person']] = {so_dict['customer']:[so_dict]}
                    else:
                        if so_dict['customer'] in dict_for_sp[so_dict['sales_person']]:
                            dict_for_sp[so_dict['sales_person']][so_dict['customer']].append(so_dict)
                        else:
                            dict_for_sp[so_dict['sales_person']][so_dict['customer']] = [so_dict]

        message_for_salesman = "<p>Dear sir,&nbsp;</p><p>Here is the list of customers invoices.&nbsp;</p><ul>"
        for i in dict_for_sp:
            for j in dict_for_sp[i]:
                paragraph = "<li ><p><b>%s</b></p><ul class="">"%(j)
                for k in dict_for_sp[i][j]:
                    user_id = k['sales_person_id']
                    paragraph+="<li><p><b>Date:</b> %s - <b>Invoice No.:</b> %s - <b>Total:</b> %s - <b>Due Amount:</b> %s</p></li>"%(k['invoice_date'],k['invoice_num'],k['invoice_amount'],k['due_amount'])
                paragraph+="</ul></li>"
                message_for_salesman+=paragraph
            message_for_salesman+="</ul>"
        self.notification_to_user("Due notification", message_for_salesman, user_id)
        message_for_salesman = "<p>Dear sir,&nbsp;</p><p>Here is the list of customers invoices.&nbsp;</p><ul>"

        message_for_customer = "<p>Dear sir,&nbsp;</p><p>We would like to give you a reminder for the payment of the following due invoices.&nbsp;</p><ul>"
        for i in dict_for_cust:
            for j in dict_for_cust[i]:
                cust_email = j['customer_email']
                partner_id = j['customer_id']
                message_for_customer += "<li><p><b>Date:</b> %s - <b>Invoice No.:</b> %s - <b>Total:</b> %s - <b>Due Amount:</b> %s</p></li>"%(j['invoice_date'],j['invoice_num'],j['invoice_amount'],j['due_amount'])
            self.notification_to_customer("Due notification", message_for_customer, partner_id)
            message_for_customer = "<p>Dear sir,&nbsp;</p><p>We would like to give you a reminder for the payment of the following due invoices.&nbsp;</p><ul>"

    def notification_to_customer(self, name, msg, partner_id):
        body = msg
        values = {
            'subject': name,
            'body_html': body,
            'record_name': "Due Notification",
            'email_from': self.env.user.email_formatted,
            'reply_to': self.env.user.email_formatted,
            'email_to': self.env['res.partner'].search([('id', '=', partner_id)]).email,
            'model': 'account.move',
            'res_id': self.id,
            'message_type': 'user_notification',
        }
        message = self.env['mail.mail'].sudo().create(values)
        notification = self.env['mail.notification'].sudo().create({
            'mail_message_id': message.id,
            'notification_type': 'email',
            'res_partner_id': partner_id
        })
        notification = self.env['mail.notification'].sudo().create({
            'mail_message_id': message.id,
            'notification_type': 'email',
            'res_partner_id': partner_id
        })

    def notification_to_user(self, name, msg, user_id):
        user_id = self.env['res.users'].search([('id', '=', user_id)]).partner_id
        partner_id = self.env['res.partner'].search([('id', '=', user_id.id)]).id
        body = msg
        values = {
            'subject': name,
            'body_html': body,
            'record_name': "Due Notification",
            'email_from': self.env.user.email_formatted,
            'reply_to': self.env.user.email_formatted,
            'email_to': self.env['res.partner'].search([('id', '=', partner_id)]).email,
            'model': 'account.move',
            'res_id': self.id,
            'message_type': 'user_notification',
        }
        message = self.env['mail.mail'].sudo().create(values)
        notification = self.env['mail.notification'].sudo().create({
            'mail_message_id': message.id,
            'notification_type': 'email',
            'res_partner_id': partner_id
        })
        notification = self.env['mail.notification'].sudo().create({
            'mail_message_id': message.id,
            'notification_type': 'email',
            'res_partner_id': partner_id
        })

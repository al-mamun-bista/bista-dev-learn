from odoo import api,fields,models
from datetime import datetime
from xlsxwriter import Workbook
import base64
import io



class InventoryConsolidatedWizard(models.TransientModel):
    _name = 'consolidated.report.wizard'
    _description='Wizard For Inventory Report'

    from_date = fields.Datetime( string='From Date', default=fields.Datetime.now(), required=True )
    to_date = fields.Datetime( string='To Date', default=fields.Datetime.now(), required=True)
    picking_type_id = fields.Many2one( 'stock.picking.type', string='Operation Type')
    download_file = fields.Binary('File')

    # Function for retriving report's data
    def retrive_data(self,from_date,to_date,picking_type_id):
        result = []
        dict = {}
        company_id = self.env.context.get('allowed_company_ids')
        
        # For retriving Assigned State Data
        if picking_type_id:
            stock_pickings_data = self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('picking_type_id','=',picking_type_id),('state','=','assigned'),('company_id','=',company_id[0])])
        else:
            stock_pickings_data=self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('state','=','assigned'),('company_id','=',company_id[0])])   
        if stock_pickings_data:
            dict = {'state':'Ready'}
            list_of_data = []
            for i in stock_pickings_data:
                inner_dict = {}
                inner_dict['reference'] = i.name
                inner_dict['from_location'] = i.location_id.complete_name
                inner_dict['to_location'] = i.location_dest_id.complete_name
                inner_dict['origin']=i.origin
                list_of_data.append(inner_dict)
            dict['data'] = list_of_data
            result.append(dict)

        # For retriving Done State Data
        if picking_type_id:
            stock_pickings_data = self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('picking_type_id','=',picking_type_id),('state','=','done'),('company_id','=',company_id[0])])
        else:
            stock_pickings_data = self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('state','=','done'),('company_id','=',company_id[0])])    
        if stock_pickings_data:
            dict = {'state':'Done'}
            list_of_data = []
            for i in stock_pickings_data:
                inner_dict = {}
                inner_dict['reference'] = i.name
                inner_dict['from_location'] = i.location_id.complete_name
                inner_dict['to_location'] = i.location_dest_id.complete_name
                inner_dict['origin']=i.origin
                list_of_data.append(inner_dict)
            dict['data'] = list_of_data
            result.append(dict)

        # For retriving Draft State Data
        if picking_type_id:
            stock_pickings_data = self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('picking_type_id','=',picking_type_id),('state','=','draft'),('company_id','=',company_id[0])])
        else:    
            stock_pickings_data = self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('state','=','draft'),('company_id','=',company_id[0])])
        if stock_pickings_data:
            dict = {'state':'Draft'}
            list_of_data = []
            for i in stock_pickings_data:
                inner_dict = {}
                inner_dict['reference'] = i.name
                inner_dict['from_location'] = i.location_id.complete_name
                inner_dict['to_location'] = i.location_dest_id.complete_name
                inner_dict['origin']=i.origin
                list_of_data.append(inner_dict)
            dict['data'] = list_of_data
            result.append(dict)

        # For retriving Confirmed State Data
        if picking_type_id:    
            stock_pickings_data=self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('picking_type_id','=',picking_type_id),('state','=','confirmed'),('company_id','=',company_id[0])])
        else:
            stock_pickings_data=self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('state','=','confirmed'),('company_id','=',company_id[0])])
        if stock_pickings_data:
            dict = {'state':'Wating'}
            list_of_data = []
            for i in stock_pickings_data:
                inner_dict = {}
                inner_dict['reference'] = i.name
                inner_dict['from_location'] = i.location_id.complete_name
                inner_dict['to_location'] = i.location_dest_id.complete_name
                inner_dict['origin']=i.origin
                list_of_data.append(inner_dict)
            dict['data'] = list_of_data
            result.append(dict)

        # For retriving Waiting State Data
        if picking_type_id:
            stock_pickings_data = self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('picking_type_id','=',picking_type_id),('state','=','wating'),('company_id','=',company_id[0])])
        else:
            stock_pickings_data = self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('state','=','wating'),('company_id','=',company_id[0])])    
        if stock_pickings_data:
            dict = {'state':'Wating Another Operation'}
            list_of_data = []
            for i in stock_pickings_data:
                inner_dict = {}
                inner_dict['reference'] = i.name
                inner_dict['from_location'] = i.location_id.complete_name
                inner_dict['to_location'] = i.location_dest_id.complete_name
                inner_dict['origin']=i.origin
                list_of_data.append(inner_dict)
            dict['data'] = list_of_data
            result.append(dict) 

        # For retriving Cancel State Data
        if picking_type_id:
            stock_pickings_data = self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('picking_type_id','=',picking_type_id),('state','=','cancel'),('company_id','=',company_id[0])])
        else:
            stock_pickings_data = self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('state','=','cancel'),('company_id','=',company_id[0])])    
        if stock_pickings_data:
            dict = {'state':'Cancel'}
            list_of_data = []
            for i in stock_pickings_data:
                inner_dict = {}
                inner_dict['reference'] = i.name
                inner_dict['from_location'] = i.location_id.complete_name
                inner_dict['to_location'] = i.location_dest_id.complete_name
                inner_dict['origin']=i.origin
                list_of_data.append(inner_dict)
            dict['data'] = list_of_data
            result.append(dict)        
       
        return result # Return Final Result

    # Function for print the pdf report
    def print_report(self,data=None):
        docids = self.env['consolidated.report.wizard'].search([]).ids
        data={
            'from_date':self.from_date,
            'to_date':self.to_date,
            'picking_type_id':self.picking_type_id.id
        }
        
        return self.env.ref('inventory_transfar.action_report_inventory_consolidated').report_action(docids, data=data)

    # Function for print xlsx report    
    def print_excel_report(self):
        result = self.retrive_data(self.from_date, self.to_date, self.picking_type_id.id )
        s_date = str(self.from_date) # start date
        e_date = str(self.to_date) # end date
        type = self.picking_type_id.name # operation type or picking type name
        stream = io.BytesIO()

        workbook = Workbook(stream, {'in_memory': True})
        worksheet = workbook.add_worksheet('Inventory Consolidated Report')
        worksheet2=workbook.add_worksheet('Test')


        # format to use the column element align in the center
        center = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
        })
        # format to use for make column element bold
        bold = workbook.add_format({'bold':True,
        'bg_color':'#BCE4E5',
        'border': 0
        })
        # Created a format to use in the merged range for Report name Heading.
        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#FF7276',
            'font_size':18
            })
        # Created a format to use in column Heading
        merge_format_coloumn_header = workbook.add_format({
            'bold': 1,
            'border': 0,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#F8AA97',
            'font_size':14
            })
        # Created a format to use in other heading element like strat date, end date, operation type
        merge_format_2 = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size':11
        })    

        # Format for border on cell's top,left,right
        format_top=workbook.add_format({
            'left': 5,'top':5,'right':5,'border_color':'#0000FF'
        })  
        # Format for border on cell's left,right
        format_left_right=workbook.add_format({
            'left': 5,'right':5,'border_color':'#0000FF'
        })  
        # Format for border on cell's left,right,bottom
        format_bottom=workbook.add_format({
            'left':5,'bottom':5,'right':5,'border_color':'#0000FF'
        })
        # format for white back-ground on cells
        format_white=workbook.add_format({
            'bg_color':'#ffffff'
        })

        # starting row and column for result data
        if self.picking_type_id:
            row = 7
            col = 1
        else:
            row = 6    
            col = 1   

        # start Design for xlsx report

        # create boder arround three criteria of report like start date,end date,operation type 
        if self.picking_type_id:
            worksheet.conditional_format(2,1,2,1,{'type':'formula','criteria': 'True','format':format_top})   
            worksheet.conditional_format(3,1,3,1,{'type':'formula','criteria': 'True','format':format_left_right})   
            worksheet.conditional_format(4,1,4,1,{'type':'formula','criteria': 'True','format':format_bottom})
        else:
            worksheet.conditional_format(2,1,2,1,{'type':'formula','criteria': 'True','format':format_top})
            worksheet.conditional_format(3,1,3,1,{'type':'formula','criteria': 'True','format':format_bottom})

        # insert image and make cell's background white
        worksheet.insert_image('E1','/home/ankit/Downloads/bista_logo.png',{'x_scale': 0.37, 'y_scale':0.31})  
        worksheet.write(2,4,'',format_white)           
        worksheet.write(3,4,'',format_white)           
        worksheet.write(4,4,'',format_white)

        # border around logo's cell top,left,right
        worksheet.conditional_format(2,4,2,4,{'type':'formula','criteria': 'True','format':workbook.add_format({
            'top':1,
            'left':1,
            'right':1
        })})
        # border around logo,s right
        worksheet.conditional_format(3,4,3,4,{'type':'formula','criteria': 'True','format':workbook.add_format({  
            'right':1
        })})
        # border around logo,s bottom,left,right
        worksheet.conditional_format(4,4,4,4,{'type':'formula','criteria': 'True','format':workbook.add_format({
            'bottom':1,
            'left':1,
            'right':1
        })})     
        worksheet.merge_range('B1:E1','Inventory Consolidated Report',merge_format)    
        worksheet.merge_range('B3:D3','Start Date:'+s_date,merge_format_2)
        worksheet.merge_range('B4:D4','End Date:'+e_date,merge_format_2)
        if self.picking_type_id:
            worksheet.merge_range('B5:D5','Operation Type:'+type,merge_format_2)    
        worksheet.set_row(0,25)
        worksheet.set_column(0,0,5)
        worksheet.set_column(1,1,25)
        worksheet.set_column(2,2,25)
        worksheet.set_column(3,3,25)
        worksheet.set_column(4,4,25)
        worksheet.write(row, col, 'Reference', merge_format_coloumn_header)
        worksheet.write(row, col+1, 'From', merge_format_coloumn_header)
        worksheet.write(row, col+2, 'To', merge_format_coloumn_header)
        worksheet.write(row, col+3, 'Source Document', merge_format_coloumn_header)
        r = 1 # counter for incriment the row 
        for i in result:
            state = i['state']
            worksheet.write(row+r,col,state,bold)
            worksheet.write(row+r,col+1,'',bold)
            worksheet.write(row+r,col+2,'',bold)
            worksheet.write(row+r,col+3,'',bold)
            inner_row = row+r+1
            for rec in i['data']:
                ref = rec['reference']
                from_location = rec['from_location']
                to_location = rec['to_location']
                origin=rec['origin']
                worksheet.write(inner_row, col, ref,center)
                worksheet.write(inner_row, col+1, from_location)
                worksheet.write(inner_row, col+2, to_location)
                worksheet.write(inner_row, col+3, origin)
                inner_row += 1
                r = r+1
            r = r + 1    
        
        bold_bottom_element_lable=workbook.add_format({
            'bold':True,
            'border':1
        })
        worksheet.write(row+r+2,col+1,'User Name',bold_bottom_element_lable)
        worksheet.write(row+r+2+1,col+1,'E-Mail',bold_bottom_element_lable)
        worksheet.write(row+r+2+2,col+1,'Phone',bold_bottom_element_lable)

        uid=self.env.context.get('uid')
        user_object=self.env['res.users'].browse([uid])

        border_bottom_element=workbook.add_format({
            'border':1
        })
        worksheet.write(row+r+2,col+2,user_object.partner_id.name,border_bottom_element)
        worksheet.write_url(row+r+2+1,col+2,user_object.partner_id.email,border_bottom_element)
        worksheet.write(row+r+2+2,col+2,user_object.partner_id.phone,border_bottom_element)
        worksheet2.write('A1','Reference Cell')
        worksheet.write_formula(row+r+2+4,col+1,"=Test!A1")

        workbook.close() # end of design and close the xlsx workbook object

        stream.seek(0)
        self.download_file = base64.encodebytes(stream.getvalue())
        stream.close()

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content?model=consolidated.report.wizard&field=download_file&id=%s&filename=InventoryReport.xlsx' % (self.id),
            'target': 'new',
        }


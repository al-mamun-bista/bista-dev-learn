from odoo import models,api

class AbstractInventoryConsolidated(models.AbstractModel):
    _name='report.inventory_transfar.report_inventory'



    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['consolidated.report.wizard'].browse(docids)

        from_date=data['from_date']

        to_date=data['to_date']

        picking_type_id=data['picking_type_id']

        data_line=self.retrive_data(from_date,to_date,picking_type_id)

        return {
              'doc_ids': self.ids,
              'doc_model':'report.action_report_inventory_consolidated.report_inventory',
              'docs': docs,
              'data':data_line
        }


    # Function for retriving report's data
    def retrive_data(self,from_date,to_date,picking_type_id):

        result=[]
        dict={}
        company_id=self.env.context.get('allowed_company_ids')
        
        # For retriving Assigned State Data
        if picking_type_id:
            stock_pickings_data=self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('picking_type_id','=',picking_type_id),('state','=','assigned'),('company_id','=',company_id[0])])
        else:
            stock_pickings_data=self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),('state','=','assigned'),('company_id','=',company_id[0])])   

        if stock_pickings_data:

            dict={'state':'Ready'}

            list_of_data=[]

            for i in stock_pickings_data:

                inner_dict={}
                inner_dict['reference']=i.name
                inner_dict['from_location']=i.location_id.complete_name
                inner_dict['to_location']=i.location_dest_id.complete_name
                list_of_data.append(inner_dict)

            dict['data']=list_of_data

            result.append(dict)

        # For retriving Done State Data
        if picking_type_id:
            stock_pickings_data=self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('picking_type_id','=',picking_type_id),('state','=','done'),('company_id','=',company_id[0])])
        else:
            stock_pickings_data=self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),('state','=','done'),('company_id','=',company_id[0])])    

        if stock_pickings_data:

            dict={'state':'Done'}

            list_of_data=[]

            for i in stock_pickings_data:

                inner_dict={}
                inner_dict['reference']=i.name
                inner_dict['from_location']=i.location_id.complete_name
                inner_dict['to_location']=i.location_dest_id.complete_name
                list_of_data.append(inner_dict)

            dict['data']=list_of_data

            result.append(dict)

        # For retriving Draft State Data
        if picking_type_id:
            stock_pickings_data=self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('picking_type_id','=',picking_type_id),('state','=','draft'),('company_id','=',company_id[0])])
        else:    
            stock_pickings_data=self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),('state','=','draft'),('company_id','=',company_id[0])])

        if stock_pickings_data:

            dict={'state':'Draft'}

            list_of_data=[]

            for i in stock_pickings_data:

                inner_dict={}
                inner_dict['reference']=i.name
                inner_dict['from_location']=i.location_id.complete_name
                inner_dict['to_location']=i.location_dest_id.complete_name
                list_of_data.append(inner_dict)

            dict['data']=list_of_data
            
            result.append(dict)

        # For retriving Confirmed State Data
        if picking_type_id:    
            stock_pickings_data=self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('picking_type_id','=',picking_type_id),('state','=','confirmed'),('company_id','=',company_id[0])])
        else:
            stock_pickings_data=self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),('state','=','confirmed'),('company_id','=',company_id[0])])
    

        if stock_pickings_data:

            dict={'state':'Wating'}

            list_of_data=[]

            for i in stock_pickings_data:

                inner_dict={}
                inner_dict['reference']=i.name
                inner_dict['from_location']=i.location_id.complete_name
                inner_dict['to_location']=i.location_dest_id.complete_name
                list_of_data.append(inner_dict)

            dict['data']=list_of_data
            
            result.append(dict)

        # For retriving Waiting State Data
        if picking_type_id:
            stock_pickings_data=self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('picking_type_id','=',picking_type_id),('state','=','wating'),('company_id','=',company_id[0])])
        else:
            stock_pickings_data=self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),('state','=','wating'),('company_id','=',company_id[0])])    

        if stock_pickings_data:

            dict={'state':'Wating Another Operation'}

            list_of_data=[]

            for i in stock_pickings_data:

                inner_dict={}
                inner_dict['reference']=i.name
                inner_dict['from_location']=i.location_id.complete_name
                inner_dict['to_location']=i.location_dest_id.complete_name
                list_of_data.append(inner_dict)

            dict['data']=list_of_data
            
            result.append(dict) 

        # For retriving Cancel State Data
        if picking_type_id:
            stock_pickings_data=self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),
            ('picking_type_id','=',picking_type_id),('state','=','cancel'),('company_id','=',company_id[0])])
        else:
            stock_pickings_data=self.env['stock.picking'].search([('create_date', '>=', from_date),('create_date', '<=', to_date),('state','=','cancel'),('company_id','=',company_id[0])])    

        if stock_pickings_data:

            dict={'state':'Cancel'}

            list_of_data=[]

            for i in stock_pickings_data:

                inner_dict={}
                inner_dict['reference']=i.name
                inner_dict['from_location']=i.location_id.complete_name
                inner_dict['to_location']=i.location_dest_id.complete_name
                list_of_data.append(inner_dict)

            dict['data']=list_of_data
            
            result.append(dict)        
       

                  

        return result

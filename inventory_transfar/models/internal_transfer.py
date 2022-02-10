from odoo import models,fields,api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class InternalTransfer(models.Model):
    _name='internal.transfer'
    _description='Product Internal Transfer'


    name=fields.Char(string='Name',readonly=True, default=lambda self: _('New'))

    partner_id=fields.Many2one('res.partner',string='Employe',required=True)

    location_from_id = fields.Many2one('stock.location', string="Source Location",required=True)

    location_destination_id=fields.Many2one('stock.location',string="Destination Location",required=True)

    date=fields.Datetime(string='Date',default=datetime.now())

    user_id=fields.Many2one('res.users',string='User',default=lambda self: self.env.user)

    transfer_ids=fields.One2many('internal.transfer.line','transfer_id',string='Transfer Ids')

    user_dest_id=fields.Many2one('res.users',string='Destination Location Manager',required=True)

    hide=fields.Boolean(default=False,compute='_check_user_dest_id')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirm'),
        ('sent', 'Delevery Created'),
        ('delivered', 'Delivered'),
        ('received', 'Received')], default='draft')
   
    stock_picking_id=fields.Many2one('stock.picking',string='Picking Id')

    lable=fields.Char('Lable',compute='_change_lable')

    # checking the demand quantity of product which is available in destination stock
    def _check_quantity(self):
        for rec in self.transfer_ids:
            data=self.env['stock.quant'].search([('location_id','=',self.location_from_id.id),('lot_id','=',rec.lot_id.id),('product_id','=',rec.product_id.id),('quantity','<',rec.product_qty)])
        return data    



    # button function for confirm the transfer of products and set the state to confirmed
    def action_confirm(self):

        if self._check_quantity():
            raise ValidationError('Demand Quantity is Gater Than Stock Quantity')
        template_id=self.env.ref('inventory_transfar.mail_transfer_mail_template')
        if template_id:
            template_id.send_mail(self.id,force_send=True,raise_exception=True,email_values={'email_to':self.user_dest_id.email})    
        self.state='confirmed'


    # override the create method for create a sequence value for 'name' field
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('internal.transfer') or _('New')     
        result = super(InternalTransfer, self).create(vals)
        return result


    # creating record for stock.picking and stock.move model 
    def create_picking(self):   

        type_id =self.env['stock.picking.type'].search([('name','=','Internal Transfers')],order='id asc',limit=1)   

        stock_picking_vals={
            'origin':self.name,
            'move_type':'direct',
            'state':'assigned',
            'date':self.date,
            'location_id':self.location_from_id.id,
            'location_dest_id':self.location_destination_id.id,
            'picking_type_id':type_id.id,
            'partner_id':self.partner_id.id,
            'company_id':self.env.user.company_id.id,
            'user_id':self.user_id.id,
        } 

        # creating record in stock.picking model
        picking_id=self.env['stock.picking'].create(stock_picking_vals)


        # store the  picking_id
        self.stock_picking_id=picking_id.id

        for transfer_ids in self.transfer_ids:

            stock_move_vals={
                'name':transfer_ids.product_id.name,
                'date':self.date,
                'company_id':self.env.user.company_id.id,
                'product_id':transfer_ids.product_id.id,
                'product_uom':transfer_ids.uom_id.id,
                'product_uom_qty':transfer_ids.product_qty,
                'location_id':self.location_from_id.id,
                'location_dest_id':self.location_destination_id.id,
                'partner_id':self.partner_id.id,
                'picking_id':picking_id.id,
                'state':'assigned',
                'origin':self.name,
                'procure_method':'make_to_stock',
                'picking_type_id':type_id.id,
            }

            # creating record in stock.move model
            move_id=self.env['stock.move'].create(stock_move_vals)

            stock_move_line_vals={
                'picking_id':picking_id.id,
                'move_id':move_id.id,
                'company_id':self.env.user.company_id.id,
                'product_id':transfer_ids.product_id.id,
                'product_uom_id':transfer_ids.uom_id.id,
                'product_uom_qty':transfer_ids.product_qty,
                'lot_id':transfer_ids.lot_id.id,
                'lot_name':transfer_ids.lot_id.name,
                'date':self.date,
                'location_id':self.location_from_id.id,
                'location_dest_id':self.location_destination_id.id,
                'state':'assigned',
                
            }

            # creating record in stock.move.line
            self.env['stock.move.line'].create(stock_move_line_vals)
            

        # change state value to 'sent'
        self.state='sent'



    # smart button function which redirect to form view of particular record from stock.picking model 
    def button_smart(self):   

        stock_picking_form = self.env.ref('stock.view_picking_form')

        return {
                    'name': _('Stock Picking'),
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'stock.picking',
                    'view_id': stock_picking_form.id,
                    'target': 'self',
                    'res_id':self.stock_picking_id.id,  
                }
                

    # function for change lable    
    def _change_lable(self):

        if self.stock_picking_id.state != 'done':
             self.lable='Delivery Created' 
             return self.lable
                    
        self.lable='Delivery Done'
        return self.lable

    # Deliver Button Function
    def button_delivery(self):

        stock_imdiate_transfer_vals={'show_transfers':False}

        # create record in stock.immediate.transfer for get the object 
        stock_imd_transfer_id=self.env['stock.immediate.transfer'].create(stock_imdiate_transfer_vals)
        
        for transfer_ids in self.transfer_ids:

            stock_imdiate_transfer_line_vals={
                'immediate_transfer_id':stock_imd_transfer_id.id,
                'picking_id':self.stock_picking_id.id,
                'to_immediate':True
            }

            # create record in stock.immediate.transfer.line
            stock_imd_transfer_line_id=self.env['stock.immediate.transfer.line'].create(stock_imdiate_transfer_line_vals)    

        # call the process function from this model using the object of stock.immediate.transfer model
        stock_imd_transfer_id.with_context({'button_validate_picking_ids':self.stock_picking_id.id}).process()

        self.state='delivered'

    
    # checking the logged in user and destination user both are same or not for hiding the receive button
    def _check_user_dest_id(self):

        user_id = self.env['res.users'].browse(self._uid)

        if self.user_dest_id:
            if user_id.id != self.user_dest_id.id:
                self.hide = True
                return self.hide
                
            self.hide = False
            return self.hide
          
    # Receive Button Function
    def button_receive(self):
        self.state='received' 
          

   


class InternalTransferLine(models.Model):
    _name='internal.transfer.line'
    _description='Product Lines for Internal Transfer'

    product_id = fields.Many2one('product.product', 'Product',index=True, required=True)

    product_qty=fields.Float('Quantity')    

    lot_id=fields.Many2one('stock.production.lot',string='Lot/Serial Number',domain="[('product_id', '=', product_id)]")

    uom_id=fields.Many2one('uom.uom','Unit of Measure')

    transfer_id=fields.Many2one('internal.transfer','Transfer Id')

    # changing uom_id value according to selected product_id
    @api.onchange('product_id')
    def _change_uom_id(self):
        
        self.uom_id=self.product_id.uom_id

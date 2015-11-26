# coding: utf-8
############################################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2011 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    coded by: hugo@vauxoo.com
#    planned by: Nhomar Hernandez <nhomar@vauxoo.com>
############################################################################
from openerp import fields, models, api, _
from lxml import etree


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Barrio
    hood_id = fields.Many2one('res.country.state.district.township.hood',
                              'Neighborhood')
    # Corregimiento
    township_id = fields.Many2one('res.country.state.district.township',
                                  'Township')
    # Distrito
    district_id = fields.Many2one('res.country.state.district',
                                  'District')

    @api.model
    def fields_view_get_address(self, arch):
        print '1====', arch
        street = _('Street...')
        street2 = _('Building, apartment, house...')
        country = _('Country...')
        state = _('Province...')
        district = _('District/City...')
        township = _('Township...')
        hood = _('Neighborhood...')
        city2 = _('City...')
        res = super(ResPartner, self).fields_view_get_address(arch)
        user_obj = self.env['res.users']
        fmt = user_obj.browse(self._uid).company_id.country_id
        fmt = fmt and fmt.address_format
        city = '<field name="city" placeholder="City..." style="width:\
                    40%%" modifiers="{&quot;invisible&quot;: true}"/>'
        for name in self._columns.keys():
            if name == 'city_id':
                city = '<field name="city" \
                        modifiers="{&quot;invisible&quot;: true}" \
                        placeholder="%s" style="width: 50%%" \
                        invisible="1"/><field name="city_id" \
                        on_change="onchange_city(city_id)" \
                        placeholder="%s" style="width: 40%%" \
                        modifiers="{&quot;invisible&quot;: true}"/>' % (
                    city2, city2)
        print 'self._context', self._context
        layouts = {
            '%(street)s %(street2)s\n%(state_name)s %(district_name)s %(township_name)s %(hood_name)s %(country_name)s': """
<page string="Contactos" attrs="{'invisible': [('is_company','=',False), ('child_ids', '=', [])]}" autofocus="autofocus" modifiers="{&quot;invisible&quot;: [[&quot;is_company&quot;, &quot;=&quot;, false], [&quot;child_ids&quot;, &quot;=&quot;, []]]}">
    <field name="child_ids" mode="tree" context="{'form_view_ref': 'l10n_pa_localization.view_partner_simple_form_panama', 'default_parent_id': active_id, 'default_street': street, 'default_street2': street2, 'default_city': city, 'default_state_id': state_id, 'default_zip': zip, 'default_country_id': country_id, 'default_supplier': supplier, 'default_customer': customer, 'default_use_parent_address': True}" modifiers="{}">
    </field>
</page>
"""
        }
        layouts2 = {
            '%(street)s %(street2)s\n%(state_name)s %(district_name)s %(township_name)s %(hood_name)s %(country_name)s': """
        <group>
            <label for="type"/>
            <div name="div_type">
                <field class="oe_inline" name="type" modifiers="{}"/>
            </div>
            <label for="street" string="Direcci&#243;n" attrs="{'invisible': [('use_parent_address','=', True)]}" modifiers="{&quot;invisible&quot;: [[&quot;use_parent_address&quot;, &quot;=&quot;, true]]}"/>
            <div attrs="{'invisible': [('use_parent_address','=', True)]}" name="div_address" modifiers="{&quot;invisible&quot;: [[&quot;use_parent_address&quot;, &quot;=&quot;, true]]}">
                <field name="street" placeholder="Calle..." modifiers="{}"/>
                <field name="street2" modifiers="{}"/>
                <field name="state_id" class="oe_no_button" placeholder="Province" modifiers="{}"/>
                <field name="country_id" placeholder="Pa&#237;s" class="oe_no_button" options="{&quot;no_open&quot;: True}" modifiers="{}"/>
            </div>
        </group>
"""
        }

#        layouts = {
#             '%(street)s %(street2)s\n%(state_name)s %(district_name)s '
#             '%(township_name)s %(hood_name)s %(country_name)s': """
# <group>
#     <group>
#         <label for="type" attrs="{'invisible': [('parent_id','=', False)]}"/>
#         <div attrs="{'invisible': [('parent_id','=', False)]}" name="div_type">
#             <field class="oe_inline"
#                 name="type"/>
#             <label for="use_parent_address" class="oe_edit_only"/>
#             <field name="use_parent_address" class="oe_edit_only oe_inline"
#                 on_change="onchange_address(use_parent_address, parent_id)"/>
#         </div>

#         <label for="street" string="Address"/>
#         <div>
#             %s
#             <field name="zip" modifiers="{&quot;invisible&quot;: true}"/>
#             <field name="street" placeholder="%s" class="o_address_street"
#             modifiers="{&quot;readonly&quot;: [[&quot;use_parent_address&quot;,
#             &quot;=&quot;, true]]}"/>
#             <field name="street2" placeholder="%s" class="o_address_street"
#             modifiers="{&quot;readonly&quot;: [[&quot;use_parent_address&quot;,
#             &quot;=&quot;, true]]}"/>
#             <field name="country_id" placeholder="%s" class="o_address_country"
#             options='{"no_open": True, "no_create": True}'
#             modifiers="{&quot;readonly&quot;: [[&quot;use_parent_address&quot;,
#             &quot;=&quot;, true]]}"/>
#             <field name="state_id" placeholder="%s" \
#             class="oe_no_button" on_change="onchange_state(state_id)" \
#             options='{"no_open": True}'
#             modifiers="{&quot;readonly&quot;: [[&quot;use_parent_address&quot;,
#             &quot;=&quot;, true]]}"/>
#             <field name="district_id" placeholder="%s" \
#             class="oe_no_button" options='{"no_open": True}'
#             modifiers="{&quot;readonly&quot;: [[&quot;use_parent_address&quot;,
#             &quot;=&quot;, true]]}"/>
#             <field name="township_id" placeholder="%s" \
#             class="oe_no_button" options='{"no_open": True}'
#             modifiers="{&quot;readonly&quot;: [[&quot;use_parent_address&quot;,
#             &quot;=&quot;, true]]}"/>
#             <field name="hood_id" placeholder="%s" \
#             class="oe_no_button" options='{"no_open": True}'
#             modifiers="{&quot;readonly&quot;: [[&quot;use_parent_address&quot;,
#             &quot;=&quot;, true]]}"/>
#         </div>
#         <field name="website" widget="url" placeholder="e.g. www.openerp.com"/>
#     </group>
#     <group>
#         <field name="function" placeholder="e.g. Sales Director"
#             attrs="{'invisible': [('is_company','=', True)]}"/>
#         <field name="phone" placeholder="e.g. +32.81.81.37.00"/>
#         <field name="mobile"/>
#         <field name="fax"/>
#         <field name="email" widget="email"/>
#         <field name="title" domain="[('domain', '=', 'contact')]"
#             options='{"no_open": True}' \
#             attrs="{'invisible': [('is_company','=', True)]}" />
#     </group>
# </group>
#             """ % (
#                 city, street, street2, country, state, district, township,
#                 hood)
#         }
        

        arch = res
        # for k, v in layouts.items():
        #     print '?'*32
        #     print 'kkk', k
        #     print 'fmt', fmt
        #     if fmt and (k in fmt):
        #         doc = etree.fromstring(res)
        #         # import pdb;pdb.set_trace()
        #         for node in doc.xpath("//field[@name='child_ids']"):
        #             print 'node', node
        #             # import pdb;pdb.set_trace()
        #             tree = etree.fromstring(v)
        #             node.getparent().replace(node, tree)

        #         arch = etree.tostring(doc)
        for k, v in layouts2.items():
            print '?'*32
            print 'kkk', k
            print 'fmt', fmt
            if fmt and (k in fmt):
                doc = etree.fromstring(res)
                # import pdb;pdb.set_trace()
                for node in doc.xpath("//field[@name='child_ids']"):
                    node.set('context', "{'kanban_view_ref': 'l10n_pa_localization.view_partner_simple_kanban_panama', 'form_view_ref': 'l10n_pa_localization.view_partner_simple_form_panama', 'default_parent_id': active_id, 'default_street': street, 'default_street2': street2, 'default_city': city, 'default_state_id': state_id, 'default_zip': zip, 'default_country_id': country_id, 'default_supplier': supplier, 'default_customer': customer, 'default_use_parent_address': True}")
                for node in doc.xpath("//div[@name='div_address']"):
                    print 'node', node
                    # import pdb;pdb.set_trace()
                    tree = etree.fromstring(v)
                    node.getparent().replace(node, tree)

                arch = etree.tostring(doc)
        print 'arch', arch
        return arch

    def fields_view_get(self, cr, user, view_id=None, view_type='form',
                        context=None, toolbar=False, submenu=False):
        if (not view_id) and (view_type == 'form') and context and context.get(
                'force_email', False):
            view_id = self.pool.get('ir.model.data').get_object_reference(
                cr, user, 'base', 'view_partner_form')[1]
        res = super(ResPartner, self).fields_view_get(
            cr, user, view_id, view_type, context, toolbar=toolbar,
            submenu=submenu)
        if view_type == 'form':
            fields_get = self.fields_get(
                cr, user, ['township_id', 'hood_id'], context)
            res['fields'].update(fields_get)
        return res

    def _address_fields(self, cr, uid, context=None):
        """ Returns the list of address fields that are synced from the parent
        when the `use_parent_address` flag is set. """
        res = super(ResPartner, self)._address_fields(cr, uid, context=context)
        res = res + ['district_id', 'township_id', 'hood_id']
        return res

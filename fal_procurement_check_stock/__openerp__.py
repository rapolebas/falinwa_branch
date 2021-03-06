# -*- coding: utf-8 -*-
# Falinwa Hans
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# -*- coding: utf-8 -*-
{
    "name": "PRO-16_Falinwa Procurement Check Stock First",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to provide automatic check stock first in make to order procurement method.
    """,
    "depends" : ['base', 'sale', 'stock', 'purchase', 'mrp', 'sale_stock', 'sale_mrp'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'stock_view.xml',
    ],
    'css': [],
    'js' : [
    ],
    'qweb': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
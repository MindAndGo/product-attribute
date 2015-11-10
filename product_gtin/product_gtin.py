# -*- coding: utf-8 -*-
##############################################################################
#
#    Product GTIN module for Odoo
#    Copyright (C) 2004-2011 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2010-2011 Camptocamp (<http://www.camptocamp.at>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import logging
_logger = logging.getLogger(__name__)

from openerp import models, fields, api, _
import operator
from openerp.exceptions import Warning, ValidationError


CONSTRAINT_MESSAGE = 'Error: Invalid EAN/GTIN code'
HELP_MESSAGE = ("EAN8 EAN13 UPC JPC GTIN \n"
                "http://en.wikipedia.org/wiki/Global_Trade_Item_Number")


def is_pair(x):
    return not x % 2


def check_ean8(eancode):
    """Check if the given ean code answer ean8 requirements
    For more details: http://en.wikipedia.org/wiki/EAN-8

    :param eancode: string, ean-8 code
    :return: boolean
    """
    if not eancode or not eancode.isdigit():
        return False

    if not len(eancode) == 8:
        _logger.warn('Ean8 code has to have a length of 8 characters.')
        return False

    sum = 0
    ean_len = int(len(eancode))
    for i in range(ean_len-1):
        if is_pair(i):
            sum += 3 * int(eancode[i])
        else:
            sum += int(eancode[i])
    check = 10 - operator.mod(sum, 10)
    if check == 10:
        check = 0

    return check == int(eancode[-1])


def check_upc(upccode):
    """Check if the given code answers upc requirements
    For more details:
    http://en.wikipedia.org/wiki/Universal_Product_Code

    :param upccode: string, upc code
    :return: bool
    """
    if not upccode or not upccode.isdigit():
        return False

    if not len(upccode) == 12:
        _logger.warn('UPC code has to have a length of 12 characters.')
        return False

    sum_pair = 0
    ean_len = int(len(upccode))
    for i in range(ean_len-1):
        if is_pair(i):
            sum_pair += int(upccode[i])
    sum = sum_pair * 3
    for i in range(ean_len-1):
        if not is_pair(i):
            sum += int(upccode[i])
    check = ((sum/10 + 1) * 10) - sum

    return check == int(upccode[-1])


def check_ean13(eancode):
    """Check if the given ean code answer ean13 requirements
    For more details:
    http://en.wikipedia.org/wiki/International_Article_Number_%28EAN%29

    :param eancode: string, ean-13 code
    :return: boolean
    """
    if not eancode or not eancode.isdigit():
        return False

    if not len(eancode) == 13:
        _logger.warn('Ean13 code has to have a length of 13 characters.')
        return False

    sum = 0
    ean_len = int(len(eancode))
    for i in range(ean_len-1):
        pos = int(ean_len-2-i)
        if is_pair(i):
            sum += 3 * int(eancode[pos])
        else:
            sum += int(eancode[pos])
    check = 10 - operator.mod(sum, 10)
    if check == 10:
        check = 0

    return check == int(eancode[-1])


def check_ean11(eancode):
    pass


def check_gtin14(eancode):
    pass


DICT_CHECK_EAN = {8: check_ean8,
                  11: check_ean11,
                  12: check_upc,
                  13: check_ean13,
                  14: check_gtin14,
                  }


def check_ean(eancode):
    if not eancode:
        return True
    if not len(eancode) in DICT_CHECK_EAN:
        return False
    try:
        int(eancode)
    except:
        return False
    return DICT_CHECK_EAN[len(eancode)](eancode)


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.one
    @api.constrains("barcode")
    def _check_ean_key(self):
        _logger.debug('Barcode check in product.')
        _logger.debug(self)
        if not check_ean(self.barcode):
            raise ValidationError(CONSTRAINT_MESSAGE)

#        return True

    barcode = fields.Char(
            'EAN/GTIN', size=14,
            help="Code for %s" % HELP_MESSAGE)
        

class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    
    @api.one
    @api.constrains("barcode")
    def _check_ean_key(self):
        if not check_ean(self.barcode):
                raise ValidationError(CONSTRAINT_MESSAGE)
            
            
    barcode = fields.Char(
            'EAN/GTIN', size=14,
            help="Code for %s" % HELP_MESSAGE)
    

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    @api.one
    @api.constrains("barcode")
    def _check_ean_key(self):
        if not check_ean(self.barcode):
            raise ValidationError(CONSTRAINT_MESSAGE)
    
    barcode = fields.Char(
            'EAN/GTIN', size=14,
            help="Code for %s" % HELP_MESSAGE)
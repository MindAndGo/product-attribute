# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3).
# © 2009 Sharoon Thomas Open Labs Business Solutions
# © 2014 Serv. Tecnol. Avanzados Pedro M. Baeza
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# © 2016 Pedro M. Baeza, Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.addons.base_multi_image.hooks import pre_init_hook_for_submodules


def pre_init_hook(cr):
    pre_init_hook_for_submodules(cr, "product.template", "image")

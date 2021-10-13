# -*- coding: utf-8 -*-

# Copyright © 2018-2020 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

{
    'name': 'Restriction of Analytic Account User',

    'depends': [
        'account',
    ],
    'data': [
        'security/analytic_account_user_restrict_security.xml',
        'views/res_users_views.xml',
        'views/account_move.xml',
    ],

}

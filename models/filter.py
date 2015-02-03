__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class WechatFilter(models.Model):
    _name = 'wechat.enterprise.filter'

    _order = 'sequence'

    name = fields.Char('Name', required=True)
    is_active = fields.Boolean('Is Active')
    is_template = fields.Boolean('Is Template')
    sequence = fields.Integer('Sequence')
    match = fields.Text('Match')
    action = fields.Text('Action')
    application = fields.Many2one('wechat.enterprise.application')

    _defaults = {
        'is_active': True,
        'sequence': 10,
    }
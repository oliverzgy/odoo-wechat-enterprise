__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class WechatAccount(models.Model):
    _name = 'wechat.enterprise.account'

    name = fields.Char('Name')
    code = fields.Char('Code')
    corp_id = fields.Char('CorpID')
    corpsecret = fields.Char('Corpsecret')


class WechatApplication(models.Model):
    _name = 'wechat.enterprise.application'

    name = fields.Char('Name')
    application_id = fields.Integer('Application ID')
    code = fields.Char('Code')
    token = fields.Char('Token')
    ase_key = fields.Char('EncodingAESKey')
    account = fields.Many2one('wechat.enterprise.account', 'Enterprise Account')

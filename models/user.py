__author__ = 'cysnake4713'

# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class WechatUser(models.Model):
    _name = 'wechat.enterprise.user'

    name = fields.Char('Name')
    login = fields.Char('Login')

    wechat_login = fields.Char('Wechat Account')
    mobile = fields.Char('Mobile')
    email = fields.Char('Email')
    job = fields.Char('Job')

    # TODO: department support



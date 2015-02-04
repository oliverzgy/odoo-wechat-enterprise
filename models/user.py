__author__ = 'cysnake4713'

# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _
from wechatpy.enterprise import WeChatClient


class WechatUser(models.Model):
    _name = 'wechat.enterprise.user'

    name = fields.Char('Name', required=True)
    login = fields.Char(' Login', required=True)

    user = fields.Many2one('res.users', 'User')

    wechat_login = fields.Char('Wechat Account')

    mobile = fields.Char('Mobile')
    email = fields.Char('Email')

    job = fields.Char('Job')
    # TODO: department support

    account = fields.Many2one('wechat.enterprise.account', required=True)

    _sql_constraints = [
        ('login_uniq', 'unique (login)', 'The login must be unique')
    ]


    @api.one
    @api.constrains('wechat_login', 'mobile', 'email')
    def _check_wechat_info(self):
        if not self.wechat_login and not self.mobile and not self.email:
            raise Warning(_('wechat_login, mobile, email can not be all none'))

    @api.model
    def create(self, vals):
        res = super(WechatUser, self).create(vals)
        client = WeChatClient(res.account.corp_id, res.account.corpsecret)

        client.user.create(user_id=vals['login'], name=vals['name'], department=1, position=vals['job'],
                           mobile=vals['mobile'], email=vals['email'], weixin_id=vals['wechat_login'])
        return res

    @api.multi
    def write(self, vals):
        res = super(WechatUser, self).write(vals)
        for user in self:
            client = WeChatClient(user.account.corp_id, user.account.corpsecret)
            client.user.update(user_id=user.login, name=user.name, department=1, position=user.job,
                               mobile=user.mobile, email=user.email, weixin_id=user.wechat_login)
        return res

    @api.multi
    def unlink(self):
        for user in self:
            client = WeChatClient(user.account.corp_id, user.account.corpsecret)
            client.user.delete(user_id=user.login)

        res = super(WechatUser, self).unlink()
        return res

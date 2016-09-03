from wechatpy.exceptions import WeChatClientException
from openerp.exceptions import ValidationError
__author__ = 'cysnake4713'

# coding=utf-8
from openerp import tools
import logging
from openerp import models, fields, api
from openerp.tools.translate import _
from wechatpy.enterprise import WeChatClient

_logger = logging.getLogger(__name__)


class WechatUser(models.Model):
    _name = 'wechat.enterprise.user'

    state = fields.Selection([('unbind', 'Unbind'), ('bind', 'Bind'),
                              ('invite','Invite'),('invited','Invited')], 'State')
    name = fields.Char('Name', required=True)
    login = fields.Char('Login', required=True)

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

    _defaults = {
        'state': 'unbind',
    }

    @api.one
    @api.constrains('wechat_login', 'mobile', 'email')
    def _check_wechat_info(self):
        if not self.wechat_login and not self.mobile and not self.email:
            raise Warning(_('wechat_login, mobile, email can not be all none'))

    @api.multi
    def bind(self):
        for user in self:
            client = WeChatClient(user.account.corp_id, user.account.corpsecret)
            try:
                wechat_user_info = client.user.get(user.login)
            except WeChatClientException:
                wechat_user_info = None
            if wechat_user_info:
                val = {'state': 'bind',
                       'name': wechat_user_info.get('name', None),
                       'job': wechat_user_info.get('position', None),
                       'mobile': wechat_user_info.get('mobile', None),
                       'email': wechat_user_info.get('email', None),
                       'wechat_login': wechat_user_info.get('weixinid', None),
                }
                user.write(val)
            else:
                client.user.create(user_id=user.login, name=user.name, department=1, position=user.job,
                                   mobile=user.mobile, email=user.email, weixin_id=user.wechat_login)
                user.state = 'bind'

    @api.multi
    def unbind(self):
        for user in self:
            if user.state == 'bind':
                client = WeChatClient(user.account.corp_id, user.account.corpsecret)
                try:
                    client.user.delete(user_id=user.login)
                except WeChatClientException, e:
                    _logger.error(e)
            user.state = 'unbind'

    @api.multi
    def write(self, vals):
        res = super(WechatUser, self).write(vals)
        for user in self:
            if user.state == 'bind':
                client = WeChatClient(user.account.corp_id, user.account.corpsecret)
                client.user.update(user_id=user.login, name=user.name, department=1, position=user.job,
                                   mobile=user.mobile, email=user.email, weixin_id=user.wechat_login)
        return res

    @api.multi
    def unlink(self):
        for user in self:
            if user.state == 'bind':
                client = WeChatClient(user.account.corp_id, user.account.corpsecret)
                client.user.delete(user_id=user.login)

        res = super(WechatUser, self).unlink()
        return res
    
    @api.multi
    def invite(self):
        for user in self:
            client = WeChatClient(user.account.corp_id, user.account.corpsecret)
            try:
                user.state='bind'
            except:
                user.state='unbind'
                raise ValidationError("%s hasn't been binded yet." % user.name)
            client.user.invite(user_id=user.login)
            user.state="invited"
            
            
                
                
        
        
import logging

__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _
from wechatpy.enterprise import WeChatClient

_logger = logging.getLogger(__name__)


class Message(models.Model):
    _name = 'wechat.enterprise.message'

    state = fields.Selection([('draft', 'Draft'), ('send', 'Send'), ('fail', 'Fail')], 'Status')

    account = fields.Many2one('wechat.enterprise.account')

    application = fields.Many2one('wechat.enterprise.application', 'Application')

    users = fields.Many2many('wechat.enterprise.user', 'rel_wechat_ep_message_user', 'message_id', 'user_id', 'Users')

    content = fields.Text('Content')

    result = fields.Text('result')

    _defaults = {
        'state': 'draft',
    }

    @api.model
    def process_message(self):
        self.search([('state', '=', 'draft')]).sent_message()

    @api.multi
    def sent_message(self):
        for message in self:
            user_ids = '|'.join([u.login for u in message.users])
            try:
                client = WeChatClient(message.account.corp_id, message.account.corpsecret)
                # TODO: all support
                client.message.send_text(message.application.application_id, user_ids, message.content)
                message.state = 'send'
            except Exception, e:
                message.state = 'fail'
                message.result = str(e)
                _logger.error(e)
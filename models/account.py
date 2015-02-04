__author__ = 'cysnake4713'
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.tools.safe_eval import safe_eval as eval
import re


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
    filters = fields.One2many('wechat.enterprise.filter', 'application', 'Filters')

    @api.one
    def process_request(self, msg):
        for a_filter in self.filters.filtered(lambda f: f.is_active is True):
            match_context = {
                'self': self,
                'msg': msg,
                'result': False,
                'context': {},
                're': re,
            }
            eval(a_filter.match, match_context, mode="exec", nocopy=True)
            if match_context['result']:
                action_context = {
                    'self': self,
                    'msg': msg,
                    'result': None,
                    'context': match_context['context'],
                    'template': a_filter.template
                }
                eval(a_filter.action, action_context, mode="exec", nocopy=True)
                return action_context['result']
        else:
            return None



from wechatpy.exceptions import InvalidSignatureException
from werkzeug.exceptions import abort

__author__ = 'cysnake4713'

import logging
from openerp import http
from wechatpy.enterprise import WeChatClient, WeChatCrypto

_logger = logging.getLogger(__name__)


class WechatControllers(http.Controller):
    @http.route('/wechat_enterprise/<string:code>/api', type='http', auth="public", methods=['GET', 'POST'])
    def process(self, request, code, msg_signature, timestamp, nonce, echostr=None):
        _logger.debug('WeChat Enterprise connected:  code=%s, msg_signature=%s, timestamp=%s, nonce=%s, echostr=%s', code, msg_signature, timestamp,
                      nonce, echostr)
        request.uid = 1
        application_obj = request.registry['wechat.enterprise.application']
        application = application_obj.search(request.cr, request.uid, [('code', '=', code)], context=request.context)
        if not application:
            _logger.warning('Cant not find application.')
            abort(403)
        else:
            application = application_obj.browse(request.cr, request.uid, application[0], context=request.context)
        wechat_crypto = WeChatCrypto(application.token, application.ase_key, application.account.corp_id)

        if request.httprequest.method == 'GET':
            try:
                echo_str = wechat_crypto.check_signature(
                    msg_signature,
                    timestamp,
                    nonce,
                    echostr
                )
            except InvalidSignatureException:
                _logger.warning('check_signature fail.')
                abort(403)
            return echo_str
        else:
            pass
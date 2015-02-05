__author__ = 'cysnake4713'
from wechatpy.enterprise.exceptions import InvalidCorpIdException
from wechatpy.enterprise import WeChatClient, WeChatCrypto, parse_message, create_reply
from wechatpy.exceptions import InvalidSignatureException
from werkzeug.exceptions import abort
import logging
from openerp import http

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
            echo_str = ''
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
            try:
                msg = wechat_crypto.decrypt_message(
                    request.httprequest.data,
                    msg_signature,
                    timestamp,
                    nonce
                )
                msg = parse_message(msg)
                reply_msg = application.process_request(msg)[0]
                if reply_msg:
                    # if isinstance(reply_msg, list):
                    # reply_msg = reply_msg[0]
                    reply = create_reply(reply_msg, msg).render()
                    return wechat_crypto.encrypt_message(reply, nonce, timestamp)
                else:
                    _logger.info('reply None! msg= %s, reply_msg= %s', msg, reply_msg)
                    return ''
            except (InvalidSignatureException, InvalidCorpIdException), e:
                _logger.warning('decrypt_message fail.')
                abort(403)
            except Exception, e:
                _logger.error('process error')
                abort(403)


    @http.route('/wechat_enterprise/<string:code>/api/debug', type='http', auth="public", methods=['GET', 'POST'])
    def process_debug(self, request, code, msg_signature, timestamp, nonce, msg=None, echostr=None):
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
            return echo_str or ''
        else:
            try:
                reply_msg = application.process_request(msg)[0]
                if reply_msg:
                    # if isinstance(reply_msg, list):
                    # reply_msg = reply_msg[0]
                    reply = create_reply(reply_msg, msg).render()
                    return wechat_crypto.encrypt_message(reply, nonce, timestamp)
                else:
                    _logger.debug('reply_msg is None %s', reply_msg)
            except Exception, e:
                _logger.error('process_request error: %s', e)
                abort(403)
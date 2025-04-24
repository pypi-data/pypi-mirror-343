from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_MERCHANT_BASICDATA_SMS_SEND



class V2MerchantBasicdataSmsSendRequest(object):
    """
    商户短信发送
    """

    # 请求流水号
    req_seq_id = ""
    # 请求时间
    req_date = ""
    # 商户汇付Id
    huifu_id = ""
    # 手机号
    phone = ""
    # 验证类型
    verify_type = ""

    def post(self, extend_infos):
        """
        商户短信发送

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date,
            "huifu_id":self.huifu_id,
            "phone":self.phone,
            "verify_type":self.verify_type
        }
        required_params.update(extend_infos)
        return request_post(V2_MERCHANT_BASICDATA_SMS_SEND, required_params)

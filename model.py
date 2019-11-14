# coding=utf-8
import json

from workflow import web


class Detail(object):
    TITLE_FORMAT = "{} at {}|{}"
    SUBTITLE_FORMAT = "服务商: {}"

    def __init__(self, ip, country=None, region=None, provider=None):
        self.ip = ip  # type:str
        self.country = country  # type:str
        self.region = region  # type:str
        self.provider = provider  # type:str

    def __str__(self):
        return u"ip:{} country:{} region:{}".format(self.ip, self.country, self.region)

    def get_title(self):
        return Detail.TITLE_FORMAT.format(self.ip, self.country, self.region)

    def get_subtitle(self):
        return Detail.SUBTITLE_FORMAT.format(self.provider)


class Api(object):

    def __init__(self, ip):
        self.ip = ip

    def get_result(self):
        # 返回true or false
        pass


class ApiTaobao(Api):
    def __init__(self, ip, url="http://ip.taobao.com/service/getIpInfo.php?ip={}"):
        super(ApiTaobao, self).__init__(ip)
        self.url = url

    def get_result(self):
        """
            淘宝api格式
            content = {"code":0,"data":{"ip":"59.64.129.131","country":"中国","area":"","region":"北京","city":"北京","county":"XX","isp":"教育网","country_id":"CN","area_id":"","region_id":"110000","city_id":"110100","county_id":"xx","isp_id":"100027"}}

            :param ip:
            :return:
            """
        # 通过淘宝的api获取
        full_url = self.url.format(self.ip)
        text = web.request("get", full_url).text
        return ApiTaobao.text_to_detail(text)

    @staticmethod
    def get_myip():
        # 获取本机的外部ip信息
        url = "http://ip.taobao.com/service/getIpInfo2.php"
        text = web.request("post", url, data={'ip': 'myip'}).text
        return ApiTaobao.text_to_detail(text)

    @staticmethod
    def text_to_detail(text):
        content = json.loads(text)
        if content['code'] != 0:
            raise RuntimeError("淘宝 API请求失败")

        data = content["data"]
        detail = Detail(data["ip"], data["country"], data["region"], data["isp"])
        return detail

# class ApiSina(Api):
#
#     def get_result(self):
#         raise RuntimeError("新浪 API请求失败")

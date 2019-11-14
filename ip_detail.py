# coding=utf-8
import inspect
import os
import re
import sys
from logger import logger
from workflow import Workflow, web
import model
from model import Detail, Api, ApiTaobao

reload(sys)
sys.setdefaultencoding('utf8')

png_info = {
    "error": "src/error.png",  # 结果错误图标
    "ok": "src/ok.png"  # 结果正确图标
}

REGEXP_IP = re.compile(r'(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)')


def get_ip_detail(ip):
    for name, obj in inspect.getmembers(model):
        if inspect.isclass(obj) and obj != Api and issubclass(obj, Api):
            api_impl = obj(ip)
            try:
                result = api_impl.get_result()
                if result:
                    logger.debug("调用{}的api成功,结果:{}".format(name, result))
                    return result
            except RuntimeError as e:
                logger.error(e.message)
    return None


def get_details(wf, ip_arg):
    all_ip = REGEXP_IP.findall(ip_arg)
    for ip in all_ip:
        result = get_ip_detail(ip)  # type: Detail
        if result:
            logger.debug("调用api:" + ip)
            wf.add_item(title=result.get_title(), subtitle=result.get_subtitle(), icon=png_info['ok'], valid=True,
                        arg=result.get_title())
        else:
            wf.add_item(title=result.ip, subtitle="无法获取到对应的ip信息", icon=png_info['error'])


def get_local_ip(wf):
    local_ipv4 = None
    local_ipv6 = None
    external_detail = None
    try:
        local_ipv4 = os.popen("ifconfig | grep inet |   grep broadcast |cut -d ' ' -f2").read().strip()
        local_ipv6 = os.popen("ifconfig | grep inet6 | grep dynamic | cut -d ' ' -f2").read().strip()
        external_detail = ApiTaobao.get_myip()
    except Exception as e:
        logger.error(e)

    if local_ipv4:
        wf.add_item(title="IPv4", subtitle=local_ipv4, valid=True, arg=local_ipv4)
    if local_ipv6:
        wf.add_item(title="IPv6", subtitle=local_ipv6, valid=True, arg=local_ipv6)
    if external_detail:
        wf.add_item(title=external_detail.get_title(), subtitle=external_detail.get_subtitle(), icon=png_info['ok'],
                    valid=True,
                    arg=external_detail.ip)


def main(wf):
    if wf.args:
        # 有参数的请求,获取ip详细信息
        get_details(wf, " ".join(wf.args))
    else:
        # 无参数的请求,获取本地ip
        get_local_ip(wf)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))

''''
@Project: autotest   #项目名称
@Description: TODO          #描述
@Time:2021/9/8 7:32 下午       #日期
@Author:Tatu               #创建人
 
'''

import requests
import json
import simplejson
import logging
from lxml import html
from getRootPath import file_data_root

def post(headers,url,request_parameter_type=None,reponse_type=None,xpath=None,timeout=8,parameter=None,data=None,files=None,cookies=None,proxies=None):
    """
    封装post请求
    :param header:请求头
    :param url: 请求地址
    :param request_parameter_type:请求参数类型content-type
    :param reponse_type: 返回参数类型
    :param xpath: xpath表达式
    :param timeout: 超时时间
    :param parameter: url请求参数
    :param data: 请求体参数
    :param files: 上传文件
    :param cookie:
    :param proxies:
    :return:
    """

    if request_parameter_type == 'form-data':
        request_files = []
        if files:
            for i in files:
                file_path=file_data_root+i[1]
                request_files.append(i[0],(i[1],open(file_path,'rb'),i[2]))
        response = requests.post(url,params=parameter,data,proxies,files=request_files,timeout,cookies=cookies,proxies=proxies,headers)

    elif request_parameter_type == 'json':
        response = requests.post(url,params=parameter,json=data,headers=headers,cookies=cookies,proxies=proxies,timeout=timeout)

    elif request_parameter_type == 'x-www-form-urlencoded':
        response = requests.post(url, params=parameter, data=data, headers=headers, cookies=cookies, proxies=proxies,
                                 timeout=timeout)
    else:
        response = requests.post(url, params=parameter, data=data, headers=headers, cookies=cookies, proxies=proxies,
                                 timeout=timeout,files=files)

    if reponse_type == 'json':
        try:
            if response.status_code==200:
                return response.status_code,response.json()
            else:
                logging.debug('返回错误%s,%s',str(response.status_code),response.text)
                return response.status_code, response.json()
        except json.decoder.JSONDecodeError:
            return response.status_code,response.text
        except simplejson.decoder.JSONDecodeError:
            return response.status_code, response.text
        except Exception as e:
            logging.exception('ERROR')
            logging.error(e)
    elif reponse_type == 'string':
        try:
            return response.status_code,{'response':response.json()}
        except Exception as e:
            logging.exception('ERROR')
            logging.error(e)
            raise

    elif reponse_type =='html':
        resp_dict={}
        try:
            if response.status_code!=200:
                return response.status_code,response.text
            else:
                tree = html.fromstring(response.content)
                if xpath:
                    for key,value in xpath.items():
                        xpath_value = tree.xpath(value)
                        #去重
                        xpath_value = list(set(xpath_value))
                        if len(xpath_value)==1:
                            xpath_value = xpath_value[0]
                        resp_dict[key]=xpath_value

                return response.status_code,resp_dict
        except Exception as e:
            logging.exception('ERROR')
            logging.error(e)
            raise


def get(headers, url, request_parameter_type=None, reponse_type=None, xpath=None, timeout=8, parameter=None, data=None,
         files=None, cookies=None, proxies=None):
    """
    封装get请求
    :param header:请求头
    :param url: 请求地址
    :param request_parameter_type:请求参数类型content-type
    :param reponse_type: 返回参数类型
    :param xpath: xpath表达式
    :param timeout: 超时时间
    :param parameter: url请求参数
    :param data: 请求体参数
    :param files: 上传文件
    :param cookie:
    :param proxies:
    :return:
    """

    if request_parameter_type == 'form-data':
        request_files = []
        if files:
            for i in files:
                file_path = file_data_root + i[1]
                request_files.append(i[0], (i[1], open(file_path, 'rb'), i[2]))
        response = requests.post(url, params=parameter, data, proxies, files=request_files, timeout, cookies=cookies,
                                 proxies=proxies, headers)

    elif request_parameter_type == 'json':
        response = requests.post(url, params=parameter, json=data, headers=headers, cookies=cookies, proxies=proxies,
                                 timeout=timeout)

    elif request_parameter_type == 'x-www-form-urlencoded':
        response = requests.post(url, params=parameter, data=data, headers=headers, cookies=cookies, proxies=proxies,
                                 timeout=timeout)
    else:
        response = requests.post(url, params=parameter, data=data, headers=headers, cookies=cookies, proxies=proxies,
                                 timeout=timeout, files=files)

    if reponse_type == 'json':
        try:
            if response.status_code == 200:
                return response.status_code, response.json()
            else:
                logging.debug('返回错误%s,%s', str(response.status_code), response.text)
                return response.status_code, response.json()
        except json.decoder.JSONDecodeError:
            return response.status_code, response.text
        except simplejson.decoder.JSONDecodeError:
            return response.status_code, response.text
        except Exception as e:
            logging.exception('ERROR')
            logging.error(e)
    elif reponse_type == 'string':
        try:
            return response.status_code, {'response': response.json()}
        except Exception as e:
            logging.exception('ERROR')
            logging.error(e)
            raise

    elif reponse_type == 'html':
        resp_dict = {}
        try:
            if response.status_code != 200:
                return response.status_code, response.text
            else:
                tree = html.fromstring(response.content)
                if xpath:
                    for key, value in xpath.items():
                        xpath_value = tree.xpath(value)
                        # 去重
                        xpath_value = list(set(xpath_value))
                        if len(xpath_value) == 1:
                            xpath_value = xpath_value[0]
                        resp_dict[key] = xpath_value

                return response.status_code, resp_dict
        except Exception as e:
            logging.exception('ERROR')
            logging.error(e)
            raise

# -*- coding: UTF-8 -*-

import requests
import os
import mimetypes
import base64

from potx.lib.enums.FileTypeEnum import FileTypeEnum
from loguru import logger


def get_url_type(file_url):
    """
    根据文件url链接返回文件类型

    Args:
        file_url: 文件的url链接

    Returns: 返回FileTypeEnum类型
    """
    try:
        response = requests.head(file_url, allow_redirects=True)
        content_type = response.headers.get('Content-Type', '').lower()
        if 'application/pdf' in content_type:
            return FileTypeEnum.PDF
        elif 'image/' in content_type:
            return FileTypeEnum.IMAGE
        else:
            return FileTypeEnum.OTHER
    except Exception as e:
        logger.error(f"访问url异常!异常原因:{e}")
        return FileTypeEnum.OTHER


def get_file_type(file_path):
    """
    根据文件路径获取文件类型
    Args:
        file_path: 文件路径

    Returns: 返回FileTypeEnum类型
    """
    absolute_path = os.path.abspath(file_path)
    # 获取文件的MIME类型
    mime_type, _ = mimetypes.guess_type(absolute_path)
    if mime_type:
        if mime_type.startswith('application/pdf'):
            return FileTypeEnum.PDF
        elif mime_type.startswith('image'):
            return FileTypeEnum.IMAGE
        else:
            return FileTypeEnum.OTHER
    else:
        return FileTypeEnum.OTHER


def get_error_info(error_info):
    """
    检查接口返回数据是否错误
    :param error_info: 调用接口的返回数据
    :return:
    """
    error_url = 'http://python4office.cn/pobaidu/pobaidu-error/'
    if error_info.get('error_code', False):
        return f"接口调用错误，错误信息是{error_info}，原因和解决方法请查看官方文档：{error_url}"
    return False


def img2base64(imgPath):
    with open(imgPath, "rb") as f:
        data = f.read()
        encodestr = base64.b64encode(data)  # 得到 byte 编码的数据
        picbase = str(encodestr, 'utf-8')
        return picbase


def pdf2base64(pdf_path):
    base64_encoded_pdf = []
    pdf = fitz.open(pdf_path)
    for i in range(len(pdf)):
        pdf_bytes = pdf.convert_to_pdf(i, i + 1)
        # 灏嗗浘鐗囪浆鎹负Base64缂栫爜鐨勫瓧绗︿覆
        base64_encoded_pdf.append(base64.b64encode(pdf_bytes).decode('utf-8'))
    # 鍏抽棴PDF鏂囨。
    pdf.close()
    return base64_encoded_pdf

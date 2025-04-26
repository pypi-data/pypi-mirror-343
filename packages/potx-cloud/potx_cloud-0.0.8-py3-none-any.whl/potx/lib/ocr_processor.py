concurrent_map = {
    'AdvertiseOCR': 20,
    'ArithmeticOCR': 10,
    'BankCardOCR': 10,
    'BankSlipOCR': 10,
    'BizLicenseOCR': 10,
    'BusInvoiceOCR': 5,
    'BusinessCardOCR': 10,
    'CarInvoiceOCR': 5,
    'ClassifyDetectOCR': 20,
    'DriverLicenseOCR': 10,
    'RecognizeGeneralInvoice': 5,
    'WaybillOCR': 10,
    'VinOCR': 10,
    'DutyPaidProofOCR': 5,
    'EduPaperOCR': 5,
    'EnglishOCR': 10,
    'EnterpriseLicenseOCR': 5,
    'EstateCertOCR': 5,
    'FinanBillOCR': 5,
    'FinanBillSliceOCR': 5,
    'FlightInvoiceOCR': 5,
    'FormulaOCR': 5,
    'GeneralAccurateOCR': 10,
    'GeneralBasicOCR': 20,
    'GeneralEfficientOCR': 10,
    'GeneralFastOCR': 10,
    'GeneralHandwritingOCR': 10,
    'HKIDCardOCR': 5,
    'HmtResidentPermitOCR': 20,
    'IDCardOCR': 20,
    'ImageEnhancement': 10,
    'InstitutionOCR': 5,
    'InvoiceGeneralOCR': 5,
    'LicensePlateOCR': 10,
    'MLIDCardOCR': 5,
    'MLIDPassportOCR': 5,
    'MainlandPermitOCR': 20,
    'MixedInvoiceDetect': 5,
    'MixedInvoiceOCR': 5,
    'OrgCodeCertOCR': 5,
    'PassportOCR': 10,
    'PermitOCR': 10,
    'PropOwnerCertOCR': 5,
    'QrcodeOCR': 5,
    'QuotaInvoiceOCR': 5,
    'RecognizeContainerOCR': 5,
    'RecognizeHealthCodeOCR': 10,
    'RecognizeMedicalInvoiceOCR': 5,
    'RecognizeOnlineTaxiItineraryOCR': 20,
    'RecognizeTableOCR': 10,
    'RecognizeThaiIDCardOCR': 10,
    'RecognizeTravelCardOCR': 20,
    'ResidenceBookletOCR': 5,
    'RideHailingDriverLicenseOCR': 5,
    'RideHailingTransportLicenseOCR': 5,
    'SealOCR': 5,
    'ShipInvoiceOCR': 5,
    'SmartStructuralOCR': 5,
    'TableOCR': 10,
    'TaxiInvoiceOCR': 5,
    'TextDetect': 5,
    'TollInvoiceOCR': 5,
    'TrainTicketOCR': 5,
    'VatInvoiceOCR': 10,
    'VatInvoiceVerify': 20,
    'VatInvoiceVerifyNew': 20,
    'VatRollInvoiceOCR': 5,
    'VehicleLicenseOCR': 10,
    'VehicleRegCertOCR': 5,
    'VerifyOfdVatInvoiceOCR': 10,
    'SmartStructuralOCRV2': 5,
    'SmartStructuralPro': 5
}
# -*- coding: UTF-8 -*-
import pymupdf
import concurrent.futures
import threading
import base64

from potx.core.OCR import OCR
from potx.lib.enums.FileTypeEnum import FileTypeEnum
from potx.lib.CommonUtils import img2base64, get_file_type


def get_max_concurrent_nums(OCR_NAME):
    """
    获取最大的并发数
    Args:
        OCR_NAME: OCR_NAME

    Returns: 当前ocr接口的最大并发数

    """
    return concurrent_map[OCR_NAME] if concurrent_map[OCR_NAME] is not None else 1


def get_ocr(configPath, id, key):
    """
    初始化OCR对象
    Args:
        configPath: 配置信息
        id: SecretId
        key: SecretKey

    Returns: OCR对象

    """
    ocr = OCR()
    ocr.set_config(configPath, id, key)
    return ocr


def process_pdf_page(OCR_NAME, pdf, page_num, ocr, semaphore):
    """
    多线程处理pdf

    Args:
        OCR_NAME: OCR_NAME
        pdf: 指向pdf资源
        page_num: 处理pdf页号
        ocr: ocr对象
        semaphore: 信号量

    Returns: 返回获取结果

    """
    with semaphore:
        pdf_bytes = pdf.convert_to_pdf(page_num, page_num + 1)
        base64_encoded_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        return ocr.DoOCR(OCR_NAME, ImageBase64=base64_encoded_pdf, IsPdf=True)


def do_api(OCR_NAME, file_path, file_url, configPath, id, key):
    """
    通用api处理
    Args:
        OCR_NAME: OCR_NAME
        file_path: 本地文件路径
        file_url: 线上文件url
        configPath: 配置信息
        id: SecretId
        key: SecretKey

    Returns: 最终获取结果数据

    """
    ocr = get_ocr(configPath, id, key)
    if file_url:
        return ocr.DoOCR(OCR_NAME, ImageUrl=file_url)

    if file_path:
        img_type = get_file_type(file_path)
        if img_type == FileTypeEnum.OTHER:
            raise Exception("文件类型不符合!")
    if img_type == FileTypeEnum.PDF:
        semaphore = threading.Semaphore(get_max_concurrent_nums(OCR_NAME))
        with pymupdf.open(file_path) as pdf:
            # 使用线程池并行处理页面
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(process_pdf_page, OCR_NAME, pdf, page_num, ocr, semaphore)
                    for page_num in range(len(pdf))
                ]
                all_results = [future.result() for future in concurrent.futures.as_completed(futures)]
        # 否则返回所有页面的结果列表
        return all_results[0] if len(all_results) == 1 else all_results
    else:
        ImageBase64 = img2base64(file_path)
        return ocr.DoOCR(OCR_NAME, ImageBase64=ImageBase64)

import os
import unittest

from potx.api.ocr2excel import *


class Ocr2Excel(unittest.TestCase):
    """
    test for ocr2excel.py
    """

    def setUp(self):
        # 腾讯
        self.SecretId = os.getenv("SecretId", None)
        self.SecretKey = os.getenv("SecretKey", None)

    def test_RecognizeGeneralInvoiceOCR2Excel(self):
        RecognizeGeneralInvoiceOCR2Excel(input_path='../test_files/RecognizeGeneralInvoiceOCR/样例.png',
                                         output_path='../test_files/RecognizeGeneralInvoiceOCR',
                                         id=self.SecretId,
                                         key=self.SecretKey, sub_type=2)
        self.assertTrue(
            os.path.exists("../test_files/RecognizeGeneralInvoiceOCR/RecognizeGeneralInvoiceOCR2Excel.xlsx"))
        os.remove('../test_files/RecognizeGeneralInvoiceOCR/RecognizeGeneralInvoiceOCR2Excel.xlsx')
        RecognizeGeneralInvoiceOCR2Excel(img_url='https://ocr-demo-1254418846.cos.ap-guangzhou.'
                                                 'myqcloud.com/invoice/MixedInvoiceDetect/MixedInvoiceDetect2.jpg',
                                         output_path='../test_files/RecognizeGeneralInvoiceOCR',
                                         id=self.SecretId,
                                         key=self.SecretKey)
        self.assertTrue(
            os.path.exists("../test_files/RecognizeGeneralInvoiceOCR/RecognizeGeneralInvoiceOCR2Excel.xlsx"))
        os.remove('../test_files/RecognizeGeneralInvoiceOCR/RecognizeGeneralInvoiceOCR2Excel.xlsx')

    def test_VatInvoiceOCR2Excel(self):
        VatInvoiceOCR2Excel(input_path='../test_files/VatInvoiceOCR/img.png',
                            output_path=r'../test_files/VatInvoiceOCR',
                            id=self.SecretId,
                            key=self.SecretKey)
        self.assertTrue(
            os.path.exists("../test_files/VatInvoiceOCR/VatInvoiceOCR2Excel.xlsx"))
        os.remove('../test_files/VatInvoiceOCR/VatInvoiceOCR2Excel.xlsx')

    def test_BankCardOCR2Excel(self):
        BankCardOCR2Excel(input_path='../test_files/BankCard/bankcard.png',
                          output_path=r'../test_files/BankCard',
                          id=self.SecretId,
                          key=self.SecretKey)
        self.assertTrue(
            os.path.exists("../test_files/BankCard/BankCardOCR2Excel.xlsx"))
        os.remove('../test_files/BankCard/BankCardOCR2Excel.xlsx')

    def test_BankSlipOCR2Excel(self):
        BankSlipOCR2Excel(input_path='../test_files/BankSlip/bankslip.png',
                          output_path=r'../test_files/BankSlip',
                          id=self.SecretId,
                          key=self.SecretKey)
        self.assertTrue(
            os.path.exists("../test_files/BankSlip/BankSlipOCR2Excel.xlsx"))
        os.remove('../test_files/BankSlip/BankSlipOCR2Excel.xlsx')
        IDCardOCR2Excel(img_url='https://ocr-demo-1254418846.cos.ap-guangzhou.'
                                'myqcloud.com/card/IDCardBackOCR/IDCardBackOCR2.jpg',
                        output_path='../test_files/IDCard',
                        id=self.SecretId,
                        key=self.SecretKey)
        self.assertTrue(
            os.path.exists("../test_files/IDCard/IDCardOCR2Excel.xlsx"))
        os.remove('../test_files/IDCard/IDCardOCR2Excel.xlsx')

    def test_IDCardOCRFront2Excel(self):
        IDCardOCR2Excel(input_path='../test_files/IDCard/idcard_front.png',
                        output_path=r'../test_files/IDCard',
                        id=self.SecretId,
                        key=self.SecretKey)
        self.assertTrue(
            os.path.exists("../test_files/IDCard/IDCardOCR2Excel.xlsx"))
        os.remove('../test_files/IDCard/IDCardOCR2Excel.xlsx')
        IDCardOCR2Excel(img_url='https://ocr-demo-1254418846.cos.ap-guangzhou.'
                                'myqcloud.com/card/IDCardOCR/IDCardOCR1.jpg',
                        output_path='../test_files/IDCard',
                        id=self.SecretId,
                        key=self.SecretKey)
        self.assertTrue(
            os.path.exists("../test_files/IDCard/IDCardOCR2Excel.xlsx"))
        os.remove('../test_files/IDCard/IDCardOCR2Excel.xlsx')

    def test_IDCardOCRBack2Excel(self):
        IDCardOCR2Excel(input_path='../test_files/IDCard/idcard_bak.png',
                        output_path=r'../test_files/IDCard',
                        id=self.SecretId,
                        key=self.SecretKey)
        self.assertTrue(
            os.path.exists("../test_files/IDCard/IDCardOCR2Excel.xlsx"))
        os.remove('../test_files/IDCard/IDCardOCR2Excel.xlsx')

    def test_TrainTicketOCR2Excel(self):
        TrainTicketOCR2Excel(input_path=r'../test_files/TrainTicket/img.png',
                             output_path=r'../test_files/TrainTicket',
                             output_excel='ticket.xlsx',
                             configPath=r'../test_files/poocr-config.toml',
                             id=self.SecretId,
                             key=self.SecretKey)
        self.assertTrue(
            os.path.exists("../test_files/TrainTicket/ticket.xlsx"))
        os.remove('../test_files/TrainTicket/ticket.xlsx')

    def test_LicensePlateOCR2Excel(self):
        LicensePlateOCR2Excel(input_path=r'../test_files/LicensePlate/img.png',
                              output_path=r'../test_files/LicensePlate',
                              configPath=r'../test_files/poocr-config.toml',
                              id=self.SecretId,
                              key=self.SecretKey)
        self.assertTrue(
            os.path.exists("../test_files/LicensePlate/LicensePlateOCR2Excel.xlsx"))
        os.remove('../test_files/LicensePlate/LicensePlateOCR2Excel.xlsx')

    def test_BizLicenseOCR2Excel(self):
        BizLicenseOCR2Excel(input_path=r'../test_files/BizLicense/img.png',
                            output_excel=r'../test_files/BizLicense/BizLicense.xlsx',
                            configPath=r'../test_files/poocr-config.toml',
                            id=self.SecretId,
                            key=self.SecretKey)
        self.assertTrue(
            os.path.exists("../test_files/BizLicense/BizLicense.xlsx"))
        os.remove('../test_files/BizLicense/BizLicense.xlsx')
        BizLicenseOCR2Excel(img_url='https://ocr-demo-1254418846.cos.ap-guangzhou.'
                                    'myqcloud.com/card/BizLicenseOCR/BizLicenseOCR2.jpg',
                            output_excel=r'../test_files/BizLicense/BizLicense.xlsx',
                            configPath=r'../test_files/poocr-config.toml',
                            id=self.SecretId,
                            key=self.SecretKey)
        self.assertTrue(
            os.path.exists("../test_files/BizLicense/BizLicense.xlsx"))
        os.remove('../test_files/BizLicense/BizLicense.xlsx')

    def test_VehicleLicenseOCR2Excel(self):
        VehicleLicenseOCR2Excel(input_path=r'../test_files/VehicleLicense/img.png',
                                output_path=r'../test_files/VehicleLicense',
                                id=self.SecretId,
                                key=self.SecretKey)
        self.assertTrue(
            os.path.exists("../test_files/VehicleLicense/VehicleLicenseOCR2Excel.xlsx"))
        os.remove('../test_files/VehicleLicense/VehicleLicenseOCR2Excel.xlsx')

    def test_DriverLicenseOCR2Excel(self):
        DriverLicenseOCR2Excel(input_path=r'../test_files/DriverLicense/img.png',
                               output_path=r'../test_files/DriverLicense',
                               id=self.SecretId,
                               key=self.SecretKey)
        self.assertTrue(
            os.path.exists("../test_files/DriverLicense/DriverLicenseOCR2Excel.xlsx"))
        os.remove('../test_files/DriverLicense/DriverLicenseOCR2Excel.xlsx')

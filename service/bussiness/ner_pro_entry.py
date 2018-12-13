# -*- coding:utf-8 -*-

import re
from bussiness.predictModel import predict_pro_model

MODEL = predict_pro_model.NerPro()


def extract_api(content):
    """
    机构名、人名抽取入口
    """
    resp = MODEL.predict(content)
    return resp
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from xync_client.Abc.types import CredExOut

class ModelField(BaseModel):
    fieldId: str
    name: str
    fieldType: str
    index: int
    maxLength: int
    required: bool
    copyable: bool
    remindWord: str
    valueType: str
    value: str

class CredEpyd(CredExOut):
    id: int
    uid: int
    userName: str
    bankType: int
    bankNumber: str
    bankName: str
    bankAddress: Optional[str] = None
    qrCode: Optional[str] = None
    isShow: int
    buyingEnable: bool
    sellingEnable: bool
    disabledCurrencyList: List[int]
    modelFields: str
    modelFieldsList: List[ModelField]
    color: str
    payMethodName: str

# REMEMBER: this is python 2.7
import inspect


class ObjectType:
    POU = "POU"
    DUT = "DUT"
    GVL = "EVL"
    EVC = "EVC"
    METHOD = "METHOD"
    PROPERTY = "PROPERTY"
    ACTION = "ACTION"
    TRANSITION = "TRANSITION"
    LIBRARY_MANAGER = "LIBRARY_MANAGER"
    TASK_CONFIGURATION = "TASK_CONFIGURATION"
    PROJECT_INFORMATION = "PROJECT_INFORMATION"
    PROJECT_SETTINGS = "PROJECT_SETTINGS"
    DEVICE = "DEVICE"
    FOLDER = "FOLDER"
    CALL_TO_POU = "CALL_TO_POU"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def __iter__(cls):
        elements = []
        for member, value in inspect.getmembers(cls):
            if not member.startswith("_") and not inspect.ismethod(value):
                elements.append(value)
        return elements


GUID_TYPE_MAPPING = {
    "6f9dac99-8de1-4efc-8465-68ac443b7d08": ObjectType.POU,
    "2db5746d-d284-4425-9f7f-2663a34b0ebc": ObjectType.DUT,
    "ffbfa93a-b94d-45fc-a329-229860183b1d": ObjectType.GVL,
    "327b6465-4e7f-4116-846a-8369c730fd66": ObjectType.EVC,
    "f8a58466-d7f6-439f-bbb8-d4600e41d099": ObjectType.METHOD,
    "5a3b8626-d3e9-4f37-98b5-66420063d91e": ObjectType.PROPERTY,
    "8ac092e5-3128-4e26-9e7e-11016c6684f2": ObjectType.ACTION,
    "a10c6218-cb94-436f-91c6-e1652575253d": ObjectType.TRANSITION,
    "adb5cb65-8e1d-4a00-b70a-375ea27582f3": ObjectType.LIBRARY_MANAGER,
    "ae1de277-a207-4a28-9efb-456c06bd52f3": ObjectType.TASK_CONFIGURATION,
    "085afe48-c5d8-4ea5-ab0d-b35701fa6009": ObjectType.PROJECT_INFORMATION,
    "8753fe6f-4a22-4320-8103-e553c4fc8e04": ObjectType.PROJECT_SETTINGS,
    "225bfe47-7336-4dbc-9419-4105a7c831fa": ObjectType.DEVICE,
    "738bea1e-99bb-4f04-90bb-a7a567e74e3a": ObjectType.FOLDER,
    "413e2a7d-adb1-4d2c-be29-6ae6e4fab820": ObjectType.CALL_TO_POU,
}


def get_object_type(obj):
    return GUID_TYPE_MAPPING.get(str(obj.type), ObjectType.UNKNOWN)

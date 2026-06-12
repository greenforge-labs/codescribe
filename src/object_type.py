# REMEMBER: this is python 2.7
import inspect


class ObjectType:
    POU = "POU"
    DUT = "DUT"
    GVL = "GVL"
    GVL_PERSISTENT = "GVL_PERSISTENT"
    EVC = "EVC"
    INTERFACE = "INTERFACE"
    TASK = "TASK"
    METHOD = "METHOD"
    METHOD_NORET = "METHOD_NORET"
    PROPERTY = "PROPERTY"
    PROPERTY_METHOD = "PROPERTY_METHOD"
    ACTION = "ACTION"
    TRANSITION = "TRANSITION"
    IMAGEPOOL = "IMAGEPOOL"
    TEXTLIST = "TEXTLIST"
    GLOBAL_TEXTLIST = "GLOBAL_TEXTLIST"
    LIBRARY_MANAGER = "LIBRARY_MANAGER"
    TASK_CONFIGURATION = "TASK_CONFIGURATION"
    PROJECT_INFORMATION = "PROJECT_INFORMATION"
    PROJECT_SETTINGS = "PROJECT_SETTINGS"
    DEVICE = "DEVICE"
    FOLDER = "FOLDER"
    CALL_TO_POU = "CALL_TO_POU"
    VISUALISATION = "VISUALISATION"
    VISUALISATION_MANAGER = "VISUALISATION_MANAGER"
    TARGET_VISUALISATION = "TARGET_VISUALISATION"
    WEB_VISUALISATION = "WEB_VISUALISATION"
    VISUALISATION_STYLE = "VISUALISATION_STYLE"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def __iter__(cls):
        elements = []
        for member, value in inspect.getmembers(cls):
            if not member.startswith("_") and not inspect.ismethod(value):
                elements.append(value)
        return elements


# Other mapping lists:
# https://github.com/tkucic/codesys_workflow_automation/blob/main/src/codesysBulker.py#L9
# https://github.com/18thCentury/CodeSys/blob/master/export.py#L10

GUID_TYPE_MAPPING = {
    "6f9dac99-8de1-4efc-8465-68ac443b7d08": ObjectType.POU,
    "2db5746d-d284-4425-9f7f-2663a34b0ebc": ObjectType.DUT,
    "ffbfa93a-b94d-45fc-a329-229860183b1d": ObjectType.GVL,
    "261bd6e6-249c-4232-bb6f-84c2fbeef430": ObjectType.GVL_PERSISTENT,
    "327b6465-4e7f-4116-846a-8369c730fd66": ObjectType.EVC,
    "6654496c-404d-479a-aad2-8551054e5f1e": ObjectType.INTERFACE,
    "98a2708a-9b18-4f31-82ed-a1465b24fa2d": ObjectType.TASK,
    "f8a58466-d7f6-439f-bbb8-d4600e41d099": ObjectType.METHOD,
    "f89f7675-27f1-46b3-8abb-b7da8e774ffd": ObjectType.METHOD_NORET,
    "5a3b8626-d3e9-4f37-98b5-66420063d91e": ObjectType.PROPERTY,
    "792f2eb6-721e-4e64-ba20-bc98351056db": ObjectType.PROPERTY_METHOD,
    "8ac092e5-3128-4e26-9e7e-11016c6684f2": ObjectType.ACTION,
    "bb0b9044-714e-4614-ad3e-33cbdf34d16b": ObjectType.IMAGEPOOL,
    "2bef0454-1bd3-412a-ac2c-af0f31dbc40f": ObjectType.TEXTLIST,
    "63784cbb-9ba0-45e6-9d69-babf3f040511": ObjectType.GLOBAL_TEXTLIST,
    "a10c6218-cb94-436f-91c6-e1652575253d": ObjectType.TRANSITION,
    "adb5cb65-8e1d-4a00-b70a-375ea27582f3": ObjectType.LIBRARY_MANAGER,
    "ae1de277-a207-4a28-9efb-456c06bd52f3": ObjectType.TASK_CONFIGURATION,
    "085afe48-c5d8-4ea5-ab0d-b35701fa6009": ObjectType.PROJECT_INFORMATION,
    "8753fe6f-4a22-4320-8103-e553c4fc8e04": ObjectType.PROJECT_SETTINGS,
    "225bfe47-7336-4dbc-9419-4105a7c831fa": ObjectType.DEVICE,
    "738bea1e-99bb-4f04-90bb-a7a567e74e3a": ObjectType.FOLDER,
    "413e2a7d-adb1-4d2c-be29-6ae6e4fab820": ObjectType.CALL_TO_POU,
    "f18bec89-9fef-401d-9953-2f11739a6808": ObjectType.VISUALISATION,
    # Visualisation service objects. Named so the UNKNOWN export fallback does not pick
    # them up: exporting the manager makes every later import raise an interactive
    # overwrite dialog, and the project template carries these objects anyway.
    "4d3fdb8f-ab50-4c35-9d3a-d4bb9bb9a628": ObjectType.VISUALISATION_MANAGER,
    "bc63f5fa-d286-4786-994e-7b27e4f97bd5": ObjectType.TARGET_VISUALISATION,
    "0fdbf158-1ae0-47d9-9269-cd84be308e9d": ObjectType.WEB_VISUALISATION,
    "8e687a04-7ca7-42d3-be06-fcbda676c5ef": ObjectType.VISUALISATION_STYLE,
}


def get_object_type(obj):
    return GUID_TYPE_MAPPING.get(str(obj.type), ObjectType.UNKNOWN)

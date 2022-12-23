from tuya_connector import (
   TuyaOpenAPI,
   TuyaOpenPulsar,
   TuyaCloudPulsarTopic,
)


class Tuya:

    def __init__(self,
                 Client_id: str,
                 Client_secret: str,
                 url: str = "https://openapi.tuyaeu.com"
                 ):
        self.Client_id = Client_id
        self.Client_secret = Client_secret
        self.url = url

        self.openapi = TuyaOpenAPI(self.url, self.Client_id, self.Client_secret)
        self.openapi.connect()

        if not self.openapi.is_connect():
            raise Exception("Not able to connect to Tuya ioT. Check URL and Access Key.")

    def get_device_info(self,
                        device_id: str,
                        params: dict = {}
                        ) -> bool and str and dict:
        result = self.openapi.get(f"/v1.0/devices/{device_id}", params)
        if result["success"]:
            return True, None, result
        if not result["success"]:
            return False, result["msg"], None
        else:
            return False, "Cloud connectivity issue.", result

    def get_device_status(self,
                          device_id: str,
                          switch_list: list,
                          params: dict = {}
                          ) -> bool and str and dict:
        result = self.openapi.get(f"/v1.0/devices/{device_id}", params)

        if not result["success"]:
            return False, result["msg"], None

        result_dict = {"online": result["result"]["online"], "switch": {}}
        for switch in switch_list:
            for i in result["result"]["status"]:
                if switch == i["code"]:
                    result_dict["switch"][switch] = i["value"]

        return True, None, result_dict

    def send_command(self,
                     device_id: str,
                     command_dict: dict
                     ) -> bool and str:
        cmd_list = []
        for key in command_dict.keys():
            cmd_list.append({"code": key, "value": command_dict[key]})

        response = self.openapi.post(f"/v1.0/devices/{device_id}/commands", {"commands": cmd_list})

        if not response["success"]:
            return False, response["msg"] + ". Try checking the switch name."

        if response["success"]:
            return True, "Successfully triggered."

        return False, "Fatal error."




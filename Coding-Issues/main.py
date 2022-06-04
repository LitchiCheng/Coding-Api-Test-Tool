# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets,QtCore   
from ui import Ui_Form

import json
import requests
import os

login_url = "https://e.coding.net/open-api"

header = {
    "User-Agent": "PostmanRuntime/7.28.2",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Content-Length": "423",
    "Connection": "keep-alive",
    "Authorization":"Bearer  "
}

body = {
  "Action": "DescribeIssueListWithPage",
  "ProjectName": "issue_pool",
  "IssueType": "ALL",
  "PageNumber": 1,
  "PageSize": 20,
  "Conditions": [
    {
      "Key": "ASSIGNEE",
      "Value": "8079645"
    }
  ]
}

code_type_dict = {
    "DEFECT":"bug-tracking",
    "MISSION":"assignments",
    "REQUIREMENT":"requirements"
}

body_person_info_query = {
  "Action": "DescribeCodingCurrentUser"
}


project_name = [
    "issue_pool",
    "src",
    "test_center",
    "qm",
    "robokit",
    "order_issue_pool"
]

class mywindow(QtWidgets.QWidget,Ui_Form):  
    def __init__(self):
        super(mywindow,self).__init__()        
        self.setupUi(self)
        self.qurey_button.clicked.connect(self.query)
        self.output.setCurrentIndex(0)
        self.person_name = "无"
        self.person_id = "00000"
        try:
            if os.path.exists("token"):
                with open("token") as fp:
                    token_str=fp.read();
                    self.token_input.setText(token_str)
            else:
                self.token_input.setText("Pleace Copy Your Bearer Token Here.")
        except:
            self.token_input.setText("Pleace Copy Your Bearer Token Here.")
        
    def query(self):
        self.output.setCurrentIndex(0)
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        header["Authorization"] = "Bearer " + self.token_input.text()

        s = requests.session()
        # get person info
        body_json = json.dumps(body_person_info_query)
        login_ret = s.post(login_url, headers=header, data=body_json)
        try:
            person_info_josn = json.loads(login_ret.text)
            js = json.dumps(person_info_josn, indent=4, sort_keys=True, ensure_ascii=False)
            self.textBrowser_2.append(js)
            self.person_name = person_info_josn["Response"]["User"]["Name"]
            self.person_id = person_info_josn["Response"]["User"]["Id"]

            with open("token",'w') as wf:
                wf.write(self.token_input.text())

        except:
            self.textBrowser.append("Error! Check the raw data.")
       
        # get person issues
        body["Conditions"][0]["Value"] = str(self.person_id)
        for proj in project_name:
            body["ProjectName"] = proj
            body_json = json.dumps(body)
            login_ret = s.post(login_url, headers=header, data=body_json)
            try:
                ret_josn = json.loads(login_ret.text)
                js = json.dumps(ret_josn, indent=4, sort_keys=True, ensure_ascii=False)
                self.textBrowser_2.append(js)
                list = ret_josn["Response"]["Data"]["List"]
                for item in list:
                    if item["IssueStatusType"] != "COMPLETED":
                        info = proj + "#" + str(item["Code"]) + "-" + self.person_name+"-"+item["Name"] + "-" + "https://seer-group.coding.net/p/" +body["ProjectName"] + "/"+ code_type_dict[item["Type"]] + "/issues/" + str(item["Code"]) + "/detail"
                        self.textBrowser.append(info)
            except:
                self.textBrowser.append("Error! Check the raw data.")
        

if __name__=="__main__":
    import sys

    app=QtWidgets.QApplication(sys.argv)
    myshow=mywindow()                
    myshow.show()
    sys.exit(app.exec())
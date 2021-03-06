
# coding: utf-8

# In[1]:



#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()


# In[2]:


from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError


# In[3]:


import json
import os
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# In[4]:


from flask import Flask
from flask import request
from flask import make_response


# In[5]:


# Flask app should start in global layout
app = Flask(__name__)


# In[6]:


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# ### check point: action 이름이 정확한지, 필수 파라미터 값이 있는지

# In[7]:


def processRequest(req):
    if req.get("result").get("action") == "airport_pic":
        result = req.get("result")
        parameters = result.get("parameters")
        location = parameters.get("sys_lc_here")
        speech = ""

        if location is None or not location:
            speech = "사진 촬영 금지된 구역입니다."
        else:
            speech = "네 같이 찍어요."

        return {
            "speech": speech,
            "displayText": speech,
            # "data": data,
            # "contextOut": [],
            "source": "airport-robert-customized"
        }
    elif req.get("result").get("action") == "airport_category_search":
        result = req.get("result")
        parameters = result.get("parameters")
        dr_vehicle = parameters.get("dr_vehicle")
        gate_type = parameters.get("gate_type")
        speech = "좀 헷갈리네요. 다시 말해주세요."

        if dr_vehicle is None or not dr_vehicle:    # dr_vehicle is null and gate_type is not null
            if gate_type is not None or gate_type:
                speech = "GATE_SEARCH"
        elif gate_type is None or not gate_type:    # dr_vehicle is not null and gate_type is null
            if dr_vehicle is not None or dr_vehicle:
                speech = "FACILITY_SEARCH + Param{bus stop}"

        return {
            "speech": speech,
            "displayText": speech,
            # "data": data,
            # "contextOut": [],
            "source": "airport-robert-customized"
        }
    else:
        return {}
    
    


# In[ ]:


app.run(debug=False, port=9999)


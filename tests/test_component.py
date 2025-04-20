#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import yaml
import asyncio
import pytest
import httpx
from urllib.parse import urljoin
from dotenv import load_dotenv

from fast_crm.plugin.message import sender



class TestLogin:

    # @pytest.fixture(autouse=True)
    # def load_env():
    #     load_dotenv()

    # @pytest.fixture
    # def env_resource(self):
    #     # yield
    #     with open('config.yaml', 'r') as f:
    #         config = yaml.safe_load(f)
    #         print("config ", config)
    #         os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'] = config['ALIBABA_CLOUD_ACCESS_KEY_ID']
    #         os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'] = config['ALIBABA_CLOUD_ACCESS_KEY_SECRET']

    @pytest.fixture
    def patch(self):
        return urljoin("http://localhost:8100", "/co/")
    
    @pytest.fixture
    def patch_phone(self):
        return "13776668123"
    
    @pytest.fixture
    def patch_verify(self):
        template_code = "SMS_314795532"
        verify="123456"
        # template_param = "{\"code\": \"123456\"}"
        # template_param = "{code: {code}}".format(code=verify)
        template_param = json.dumps({"code": verify})
        return template_code, template_param
    
    def test_verify(self, patch_phone, patch_verify):
        template_code, template_param = patch_verify
        asyncio.run(sender.send_message(patch_phone, template_code, template_param))
        assert True
    
    # @pytest.mark.dependency()
    # def test_register(self, patch, patch_register):
    #     url = urljoin(patch, "on_register")
    #     response = httpx.post(url, json=patch_register)
    #     # response = httpx.get(url, headers={"Authorization": "Bearer a8894326-edf0-48ff-8a15-ca82e2d8a74f"})
    #     print(response.json())
    #     assert response.status_code == 200
    #     assert response.json()["status"] == 0

    # @pytest.mark.dependency(depends=["test_register"])
    # def test_login(self, patch, patch_login):
    #     url = urljoin(patch, "on_login")
    #     # response = httpx.post(url, json=patch_login, headers={"Authorization": "Bearer a8894326-edf0-48ff-8a15-ca82e2d8a74f"})
    #     response = httpx.post(url, json=patch_login)
    #     assert response.status_code == 200
    #     print(response.json())
    #     assert response.json()["status"] == 0
    
    def test_api(self, patch):
        url = urljoin(patch, "api")
        response = httpx.get(url)
        assert response.status_code == 200

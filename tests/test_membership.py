#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import pytest
import httpx
from urllib.parse import urljoin
from fast_crm.plugin.message import sender


class TestMembership:

    @pytest.fixture
    def patch_url(self):
        return urljoin("http://localhost:8100", "/membership/")
    
    @pytest.fixture
    def patch_phone(self):
        return "13776668123"
    
    @pytest.fixture
    def patch_token(self):
        token = "e991ab1c-1b16-444a-b973-10eb5290cdb1"
        return token
    
    @pytest.fixture
    def patch_member_id(self):
        return "7f99b1b1-c207-4bfc-bbd5-3d85fa85455d"

    @pytest.fixture
    def patch_charge(self):
        template_code = "SMS_480490015"
        template_param = "{\"name\": \"测试\", \"charge\": \"1000\", \"balance\": \"1100\"}"
        return template_code, template_param
    
    @pytest.fixture
    def patch_consume(self):
        template_code = "SMS_480470024"
        template_param = "{\"name\": \"测试\", \"consume\": \"1375\", \"balance\": \"600\"}"
        return template_code, template_param

    @pytest.fixture
    def patch_birthday(self):
        template_code = "SMS_480440021"
        template_param = "{\"name\": \"测试\"}"
        return template_code, template_param
    
    # @pytest.mark.dependency()
    # def test_register(self, patch_url, patch_token):
    #     url = urljoin(patch_url, "on_register")
    #     headers={"Authorization": f"Bearer {patch_token}"}
    #     params = {"member_name": "test", "member_phone": 13776668123, "birth_date": 19900101}
    #     response = httpx.post(url, json=params, headers=headers)
    #     print(response.json())
    #     assert response.status_code == 200

    # @pytest.mark.dependency(depends=["test_register"])
    # def test_charge(self, patch_url, patch_token, patch_member_id):
    #     url = urljoin(patch_url, "on_charge")
    #     headers={"Authorization": f"Bearer {patch_token}"}
    #     params = {"member_id": patch_member_id, "charge": 1000, "discount": 10}
    #     response = httpx.post(url, json=params, headers=headers)
    #     assert response.status_code == 200
    #     print(response.json())
    #     assert response.json()["status"] == "success"

    # @pytest.mark.dependency(depends=["test_charge"])
    # def test_consume(self, patch_url, patch_token, patch_member_id):
    #     url = urljoin(patch_url, "on_consume")
    #     headers={"Authorization": f"Bearer {patch_token}"}
    #     params = {"member_id": patch_member_id, "consume": 100}
    #     response = httpx.post(url, json=params, headers=headers)
    #     print(response.json())
    #     assert response.status_code == 200
    #     assert response.json()["status"] == "success"

    # @pytest.mark.dependency(depends=["test_charge"])
    # def test_charge_send(self, patch_phone, patch_charge):
    #     template_code, template_param = patch_charge
    #     asyncio.run(sender.send_message(patch_phone, template_code, template_param))
    #     assert True
    
    # @pytest.mark.dependency(depends=["test_consume"])
    # def test_consume_send(self, patch_phone, patch_consume):
    #     template_code, template_param = patch_consume
    #     asyncio.run(sender.send_message(patch_phone, template_code, template_param))
    #     assert True
    
    def test_birthday(self, patch_phone, patch_birthday):
        template_code, template_param = patch_birthday
        asyncio.run(sender.send_message(patch_phone, template_code, template_param))
    
    # def test_upload(self, patch_url, patch_token):
    #     url = urljoin(patch_url, "upload")
    #     headers={"Authorization": f"Bearer {patch_token}"}
    #     with open("example.txt", "rb") as file:
    #         # The tuple format is (filename, fileobj, content_type)
    #         # files = {"file": ("example.xlsx", file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    #         files = {"file": ("example.csv", file, "text/plain")}
    #     response = httpx.post(url, files=files, headers=headers)
    #     print(response.status_code)
    #     print(response.json())
    #     assert response.status_code == 200

    def test_api(self, patch_url):
        url = urljoin(patch_url, "api")
        response = httpx.get(url)
        print(response.json())
        assert response.status_code == 200
    
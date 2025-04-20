#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import httpx
from urllib.parse import urljoin


class TestCoprate:

    @pytest.fixture
    def patch_url(self):
        return urljoin("http://localhost:8100", "/coprate/")
    
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
    
    @pytest.mark.dependency(depends=["test_upload"])
    def test_delete(self, patch_url, patch_token, patch_member_id):
        url = urljoin(patch_url, "on_delete")
        headers={"Authorization": f"Bearer {patch_token}"}
        params = {"member_id": patch_member_id, "charge": 1000, "discount": 10}
        response = httpx.post(url, json=params, headers=headers)
        assert response.status_code == 200
        print(response.json())
        assert response.json()["status"] == "success"

    @pytest.mark.dependency(depends=["test_delete"])
    def test_query(self, patch_url, patch_token):
        url = urljoin(patch_url, "on_query")
        headers={"Authorization": f"Bearer {patch_token}"}
        response = httpx.get(url, headers=headers)
        print(response.json())
        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_upload(self, patch_url, patch_token):
        url = urljoin(patch_url, "upload")
        headers={"Authorization": f"Bearer {patch_token}"}
        with open("example.txt", "rb") as file:
            # The tuple format is (filename, fileobj, content_type)
            # files = {"file": ("example.xlsx", file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            files = {"file": ("example.csv", file, "text/plain")}
        response = httpx.post(url, files=files, headers=headers)
        print(response.status_code)
        print(response.json())
        assert response.status_code == 200

    def test_api(self, patch_url):
        url = urljoin(patch_url, "api")
        response = httpx.get(url)
        print(response.json())
        assert response.status_code == 200
    
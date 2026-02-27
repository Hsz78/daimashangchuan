import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from 密文储存 import app, unsafe_login

# 测试正常路径：用户名和密码正确
@patch('密文储存.pymysql.connect')
def test_unsafe_login_success(mock_connect):
    """
    测试正常路径：用户名和密码正确时，返回登录成功。
    """
    # 模拟数据库连接和游标
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {'username': 'test_user', 'password': 'test_pwd'}

    # 模拟请求数据
    with app.test_request_context('/unsafe_login', method='POST', json={'username': 'test_user', 'password': 'test_pwd'}):
        response, status_code = unsafe_login()

    # 验证结果
    assert status_code == 200
    assert response.json == {'code': 200, 'msg': '登录成功'}

# 测试边界条件：缺少用户名或密码
@patch('密文储存.pymysql.connect')
def test_unsafe_login_missing_parameters(mock_connect):
    """
    测试边界条件：缺少用户名或密码时，返回参数错误。
    """
    # 模拟请求数据
    with app.test_request_context('/unsafe_login', method='POST', json={'username': 'test_user'}):
        response, status_code = unsafe_login()

    # 验证结果
    assert status_code == 400
    assert response.json == {'code': 400, 'msg': '参数错误,请输入正确的用户名和密码'}

# 测试边界条件：用户名或密码错误
@patch('密文储存.pymysql.connect')
def test_unsafe_login_failure(mock_connect):
    """
    测试边界条件：用户名或密码错误时，返回登录失败。
    """
    # 模拟数据库连接和游标
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    # 模拟请求数据
    with app.test_request_context('/unsafe_login', method='POST', json={'username': 'wrong_user', 'password': 'wrong_pwd'}):
        response, status_code = unsafe_login()

    # 验证结果
    assert status_code == 401
    assert response.json == {'code': 401, 'msg': '用户名或密码错误'}

# 测试错误路径：数据库异常
@patch('密文储存.pymysql.connect')
def test_unsafe_login_database_error(mock_connect):
    """
    测试错误路径：数据库连接或查询异常时，返回服务器错误。
    """
    # 模拟数据库连接异常
    mock_connect.side_effect = Exception("Database connection failed")

    # 模拟请求数据
    with app.test_request_context('/unsafe_login', method='POST', json={'username': 'test_user', 'password': 'test_pwd'}):
        response, status_code = unsafe_login()

    # 验证结果
    assert status_code == 500
    assert response.json == {'code': 500, 'msg': '服务器错误'}
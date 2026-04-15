// 引入express
const express = require('express')
//引入dotenv
require('dotenv').config()
//初始化创建实例
const app = express()
// 解析json数据
app.use(express.json())
// 设置端口3000
const PORT = process.env.PORT || 3000
//引入中间件
const { authenticate, requireRole } = require('./middlewares/auth');
//引入jwt工具
const { generateAccessToken, generateRefreshToken, verifyToken } = require('./jwt');

//启动服务
app.get('/', (req, res) => {
  res.send('Hello World JWT 服务已经启动')
});

//接入登录接口代码
app.post('/login', (req, res) => {
  const { username, password } = req.body;

  if (username === 'admin' && password === '123456') {
    const payload = {
      userId: 1,
      role: 'admin'
    };

    const access_token = generateAccessToken(payload);
    const refresh_token = generateRefreshToken(payload);

    return res.json({
      user: { id: 1, username: 'admin' },
      access_token,
      refresh_token
    });
  }

  res.status(401).json({ message: '用户名或密码错误' });
});

// 刷新 token 接口（我帮你修好了！）
app.post('/auth/refresh', (req, res) => {
  const { refresh_token } = req.body;

  if (!refresh_token) {
    return res.status(401).json({ message: '缺少 refresh_token' });
  }

  try {
    const decoded = verifyToken(refresh_token);

    const newAccessToken = generateAccessToken({
      userId: decoded.userId,
      role: decoded.role
    });

    return res.json({ access_token: newAccessToken });
  } catch (err) {
    return res.status(401).json({ message: 'refresh_token 无效或已过期' });
  }
});

// 只有管理员能访问
app.get('/admin/info', authenticate, requireRole('admin'), (req, res) => {
  res.json({ 
    message: '欢迎管理员', 
    user: req.user 
  });
});

// 普通用户就能访问
app.get('/user/info', authenticate, requireRole('user'), (req, res) => {
  res.json({ 
    message: '欢迎普通用户', 
    user: req.user 
  });
});

// 监听端口
app.listen(PORT, () => {
    console.log(`服务启动在 http://localhost:${PORT}`);
});
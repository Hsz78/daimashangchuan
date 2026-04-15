//引入jsonwebtoken
const jwt = require('jsonwebtoken');
//从环境变量中获取密钥
const secret = process.env.JWT_SECRET;
//短的过期时间
function generateAccessToken(payload) {
  return jwt.sign(payload, secret, { 
    expiresIn: process.env.ACCESS_EXPIRES 
  });
}
//长的过期时间
function generateRefreshToken(payload) {
  return jwt.sign(payload, secret, { 
    expiresIn: process.env.REFRESH_EXPIRES 
  });
}
//验证token
function verifyToken(token) {
  try {
    return jwt.verify(token, secret);
  } catch (err) {
    throw err; // 后面中间件会捕获
  }
}
//导出三个函数
module.exports = {
  generateAccessToken,
  generateRefreshToken,
  verifyToken
};
const { verifyToken } = require('../jwt');

function authenticate(req, res, next) {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({ message: '未提供token' });
    }

    const token = authHeader.split(' ')[1];

    try {
        const decoded = verifyToken(token);
        req.user = decoded;
        next();
    } catch (err) {
        if (err.name === 'TokenExpiredError') {
            return res.status(401).json({ message: 'token已过期' });
        }
        return res.status(401).json({ message: 'token无效' });
    }
}

function requireRole(role) {
    return (req, res, next) => {
        if (!req.user) {
            return res.status(401).json({ message: '未登录' });
        }

        if (req.user.role !== role) {
            return res.status(403).json({ message: '无权访问' });
        }

        next();
    };
}

module.exports = { authenticate, requireRole };
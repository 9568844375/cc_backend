const express = require('express');
const router = express.Router();

// ✅ Import the whole object
const authController = require('../controllers/authController');

// ✅ Use named functions on the object
router.post('/signup', authController.signup);
router.post('/login', authController.login);

module.exports = router;

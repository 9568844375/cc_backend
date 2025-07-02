// routes/applicationRoutes.js

const express = require('express');
const router = express.Router();

// ✅ Destructure the named exports from the controller
const {
  submitApplication,
  getMyApplications
} = require('../controllers/applicationController');

// ✅ Middleware for auth (assuming it's created and working)
const auth = require('../middleware/authMiddleware');

// ✅ Routes
router.post('/', auth, submitApplication);
router.get('/my', auth, getMyApplications);

module.exports = router;

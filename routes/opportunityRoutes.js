const express = require('express');
const { createOpportunity, getAllOpportunities } = require('../controllers/opportunityController');
const auth = require('../middleware/authMiddleware');
const router = express.Router();

router.post('/', auth, createOpportunity);
router.get('/', getAllOpportunities);

module.exports = router;

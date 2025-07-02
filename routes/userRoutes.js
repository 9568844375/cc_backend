const express = require('express');
const { uploadExcelAndImport } = require('../controllers/userController');
const multer = require('multer');
const router = express.Router();
const upload = multer({ dest: 'uploads/' });

router.post('/import', upload.single('file'), uploadExcelAndImport);

module.exports = router;

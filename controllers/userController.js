const { importUsersFromExcel } = require('../utils/excelImporter');

exports.uploadExcelAndImport = async (req, res) => {
  try {
    await importUsersFromExcel(req.file.path);
    res.status(200).json({ message: 'Users imported successfully' });
  } catch (err) {
    res.status(500).json({ message: 'Import failed', error: err.message });
  }
};

const xlsx = require('xlsx');
const User = require('../models/User');
const bcrypt = require('bcrypt');

async function importUsersFromExcel(filePath) {
  const wb = xlsx.readFile(filePath);
  const sheet = wb.Sheets[wb.SheetNames[0]];
  const data = xlsx.utils.sheet_to_json(sheet);

  for (const row of data) {
    const { name, email, password, mobile, university, role } = row;
    const hashedPassword = await bcrypt.hash(password, 10);

    await User.updateOne(
      { email },
      { $set: { name, email, password: hashedPassword, mobile, university, role } },
      { upsert: true }
    );
  }
}

module.exports = { importUsersFromExcel };

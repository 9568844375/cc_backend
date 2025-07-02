const mongoose = require('mongoose');

const applicationSchema = new mongoose.Schema({
  student: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  opportunity: { type: mongoose.Schema.Types.ObjectId, ref: 'Opportunity' },
  formData: Object,
  status: { type: String, default: 'Pending' },
  appliedAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Application', applicationSchema);

const mongoose = require('mongoose');

const opportunitySchema = new mongoose.Schema({
  title: String,
  description: String,
  skills: [String],
  deadline: String,
  stipend: String,
  postedBy: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Opportunity', opportunitySchema);

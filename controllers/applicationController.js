const Application = require('../models/Application');

exports.submitApplication = async (req, res) => {
  try {
    const { opportunityId, ...formData } = req.body;
    const cvFile = req.file ? req.file.filename : null;

    const application = await Application.create({
      student: req.userId,
      opportunity: opportunityId,
      formData: { ...formData, cv: cvFile }
    });

    res.status(201).json(application);
  } catch (err) {
    res.status(500).json({ message: 'Application failed', error: err.message });
  }
};


exports.getMyApplications = async (req, res) => {
  const applications = await Application.find({ student: req.userId }).populate('opportunity');
  res.json(applications);
};

const Opportunity = require('../models/Opportunity');

exports.createOpportunity = async (req, res) => {
  const { title, description, skills, deadline, stipend } = req.body;
  try {
    const opportunity = await Opportunity.create({
      title,
      description,
      skills: skills.split(',').map(s => s.trim()),
      deadline,
      stipend,
      postedBy: req.userId
    });
    res.status(201).json(opportunity);
  } catch (err) {
    res.status(400).json({ message: 'Error creating opportunity', error: err.message });
  }
};

exports.getAllOpportunities = async (req, res) => {
  const opportunities = await Opportunity.find().populate('postedBy', 'name email');
  res.json(opportunities);
};

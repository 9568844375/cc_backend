const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const User = require('../models/User');

/**
 * Handle user signup
 * @route POST /api/auth/signup
 */
exports.signup = async (req, res) => {

   console.log("📨 Signup request received:", req.body);
   
  try {
    const { name, email, password, mobile, university, role } = req.body;

    // Check if user already exists
    const existingUser = await User.findOne({ $or: [{ email }, { mobile }] });
    if (existingUser) {
      return res.status(409).json({ message: 'User with this email or mobile already exists' });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Create user
    const user = await User.create({
      name,
      email,
      password: hashedPassword,
      mobile,
      university,
      role
    });

    res.status(201).json({ user });
  } catch (err) {
    console.error('Signup Error:', err);
    res.status(500).json({ message: 'Signup failed', error: err.message });
  }
};

/**
 * Handle user login
 * @route POST /api/auth/login
 */
exports.login = async (req, res) => {
  try {
    const { loginId, password } = req.body;

    // Find user by email or mobile
    const user = await User.findOne({ $or: [{ email: loginId }, { mobile: loginId }] });
    if (!user) {
      return res.status(401).json({ message: 'User not found' });
    }

    // Check password
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(401).json({ message: 'Incorrect password' });
    }

    // Generate token
    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '1d' });

    res.status(200).json({ user, token });
  } catch (err) {
    console.error('Login Error:', err);
    res.status(500).json({ message: 'Login failed', error: err.message });
  }
};

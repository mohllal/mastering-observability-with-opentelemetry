const express = require('express');
const axios = require('axios');
const router = express.Router();

const GATEWAY_URL = process.env.GATEWAY_URL || 'http://service-gateway:5000';
const VALID_CHOICES = ['spaces', 'tabs', 'clear'];

class VoteController {
  /**
   * Handles the voting request and renders the response
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   * @param {Function} next - Express next middleware function
   */
  static async handleVote(req, res, next) {
    try {
      const { choice } = req.query;

      // Validate choice if present
      if (choice && !VALID_CHOICES.includes(choice)) {
        return res.status(400).json({
          error: 'Invalid choice. Must be one of: spaces, tabs, clear'
        });
      }

      // Forward request to gateway service
      const response = await axios.get(`${GATEWAY_URL}`, {
        params: { choice },
        timeout: 5000
      });

      return res.render('index', response.data);
    } catch (error) {
      return next(error);
    }
  }
}

// Routes
router.get('/', VoteController.handleVote);

module.exports = () => router;

const express = require('express');
const router = express.Router();

const logger = require('../config/logger');
const VoteModel = require('../models/VoteModel');

class VoteController {
  /**
   * Process voting request
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  static async handleVote(req, res) {
    try {
      const { choice } = req.query;

      if (choice === 'clear') {
        await VoteModel.clearVotes();
        logger.info('Votes cleared successfully');
      } else if (choice) {
        await VoteModel.addVote(choice);
        logger.info(`Vote recorded for: ${choice}`);
      }

      const counts = await VoteModel.getCounts();
      return res.json(counts);

    } catch (error) {
      logger.error('Error processing vote:', error);
      return res.status(500).json({
        error: 'Internal server error',
        message: error.message
      });
    }
  }
}

// Routes
router.get('/', VoteController.handleVote);

module.exports = router;

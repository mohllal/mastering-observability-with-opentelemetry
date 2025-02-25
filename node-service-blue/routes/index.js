const express = require('express');
const router = express.Router();

const { initLogger } = require("@local/opentelemetry-js");
const VoteModel = require('../models/VoteModel');
const SlowOperation = require('../utils/SlowOperation');


const logger = initLogger();

class VoteController {
  /**
   * Process voting request
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  static async handleVote(req, res) {
    try {
      const { choice } = req.query;

      // Randomly trigger slow operation (20% chance)
      if (Math.random() < 0.5) {
        logger.info('Triggering random slow operation');
        await SlowOperation.call("process-vote-slow-operation");
      }

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

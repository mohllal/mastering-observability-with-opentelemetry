const mongoose = require('mongoose');

class VoteModel {
  constructor() {
    this.schema = new mongoose.Schema({
      choice: {
        type: String,
        enum: ['spaces', 'tabs'],
        required: true
      },
      createdAt: {
        type: Date,
        default: Date.now
      }
    });

    this.model = mongoose.model('Vote', this.schema);
  }

  /**
   * Add a new vote
   * @param {string} choice - The vote choice (spaces/tabs)
   * @returns {Promise} - The saved vote
   */
  async addVote(choice) {
    const vote = new this.model({ choice });
    return await vote.save();
  }

  /**
   * Get vote counts
   * @returns {Promise<Object>} - Object containing vote counts
   */
  async getCounts() {
    const spaces = await this.model.countDocuments({ choice: 'spaces' });
    const tabs = await this.model.countDocuments({ choice: 'tabs' });
    return { spaces, tabs };
  }

  /**
   * Clear all votes
   * @returns {Promise} - The delete result
   */
  async clearVotes() {
    return await this.model.deleteMany({});
  }
}

module.exports = new VoteModel();
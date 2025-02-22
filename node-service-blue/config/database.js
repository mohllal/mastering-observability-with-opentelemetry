const MONGODB_URI = process.env.MONGODB_URL || 'mongodb://localhost:27017/voting';

module.exports = {
  url: MONGODB_URI,
  options: {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  }
};

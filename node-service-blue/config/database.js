const MONGODB_URI = 'mongodb://database:27017/voting';

module.exports = {
  url: MONGODB_URI,
  options: {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  }
};

require("./utils/instrumentation");

const createError = require("http-errors");
const express = require('express');
const morgan = require("morgan");
const mongoose = require('mongoose');

const dbConfig = require('./config/database');
const indexRouter = require("./routes/index");
const { initLogger } = require("@local/opentelemetry-js");

const app = express();
const logger = initLogger();

logger.info('Starting service-blue application...');

app.use(morgan("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// Connect to MongoDB
mongoose.connect(dbConfig.url, {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => {
  logger.info('Connected to MongoDB');
}).catch((err) => {
  logger.error('Error connecting to MongoDB', err);
});

app.use("/", indexRouter);

// catch 404 and forward to error handler
app.use((req, res, next) => {
  next(createError(404));
});

// error handler
// eslint-disable-next-line no-unused-vars
app.use((err, req, res, next) => {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get("env") === "development" ? err : {};

  logger.error(err);

  // render the error page
  res.status(err.status || 500);
  return res.json({ error: err });
});

module.exports = app;

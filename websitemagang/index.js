const express = require("express");
const app = express();
const mongoose = require("mongoose");
const dotenv = require("dotenv");
const session = require('express-session');
dotenv.config();
const path = require("path");
const passport = require("passport");
const { loginCheck } = require("./auth/passport");
loginCheck(passport);

app.use(express.static('public'));
app.use('/css', express.static(__dirname + 'public/css'));

// Mongo DB conncetion
const database = process.env.MONGOLAB_URI;
mongoose
  .connect(`mongodb://127.0.0.1:27017/pi`, { useUnifiedTopology: true, useNewUrlParser: true })
  .then(() => console.log("e don connect"))
  .catch((err) => console.log(err));

app.set("view engine", "ejs");

//BodyParsing
app.use(express.urlencoded({ extended: false }));
app.use(session({
    secret:'oneboy',
    saveUninitialized: true,
    resave: true
  }));
  

app.use(passport.initialize());
app.use(passport.session());
//Routes
app.use("/", require("./routes/login"));

const PORT = process.env.PORT || 4111;

app.listen(PORT, console.log("Server has started at port " + PORT));


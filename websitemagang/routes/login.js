const express = require("express");

const {
  registerView,
  loginView,
  registerUser,
  loginUser,
} = require("../controllers/loginController");
const { DatasView, DatasViewFilter } = require("../controllers/dataController");
const { dashboardView, dashboardViewStartEnd } = require("../controllers/dashboardController");
const { protectRoute } = require("../auth/protect");

const router = express.Router();

router.get("/register", registerView);
router.get("/login", loginView);
//setelah login
router.get("/dashboard", protectRoute, dashboardView);
router.post("/dashboard", protectRoute, dashboardViewStartEnd)
router.get("/data", protectRoute, DatasView);
router.post("/data", protectRoute, DatasViewFilter);

router.post("/register", registerUser);
router.post("/login", loginUser);

module.exports = router;

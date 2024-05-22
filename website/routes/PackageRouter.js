const express = require('express');
const projectController = require('../controllers/ProjectController.js');
const modelController = require('../controllers/ModelController.js'); // Fix the casing of the import statement
const packageRouter = express.Router();

packageRouter.post("/model/create", modelController.createModel);
packageRouter.patch("/model/update", modelController.updateModel);

module.exports = packageRouter;
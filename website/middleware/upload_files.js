const multer = require('multer');
const fs = require('fs');
const path = require('path');

// Base directory for uploads
const baseDir = path.resolve(__dirname, '..', 'uploads');

// Function to create directory if it doesn't exist
const ensureDirectoryExistence = (filePath) => {
  const dirname = path.resolve(filePath);
  if (!fs.existsSync(dirname)) {
    fs.mkdirSync(dirname, { recursive: true });
    // console.log(`Directory created: ${dirname}`);
  } else {
    // console.log(`Directory already exists: ${dirname}`);
  }
};

// Function to get the upload path
const getUploadPath = (req, file, cb) => {
  const routerName = req.baseUrl;
  let destination_path;
  if (routerName.startsWith('/user')) {
    destination_path = path.join(baseDir, 'user_files');
  } else if (routerName.startsWith('/package')) {
    destination_path = path.join(baseDir, 'model_files');
  } else {
    destination_path = path.join(baseDir, 'default');
  }
  ensureDirectoryExistence(destination_path);
  console.log(`Upload path set to: ${destination_path}`);
  cb(null, destination_path);
};

// File type filter function
const fileTypeFilter = (req, file, cb) => {
  if (req.baseUrl.startsWith('/user') && !file.originalname.match(/\.(jpg|jpeg|png)$/)) {
    return cb(new Error('Invalid file type for UserRouter. Only JPG, JPEG, and PNG files allowed.'));
  }
  cb(null, true);
};

// Multer storage configuration
const storage = multer.diskStorage({
  destination: getUploadPath,
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  }
});

// Multer upload configuration
const upload = multer({
  storage: storage,
  limits: { fileSize: 5120000 }, // 5MB in bytes
  fileFilter: fileTypeFilter,
});

module.exports = {
  uploadUserFile: upload.single('userAvatar'),
  uploadPackageFile: upload.single('modelFile'),
};

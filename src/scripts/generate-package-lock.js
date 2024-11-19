// src/scripts/generate-package-lock.js
const fs = require('fs');
const { execSync } = require('child_process');
const path = require('path');

function generatePackageLock() {
  const frontendDir = path.join(__dirname, '../../frontend');
  
  // Check if we need to generate package-lock.json
  if (!fs.existsSync(path.join(frontendDir, 'package-lock.json'))) {
    console.log('Generating package-lock.json...');
    
    try {
      // Run npm install to generate package-lock.json
      execSync('npm install', { 
        cwd: frontendDir,
        stdio: 'inherit'
      });
      
      console.log('Successfully generated package-lock.json');
    } catch (error) {
      console.error('Error generating package-lock.json:', error);
      process.exit(1);
    }
  } else {
    console.log('package-lock.json already exists');
  }
}

// Run if called directly
if (require.main === module) {
  generatePackageLock();
}

module.exports = generatePackageLock;

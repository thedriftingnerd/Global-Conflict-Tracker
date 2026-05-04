module.exports = function override(config, env) {
  // Add webpack alias to handle three.js missing exports
  if (!config.resolve.alias) {
    config.resolve.alias = {};
  }
  
  // Alias the problematic imports to empty modules
  config.resolve.alias['three/addons/renderers/webgpu/WebGPURenderer.js'] = false;
  config.resolve.alias['three/addons/renderers/webgpu_wgsl/WebGPURenderer.js'] = false;
  
  return config;
};

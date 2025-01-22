module.exports = {
  transform: {
    '^.+\\.jsx?$': 'babel-jest',
  },
  transformIgnorePatterns: ['node_modules/(?!(axios|some-other-module)/)'],
  moduleFileExtensions: ['js', 'jsx', 'json', 'node'],
};

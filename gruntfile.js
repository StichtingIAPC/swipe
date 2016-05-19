module.exports = function(grunt){
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    bower: {
      dev: {
        options: {
          copy: false,
          install: true,
          bowerOptions: {
            production: false
          }
        }
      },
      deploy: {
        options: {
          copy: false,
          install: true,
          bowerOptions: {
            production: true
          },
          verbose: false
        }
      },
      debug: {
        options: {
          copy: false,
          install: true,
          verbose: true,
          bowerOptions: {
            production: false
          }
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-bower-task');

  grunt.registerTask('default', [
    'bower:dev'
  ]);
  grunt.registerTask('deploy', [
    'bower:deploy'
  ]);
  grunt.registerTask('dev', [
    'bower:dev'
  ]);
  grunt.registerTask('debug', [
    'bower:debug'
  ])
};
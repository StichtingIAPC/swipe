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
    },

    requirejs: {
      dev: {
        options: {
          mainConfigFile: 'static/js/config.js',
          include: ['main'],
          generateSourceMaps: true,
          preserveLicenseComments: false,
          name: '../build/bower_components/almond/almond',
          out: 'static/build/js/<%= pkg.name %>.min.js'
        }
      },
      deploy: {
        options: {
          mainConfigFile: 'static/js/config.js',
          include: ['main'],
          generateSourceMaps: false,
          preserveLicenseComments: true,
          name: '../build/bower_components/almond/almond',
          out: 'static/build/js/<%= pkg.name %>.min.js'
        }
      }
    },

    sass: {
      dev: {
        options: {
          sourceMap: true,
          sourceComments: true
        },
        files: {
          'static/build/css/<%= pkg.name %>.min.css': 'static/scss/main.scss'
        }
      },
      deploy: {
        options: {
          sourceMap: false,
          outputStyle: 'compressed'
        },
        files: {
          'static/build/css/<%= pkg.name %>.min.css': 'static/scss/main.scss'
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-bower-task');
  grunt.loadNpmTasks('grunt-contrib-requirejs');
  grunt.loadNpmTasks('grunt-sass');

  grunt.registerTask('default', [
    'bower:dev',
    'requirejs:dev',
    'sass:dev'
  ]);
  grunt.registerTask('deploy', [
    'bower:install',
    'requirejs:deploy',
    'sass:deploy'
  ]);
  grunt.registerTask('dev', [
    'bower:install',
    'requirejs:dev',
    'sass:dev'
  ]);
  grunt.registerTask('debug', [
    'bower:debug',
    'requirejs:dev',
    'sass:dev'
  ])
};
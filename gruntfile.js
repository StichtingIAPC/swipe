module.exports = function(grunt){
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

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

  grunt.loadNpmTasks('grunt-contrib-requirejs');
  grunt.loadNpmTasks('grunt-sass');

  grunt.registerTask('default', [
    'requirejs:dev',
    'sass:dev'
  ]);
  grunt.registerTask('deploy', [
    'requirejs:deploy',
    'sass:deploy'
  ]);
  grunt.registerTask('dev', [
    'requirejs:dev',
    'sass:dev'
  ])
};
module.exports = function(grunt){
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    dest: {
      js: 'static/build/js',
      css: 'static/build/css',
      name: '<%= pkg.name %>'
    },
    src: {
      js: 'static/js',
      css: 'static/scss'
    },

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

    browserify: {
      dev: {
        options: {
          browserifyOptions: {
            debug: true
          },
          transform: [
            ['babelify', {
              sourceMaps: true
            }]
          ]
        },
        files: {
          '<%= dest.js %>/raw/<%= dest.name %>.js': ['<%= src.js %>/main.js']
        }
      },
      deploy: {
        options: {
          browserifyOptions: {},
          transform: [
            ['babelify', {}]
          ]
        },
        files: {
          '<%= dest.js %>/raw/<%= dest.name %>.js': ['<%= src.js %>/main.js']
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
          '<%= dest.css %>/<%= pkg.name %>.min.css': '<%= src.css %>/main.scss'
        }
      },
      deploy: {
        options: {
          sourceMap: false,
          outputStyle: 'compressed'
        },
        files: {
          '<%= dest.css %>/<%= pkg.name %>.min.css': '<%= src.src %>/main.scss'
        }
      }
    },

    uglify: {
      dev: {
        options: {
          sourceMap: true,
          sourceMapIncludeSources: true
        },
        files: {
          '<%= dest.js %>/<%= dest.name %>.min.js': '<%= dest.js %>/raw/<%= dest.name %>.js'
        }
      },
      deploy: {
        options: {
          sourceMap: false,
          sourceMapIncludeSources: false
        },
        files: {
          '<%= dest.js %>/<%= dest.name %>.min.js': '<%= dest.js %>/raw/<%= dest.name %>.js'
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-bower-task');
  grunt.loadNpmTasks('grunt-browserify');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-sass');

  grunt.registerTask('default', [
    'bower:dev',
    'browserify:dev',
    'uglify:dev',
    'sass:dev'
  ]);
  grunt.registerTask('deploy', [
    'bower:deploy',
    'browserify:dev',
    'uglify:deploy',
    'sass:deploy'
  ]);
  grunt.registerTask('dev', [
    'bower:dev',
    'browserify:dev',
    'uglify:dev',
    'sass:dev'
  ]);
  grunt.registerTask('debug', [
    'bower:debug',
    'browserify:dev',
    'uglify:dev',
    'sass:dev'
  ])
};
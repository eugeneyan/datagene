# config valid only for Capistrano 3.1
# lock '3.1.0'

set :application, 'skillsort'

set :stages, ["production"]
set :default_stage, "production"
set :rails_env, "production"

set :scm, :git
set :branch, 'master'
set :repo_url, 'git@bitbucket.org:kennlim87/skillsort.git'
set :deploy_to, "/vol/sites/project_sites/skillsort"

set :keep_releases, 5     # Default value for keep_releases is 5
set :pty, true            # Make sure any needed passwors prompts from SSH show up so that it can be handled

# set :use_sudo, true

# set :repo_url, 'git@example.com:me/my_repo.git'

# Default branch is :master
# ask :branch, proc { `git rev-parse --abbrev-ref HEAD`.chomp }

# Default value for :format is :pretty
# set :format, :pretty

# Default value for :log_level is :debug
# set :log_level, :debug

# Default value for :pty is false

# Default value for :linked_files is []
# set :linked_files, %w{config/database.yml}

# Default value for linked_dirs is []
# set :linked_dirs, %w{bin log tmp/pids tmp/cache tmp/sockets vendor/bundle public/system}

# Default value for default_env is {}
# set :default_env, { path: "/opt/ruby/bin:$PATH" }

namespace :db do

  desc 'Backup current DB'
  task :backup do
    on roles(:db), in: :sequence, wait: 5 do
      backup_filename = Time.now.strftime("%Y%m%d%H%M%S") + "production.sqlite3"
      execute :cp, "/vol/sites/project_sites/skillsort/db_prod/production.sqlite3 /vol/sites/project_sites/skillsort/db_backup/#{backup_filename}"
      `scp -i ~/aws/heartcomputing.pem ec2-user@codingops.com:/vol/sites/project_sites/skillsort/db_prod/production.sqlite3 ~/rails_projects/skillsort_db/#{backup_filename}`
    end
  end

  desc 'Restore latest DB to current'
  task :restore do
    on roles(:db), in: :sequence, wait: 5 do
      list = `ssh -i ~/aws/heartcomputing.pem ec2-user@heartcomputing.com ls /vol/sites/project_sites/skillsort/db_backup`.split("\n")

      unless list.empty?

        # Get latest production DB file
        latest = list[0];
        list.each { |f| latest = f if f > latest }

        execute :sudo, 'service httpd stop'
        
        # Restore latest to current
        execute :rm, "-f /vol/sites/project_sites/skillsort/db_prod/production.sqlite3"
        execute :cp, "/vol/sites/project_sites/skillsort/db_backup/#{latest} /vol/sites/project_sites/skillsort/db_prod/production.sqlite3"

        # Run rake db:migrate
        migrate_status = `ssh -i ~/aws/heartcomputing.pem ec2-user@heartcomputing.com cd /vol/sites/project_sites/skillsort/current/ && rake db:migrate RAILS_ENV=production`
        puts migrate_status
        
        execute :sudo, 'service httpd start'

      end

    end
  end

end 


namespace :deploy do

  desc 'Restart application'
  task :restart do
    on roles(:app), in: :sequence, wait: 5 do
      # Your restart mechanism here, for example:
      execute :sudo, 'service httpd stop'
      execute :sudo, 'service httpd start'
    end
  end

  after :publishing, :restart

  after :restart, :clear_cache do
    on roles(:web), in: :groups, limit: 3, wait: 10 do
      # Here we can do anything such as:
      # within release_path do
      #   execute :rake, 'cache:clear'
      # end
    end
  end

end

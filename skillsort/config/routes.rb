Skillsort::Application.routes.draw do


  root 'main#index'


  # API
  namespace :api do
    resources :skills, only: :index
    resources :axes, only: :index
  end


  # Admin
  namespace :admin do
    resources :industries
    resources :functions
    resources :countries
    resources :axes
    resources :skills
    resources :games


    get "download-all-games" => "games#download_all", as: :download_all_games
    get "games/:id/download" => "games#download", as: :download_game
  end


  # Main
  get "main/index"
  get "login" => "main#index"
  get "about" => "main#about"
  get "about_us" => "main#about_us"
  get "privacy-terms" => "main#privacy_terms"
  get "feedback" => "main#feedback"
  post "feedback-submit" => "main#feedback_submit"


  # Skillsort
  get 'try-game', to: 'skillsort#try_game'
  get "play-game/:game_type" => 'skillsort#play_game'
  get "job-information" => "skillsort#job_information", as: :job_information
  post "job-information-submit" => "skillsort#job_information_submit", as: :job_information_submit
  get "dashboard" => "skillsort#dashboard", as: :dashboard
  post "submit-game" => "skillsort#submit_game"


  # devise_for :users
  devise_scope :user do
    post "/register" => "account#create", as: :user_registration
  end
  devise_for :users, :path => '', :path_names => {:sign_in => 'login', :sign_out => 'logout'}
end

module Features
  module SessionHelper
    
    def log_in_with(email, password)
      visit '/'
      within '#login-form' do
        fill_in 'user[email]', with: email
        fill_in 'user[password]', with: password
        click_button 'Login'
      end
    end


    def log_in
      visit '/'
      within '#login-form' do
        fill_in 'user[email]', with: 'email1@factory.com'
        fill_in 'user[password]', with: 'password'
        click_button 'Login'
      end
    end

  end
end
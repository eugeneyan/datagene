require 'spec_helper'
require 'support/features/session_helper'


RSpec.configure do |config|
  config.include Features::SessionHelper, type: :feature
end


feature 'Login/Logout:' do

  before(:all) { User.delete_all; user = FactoryGirl.create(:user) }

  scenario 'User logs into account' do
    log_in_with 'email1@factory.com', 'password'
    
    expect(page).to have_content('Log out')
    expect(page).to have_content('Signed in successfully')
  end


  context 'When user has logged in' do
    before(:all) { log_in }
    scenario 'User log out from account' do
      click_link 'Log out'
      expect(page).to have_content('Signed out successfully.')
    end
  end

end
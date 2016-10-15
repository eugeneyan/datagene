require 'spec_helper'


feature 'Register:' do
  scenario 'Guest register a new account' do 
    visit '/'
    within '#register-form' do
      fill_in 'user[first_name]', with: 'John'
      fill_in 'user[last_name]', with: 'Smith'
      fill_in 'user[email]', with: 'john.smith@gmail.com'
      fill_in 'user[password]', with: 'mymomisawesome'
      fill_in 'user[password_confirmation]', with: 'mymomisawesome'
      select '30', from: 'user[birthday_day]'
      select 'December', from: 'user[birthday_month]'
      select '1980', from: 'user[birthday_year]'
      choose('Male')
      click_button 'Register'
    end

    expect(page).to have_content('Log out')
    expect(page).to have_content('Congratulations! You have successfully signed up for a new account.')
    expect(page).to have_content('Logged in as')
    expect(page).to have_content('john.smith@gmail.com')
  end
end
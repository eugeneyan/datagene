require 'spec_helper'

feature 'Guest/User' do

  scenario 'visit the home page' do
    visit '/'
    expect(page).to have_content "Data-Driven Career Discovery"
    expect(page).to have_content "Try SortMySkills!"
  end


  scenario 'navigate to the about page' do
    visit '/'
    click_link 'About'
    expect(page).to have_content "Learn about your innate skill preferences and plot your career roadmap."
  end


  scenario 'navigate to the about us page' do
    visit '/'
    click_link 'About Us'
    expect(page).to have_content "product engineer"
    expect(page).to have_content "data scientist"
  end


  scenario 'navigate to the feedback page' do
    visit '/'
    click_link 'Feedback'
    expect(page).to have_content "Feedback Form"
  end


  scenario 'navigate to the try SortyMySkills page' do
    visit '/'
    click_link 'Try SortMySkills!'
    expect(page).to have_content "Welcome to Game 1"
  end

end
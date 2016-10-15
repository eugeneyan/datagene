require 'spec_helper'
require 'support/features/session_helper'


RSpec.configure do |config|
  config.include Features::SessionHelper, type: :feature
end


feature 'Play game:' do

  context 'Guest' do
    scenario 'should be able to Try SortMySkills!, play the game, submit the game and view top 5 skills', js: true do
      visit '/'
      click_on 'Try SortMySkills!'
      expect(page).to have_content('Welcome to Game 1')

      click_link 'Next'      
      click_link 'Next'
      click_link 'Next'
      click_link 'Start Game!'

      (1..5).each { click_button '5' }
      (1..45).each { click_button '3' }

      page.find(:css, '#submit-game').click

      expect(page).to have_content('Your Top 5 Preferred Skills Are')
    end
  end


  context 'User' do

    before(:all) { User.delete_all; Game.delete_all; FactoryGirl.create(:user) }


    scenario 'should be able to play game 1, complete the game and view dashboard', js: true do
      visit '/'
      log_in
      click_on 'SortMySkills!'
      click_on 'Game 1: Discover your Passion'
      expect(page).to have_content('Welcome to Game 1')

      click_link 'Next'      
      click_link 'Next'
      click_link 'Next'
      click_link 'Start Game!'

      (1..5).each { click_button '5' }
      (1..45).each { click_button '3' }

      page.find(:css, '#submit-game').click

      expect(page).to have_content('Skill Preferences Overview')
    end


    context 'has not completed game 1,' do
      
      before(:all) { Game.delete_all }
      
      scenario 'he should not be able to play Game 2', js: true do
        visit '/'
        log_in
        click_on 'SortMySkills!'
        click_on 'Game 2: Evaluate Proficiency'
        expect(page).to have_content('You will have to complete game Game 1 first.')
      end


      scenario 'he should not be able to play Game 3', js: true do
        visit '/'
        log_in
        click_on 'SortMySkills!'
        click_on 'Game 3: Measure Usage'
        expect(page).to have_content('You will have to complete game Game 1 first.')
      end
    end


    context 'has completed game 1 but not game 2' do
      before(:all) { Game.delete_all; Game.create(user_id: User.all.first.id, result: 'results', version: 'v0.2', game_type: 1) }
      

      scenario 'he should able to play Game 2', js: true do
        visit '/'
        log_in
        click_on 'SortMySkills!'
        click_on 'Game 2: Evaluate Proficiency'
        expect(page).to have_content('Welcome to Game 2')
      end
      

      scenario 'he should not be able to play Game 3', js: true do
        visit '/'
        log_in
        click_on 'SortMySkills!'
        click_on 'Game 3: Measure Usage'
        expect(page).to have_content('You will have to complete game Game 2 first.')
      end
    end

  end

end
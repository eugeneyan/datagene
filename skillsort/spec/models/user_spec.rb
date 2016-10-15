require 'spec_helper'

describe User do

  before(:each) { User.delete_all }

  it { should validate_presence_of(:first_name) }
  it { should validate_presence_of(:last_name) }
  it { should validate_presence_of(:email) }
  it { should validate_presence_of(:password) }
  it { should validate_presence_of(:birthday_day) }
  it { should validate_presence_of(:birthday_month) }
  it { should validate_presence_of(:birthday_year) }
  it { should validate_presence_of(:gender) }


  it 'should not be able to create new user with used email address' do
    user1 = FactoryGirl.create(:user)
    user2 = FactoryGirl.build(:user)
    user2.email = user1.email
    expect { user2.save }.to change { User.count }.by 0
  end


  it 'should not be able to create new user when password do not match' do
    user = FactoryGirl.build(:user)
    user.password = 'password1'
    user.password_confirmation = 'password2'
    expect { user.save }.to change { User.count }.by 0
  end


  it 'should be able to be assigned to games' do
    user = FactoryGirl.create(:user)
    20.times { FactoryGirl.create(:game, user: user) }
    user.games.count.should == 20
  end
end

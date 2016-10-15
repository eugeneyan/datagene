require 'spec_helper'

describe Game do
  let(:user) { User.delete_all; FactoryGirl.create(:user) }
  subject(:game) { Game.delete_all; Game.create(user_id: user.id, version: 'v0.2', result: '1,5;2,5;3,3;4,2;', game_type: 1) }
  

  it { should belong_to(:user) }
  it { should validate_presence_of(:user) }
  it { should validate_presence_of(:result) }
  it { should validate_presence_of(:version) }
  it { should validate_presence_of(:game_type) }


  it 'should be able to return a result hash' do
    h = {1 => 5, 2 => 5, 3 => 3, 4 => 2}
    game.result_hash.should == h
  end
end
